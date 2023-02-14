from textwrap import dedent
import sys
from redmail import EmailSender

import pytest

from convert import remove_extra_lines, payloads_to_dict
from getpass import getpass, getuser
from platform import node

from convert import remove_email_extra, remove_email_content_id, prune_generated_headers

IS_PY37 = sys.version_info < (3, 8)

def test_text_message():

    sender = EmailSender(host=None, port=1234)
    if IS_PY37:
        # CI has FQDN that has UTF-8 chars and goes to new line
        # for Python <=3.7. We set a realistic looking domain
        # name for easier testing
        sender.domain = "REDMAIL-1234.mail.com"

    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="Some news",
        text="Hi, nice to meet you.",
    )
    msg = prune_generated_headers(str(msg))
    assert str(msg) == dedent("""
    From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <<message_id>>
    Date: <date>
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    Hi, nice to meet you.
    """)[1:].replace('\n', '\r\n')


def test_html_message():

    sender = EmailSender(host=None, port=1234)
    if IS_PY37:
        # CI has FQDN that has UTF-8 chars and goes to new line
        # for Python <=3.7. We set a realistic looking domain
        # name for easier testing
        sender.domain = "REDMAIL-1234.mail.com"

    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="Some news",
        html="<h3>Hi,</h3><p>Nice to meet you</p>",
    )
    msg = prune_generated_headers(str(msg))
    assert remove_email_content_id(str(msg)) == dedent("""
    From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <<message_id>>
    Date: <date>
    Content-Type: multipart/mixed; boundary="===============<ID>=="

    --===============<ID>==
    Content-Type: multipart/alternative;
     boundary="===============<ID>=="

    --===============<ID>==
    Content-Type: text/html; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    <h3>Hi,</h3><p>Nice to meet you</p>

    --===============<ID>==--

    --===============<ID>==--
    """)[1:].replace('\n', '\r\n')


def test_text_and_html_message():

    sender = EmailSender(host=None, port=1234)
    if IS_PY37:
        # CI has FQDN that has UTF-8 chars and goes to new line
        # for Python <=3.7. We set a realistic looking domain
        # name for easier testing
        sender.domain = "REDMAIL-1234.mail.com"

    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="Some news",
        html="<h3>Hi,</h3><p>nice to meet you.</p>",
        text="Hi, nice to meet you.",
    )
    msg = prune_generated_headers(str(msg))
    assert remove_email_content_id(str(msg)) == dedent("""
    From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <<message_id>>
    Date: <date>
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary="===============<ID>=="

    --===============<ID>==
    Content-Type: multipart/alternative;
     boundary="===============<ID>=="

    --===============<ID>==
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit

    Hi, nice to meet you.

    --===============<ID>==
    Content-Type: text/html; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    <h3>Hi,</h3><p>nice to meet you.</p>

    --===============<ID>==--

    --===============<ID>==--
    """)[1:].replace('\n', '\r\n')


@pytest.mark.parametrize(
    "html,expected_html,text,expected_text,extra", [
        pytest.param(
            "<h3>Hi,</h3> <p>This is {{ user }} from {{ node }}. I'm really {{ sender.full_name }}.</p>",
            f"<h3>Hi,</h3> <p>This is {getuser()} from {node()}. I'm really Me.</p>\n",

            "Hi, \nThis is {{ user }} from {{ node }}. I'm really {{ sender.full_name }}.",
            f"Hi, \nThis is {getuser()} from {node()}. I'm really Me.\n",

            None,
            id="With default extras"
        ),
        pytest.param(
            "<h3>Hi {{ receiver }},</h3> <p>This is {{ user }} from {{ node }}. I'm really {{ sender.full_name }}.</p>", 
            f"<h3>Hi you,</h3> <p>This is overridden from {node()}. I'm really Me.</p>\n",

            "Hi {{ receiver }}, This is {{ user }} from {{ node }}. I'm really {{ sender.full_name }}.",
            f"Hi you, This is overridden from {node()}. I'm really Me.\n", 

            {"user": "overridden", "receiver": "you"},
            id="Custom extra"
        ),
    ]
)
def test_with_jinja_params(html, text, extra, expected_html, expected_text):

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        text=text,
        html=html,
        body_params=extra
    )
    
    # Validate structure
    structure = payloads_to_dict(msg)
    assert structure == {
        'multipart/mixed': {
            'multipart/alternative': {
                'text/plain': structure["multipart/mixed"]["multipart/alternative"]["text/plain"],
                'text/html': structure["multipart/mixed"]["multipart/alternative"]["text/html"],
            }
        }
    }

    assert "multipart/mixed" == msg.get_content_type()
    alternative = msg.get_payload()[0]
    text_part, html_part = alternative.get_payload()
    
    text = remove_email_extra(text_part.get_payload())
    html = remove_email_extra(html_part.get_payload())

    assert expected_html == html
    assert expected_text == text

