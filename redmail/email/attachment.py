
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import io
from pathlib import Path, PurePath
from typing import Union

from .utils import PIL, plt, pd


class Attachments:

    def __init__(self, attachments:Union[list, dict], encoding='UTF-8'):
        self.attachments = attachments
        self.encoding = encoding

    def attach(self, msg:EmailMessage):
        for part in self._get_parts():
            msg.attach(part)

    def _get_parts(self):
        if isinstance(self.attachments, dict):
            for name, cont in self.attachments.items():
                yield self._get_part_named(cont, name=name)
        elif isinstance(self.attachments, (list, set, tuple)):
            for cont in self.attachments:
                yield self._get_part(cont)
        else:
            # A single attachment
            yield self._get_part(self.attachments)

    def _get_part(self, item) -> MIMEBase:
        cont = self._get_bytes(item)
        filename = self._get_filename(item)
        part = MIMEApplication(cont)
        part.add_header(
            "Content-Disposition",
            "attachment", filename=filename
        )
        part.add_header('Content-Transfer-Encoding', 'base64')
        return part

    def _get_part_named(self, item, name) -> MIMEBase:
        cont = self._get_bytes_named(item, name)

        part = MIMEApplication(cont)
        part.add_header(
            "Content-Disposition",
            "attachment", filename=name
        )
        return part

    def _get_bytes(self, item) -> bytes:
        if isinstance(item, str):
            # Considered as path
            if Path(item).is_file():
                return Path(item).read_bytes()
            else:
                raise ValueError(f"Unknown attachment '{item}'. Perhaps a mistyped path?")
        elif isinstance(item, PurePath):
            return item.read_bytes()
        else:
            raise TypeError(f"Unknown attachment {type(item)}")

    def _get_bytes_named(self, item, name:str) -> bytes:

        has_pandas = pd is not None
        has_pillow = PIL is not None
        has_matplotlib = plt is not None

        if isinstance(item, str):
            # Considered as raw document
            return item
        elif isinstance(item, PurePath):
            return item.read_bytes()
        elif has_pandas and isinstance(item, (pd.DataFrame, pd.Series)):
            buff = io.BytesIO()
            if name.endswith(".xlsx"):
                item.to_excel(buff)
                return buff.getvalue()
            elif name.endswith(".csv"):
                return item.to_csv().encode(self.encoding)
            elif name.endswith(".html"):
                return item.to_html().encode(self.encoding)
            elif name.endswith('.txt'):
                return str(item)
            else:
                raise ValueError(f"Unknown dataframe conversion for '{name}'")
        elif isinstance(item, (bytes, bytearray)):
            return item
        elif has_pillow and isinstance(item, PIL.Image.Image):
            buf = io.BytesIO()
            item.save(buf, format='PNG')
            buf.seek(0)
            return buf.read()
        elif has_matplotlib and isinstance(item, plt.Figure):
            buf = io.BytesIO()
            item.savefig(buf, format=Path(name).suffix[1:])
            buf.seek(0)
            return buf.read()
        else:
            raise TypeError(f"Unknown attachment {type(item)} ({name})")

    def _get_filename(self, item):
        if isinstance(item, str):
            # Considered as path
            # NOTE: the validation it is a file should already be
            # done
            return Path(item).name
        elif isinstance(item, PurePath):
            return item.name
        else: # pragma: no cover
            # NOTE: this piece of code should not be run as the type check is
            # done before. If this is run, then there is an unfinished feature.
            raise NotImplementedError(f"Cannot figure out filename for {item}") 