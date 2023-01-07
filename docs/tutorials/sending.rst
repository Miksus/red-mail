.. meta::
   :description: Send email in Python.
   :keywords: send, email, Python

.. _sending-emails:

Sending Emails
==============

This section covers the basics of sending emails.
See :ref:`configure` to revise how ``EmailSender``
is configured. At minimum, sending an email requires:

.. code-block:: python

    from redmail import EmailSender
    email = EmailSender(host='localhost', port=0)

    email.send(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com']
    )

.. note::

    If you don't spesify the ``sender``, the sender is considered to 
    be ``email.sender``. If ``email.sender`` is also missing, the sender
    is then set to be ``email.username``. Ensure that any of these is a 
    valid email address.

    Similar flow of logic applies to most attributes. You can set defaults on the 
    ``email`` instance which are used in case they are not passed via the 
    method call ``email.send(...)``.

    Here is an example:

    .. code-block:: python

        email = EmailSender(host='localhost', port=0)
        email.subject = "email subject"
        email.receivers = ["you@example.com"]
        email.send(
            sender="me@example.com",
            subject="important email"
        )

    The above sends an email that has ``"important email"`` as the email subject
    and the email is sent to address ``you@example.com``.

.. note::

    Some email providers (such as Gmail) do not allow specifying
    sender. For example, Gmail will outright ignore it and always
    use your own email address.

Sending Email with Text Body
----------------------------

To send an email with plain text message:

.. code-block:: python

   email.send(
       subject='email subject',
       sender="me@example.com",
       receivers=['you@example.com'],
       text="Hi, this is an email."
   )

Sending Email with HTML Body
----------------------------

To send an email with html content:

.. code-block:: python

    email.send(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        html="""
            <h1>Hi,</h1>
            <p>this is an email.</p>
        """
    )


Sending Email with text and HTML Body
-------------------------------------

You can also include both to your email:

.. code-block:: python

    email.send(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hi, this is an email.",
        html="""
            <h1>Hi,</h1>
            <p>this is an email.</p>
        """
    )

.. _send-cc-bcc:

Sending Email with cc and bcc
-----------------------------

You can also include carbon copy (cc) and blind carbon copy (bcc)
to your emails:

.. code-block:: python

    email.send(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        cc=['also@example.com'],
        bcc=['outsider@example.com']
    )

.. _send-alias:

Sending Email with Alias
------------------------

You can also alias the sender and receivers:

.. code-block:: python

    email.send(
        subject='email subject',
        sender="The Sender <me@example.com>",
        receivers=['The Receiver <you@example.com>']
    )

Alias is an alternative text that is displayed instead of 
the actual email addresses. The receivers can still get 
the addresses though.

.. _send-headers:

Sending with Custom Headers
---------------------------

Sometimes you might want to override or add custom 
email headers to your email. For example, you 
might want to set a custom date for the email and 
set it as important:

.. code-block:: python

    import datetime

    email.send(
        subject='email subject',
        sender="The Sender <me@example.com>",
        receivers=['you@example.com'],
        headers={
            "Importance": "high",
            "Date": datetime.datetime(2021, 1, 31, 6, 56, 46)
        }
    )

Read more about email headers from `IANA's website <https://www.iana.org/assignments/message-headers/message-headers.xhtml>`_.

.. note::

    Headers passed this way can override the other headers such 
    as ``From``, ``To``, ``Cc``, ``Bcc``, ``Date`` and ``Message-ID``.

.. _send-multi:

Sending Multiple Emails
-----------------------

Normally Red Mail opens and closes the connection to the SMTP
server when sending each email. If you are sending large amount
of emails it may be beneficial to leave the connection open:

.. code-block:: python

    with email:
        email.send(
            subject='email subject',
            sender="me@example.com",
            receivers=['you@example.com']
        )

        email.send(
            subject='email subject',
            sender="me@example.com",
            receivers=['they@example.com']
        )
        ...

Alternatively, you may use the ``connect`` and ``close``
methods:

.. code-block:: python

    try:
        email.connect()
        email.send(
            subject='email subject',
            sender="me@example.com",
            receivers=['you@example.com']
        )
        email.send(
            subject='email subject',
            sender="me@example.com",
            receivers=['they@example.com']
        )
        ...
    finally:
        email.close()
