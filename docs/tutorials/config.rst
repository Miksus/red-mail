
Configuring for Different Providers
===================================

.. _config-gmail:

Gmail
-----

You need to make an application password `see this Google's answer <https://support.google.com/accounts/answer/185833>`_.
You may also need to set up `2-step verification <https://support.google.com/accounts/answer/185839>`_ in order to
be able to create an application password. Don't worry, those are easy things to configure.

When you have your application password you can use Red Mail's gmail object that has the Gmail
server pre-configured:

.. code-block:: python

    from redmail import gmail
    gmail.user_name = 'example@gmail.com' # Your Gmail address
    gmail.password = '<APP PASSWORD>'

    # And then you can send emails
    gmail.send(
        subject="Example email",
        receivers=['example@gmail.com']
        text="Hi, this is an email."
    )

.. note::

    You can only send emails using your Gmail email address. Changing ``sender`` has no effect.

.. note::

    ``gmail`` is actually nothing more than an instance of :class:`redmail.EmailSender`
    with ``smtp.gmail.com`` as the host and ``587`` as the port.