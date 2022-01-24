

Email Logging with Red Mail
===========================

Red Mail also has logging handlers which
extends the :stdlib:`logging library's <logging.html>`
:stdlib:`logging handlers <logging.handlers.html>`. 
The logging library already has 
:stdlib:`SMTPHandler <logging.handlers.html#smtphandler>`
but the features are somewhat restricted. It does only 
send a logging message formatted as plain text. 

Red Mail's email handlers are capable of formatting the 
log records in arbitrary ways using Jinja, creating 
visually more pleasing HTML emails and sending multiple 
log records via email at once.

If you would like to send one email per log record,
:ref:`ext-emailhandler` is what you need. In case you 
would like to reduce the amount of emails and send 
multiple log records at once, use :ref:`ext-multiemailhandler`.

.. _ext-emailhandler:

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

============== ========================= ==================================
Argument       Type                      Description
============== ========================= ==================================
record         logging.LogRecord         Log records to send
handler        EmailHandler              EmailHandler itself
============== ========================= ==================================

And the passed Jinja parameters:

======== ================= =================
Argument Type              Description
======== ================= =================
record   logging.LogRecord Log record
msg      str               Formatted message
handler  EmailHandler      Handler itself
======== ================= =================


.. _ext-multiemailhandler:

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

============== ========================= ==================================
Argument       Type                      Description
============== ========================= ==================================
records        list of logging.LogRecord Log records to send
min_level_name str                       Name of the lowest log level name
max_level_name str                       Name of the highest log level name
handler        EmailHandler              MultiEmailHandler itself
============== ========================= ==================================

And the passed Jinja parameters:

======== ========================= ==========================
Argument Type                      Description
======== ========================= ==========================
records  list of logging.LogRecord Log record
msgs     list of str               List of formatted messages
handler  EmailHandler              Handler itself
======== ========================= ==========================


..
   External links

.. _stdlib_logging: https://docs.python.org/3/library/logging.html