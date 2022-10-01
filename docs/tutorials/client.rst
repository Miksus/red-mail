
.. _config-smtp:

Configuring SMTP Client
=======================

Often the default client setup is enough but sometimes it may become necessary to get more control
of the connection with your SMTP server. In this discussion we discuss ways to customize the connection.

By default Red Mail uses `STARTTLS <https://en.wikipedia.org/wiki/Opportunistic_TLS>`_ or opportunistic
TLS in connecting to the SMTP server. You may also change this if needed by changing the 
``cls_smtp`` to other SMTP client classes from ::stdlib:`smtplib <smtplib.html>`
in standard library.

.. note::

    Extra keyword arguments in :class:`.EmailSender` initiation are passed to the SMTP client.
    Please see the documentation of the SMTP client you are seeking.

STARTTLS
--------

By default, Red Mail uses `STARTTLS <https://en.wikipedia.org/wiki/Opportunistic_TLS>`_ 
which is configured as this:

.. code-block:: python

    from redmail import EmailSender
    from smtplib import SMTP

    email = EmailSender(
        host="smtp.example.com",
        port=587,
        cls_smtp=SMTP,
        use_starttls=True
    )


SMTP TLS
--------

You may also continue using TLS:

.. code-block:: python

    from redmail import EmailSender

    email = EmailSender(
        host="smtp.example.com",
        port=587,
        use_starttls=False
    )


SMTP SSL
--------

To use SSL:

.. code-block:: python

    from redmail import EmailSender
    from smtplib import SMTP_SSL

    email = EmailSender(
        host="smtp.example.com",
        port=587,
        cls_smtp=SMTP_SSL,
    )

You may also pass the SSL context:

.. code-block:: python

    from redmail import EmailSender
    from smtplib import SMTP_SSL
    from ssl import SSLContext

    email = EmailSender(
        host="smtp.example.com",
        port=587,
        cls_smtp=SMTP_SSL,
        context=SSLContext(...)
    )

LMTP
----

To use LMTP:

.. code-block:: python

    from redmail import EmailSender
    from smtplib import LMTP

    email = EmailSender(
        host="smtp.example.com",
        port=587,
        cls_smtp=LMTP
    )

