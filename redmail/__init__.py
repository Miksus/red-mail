from .email import EmailSender, send_email, gmail
from .log import EmailHandler, MultiEmailHandler
from . import _version
__version__ = _version.get_versions()['version']
