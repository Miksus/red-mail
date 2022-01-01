
:red:`Red` Mail
===============

Red Mail is a Python library for sending emails. 
It makes sending emails a breeze regardless of if 
you need to include HTML, embed images or tables or
attach documents. 

Sending emails is a pretty straight forward task.
However, the standard SMTP libraries don't make 
it particularly easy especially if you want to 
include more than basic text. Red Mail aims to 
fix this and it makes sending emails a breeze 
regardless of if you need to include attachments,
images or prettier HTML.


Why Red Mail?
-------------

Standard SMTP libraries are not very convenient to use. They let you modify any part of the 
message but simply sending emails **SHOULD NOT** look like this:

.. code-block:: python

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'The contents of {textfile}'
    msg['From'] = 'first.last@gmail.com'
    msg['To'] = 'first.last@example.com'

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
        subject="The contents of myfile",
        receivers=['first.last@example.com'],
        text="Hello!",
        html="<h1>Hello!</h1>"
    )

Here are also other reasons to use Red Mail:

- :ref:`You can put attachments to the email <attachments>`
- :ref:`You can include images to the body <embedding-images>`
- :ref:`You can render nicer tables to the body <embedding-tables>`
- :ref:`It has Jinja support <jinja-support>`
- :ref:`You can reuse your HTML templates <templating>`
- :ref:`Gmail pre-configured <config-gmail>`
- :ref:`Send with cc and bcc <send-cc-bcc>`

In addition, normally tables in emails look like this:

.. image:: /imgs/table_without_style.png
   :width: 200px
   
Red Email styles them like this:

.. image:: /imgs/table_with_style.png
   :width: 200px

More Examples
-------------

You could attach things to your email:

.. code-block:: python

    from pathlib import Path
    import pandas as pd

    email.send(
        subject="Email subject",
        receivers=["me@gmail.com"],
        text_body="Hi, this is a simple email.",
        attachments={
            'myfile.csv': Path("path/to/data.csv"),
            'myfile.xlsx': pd.DataFrame({'A': [1, 2, 3]}),
            'myfile.html': '<h1>This is content of an attachment</h1>'
        }
    )


By default, HTML tables in emails look ugly. Red Mail has premade templates
to turn them more visually pleasing. Just include them as Jinja parameters 
in body and pass them as Pandas dataframes:

.. code-block:: python

    import pandas as pd

    email.send(
        subject="Email subject",
        receivers=["me@gmail.com"],
        html="""
            <h1>Hi,</h1> 
            <p>have you seen this?</p> 
            {{ mytable }}
        """,
        body_tables={"mytable": pd.DataFrame({'a': [1,2,3], 'b': [1,2,3]})}
    )

You can also include images similarly:

.. code-block: python

    from pathlib import Path
    import pandas as pd

    email.send(
        subject="Email subject",
        receivers=["me@gmail.com"],
        html="""
            <h1>Hi,</h1> 
            <p>have you seen this?</p> 
            {{ myimg }}
        """,
        body_images={"myimg": "path/to/my/image.png"}
    )


Interested?
-----------

There is much more to offer. Install the package:

.. code-block:: console

    pip install redmail

and read further.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorials/index
   references


Indices and tables
==================

* :ref:`genindex`
