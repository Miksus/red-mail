
Frequently Asked Questions
==========================

Circular Import
---------------

**Question**

I get this error:

.. code-block:: console

    Traceback (most recent call last):
    File "..\email.py", line 1, in <module>
        from redmail import EmailSender
    File "..\redmail\__init__.py", line 1, in <module>
        from .email.sender import EmailSender, send_email, gmail, outlook
    File "..\redmail\email\__init__.py", line 1, in <module>
        from redmail.email.sender import EmailSender
    File "..\redmail\email\sender.py", line 3, in <module>
        from email.message import EmailMessage
    File "..\email.py", line 1, in <module>
        from redmail import EmailSender
    ImportError: cannot import name 'EmailSender' from partially initialized module 'redmail' (most likely due to a circular import) (..\redmail\__init__.py) 

**Answer**

This is due to your script is named as ´´email.py´´ and that happens 
to be the same name as the email library from standard library.
Please use another filename than *email.py*. 

From in Text Body 
-----------------

**Question**

In text body, a line starting with *From* gets turned to *>From*.
For example, I have this code:

.. code-block:: python

    from redmail import EmailSender

    email = EmailSender(...)

    email.send(
        subject="An example email",
        sender="me@example.com",
        receivers=['me@example.com'],
        text="Hi!\nFrom what we discussed..."
    )

But email body looks like this:

.. code-block:: console

    Hi!
    >From what we discussed...

**Answer**

Please use HTML body instead if this causes problems. This is a problem 
in smtplib itself and there is nothing to do with it at the moment. 
Line beginning with **From** is mangled to **>From** to avoid body 
injection and there is no way to switch that off. See more details from
`this Stackoverflow answer <https://stackoverflow.com/a/71518593/13696660>`_.
