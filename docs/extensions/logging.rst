.. meta::
   :description: Email logger for Python. 
   :keywords: send, email, Python, logging

.. _ext-logging:

Email Logging
=============

Red Mail also provides logging handlers which
extends the :stdlib:`logging library's <logging.html>`
:stdlib:`handlers <logging.handlers.html>` from the standard library. 
The logging library also has :stdlib:`SMTPHandler <logging.handlers.html#smtphandler>`
but its features are somewhat restricted. It does only 
send a logging message formatted as plain text and it 
sends only one log record per email. 

Red Mail's email handlers, on the other hand, 
are capable of formatting the emails in arbitrary ways
and it also enables to send multiple log records 
with one email. Red Mail is more feature complete and 
provides more customizable logging experience.

There are two log handlers provided by Red Mail:

- :ref:`EmailHandler <ext-emailhandler>`: Sends one log record per email
- :ref:`MultiEmailHandler <ext-multiemailhandler>`: Sends multiple log records with one email

The mechanics are simple and very similar between these two handlers.

.. _ext-emailhandler:

EmailHandler
------------

To send one log record per email, use :class:`.EmailHandler`:

.. code-block:: python

    import logging
    from redmail import EmailHandler

    hdlr = EmailHandler(
        host="localhost",
        port=0,
        subject="A log record",
        sender="no-reply@example.com",
        receivers=["me@example.com"],
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

    # To use:
    logger.warning("A warning happened")

.. note::

    You may pass the :class:`.EmailSender` 
    directly as an argument ``email``, for 
    example:

    .. code-block:: python

        from redmail import EmailSender
        hdlr = EmailHandler(
            email=EmailSender(host="localhost", port=0)
            subject="A log record",
            receivers=["me@example.com"],
        )

    Note that a copy of the :class:`.EmailSender` is created
    in order to avoid affecting the usage of the instance 
    elsewhere. Additional arguments (such as subject, sender,
    receivers, text, html, etc.) are set as attributes to 
    this copied instance.

You may also template the subject and the bodies:

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

As you may have noted, the subject can contain string formatting.
The following arguments are passed to the string format:

============== ========================= ==================================
Argument       Type                      Description
============== ========================= ==================================
record         logging.LogRecord         Log records to send
handler        EmailHandler              EmailHandler itself
============== ========================= ==================================

In addition, the text and HTML bodies are processed using Jinja and the 
following parameters are passed:

======== ================= ===================
Argument Type              Description
======== ================= ===================
record   logging.LogRecord Log record
msg      str               Formatted message
handler  EmailHandler      EmailHandler itself
======== ================= ===================


.. _ext-multiemailhandler:

MultiEmailHandler
-----------------

To send multiple log records with one email, use :class:`.MultiEmailHandler`:

.. code-block:: python

    import logging
    from redmail import MultiEmailHandler

    hdlr = MultiEmailHandler(
        capacity=2, # Sends email after every second record
        host="localhost",
        port=0,
        subject="log records",
        sender="no-reply@example.com",
        receivers=["me@example.com"],
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

    # To use:
    logger.warning("A warning happened")
    logger.warning("Another warning happened")
    # (Now an email should have been sent)

    # You may also manually flush
    logger.warning("A warning happened")
    hdlr.flush()

.. note::

    You may pass the :class:`.EmailSender` 
    directly as an argument ``email``, for 
    example:

    .. code-block:: python

        from redmail import EmailSender
        hdlr = MultiEmailHandler(
            email=EmailSender(host="localhost", port=0)
            subject="Log records",
            receivers=["me@example.com"],
        )

    Note that a copy of the :class:`.EmailSender` is created
    in order to avoid affecting the usage of the instance 
    elsewhere. Additional arguments (such as subject, sender,
    receivers, text, html, etc.) are set as attributes to 
    this copied instance.

You may also template the subject and the bodies:

.. code-block:: python

    import logging
    from redmail import EmailHandler

    hdlr = MultiEmailHandler(
        host="localhost",
        port=0,
        subject="Log Records: {min_level_name} - {max_level_name}",
        receivers=["me@example.com"],
        text="""Logging level: 
            {% for record in records %}
            Level name: {{ record.levelname }}
            Message: {{ record.msg }}
            {% endfor %}
        """,
        html="""
            <ul>
            {% for record in records %}
                <li>Logging level: {{ record.levelname }}</li>
                <li>Message: {{ record.msg }}</li>
            {% endfor %}
            </ul>
        """,
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)

As you may have noted, the subject can contain string formatting.
The following arguments are passed to the string format:

============== ========================= ==================================
Argument       Type                      Description
============== ========================= ==================================
records        list of logging.LogRecord Log records to send
min_level_name str                       Name of the lowest log level name
max_level_name str                       Name of the highest log level name
handler        MultiEmailHandler         MultiEmailHandler itself
============== ========================= ==================================

In addition, the text and HTML bodies are processed using Jinja and the 
following parameters are passed:

======== ========================= ==========================
Argument Type                      Description
======== ========================= ==========================
records  list of logging.LogRecord List of log records
msgs     list of str               List of formatted messages
handler  MultiEmailHandler         MultiEmailHandler itself
======== ========================= ==========================

