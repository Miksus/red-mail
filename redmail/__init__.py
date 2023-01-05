from .email import EmailSender, send_email, gmail, outlook
from .log import EmailHandler, MultiEmailHandler

try:
    from ._version import *
except ImportError:
    # Package was not built the standard way
    __version__ = version = '0.0.0.UNKNOWN'
    __version_tuple__ = version_tuple = (0, 0, 0, 'UNKNOWN', '')
