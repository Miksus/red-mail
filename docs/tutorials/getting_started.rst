.. meta::
   :description: Send email in Python. 
   :keywords: send, email, Python

.. _getting-started:

Getting started
===============

Install the package from `Pypi <https://pypi.org/project/redmail/>`_:

.. code-block:: console

    pip install redmail

Or install the package using Conda:

.. code-block:: console

    conda install -c conda-forge redmail

.. _configure:

Configuring Email
-----------------

You can configure your sender by:

.. code-block:: python

   from redmail import EmailSender

   email = EmailSender(
       host='<SMTP HOST>',
       port='<SMTP PORT>',
       username='<USERNAME>',
       password='<PASSWORD>'
   )

.. code-block:: python

   # Or if your SMTP server does not require credentials
   email = EmailSender(
       host='<SMTP HOST>',
       port='<SMTP PORT>',
   )

.. note::

    The correct SMTP port is typically 587.

There are guides to set up the following email providers:

- :ref:`config-gmail`
- :ref:`config-outlook`

.. note::

    By default, Red Mail uses **STARTTLS** as the protocol.
    This is suitable for majority of cases but if you need
    to use **SSL**, **TLS** or other protocols, see :ref:`config-smtp`.

Sending Emails
--------------

You can just send emails by calling the method ``send``:

.. code-block:: python

   email.send(
       subject='email subject',
       sender="me@example.com",
       receivers=['you@example.com'],
       text="Hi, this is an email."
   )

Next tutorial covers sending emails more thoroughly.
