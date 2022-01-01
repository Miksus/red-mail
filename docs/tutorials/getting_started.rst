.. _getting-started:

Getting started
===============

Install the package from `Pypi <https://pypi.org/project/redmail/>`_:

.. code-block:: console

    pip install redengine

.. _configure:

Configuring Email
-----------------

You can configure your sender by:


.. code-block:: python

   from redmail import EmailSender

   email = EmailSender(
       host='<SMTP HOST>',
       port='<SMTP PORT>',
       user_name='<USER_NAME>',
       password='<PASSWORD>'
   )

If your SMTP server does not require login to send emails then 
just don't pass ``user_name`` and ``password`` to ``EmailSender``.

Alternatively, if you use Gmail there is a pre-configured sender
which you can just import and set user name and password:

.. code-block:: python

   from redmail import gmail

   gmail.user_name = 'me@gmail.com'
   gmail.password = '<PASSWORD>'

Sending Emails
--------------

You can just send emails by calling the method ``send``:

.. code-block:: python

   email.send(
       subject='email subject',
       receivers=['first.last@example.com'],
       text="Hi, this is an email."
   )

Next tutorial covers sending emails more thoroughly.