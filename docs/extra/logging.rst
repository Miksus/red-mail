
.. _logging:

Red Mail Logging Handlers
=========================

Red Mail also has logging handlers which
work with the *logging* library from Python's
standard library. You may also use the `SMTPHandler <https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SMTPHandler>`_ 
from logging library but Red Mail provides more 
customizable alternatives. Red Mail also has a 
handler that is capable of sending multiple 
records at once.

EmailHandler
------------

To send one email per log record, use :class:`EmailHandler`.

.. code-block:: python

    import logging
    from redmail import EmailHandler

    hdlr = EmailHandler(
        host="localhost",
        port=0,
        subject="A log record",
        receivers=["me@example.com"],
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

.. note::

    You may pass the :class:`EmailSender` 
    directly as an argument ``email``, for 
    example:

    .. code-block:: python

        from redmail import EmailSender
        hdlr = EmailHandler(
            email=EmailSender(host="localhost", port=0)
            subject="A log record",
            receivers=["me@example.com"],
        )

    Note that a copy of the :class:`EmailSender` is created
    in order to avoid affecting the usage of the instance 
    elsewhere. Additional arguments (such as subject, sender,
    receivers, text, html, etc.) are set as attributes to 
    this copy.


Then to use this, simply:

.. code-block:: python

    logger.warning("A warning happened")

You may also customize the subject to include the level name (ie. info, debug, etc.):

.. code-block:: python

    hdlr = EmailHandler(
        host="localhost",
        port=0,
        subject="Log Record: {record.levelname}",
        receivers=["me@example.com"],
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

You may also customize the subject and the bodies

.. code-block:: python

    import logging
    from redmail import EmailHandler

    hdlr = EmailHandler(
        host="localhost",
        port=0,
        subject="Log Record: {record.levelname}",
        receivers=["me@example.com"],
        text="Logging level: {{ record.levelname }}\nMessage: {{ msg }}",
        html="<ul><li>Logging level: {{ record.levelname }}</li><li>Message: {{ msg }}</li></ul>",
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

The following arguments are passed to the string format:

======== =====
Argument Type  Description
======== =====
record   logging.LogRecord
handler  EmailHandler
======== =====

And the passed Jinja parameters:

======== =====
Argument Type              Description
======== =====
record   logging.LogRecord Log record
msg      str               Formatted message
handler  EmailHandler      Handler itself
======== =====


MultiEmailHandler
-----------------

In case sending emails after each log record is too much, you may use :class:`MultiEmailHandler`
that sends the log records via email after specific number of log records have occurred, when 
manually flushed or using custom logic.

A simple example:

.. code-block:: python

    import logging
    from redmail import MultiEmailHandler

    hdlr = MultiEmailHandler(
        capacity=2, # Sends email after every second record
        host="localhost",
        port=0,
        subject="log records",
        receivers=["me@example.com"],
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

Then to use this, simply:

.. code-block:: python

    logger.warning("A warning happened")
    logger.warning("A warning happened")
    # Should have now sent an email

    # Manually flush
    logger.warning("A warning happened")
    hdlr.flush()

.. note::

    You may pass the :class:`EmailSender` 
    directly as an argument ``email``, for 
    example:

    .. code-block:: python

        from redmail import EmailSender
        hdlr = MultiEmailHandler(
            email=EmailSender(host="localhost", port=0)
            subject="Log records",
            receivers=["me@example.com"],
        )

    Note that a copy of the :class:`EmailSender` is created
    in order to avoid affecting the usage of the instance 
    elsewhere. Additional arguments (such as subject, sender,
    receivers, text, html, etc.) are set as attributes to 
    this copy.

The following arguments are passed to the subject format:

======== =====
Argument Type  Description
======== =====
records        list of logging.LogRecord
min_level_name str                           Name of the lowest log level name
max_level_name str                           Name of the highest log level name
handler        EmailHandler
======== =====

And the passed Jinja parameters:

======== =====
Argument Type              Description
======== =====
record   logging.LogRecord Log record
msg      str               Formatted message
handler  EmailHandler      Handler itself
======== =====