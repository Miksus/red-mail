
import pytest
from redmail import EmailSender
from redmail import MultiEmailHandler
import logging

from convert import payloads_to_dict

def _create_dummy_send(messages:list):
    def _dummy_send(msg):
        messages.append(msg)
    return _dummy_send

def test_default_body():
    hdlr = MultiEmailHandler(host="localhost", port=0, receivers=["me@example.com"], subject="Some logging")
    # By default, this should be body if text/html/html_template/text_template not specified
    assert hdlr.email.text == MultiEmailHandler.default_text

def test_sender_with_login():
    hdlr = MultiEmailHandler(host="localhost", port=0, username="myuser", password="1234", receivers=["me@example.com"], subject="Some logging")
    # By default, this should be body if text/html/html_template/text_template not specified
    sender = hdlr.email
    assert sender.username == "myuser"
    assert sender.password == "1234"
    assert sender.receivers == ["me@example.com"]
    assert sender.subject == "Some logging"

@pytest.mark.parametrize("kwargs,exp_headers,exp_payload",
    [
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
            }, 
            {
                "From": "me@example.com",
                "To": "he@example.com, she@example.com",
                "Subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            {
                'text/plain': 'Log Recods:\na message\n'
            },
            id="Minimal",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "text": "The records: \n{% for msg in msgs %}Log: {{ msg }}{% endfor %}",
                "fmt": '%(name)s - %(levelname)s - %(message)s'
            }, 
            {
                "From": "me@example.com",
                "To": "he@example.com, she@example.com",
                "Subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            {
                'text/plain': 'The records: \nLog: _test - INFO - a message\n'
            },
            id="Custom message (msgs)",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "text": "The records: \n{% for rec in records %}Log: {{ rec.levelname }} - {{ rec.message }}{% endfor %}",
                "fmt": '%(name)s - %(levelname)s - %(message)s'
            }, 
            {
                "From": "me@example.com",
                "To": "he@example.com, she@example.com",
                "Subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            {
                'text/plain': 'The records: \nLog: INFO - a message\n',
            },
            id="Custom message (records)",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "Logs: {min_level_name} - {max_level_name}",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
            }, 
            {
                "From": "me@example.com",
                "To": "he@example.com, she@example.com",
                "Subject": "Logs: INFO - INFO",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            {
                'text/plain': 'Log Recods:\na message\n',
            },
            id="Sender with fomatted subject",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "fmt": '%(name)s - %(levelname)s - %(message)s',
                "html": "<h1>The records:</h1><p>{% for msg in msgs %}Log: {{ msg }}{% endfor %}</p>"
            }, 
            {
                "From": "me@example.com",
                "To": "he@example.com, she@example.com",
                "Subject": "A log record",
                'Content-Type': 'multipart/mixed',
            },
            {
                'multipart/mixed': {
                    'multipart/alternative': {
                        'text/html': "<h1>The records:</h1><p>Log: _test - INFO - a message</p>\n",
                    }
                }
            },
            id="Custom message (HTML, msgs)",
        ),
        pytest.param(
            {
                "email": EmailSender(host="localhost", port=0),
                "subject": "A log record",
                "sender": "me@example.com",
                "receivers": ["he@example.com", "she@example.com"],
                "fmt": '%(name)s: %(levelname)s: %(message)s',
                "html": "<h1>The records:</h1><p>{% for rec in records %}Log: {{ rec.levelname }} - {{ rec.message }}{% endfor %}</p>"
            }, 
            {
                "From": "me@example.com",
                "To": "he@example.com, she@example.com",
                "Subject": "A log record",
                'Content-Type': 'multipart/mixed',
            },
            {
                'multipart/mixed': {
                    'multipart/alternative': {
                        'text/html': "<h1>The records:</h1><p>Log: INFO - a message</p>\n",
                    }
                }
            },
            id="Custom message (HTML, records)",
        ),
    ]
)
def test_emit(logger, kwargs, exp_headers, exp_payload):
    msgs = []
    fmt = kwargs.pop("fmt", None)
    hdlr = MultiEmailHandler(**kwargs)
    hdlr.formatter = logging.Formatter(fmt)
    hdlr.email.send_message = _create_dummy_send(msgs)
    
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    logger.info("a message")
    
    hdlr.flush()

    assert len(msgs) == 1
    msg = msgs[0]
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    payload = msg.get_payload()

    assert headers == exp_headers

    structure = payloads_to_dict(msg)
    assert structure == exp_payload


def test_flush_multiple(logger):
    msgs = []
    hdlr = MultiEmailHandler(
        email=EmailSender(host="localhost", port=0),
        subject="Logs: {min_level_name} - {max_level_name}", 
        receivers=["he@example.com", "she@example.com"],
        text="Records: \n{% for rec in records %}{{ rec.levelname }} - {{ rec.message }}\n{% endfor %}"
    )
    hdlr.email.send_message = _create_dummy_send(msgs)
    
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    logger.info("an info")
    logger.debug("a debug")
    
    hdlr.flush()

    assert len(msgs) == 1
    msg = msgs[0]
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    text = msg.get_payload()

    assert headers == {
        "From": "None",
        "To": "he@example.com, she@example.com",
        "Subject": "Logs: DEBUG - INFO",
        'Content-Transfer-Encoding': '7bit',
        'Content-Type': 'text/plain; charset="utf-8"',
        'MIME-Version': '1.0',
    }

    assert text == "Records: \nINFO - an info\nDEBUG - a debug\n"

def test_flush_none():
    msgs = []
    hdlr = MultiEmailHandler(
        email=EmailSender(host="localhost", port=0),
        subject="Logs: {min_level_name} - {max_level_name}", 
        receivers=["he@example.com", "she@example.com"],
        text="Records: \n{% for rec in records %}{{ rec.levelname }} - {{ rec.message }}\n{% endfor %}"
    )
    hdlr.email.send_message = _create_dummy_send(msgs)
    
    logger = logging.getLogger("_test")
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    
    hdlr.flush()

    assert len(msgs) == 1
    msg = msgs[0]
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    text = msg.get_payload()

    assert headers == {
        "From": "None",
        "To": "he@example.com, she@example.com",
        "Subject": "Logs: NOTSET - NOTSET",
        'Content-Transfer-Encoding': '7bit',
        'Content-Type': 'text/plain; charset="utf-8"',
        'MIME-Version': '1.0',
    }

    assert text == "Records: \n"