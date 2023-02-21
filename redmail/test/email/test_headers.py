import datetime
import socket
from textwrap import dedent
import sys
import re

import pytest

from redmail import EmailSender

from convert import remove_email_content_id, prune_generated_headers

import platform
PYTHON_VERSION = sys.version_info
IS_PY37 = sys.version_info < (3, 8)

def test_date():
    format = "%a, %d %b %Y %H:%M:%S -0000"
    email = EmailSender(host=None, port=1234)

    before = datetime.datetime.now(datetime.timezone.utc)
    msg = email.get_message(sender="me@example.com", subject="Some email")
    after = datetime.datetime.now(datetime.timezone.utc)
    date_strings = re.findall(r'(?<=Date: )[^\r\n]+', str(msg))
    assert len(date_strings) == 1
    for dt_string in date_strings:

        # Validate the Date fits to the format
        datetime.datetime.strptime(dt_string, format)

        # It should not take longer than second to generate the email
        assert dt_string in (before.strftime(format), after.strftime(format))

def test_message_id():
    domain = socket.getfqdn()
    email = EmailSender(host=None, port=1234)

    if IS_PY37:
        # Python <=3.7 has problems with domain names with UTF-8
        # This is mostly problem with CI.
        # We simulate realistic domain name
        domain = "REDMAIL-1234.mail.com"
        email.domain = domain

    msg = email.get_message(sender="me@example.com", subject="Some email")
    msg2 = email.get_message(sender="me@example.com", subject="Some email")

    message_ids = re.findall(r'(?<=Message-ID: )[^\r\n]+', str(msg))
    assert len(message_ids) == 1
    message_id = message_ids[0]

    # [0-9]{{12}}[.][0-9]{{5}}[.][0-9]{{20}}
    assert bool(re.search(fr'<[0-9.]+@{domain}>', message_id))

    # Check another email has not the same Message-ID
    message_id_2 = re.findall(r'(?<=Message-ID: )[^\r\n]+', str(msg2))[0]
    assert message_id != message_id_2

def test_cc_bcc():
    email = EmailSender(host=None, port=1234)
    if IS_PY37:
        # CI has FQDN that has UTF-8 chars and goes to new line
        # for Python <=3.7. We set a realistic looking domain
        # name for easier testing
        email.domain = "REDMAIL-1234.mail.com"
    msg = email.get_message(sender="me@example.com", subject="Some email", cc=['you@example.com'], bcc=['he@example.com', 'she@example.com'])
    msg = prune_generated_headers(str(msg))
    assert remove_email_content_id(msg) == dedent("""
    From: me@example.com
    Subject: Some email
    Cc: you@example.com
    Bcc: he@example.com, she@example.com
    Message-ID: <<message_id>>
    Date: <date>

    """)[1:].replace('\n', '\r\n')

@pytest.mark.parametrize("how", ["instance", "email"])
def test_custom_headers(how):
    email = EmailSender(host=None, port=1234)
    headers = {"Importance": "high"}

    if IS_PY37:
        # Python <=3.7 has problems with domain names with UTF-8
        # This is mostly problem with CI.
        # We simulate realistic domain name
        domain = "REDMAIL-1234.mail.com"
        email.domain = domain

    if how == "email":
        msg = email.get_message(
            sender="me@example.com",
            subject="Some email",
            headers=headers
        )
    elif how == "instance":
        email.headers = headers
        msg = email.get_message(
            sender="me@example.com",
            subject="Some email",
        )
    msg = prune_generated_headers(str(msg))
    assert remove_email_content_id(msg) == dedent("""
    From: me@example.com
    Subject: Some email
    Message-ID: <<message_id>>
    Date: <date>
    Importance: high

    """)[1:].replace('\n', '\r\n')

@pytest.mark.parametrize("how", ["instance", "email"])
def test_custom_headers_override(how):
    email = EmailSender(host=None, port=1234)
    headers = {
        "Date": datetime.datetime(2021, 1, 31, 6, 56, 46, tzinfo=datetime.timezone.utc),
        "Message-ID": "<167294165062.31860.1664530310632362057@LAPTOP-1234GML0>"
    }

    if how == "email":
        msg = email.get_message(
            sender="me@example.com",
            subject="Some email",
            headers=headers
        )
    elif how == "instance":
        email.headers = headers
        msg = email.get_message(
            sender="me@example.com",
            subject="Some email",
        )
    assert str(msg) == dedent("""
    From: me@example.com
    Subject: Some email
    Message-ID: <167294165062.31860.1664530310632362057@LAPTOP-1234GML0>
    Date: Sun, 31 Jan 2021 06:56:46 +0000

    """)[1:].replace('\n', '\r\n')
