
.. meta::
   :description: Red Mail is an advanced email sender for Python. It is open source and well tested.
   :keywords: send, email, Python

:red:`Red` Mail: Send Emails in Python
=============================================

.. image:: https://badgen.net/pypi/v/redmail
   :target: https://pypi.org/project/redmail/

.. image:: https://badgen.net/pypi/python/redmail
   :target: https://pypi.org/project/redmail/

Red Mail is a Python library for sending emails. 
It makes sending emails very trivial regardless of whether 
you need to embed images, plots, tables or
attach documents. It also provides you convenient 
templating options and it is easy to create email alerts, 
email reports or client notifications with it.

Visit the `source code from Github <https://github.com/Miksus/red-mail>`_
or `releases in Pypi page <https://pypi.org/project/redmail/>`_.


Why Red Mail?
-------------

Sending emails is a pretty straight forward task.
However, the standard SMTP libraries don't make 
it particularly easy and sending emails **SHOULD NOT** 
look like this:

.. code-block:: python

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'An example email'
    msg['From'] = 'me@example.com'
    msg['To'] = 'you@example.com'

    part1 = MIMEText("Hello!", 'plain')
    part2 = MIMEText("<h1>Hello!</h1>", 'html')

    msg.attach(part1)
    msg.attach(part2)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost', port=0)
    s.send_message(msg)
    s.quit()


It should look like this:

.. code-block:: python

    from redmail import EmailSender

    email = EmailSender(host="localhost", port=0)

    email.send(
        subject="An example email",
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hello!",
        html="<h1>Hello!</h1>"
    )

There are also other reasons to use Red Mail:

- :ref:`You can put attachments to the email <attachments>`
- :ref:`You can include images to the body <embedding-images>`
- :ref:`You can render nicer tables to the body <embedding-tables>`
- :ref:`It has Jinja support <jinja-support>`
- :ref:`You can reuse your HTML templates <templating>`
- :ref:`Gmail pre-configured <config-gmail>`
- :ref:`Send with cc and bcc <send-cc-bcc>`
- And it is well tested and documented


More Examples
-------------

Interested in more? 
Here are some more quick examples:

- :ref:`examples-simple`
- :ref:`examples-attachments`
- :ref:`examples-embed-image`
- :ref:`examples-embed-plot`
- :ref:`examples-embed-table`
- :ref:`examples-parametrized`
- :ref:`examples-mega`


Interested?
-----------

Install the package:

.. code-block:: console

    pip install redmail


Some more practical examples:

- :ref:`cookbook-campaign`
- :ref:`cookbook-alerts`
- :ref:`cookbook-stats`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorials/index
   references
   versions


Indices and tables
==================

* :ref:`genindex`
