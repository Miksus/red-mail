.. _cookbook:

Cook Book
=========

This section provides various handy tips.

.. _config-gmail:

Gmail
-----

You need to make an app password `see this Google's answer <https://support.google.com/accounts/answer/185833>`_. 
When that is done you can use Red Mail's gmail object that has the Gmail
server pre-configured:

.. code-block:: python

    from redmail import gmail
    gmail.user_name = 'example@gmail.com' # Your Gmail user
    gmail.password = '<APP PASSWORD>'

    # And then you can send emails
    gmail.send(
        subject="Example email",
        receivers=['example@gmail.com']
        text="Hi, this is an email."
    )

.. note::

    You can only send emails using your Gmail email address. Changing ``sender`` has no effect.

Error Alerts
------------

If you are building long running program (ie. web app) you can make a
templated error alerts that include the full traceback:

.. code-block:: python

    from redmail import EmailSender
    
    error_email = EmailSender(...)
    error_email.receivers = ['me@example.com']
    error_email.html = """<h2>An error encountered</h2>{{ error }}"""

    try:
        raise RuntimeError("Oops")
    except:
        # Send an email including the traceback
        error_email.send(subject="Fail: doing stuff failed")