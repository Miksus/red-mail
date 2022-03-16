from redmail import EmailSender

import pytest

from convert import remove_email_extra
from getpass import getpass, getuser
from platform import node


def test_template(tmpdir):
    
    html_templates = tmpdir.mkdir("html_tmpl")
    html_templates.join("example.html").write("""<h1>Hi {{ friend }},</h1><p>have you checked this open source project '{{ project_name }}'?</p><p>- {{ sender.full_name }}</p>""")
    expected_html = f"<h1>Hi Jack,</h1><p>have you checked this open source project 'RedMail'?</p><p>- Me</p>\n"

    text_templates = tmpdir.mkdir("text_tmpl")
    text_templates.join("example.txt").write("""Hi {{ friend }}, \nhave you checked this open source project '{{ project_name }}'? \n- {{ sender.full_name }}""")
    expected_text = f"Hi Jack, \nhave you checked this open source project 'RedMail'? \n- Me\n"

    html_tables = tmpdir.mkdir("html_table_tmpl")
    html_tables.join("modest.html").write("""{{ df.to_html() }}""")
    text_tables = tmpdir.mkdir("text_table_tmpl")
    text_tables.join("pandas.txt").write("""{{ df.to_html() }}""")

    sender = EmailSender(host=None, port=1234)
    sender.set_template_paths(
        html=str(html_templates),
        text=str(text_templates),
        html_table=str(html_tables),
        text_table=str(text_tables),
    )
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers=["you@gmail.com"],
        subject="Some news",
        html_template='example.html',
        text_template='example.txt',
        body_params={"friend": "Jack", 'project_name': 'RedMail'}
    )
    
    assert "multipart/mixed" == msg.get_content_type()

    alternative = msg.get_payload()[0]
    text_part, html_part = alternative.get_payload()

    text = remove_email_extra(text_part.get_payload())
    html = remove_email_extra(html_part.get_payload())

    assert expected_html == html
    assert expected_text == text

def test_body_and_template_error(tmpdir):

    html_templates = tmpdir.mkdir("html_tmpl")
    html_templates.join("example.html").write("""<h1>Hi {{ friend }},</h1><p>have you checked this open source project '{{ project_name }}'?</p><p>- {{ sender.full_name }}</p>""")

    text_templates = tmpdir.mkdir("text_tmpl")
    text_templates.join("example.txt").write("""Hi {{ friend }}, \nhave you checked this open source project '{{ project_name }}'? \n- {{ sender.full_name }}""")

    sender = EmailSender(host="localhost", port=0)
    sender.set_template_paths(
        html=str(html_templates),
        text=str(text_templates),
    )

    with pytest.raises(ValueError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            html='This is some body',
            html_template="example.html"
        )
    with pytest.raises(ValueError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            text='This is some body',
            text_template="example.txt"
        )