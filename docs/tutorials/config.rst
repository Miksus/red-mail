
Configuring for Different Providers
===================================

Sending emails from different email providers is easy.
If you have your own SMTP server, you just need to 
set the host address, port and possibly the credentials.
There are also pre-configured sender instances for 
common email providers:

=================== =================== ================== ====
Provider            Sender instance     Host               Port
=================== =================== ================== ====
Gmail (Google)      ``redmail.gmail``   smtp.gmail.com     587
Outlook (Microsoft) ``redmail.outlook`` smtp.office365.com 587          
=================== =================== ================== ====

To use them, you may need to configure the account (see below)
and then you can use the sender:

.. code-block:: python

    from redmail import outlook
    outlook.username = 'example@hotmail.com'
    outlook.password = '<YOUR PASSWORD>'

    outlook.send(
        subject="Example email",
        receivers=['you@example.com'],
        text="Hi, this is an email."
    )

.. note::

    Often the email providers don't allow changing the sender address
    to something else than what was used to log in. Therefore, changing 
    the ``sender`` argument often has no effect.

.. note::

    By default, Red Mail uses STARTTLS which should be suitable for majority of cases
    and the pre-configured ports should support this. However, in some cases you may 
    need to use other protocol and port. In such case, you may override the ``sender.port`` 
    and ``sender.cls_smtp`` attributes. Read more about configuring different protocols 
    from :ref:`config-smtp`.


.. _config-gmail:

Gmail
-----

In order to send emails using Gmail, you need to:

- Set up `2-step verification <https://support.google.com/accounts/answer/185839>`_ (if not already)
- Generate `an App password <https://support.google.com/accounts/answer/185833>`_:

    - Go to your `Google account <https://myaccount.google.com/>`_
    - Go to *Security*
    - Go to *App passwords*
    - Generate a new one (you may use custom app and give it a custom name)

When you have your application password you can use Red Mail's gmail object that has the Gmail
server pre-configured:

.. code-block:: python

    from redmail import gmail
    gmail.username = 'example@gmail.com' # Your Gmail address
    gmail.password = '<APP PASSWORD>'

    # And then you can send emails
    gmail.send(
        subject="Example email",
        receivers=['you@example.com'],
        text="Hi, this is an email."
    )

.. note::

    Gmail requires emails sent via its API 
    to be `RFC 2822 <https://www.rfc-editor.org/rfc/rfc2822>`_
    compliant. Messages without ``Message-ID`` headers may
    fail as of 2022. Red Mail always generates a unique message ID.

.. _config-outlook:

Outlook
-------

You may also send emails from MS Outlook. To do so, you just need to have a Microsoft
account. There is a pre-configured sender which you may use:

.. code-block:: python

    from redmail import outlook
    outlook.username = 'example@hotmail.com'
    outlook.password = '<YOUR PASSWORD>'

    # And then you can send emails
    outlook.send(
        subject="Example email",
        receivers=['you@example.com'],
        text="Hi, this is an email."
    )
