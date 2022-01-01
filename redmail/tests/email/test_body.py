from redmail import EmailSender

import pytest
import pandas as pd

from convert import remove_extra_lines
from getpass import getpass, getuser
from platform import node

from redmail.tests.helpers.convert import remove_email_extra

def test_text_message():
    text = "Hi, nice to meet you."

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        text=text,
    )
    payload = msg.get_payload()
    expected_headers = {
        'from': 'me@gmail.com', 
        'subject': 'Some news', 
        'to': 'you@gmail.com', 
        'MIME-Version': '1.0', 
        'Content-Type': 'text/plain; charset="utf-8"',
        'Content-Transfer-Encoding': '7bit',
    }

    assert "text/plain" == msg.get_content_type()
    assert text + "\n" == payload

    # Test receivers etc.
    headers = dict(msg.items())
    assert expected_headers == headers

def test_html_message():
    html = "<h3>Hi,</h3><p>Nice to meet you</p>"

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html=html,
    )
    payload = msg.get_payload()
    expected_headers = {
        'from': 'me@gmail.com', 
        'subject': 'Some news', 
        'to': 'you@gmail.com', 
        #'MIME-Version': '1.0', 
        'Content-Type': 'multipart/alternative'
    }

    assert "multipart/alternative" == msg.get_content_type()
    assert html + "\n" == payload[0].get_content()

    # Test receivers etc.
    headers = dict(msg.items())
    assert expected_headers == headers

def test_text_and_html_message():
    html = "<h3>Hi,</h3><p>nice to meet you.</p>"
    text = "Hi, nice to meet you."

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html=html,
        text=text,
    )
    payload = msg.get_payload()
    expected_headers = {
        'from': 'me@gmail.com', 
        'subject': 'Some news', 
        'to': 'you@gmail.com', 
        'MIME-Version': '1.0', 
        'Content-Type': 'multipart/alternative'
    }

    assert "multipart/alternative" == msg.get_content_type()

    assert "text/plain" == payload[0].get_content_type()
    assert text + "\n" == payload[0].get_content()

    assert "text/html" == payload[1].get_content_type()
    assert html + "\n" == payload[1].get_content()

    # Test receivers etc.
    headers = dict(msg.items())
    assert expected_headers == headers
    
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
    
    assert "multipart/alternative" == msg.get_content_type()

    text = remove_email_extra(msg.get_payload()[0].get_payload())
    html = remove_email_extra(msg.get_payload()[1].get_payload())

    assert expected_html == html
    assert expected_text == text

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
    text = remove_email_extra(msg.get_payload()[0].get_payload())
    html = remove_email_extra(msg.get_payload()[1].get_payload())

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
    assert {
        'from': 'me@gmail.com', 
        'to': 'you@gmail.com, they@gmail.com', 
        'subject': 'Some email', 
        'Content-Type': 'text/plain; charset="utf-8"', 
        'Content-Transfer-Encoding': '7bit', 
        'MIME-Version': '1.0'
    } == dict(msg.items())