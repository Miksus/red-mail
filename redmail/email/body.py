from email.message import EmailMessage
import mimetypes
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Union, ByteString
from pathlib import Path

from redmail.utils import is_bytes
from redmail.utils import import_from_string

from email.utils import make_msgid, parseaddr

from jinja2.environment import Template, Environment

from markupsafe import Markup

# We try to import matplotlib and PIL but if fails, they will be None
from .utils import PIL, plt, pd, css_inline

if TYPE_CHECKING:
    # For type hinting
    from pandas import DataFrame

class BodyImage:
    "Utility class to represent image on HTML"

    def __init__(self, cid, obj, name=None):
        self.cid = cid
        self.obj = obj
        self.name = name

    def __str__(self):
        return f'<img src="{self.src}">'

    @property
    def src(self):
        return f'cid:{ self.cid }'

class Body:

    def __init__(self, jinja_env:Environment, template:Template=None, table_template:Template=None, use_jinja=True):
        self.template = template
        self.table_template = table_template
        self.jinja_env = jinja_env
        self.use_jinja = use_jinja

    def render_body(self, body:str, jinja_params:dict):
        if body is not None and self.template is not None:
            raise ValueError("Either body or template must be specified but not both.")
            
        if body is not None:
            template = self.jinja_env.from_string(body)
        else:
            template = self.template
        return template.render(**jinja_params)

    def render_table(self, tbl, extra=None):
        # TODO: Nicer tables. 
        #   https://stackoverflow.com/a/55356741/13696660
        #   Email HTML (generally) does not support CSS
        if pd is None:
            raise ImportError("Missing package 'pandas'. Prettifying tables requires Pandas.")
        
        from pandas.io.formats.style import Styler

        extra = {} if extra is None else extra

        # Allow for pandas styler object, convert to inline CSS for email client rendering
        # https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.html
        if isinstance(tbl, Styler):
            if css_inline is None:
                raise ImportError("Missing package 'css_inline'. Prettifying tables with Pandas styler requires css_inline.")
            inliner = css_inline.CSSInliner()
            return inliner.inline(tbl.to_html())

        df = pd.DataFrame(tbl)

        tbl_html = self.table_template.render({"df": df, **extra})
        return Markup(tbl_html)

    def render(self, cont:str, tables=None, jinja_params=None):
        tables = {} if tables is None else tables
        jinja_params = {} if jinja_params is None else jinja_params
        tables = {
            name: self.render_table(tbl)
            for name, tbl in tables.items()
        }
        return self.render_body(cont, jinja_params={**tables, **jinja_params})


class TextBody(Body):

    def attach(self, msg:EmailMessage, text:str, **kwargs):
        if self.use_jinja:
            text = self.render(text, **kwargs)
        msg.set_content(text)


