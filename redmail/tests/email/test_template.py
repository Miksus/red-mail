from redmail import EmailSender

import pytest
import pandas as pd

from convert import remove_extra_lines
from getpass import getpass, getuser
from platform import node


def test_template(tmpdir):
    
    html_templates = tmpdir.mkdir("html_tmpl")
    html_templates.join("example.html").write("""<h1>Hi {{ friend }},</h1><p>have you checked this open source project '{{ project_name }}'?</p><p>- {{ sender.full_name }}</p>""")
    expected_html = f"<h1>Hi Jack,</h1><p>have you checked this open source project 'RedMail'?</p><p>- Me</p>\n"

    text_templates = tmpdir.mkdir("text_tmpl")
    text_templates.join("example.txt").write("""Hi {{ friend }}, \nhave you checked this open source project '{{ project_name }}'? \n- {{ sender.full_name }}""")
    expected_text = f"Hi Jack, \nhave you checked this open source project 'RedMail'? \n- Me\n"

    sender = EmailSender(server=None, port=1234)
    sender.set_template_paths(
        html=str(html_templates),
        text=str(text_templates),
    )
    msg = sender.get_message(
        sender="me@gmail.com",
        receiver="you@gmail.com",
        subject="Some news",
        html_template='example.html',
        text_template='example.txt',
        body_params={"friend": "Jack", 'project_name': 'RedMail'}
    )
    
    assert "multipart/alternative" == msg.get_content_type()

    #text = remove_extra_lines(msg.get_payload()[0].get_payload()).replace("=20", "").replace('"3D', "")
    text = remove_extra_lines(msg.get_payload()[0].get_payload()).replace("=20", "").replace('"3D', "")
    html = remove_extra_lines(msg.get_payload()[1].get_payload()).replace("=20", "").replace('"3D', "")

    assert expected_html == html
    assert expected_text == text