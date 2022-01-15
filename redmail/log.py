
import logging
from logging import Handler, LogRecord
from logging.handlers import SMTPHandler, BufferingHandler
from textwrap import dedent
from typing import List

from redmail.email.sender import EmailSender

class _EmailHandlerMixin:

    def set_sender(self, 
                   host, port, 
                   user_name=None, password=None, 
                   sender=None, receivers=None,
                   subject=None):
        "Create a simple default sender"
        self.sender = EmailSender(
            host=host, port=port,
            user_name=user_name, password=password
        )
        self.sender.receivers = receivers
        self.sender.sender = sender
        if receivers is not None:
            self.sender.receivers = receivers
        elif user_name is not None:
            self.sender.receivers = user_name
        else:
            raise ValueError("Missing receiver")
        
        self.sender.text = self.default_text
        self.sender.subject = subject or "Log record"

    def get_subject(self, record):
        "Get subject of the email"
        if self.fmt_subject is not None:
            return self.fmt_subject.format(
                record=record, handler=self
            )


class EmailHandler(_EmailHandlerMixin, Handler):
    """Logging handler for sending a log record as an email

    Parameters
    ----------
    level : int
        Log level of the handler
    sender : EmailSender
        Sender instance to be used for sending
        the log records.
    fmt_subject : str, optional
        Format of the email subject. ``record``
        is passed as a format argument.
    kwargs : dict
        Keyword arguments for creating the 
        sender if ``sender`` was not passed.

    Examples
    --------

        Minimal example:

        .. code-block:: python

            handler = EmailHandler(
                host="smtp.myhost.com", port=0,
                fmt_subject="Log: {record.levelname}",
                sender="no-reply@example.com",
                receivers=["me@example.com"],
            )

        Customized example:

        .. code-block:: python

            from redmail import EmailSender
            email = EmailSender(
                host="smtp.myhost.com",
                port=0
            )
            email.sender = "no-reply@example.com"
            email.receivers = ["me@example.com"]
            email.html = '''
                <h1>Record: {{ record.levelname }}</h1>
                <pre>{{ record.msg }}</pre>
                <h2>Info</h2>
                <ul>
                    <li>Path: {{ record.pathname }}</li>
                    <li>Function: {{ record.funcName }}</li>
                    <li>Line number: {{ record.lineno }}</li>
                </ul>
            '''
            handler = EmailHandler(sender=email, fmt_subject="{record.name}}: {record.levelname}")

            import logging
            logger = logging.getLogger()
            logger.addHandler(handler)
    """

    def __init__(self, level:int=logging.NOTSET, sender:EmailSender=None, fmt_subject=None, **kwargs):
        super().__init__(level)
        if sender is not None:
            self.sender = sender
        else:
            self.set_sender(**kwargs)
        self.fmt_subject = fmt_subject

    default_text = "{{ msg }}"

    def emit(self, record:logging.LogRecord):
        "Emit a record"

        self.sender.send(
            subject=self.get_subject(record),
            body_params={
                "record": record,
                "msg": self.format(record),
                "handler": self,
            }
        )


class MultiEmailHandler(_EmailHandlerMixin, BufferingHandler):
    """Logging handler for sending multiple log records as an email

    Parameters
    ----------
    capacity : int
        Number of 
    sender : EmailSender
        Sender instance to be used for sending
        the log records.
    fmt_subject : str, optional
        Format of the email subject. ``record``
        is passed as a format argument.
    kwargs : dict
        Keyword arguments for creating the 
        sender if ``sender`` was not passed.

    Examples
    --------

        Minimal example:

        .. code-block:: python

            handler = MultiEmailHandler(
                host="smtp.myhost.com", port=0,
                fmt_subject="Log: {min_level_name} - {max_level_name}",
                sender="no-reply@example.com",
                receivers=["me@example.com"],
            )

        Customized example:

        .. code-block:: python

            from redmail import EmailSender
            email = EmailSender(
                host="smtp.myhost.com",
                port=0
            )
            email.sender = "no-reply@example.com"
            email.receivers = ["me@example.com"]
            email.html = '''
                <h1>Record: {{ record.levelname }}</h1>
                <pre>{{ record.msg }}</pre>
                <h2>Info</h2>
                <ul>
                    <li>Path: {{ record.pathname }}</li>
                    <li>Function: {{ record.funcName }}</li>
                    <li>Line number: {{ record.lineno }}</li>
                </ul>
            '''
            handler = EmailHandler(sender=email, fmt_subject="{record.name}}: {record.levelname}")

            import logging
            logger = logging.getLogger()
            logger.addHandler(handler)
    """

    default_text = dedent("""
    {% for record in records -%}
    Log Record
    ----------------------------
    {% set msg = handler.format(record) -%}
    {{ msg }}


    {% endfor %}""")[1:]

    def __init__(self, capacity:int, sender:EmailSender=None, fmt_subject=None, **kwargs):
        super().__init__(capacity)
        if sender is not None:
            self.sender = sender
        else:
            self.set_sender(**kwargs)
        self.fmt_subject = fmt_subject

    def flush(self):
        "Flush (send) the records"
        self.acquire()
        try:
            
            for rec in self.buffer:
            # This creates msg, exc_text etc. to LogRecords
                self.format(rec)
                # For some reason logging does not create this attr unless having asctime in the format string
                if self.formatter is None:
                    rec.asctime = logging.Formatter().formatTime(rec)

            self.sender.send(
                subject=self.get_subject(self.buffer),
                body_params={
                    "records": self.buffer,
                    "handler": self
                }
            )
            self.buffer = []
        finally:
            self.release()

    def get_subject(self, records:List[LogRecord]):
        "Get subject of the email"
        if self.fmt_subject is not None:
            min_level = min([record.levelno for record in records])
            max_level = max([record.levelno for record in records])
            return self.fmt_subject.format(
                min_level_name=logging.getLevelName(min_level), 
                max_level_name=logging.getLevelName(max_level),
                handler=self,
                records=records
            )