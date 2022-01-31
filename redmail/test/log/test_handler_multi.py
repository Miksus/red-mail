
import pytest
from redmail import EmailSender
from redmail import MultiEmailHandler
import logging

def _create_dummy_send(messages:list):
    def _dummy_send(msg):
        messages.append(msg)
    return _dummy_send

def test_default_body():
    hdlr = MultiEmailHandler(host="localhost", port=0, receivers=["me@example.com"], subject="Some logging")
    # By default, this should be body if text/html/html_template/text_template not specified
    assert hdlr.email.text == MultiEmailHandler.default_text


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
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'Log Recods:\na message\n',
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
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'The records: \nLog: _test - INFO - a message\n',
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
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'The records: \nLog: INFO - a message\n',
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
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "Logs: INFO - INFO",
                'Content-Transfer-Encoding': '7bit',
                'Content-Type': 'text/plain; charset="utf-8"',
                'MIME-Version': '1.0',
            },
            'Log Recods:\na message\n',
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
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Type': 'multipart/alternative',
            },
            ["<h1>The records:</h1><p>Log: _test - INFO - a message</p>\n"],
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
                "from": "me@example.com",
                "to": "he@example.com, she@example.com",
                "subject": "A log record",
                'Content-Type': 'multipart/alternative',
            },
            ["<h1>The records:</h1><p>Log: INFO - a message</p>\n"],
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
    headers = dict(msg.items())
    payload = msg.get_payload()

    assert headers == exp_headers

    if isinstance(payload, str):
        assert payload == exp_payload
    else:
        # HTML (and text) of payloads
        payloads = [pl.get_payload() for pl in payload]
        assert payloads == exp_payload


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
    headers = dict(msg.items())
    payload = msg.get_payload()

    assert headers == {
        "from": "None",
        "to": "he@example.com, she@example.com",
        "subject": "Logs: DEBUG - INFO",
        'Content-Transfer-Encoding': '7bit',
        'Content-Type': 'text/plain; charset="utf-8"',
        'MIME-Version': '1.0',
    }

    assert payload == "Records: \nINFO - an info\nDEBUG - a debug\n"

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
    headers = dict(msg.items())
    payload = msg.get_payload()

    assert headers == {
        "from": "None",
        "to": "he@example.com, she@example.com",
        "subject": "Logs: NOTSET - NOTSET",
        'Content-Transfer-Encoding': '7bit',
        'Content-Type': 'text/plain; charset="utf-8"',
        'MIME-Version': '1.0',
    }

    assert payload == "Records: \n"