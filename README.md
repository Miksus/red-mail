
# Red Mail: Advanced Email Sender
> Next generation email sender

---

[![Pypi version](https://badgen.net/pypi/v/redmail)](https://pypi.org/project/redmail/)
[![build](https://github.com/Miksus/red-mail/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Miksus/red-mail/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Miksus/red-mail/branch/master/graph/badge.svg?token=IMR1CQT9PY)](https://codecov.io/gh/Miksus/red-mail)
[![Documentation Status](https://readthedocs.org/projects/red-mail/badge/?version=latest)](https://red-mail.readthedocs.io/en/latest/)
[![PyPI pyversions](https://badgen.net/pypi/python/redmail)](https://pypi.org/project/redmail/)


## What is it?
Red Mail is an advanced email sender library. 
It is a sister library for [Red Box, advanced email reader](https://github.com/Miksus/red-box).
It makes sending emails trivial and has a lot of advanced features such as:

- [Attachments](https://red-mail.readthedocs.io/en/stable/tutorials/attachments.html)
- [Templating (with Jinja)](https://red-mail.readthedocs.io/en/stable/tutorials/jinja_support.html)
- [Embedded images](https://red-mail.readthedocs.io/en/stable/tutorials/body_content.html#embedded-images)
- [Prettified tables](https://red-mail.readthedocs.io/en/stable/tutorials/body_content.html#embedded-tables)
- [Send as cc or bcc](https://red-mail.readthedocs.io/en/stable/tutorials/sending.html#sending-email-with-cc-and-bcc)
- [Gmail preconfigured](https://red-mail.readthedocs.io/en/stable/tutorials/config.html#gmail)

See more from the [documentations](https://red-mail.readthedocs.io)
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

More examples:
- [simple example](https://red-mail.readthedocs.io/en/stable/tutorials/example.html#simple-example)
- [email with attachments](https://red-mail.readthedocs.io/en/stable/tutorials/example.html#attachments)
- [email with embedded images](https://red-mail.readthedocs.io/en/stable/tutorials/example.html#embedded-images)
- [email with embedded plots](https://red-mail.readthedocs.io/en/stable/tutorials/example.html#embedded-plots)
- [email with body parameters](https://red-mail.readthedocs.io/en/stable/tutorials/example.html#parametrization)

See practical examples from the [cookbook](https://red-mail.readthedocs.io/en/stable/tutorials/cookbook.html).

---

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

