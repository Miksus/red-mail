
from email.message import EmailMessage
from typing import Callable, Dict, Optional, Union

import jinja2
from redmail.email.attachment import Attachments

from redmail.email.body import HTMLBody, TextBody
from redmail.models import EmailAddress, Error
from .envs import get_span, is_last_group_row

import smtplib

from pathlib import Path
from platform import node
from getpass import getuser
import datetime

class EmailSender:
    """Email sender

    Parameters
    ----------
    host : str
        SMTP host address.
    port : int
        Port to the SMTP server.
    user : str, callable
        User name to authenticate on the server.
    password : str, callable
        User password to authenticate on the server.

    Examples
    --------
    .. code-block:: python
    
        mymail = EmailSender(server="smtp.mymail.com", port=123)
        mymail.set_credentials(
            user=lambda: read_yaml("C:/config/email.yaml")["mymail"]["user"],
            password=lambda: read_yaml("C:/config/email.yaml")["mymail"]["password"]
        )
        mymail.send(
            subject="Important email",
            html="<h1>Important</h1><img src={{ nice_pic }}>",
            body_images={'nice_pic': 'path/to/pic.jpg'},

        )
    """
    
    default_html_theme = "modest.html"
    default_text_theme = "pandas.txt"

    templates_html = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates/html"))
    templates_html_table = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates/html/table"))

    templates_text = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates/text"))
    templates_text_table = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates/text/table"))

    # Set globals
    templates_html_table.globals["get_span"] = get_span
    templates_text_table.globals["get_span"] = get_span
    
    templates_html_table.globals["is_last_group_row"] = is_last_group_row
    templates_text_table.globals["is_last_group_row"] = is_last_group_row

    attachment_encoding = 'UTF-8'

    def __init__(self, host:str, port:int, user_name:str=None, password:str=None):
        self.host = host
        self.port = port

        self.user_name = user_name
        self.password = password

        # Defaults
        self.sender = None
        self.receivers = None
        self.subject = None

        self.text = None
        self.html = None
        self.html_template = None
        self.text_template = None
        
    def send(self, **kwargs):
        """Send an email message.

        Parameters
        ----------
        subject : str
            Subject of the email.
        receivers : list, optional
            Receivers of the email.
        sender : str, optional
            Sender of the email.
        cc : list, optional
            Cc or Carbon Copy of the email.
            Extra recipients of the email.
        bcc : list, optional
            Blind Carbon Copy of the email.
            Extra recipients of the email that
            don't see who else got the email.
        html : str, optional
            HTML body of the email. May contain
            Jinja templated variables of the 
            tables, images and other variables.
        text_body : str, optional
            Text body of the email.
        body_images : dict of bytes, path-likes and figures, optional
            HTML images to embed with the html. The key should be 
            as Jinja variables in the html and the values represent
            images (path to an image, bytes of an image or image object).
        body_tables : Dict[str, pd.DataFrame], optional
            HTML tables to embed with the html. The key should be 
            as Jinja variables in the html and the values are Pandas
            DataFrames.
        html_params : dict, optional
            Extra parameters passed to html_table as Jinja parameters.

        Examples
        --------
            >>> sender = EmailSender(host="myserver", port=1234)
            >>> sender.send(
                sender="me@gmail.com",
                receiver="you@gmail.com",
                subject="Some news",
                html='<h1>Hi,</h1> Nice to meet you. Look at this: <img src="{{ my_image }}">',
                body_images={"my_image": Path("C:/path/to/img.png")}
            )
            >>> sender.send(
                sender="me@gmail.com",
                receiver="you@gmail.com",
                subject="Some news",
                html='<h1>Hi {{ name }},</h1> Nice to meet you. Look at this table: <img src="{{ my_table }}">',
                body_images={"my_image": Path("C:/path/to/img.png")},
                html_params={"name": "Jack"},
            )

        Returns
        -------
        EmailMessage
            Email message.
        """
        msg = self.get_message(**kwargs)
        self.send_message(msg)
        return msg
        
    def get_message(self, 
                  subject:str=None,
                  receivers:list=None,
                  sender:str=None,
                  cc:list=None,
                  bcc:list=None,
                  html:str=None,
                  text:str=None,
                  html_template=None,
                  text_template=None,
                  body_images:Dict[str, str]=None, 
                  body_tables:Dict[str, str]=None, 
                  body_params:dict=None,
                  attachments:dict=None) -> EmailMessage:
        """Get the email message."""

        subject = subject or self.subject
        sender = sender or self.sender or self.user_name
        receivers = receivers or self.receivers

        html = html or self.html
        text = text or self.text
        html_template = html_template or self.html_template
        text_template = text_template or self.text_template

        if subject is None:
            raise ValueError("Email must have a subject")

        msg = self._create_body(
            subject=subject, 
            sender=sender, 
            receivers=receivers,
            cc=cc,
            bcc=bcc,
        )

        if text is not None or text_template is not None:
            body = TextBody(
                template=self.get_text_template(text_template),
                table_template=self.get_text_table_template(),
            )
            body.attach(
                msg, 
                text, 
                tables=body_tables,
                jinja_params=self.get_text_params(extra=body_params, sender=sender),
            )

        if html is not None or html_template is not None:
            body = HTMLBody(
                template=self.get_html_template(html_template),
                table_template=self.get_html_table_template(),
            )
            body.attach(
                msg,
                html=html,
                images=body_images,
                tables=body_tables,
                jinja_params=self.get_html_params(extra=body_params, sender=sender)
            )
        if attachments:
            att = Attachments(attachments, encoding=self.attachment_encoding)
            att.attach(msg)
        return msg

    def _create_body(self, subject, sender, receivers=None, cc=None, bcc=None) -> EmailMessage:
        msg = EmailMessage()
        msg["from"] = sender
        msg["subject"] = subject
        
        # To whoom the email goes
        if receivers:
            msg["to"] = receivers
        if cc:
            msg['cc'] = cc
        if bcc:
            msg['bcc'] = bcc
        return msg

    def send_message(self, msg):
        "Send the created message"
        user = self.user_name
        password = self.password
        
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        if user is not None or password is not None:
            server.login(user, password)
        server.send_message(msg)
        
        server.quit()
    
    def get_params(self, sender:str):
        "Get Jinja parametes passed to template"
        # TODO: Add receivers to params
        return {
            "node": node(),
            "user": getuser(),
            "now": datetime.datetime.now(),
            "sender": EmailAddress(sender),
        }

    def get_html_params(self, extra:Optional[dict]=None, **kwargs):
        params = self.get_params(**kwargs)
        params.update({
            "error": Error(content_type='html-inline')
        })
        if extra:
            params.update(extra)
        return params

    def get_text_params(self, extra:Optional[dict]=None, **kwargs):
        params = self.get_params(**kwargs)
        params.update({
            "error": Error(content_type='text')
        })
        if extra:
            params.update(extra)
        return params

    def get_html_table_template(self, layout=None) -> jinja2.Template:
        layout = self.default_html_theme if layout is None else layout
        if layout is None:
            return None
        return self.templates_html_table.get_template(layout)

    def get_html_template(self, layout=None) -> jinja2.Template:
        if layout is None:
            return None
        return self.templates_html.get_template(layout)

    def get_text_table_template(self, layout=None) -> jinja2.Template:
        layout = self.default_text_theme if layout is None else layout
        if layout is None:
            return None
        return self.templates_text_table.get_template(layout)

    def get_text_template(self, layout=None) -> jinja2.Template:
        if layout is None:
            return None
        return self.templates_text.get_template(layout)

    def set_template_paths(self, html=None, text=None, html_table=None, text_table=None):
        """Create Jinja envs for body templates using given paths
        
        This is a shortcut for manually setting them like:
        .. clode-block:: python

            sender.templates_html = jinja2.Environment(loader=jinja2.FileSystemLoader(...))
            sender.templates_text = jinja2.Environment(loader=jinja2.FileSystemLoader(...))
            ...
        """
        if html is not None:
            self.templates_html = jinja2.Environment(loader=jinja2.FileSystemLoader(html))
        if text is not None:
            self.templates_text = jinja2.Environment(loader=jinja2.FileSystemLoader(text))
        if html_table is not None:
            self.templates_html_table = jinja2.Environment(loader=jinja2.FileSystemLoader(html_table))
        if text_table is not None:
            self.templates_text_table = jinja2.Environment(loader=jinja2.FileSystemLoader(text_table))