from .email import EmailSender, send_email, gmail, outlook
from .log import EmailHandler, MultiEmailHandler
from . import _version
__version__ = _version.get_versions()['version']