class HTMLBody(Body):

    def __init__(self, domain:str=None, **kwargs):
        super().__init__(**kwargs)
        self.domain = domain

    def attach(self, 
               msg:EmailMessage, 
               html:str, 
               images: Dict[str, Union[Path, str, bytes]]=None, 
               **kwargs):
        """Render email HTML
        
        Parameters
        ----------
            msg : EmailMessage
                Message of the email.
            html : str
                HTML that may contain Jinja syntax.
            body_images : dict of path-likes, bytes
                Images to embed to the HTML. The dict keys correspond to variables in the html.
            body_tables : dict of pd.DataFrame
                Tables to embed to the HTML
            jinja_params : dict
                Extra Jinja parameters for the HTML.
        """
        if self.use_jinja:
            domain = self.domain
            html, cids = self.render(
                html, 
                images=images,
                domain=domain,
                **kwargs
            )
        msg.add_alternative(html, subtype='html')

        if self.use_jinja and images is not None:
            # https://stackoverflow.com/a/49098251/13696660
            html_msg = msg.get_payload()[-1]
            cid_path_mapping = {cids[name]: path for name, path in images.items()}
            
            self.attach_imgs(html_msg, cid_path_mapping)

    def render(self, html:str, images:Dict[str, Union[dict, bytes, Path]]=None, tables:Dict[str, 'DataFrame']=None, jinja_params:dict=None, domain=None):
        """Render Email HTML body (sets cid for image sources and adds data as other parameters)

        Parameters
        ----------
        html : str
            HTML (template) to be rendered with images,
            tables etc. May contain...
        images : list-like, optional
            A list-like of images to be rendered to the HTML.
            Values represent the Jinja variables found in the html
            and the images are rendered on those positions.
        tables : dict, optional
            A dict of tables to render to the HTML. The keys
            should represent variables in ``html`` and values
            should be Pandas dataframes to be rendered to the HTML.
        extra : dict, optional
            Extra items to be passed to the HTML Jinja template.
        table_theme : str, optional
            Theme to use for generating the HTML version of the
            table dataframes. See included files in the 
            environment pybox.jinja2.envs.inline. The themes
            are stems of the files in templates/inline/table.

        Returns
        -------
        str, dict
            Rendered HTML and Content-IDs to the images.

        """
        
        images = {} if images is None else images

        # Define CIDs for images
        cids = {
            name: make_msgid(domain=domain)
            for name in images
        }
        html_images = {
            name: BodyImage(cid=cid[1:-1], name=name, obj=images[name]) # taking "<" and ">" from beginning and end 
            for name, cid in cids.items()
        }

        # Tables to HTML
        jinja_params = {**jinja_params, **html_images}
        html = super().render(html, tables=tables, jinja_params=jinja_params)
        return html, cids

    def attach_imgs(self, msg_body:EmailMessage, imgs:Dict[str, Union[ByteString, str, Dict[str, Union[ByteString, str]]]]):
        """Attach CID images to Message Body
        
        Examples:
        ---------
            attach_imgs(..., {"<>"})
        """

        for cid, img in imgs.items():
            if is_bytes(img) or isinstance(img, BytesIO):
                # We just assume the user meant PNG. If not, it should have been specified
                img_content = img.read() if hasattr(img, "read") else img
                kwds = {
                    'maintype': 'image',
                    'subtype': 'png',
                }

            elif isinstance(img, dict):
                # Expecting dict explanation of bytes
                # ie. {"maintype": "image", "subtype": "png", "content": b'...'}

                # Setting defaults
                img['maintype'] = img.get('maintype', 'image')

                # Validation
                required_keys = ("content", "subtype")
                if any(key not in img for key in required_keys):
                    missing_keys = tuple(key for key in required_keys if key not in img)
                    raise KeyError(f"Dict representation of an image missing keys: {missing_keys}")
                
                img_content = img.pop("content")
                kwds = img

            elif isinstance(img, Path) or (isinstance(img, str) and Path(img).is_file()):
                path = img
                maintype, subtype = mimetypes.guess_type(str(path))[0].split('/')
                
                with open(path, "rb") as img:
                    img_content = img.read()
                kwds = {
                    'maintype': maintype,
                    'subtype': subtype,
                }
            elif plt is not None and isinstance(img, plt.Figure):
                buf = BytesIO()
                img.savefig(buf, format='png')
                buf.seek(0)
                img_content = buf.read()
                kwds = {
                    'maintype': 'image',
                    'subtype': 'png',
                }
            elif PIL is not None and isinstance(img, PIL.Image.Image):
                buf = BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                img_content = buf.read()
                kwds = {
                    'maintype': 'image',
                    'subtype': 'png',
                }
            else:
                # Cannot be figured out
                if isinstance(img, str):
                    raise ValueError(f"Unknown image string '{img}'. Maybe incorrect path?")
                raise TypeError(f"Unknown image {repr(img)}")

            msg_body.add_related(
                img_content,
                cid=cid,
                **kwds
            )
