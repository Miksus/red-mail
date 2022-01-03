
# Red Mail
> Next generation email sender

---

[![Pypi version](https://badgen.net/pypi/v/redmail)](https://pypi.org/project/redmail/)
[![build](https://github.com/Miksus/red-mail/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Miksus/red-mail/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Miksus/red-mail/branch/master/graph/badge.svg?token=IMR1CQT9PY)](https://codecov.io/gh/Miksus/red-mail)
[![Documentation Status](https://readthedocs.org/projects/red-mail/badge/?version=latest)](https://red-mail.readthedocs.io/en/latest/)
[![PyPI pyversions](https://badgen.net/pypi/python/redmail)](https://pypi.org/project/redmail/)


## What is it?
Red Mail is an advanced email sender library. It makes sending emails trivial and 
has a lot of advanced features such as:

- [Attachments](https://red-mail.readthedocs.io/en/latest/tutorials/attachments.html)
- [Templating (with Jinja)](https://red-mail.readthedocs.io/en/latest/tutorials/jinja_support.html)
- [Embedded images](https://red-mail.readthedocs.io/en/latest/tutorials/body_content.html#embedded-images)
- [Prettified tables](https://red-mail.readthedocs.io/en/latest/tutorials/body_content.html#embedded-tables)
- [Send as cc or bcc](https://red-mail.readthedocs.io/en/latest/tutorials/sending.html#sending-email-with-cc-and-bcc)
- [Gmail preconfigured](https://red-mail.readthedocs.io/en/latest/tutorials/config.html#gmail)

See more from the [documentations](https://red-mail.readthedocs.io/en/latest/)
or see [release from PyPI](https://pypi.org/project/redmail/).

Install it from PyPI:

```shell
pip install redmail
```

## Why Red Mail?

Sending emails **SHOULD NOT** be this complicated:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart('alternative')
msg['Subject'] = 'An example email'
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
```

With Red Mail, it is simple as this:

```python
from redmail import EmailSender

email = EmailSender(host="localhost", port=0)

email.send(
    subject="An example email",
    sender="me@example.com",
    receivers=['first.last@example.com'],
    text="Hello!",
    html="<h1>Hello!</h1>"
)
```

You can also do more advanced things easily with it:

```python
from redmail import EmailSender

email = EmailSender(
    host="localhost", port=0,
    user_name="me@example.com", password="<PASSWORD>"
)

email.send(
    subject="An example email",
    sender="me@example.com",

    # Recipients
    receivers=['first.last@example.com'],
    cc=["also@example.com"],
    bcc=["external@example.com"],

    # Body of the email
    html="""<h1>Hello {{ friend }}!</h1>
        <p>Have you seen this thing:</p>
        {{ awesome_image }}
        <p>Or this:</p>
        {{ pretty_table }}
        <p>Or this plot:</p>
        {{ a_plot }}
        <p>Kind regards, {{ sender.full_name }}</p>
    """,

    # Content that is embed to the body
    body_params={'friend': 'Jack'},
    body_images={
        'awesome_image': 'path/to/image.png',
        'a_plot': plt.Figure(...)
    },
    body_tables={
        'pretty_table': pd.DataFrame(...)
    },

    # Attachments of the email
    attachments={
        'some_data.csv': pd.DataFrame(...),
        'file_content.html': '<h1>This is an attachment</h1>',
        'a_file.txt': pathlib.Path('path/to/file.txt')
    }
)
```

See more practical example in [cookbook](https://red-mail.readthedocs.io/en/latest/tutorials/cookbook.html).

---

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

