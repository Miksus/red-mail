from redmail import EmailSender

import pytest
import pandas as pd

from convert import remove_extra_lines
from getpass import getpass, getuser
from platform import node

def test_text_message():
    text = "Hi, nice to meet you."

    sender = EmailSender(server=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receiver="you@gmail.com",
        subject="Some news",
        text_body=text,
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

    sender = EmailSender(server=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receiver="you@gmail.com",
        subject="Some news",
        html_body=html,
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

    sender = EmailSender(server=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receiver="you@gmail.com",
        subject="Some news",
        html_body=html,
        text_body=text,
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

    sender = EmailSender(server=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receiver="you@gmail.com",
        subject="Some news",
        text_body=text,
        html_body=html,
        body_params=extra
    )
    
    assert "multipart/alternative" == msg.get_content_type()

    #text = remove_extra_lines(msg.get_payload()[0].get_payload()).replace("=20", "").replace('"3D', "")
    text = remove_extra_lines(msg.get_payload()[0].get_payload()).replace("=20", "").replace('"3D', "")
    html = remove_extra_lines(msg.get_payload()[1].get_payload()).replace("=20", "").replace('"3D', "")

    assert expected_html == html
    assert expected_text == text
