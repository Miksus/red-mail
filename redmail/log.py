
import logging
from logging import Handler, LogRecord
from logging.handlers import SMTPHandler, BufferingHandler
from textwrap import dedent
from typing import List, Optional
import warnings

from redmail.email.sender import EmailSender

class _EmailHandlerMixin:

    def __init__(self, email, kwargs):
        if email is not None:
            # Using copy to prevent modifying the sender
            # if it is used somewhere else
            email = email.copy()
            self.email = email
            self._set_email_kwargs(kwargs)
        else:
            self.set_email(**kwargs)
        self._validate_email()

    def set_email(self, 
                   host, port,
                   username=None, password=None,
                   **kwargs):
        "Create a simple default sender"
        if "user_name" in kwargs and username is None:
            warnings.warn("Argument user_name is replaced with username. Please use username instead.", FutureWarning)
            username = kwargs.pop("user_name")
        self.email = EmailSender(
            host=host, port=port,
            username=username, password=password
        )
        
        self._set_email_kwargs(kwargs)

    def get_subject(self, record):
        "Format subject of the email sender"
        return self.email.subject.format(
            record=record, handler=self
        )

    def _set_email_kwargs(self, kwargs:dict):
        for attr, value in kwargs.items():
            if not hasattr(self.email, attr):
                raise AttributeError(f"EmailSender has no attribute {attr}")
            setattr(self.email, attr, value)

        # Set default message body if nothing specified
        has_no_body = (
            self.email.text is None 
            and self.email.text_template is None 
            and self.email.html is None
            and self.email.html_template is None
        )
        if has_no_body:
            self.email.text = self.default_text

    def _validate_email(self):
        "Validate the email has all required attributes for logging"
        req_attrs = ('host', 'port', 'subject', 'receivers')
        missing = []
        for attr in req_attrs:
            if getattr(self.email, attr) is None:
                missing.append(attr)
        if missing:
            cls_name = type(self).__name__
            raise TypeError(f'{cls_name} email sender missing attributes: {missing}')

class EmailHandler(_EmailHandlerMixin, Handler):
    """Logging handler for sending a log record as an email

    Parameters
    ----------
    level : int
        Log level of the handler
    email : EmailSender
        Sender instance to be used for sending
        the log records.
    kwargs : dict
        Keyword arguments for creating the 
        sender if ``email`` was not passed.

    Examples
    --------

        Minimal example:

        .. code-block:: python

            handler = EmailHandler(
                host="smtp.myhost.com", port=0,
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
            email.email = "no-reply@example.com"
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
            handler = EmailHandler(email=email)

            import logging
            logger = logging.getLogger()
            logger.addHandler(handler)
    """
    email: EmailSender

    default_text = "{{ msg }}"

    def __init__(self, level:int=logging.NOTSET, email:EmailSender=None, **kwargs):
        _EmailHandlerMixin.__init__(self, email=email, kwargs=kwargs)
        Handler.__init__(self, level)


    def emit(self, record:logging.LogRecord):
        "Emit a record (send email)"

        self.email.send(
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
    email : EmailSender
        Sender instance to be used for sending
        the log records.
    kwargs : dict
        Keyword arguments for creating the 
        sender if ``email`` was not passed.

    Examples
    --------

        Minimal example:

        .. code-block:: python

            handler = MultiEmailHandler(
                host="smtp.myhost.com", port=0,
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
            handler = EmailHandler(sender=email)

            import logging
            logger = logging.getLogger()
            logger.addHandler(handler)
    """

    default_text = dedent("""
    Log Recods:
    {% for record in records -%}
    {{ handler.format(record) }}
    {% endfor %}""")[1:]

    def __init__(self, capacity:Optional[int]=None, email:EmailSender=None, **kwargs):
        _EmailHandlerMixin.__init__(self, email=email, kwargs=kwargs)
        BufferingHandler.__init__(self, capacity)

    def flush(self):
        "Flush the records (send an email)"
        self.acquire()
        try:
            msgs = []
            for rec in self.buffer:
                # This creates msg, exc_text etc. to the LogRecords
                msgs.append(self.format(rec))
                # For some reason logging does not create this attr unless having asctime in the format string
                if self.formatter is None:
                    rec.asctime = logging.Formatter().formatTime(rec)

            self.email.send(
                subject=self.get_subject(self.buffer),
                body_params={
                    "records": self.buffer,
                    "msgs": msgs,
                    "handler": self
                }
            )
            self.buffer = []
        finally:
            self.release()

    def shouldFlush(self, record):
        """Should the handler flush its buffer?

        Returns true if the buffer is up to capacity. This method can be overridden to implement custom flushing strategies.
        """
        if self.capacity is None:
            # Only manual flushing
            return False
        else:
            return super().shouldFlush(record)

    def get_subject(self, records:List[LogRecord]):
        "Get subject of the email"
        if records:
            min_level = min([record.levelno for record in records])
            max_level = max([record.levelno for record in records])
            fmt_kwds = {
                "min_level_name": logging.getLevelName(min_level),
                "max_level_name": logging.getLevelName(max_level),
            }
        else:
            # No log records, getting something
            fmt_kwds = {
                "min_level_name": logging.getLevelName(logging.NOTSET),
                "max_level_name": logging.getLevelName(logging.NOTSET),
            }

        return self.email.subject.format(
            **fmt_kwds,
            handler=self,
            records=records
        )