@pytest.mark.parametrize("use_jinja_obj,use_jinja", [
    pytest.param(None, False, id="Use arg"),
    pytest.param(False, None, id="Use attr"),
    pytest.param(True, False, id="Override"),
])
def test_without_jinja(use_jinja_obj, use_jinja):
    html = "<h3>Hi,</h3> <p>This is {{ user }} from { node }. I'm really {{ sender.full_name }}.</p>"
    text = "Hi, \nThis is {{ user }} from { node }. I'm really {{ sender.full_name }}."

    sender = EmailSender(host=None, port=1234)
    if IS_PY37:
        # CI has FQDN that has UTF-8 chars and goes to new line
        # for Python <=3.7. We set a realistic looking domain
        # name for easier testing
        sender.domain = "REDMAIL-1234.mail.com"

    sender.use_jinja = use_jinja_obj
    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="Some news",
        text=text,
        html=html,
        use_jinja=use_jinja,
    )
    encoding = '7bit' if IS_PY37 else 'quoted-printable' 
    expected = dedent("""
    From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <<message_id>>
    Date: <date>
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary="===============<ID>=="

    --===============<ID>==
    Content-Type: multipart/alternative;
     boundary="===============<ID>=="

    --===============<ID>==
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit

    Hi, 
    This is {{ user }} from { node }. I'm really {{ sender.full_name }}.

    --===============<ID>==
    Content-Type: text/html; charset="utf-8"
    Content-Transfer-Encoding: """ + encoding + """
    MIME-Version: 1.0

    <h3>Hi,</h3> <p>This is {{ user }} from { node }. I'm really {{ sender.full_n=
    ame }}.</p>

    --===============<ID>==--

    --===============<ID>==--
    """)[1:].replace('\n', '\r\n')
    if IS_PY37:
        expected = expected.replace('sender.full_n=\r\n', 'sender.full_n')
    msg = prune_generated_headers(str(msg))
    assert remove_email_content_id(msg) == expected


def test_with_error():
    sender = EmailSender(host=None, port=1234)
    try:
        raise RuntimeError("Deliberate failure")
    except:
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            text="Error occurred \n{{ error }}",
            html="<h1>Error occurred: </h1>{{ error }}",
        )

    alternative = msg.get_payload()[0]
    text_part, html_part = alternative.get_payload()

    text = remove_email_extra(text_part.get_payload())
    html = remove_email_extra(html_part.get_payload())

    if IS_PY37:
        text = text.replace('Error occurred \n', 'Error occurred\n')
        html = html.replace('<span style="color:', '<span style=3D"color:')
    assert text.startswith('Error occurred\nTraceback (most recent call last):\n  File "')
    assert text.endswith(', in test_with_error\n    raise RuntimeError("Deliberate failure")\nRuntimeError: Deliberate failure\n')

    assert html.startswith('<h1>Error occurred: </h1>\n        <div>\n            <h4>Traceback (most recent call last):</h4>\n            <pre><code>  File &quot;')
    assert html.endswith(', in test_with_error\nraise RuntimeError(&quot;Deliberate failure&quot;)</code></pre>\n            <span style=3D"color: red; font-weight: bold">Deliberate failure</span>: <span>RuntimeError</span>\n        </div>\n')

def test_set_defaults():
    email = EmailSender(host=None, port=1234)
    email.sender = 'me@gmail.com'
    email.receivers = ['you@gmail.com', 'they@gmail.com']
    email.subject = "Some email"
    msg = email.get_message(text="Hi, an email")
    headers = {
        key: val if key not in ('Message-ID', 'Date') else '<ID>'
        for key, val in msg.items()
    }
    assert {
        'From': 'me@gmail.com', 
        'To': 'you@gmail.com, they@gmail.com', 
        'Subject': 'Some email', 
        'Content-Type': 'text/plain; charset="utf-8"', 
        'Content-Transfer-Encoding': '7bit', 
        'MIME-Version': '1.0',
        'Message-ID': '<ID>',
        'Date': '<ID>',
    } == headers

def test_missing_subject():
    email = EmailSender(host=None, port=1234)
    with pytest.raises(ValueError):
        email.get_message(sender="me@example.com", receivers=['you@example.com'])


def test_no_table_templates():
    email = EmailSender(host="localhost", port=0)

    assert email.default_html_theme == "modest.html"
    assert email.default_text_theme == "pandas.txt"

    email.default_html_theme = None
    email.default_text_theme = None
    msg = email.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        text="An example",
        html="<h1>An example</h1>"
    )
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    assert headers == {
        'From': 'me@gmail.com', 
        'Subject': 'Some news', 
        'To': 'you@gmail.com', 
        'MIME-Version': '1.0', 
        'Content-Type': 'multipart/mixed',
    }