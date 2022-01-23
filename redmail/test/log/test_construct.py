
import pytest
from redmail import EmailHandler, MultiEmailHandler
from redmail.email.sender import EmailSender

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_construct_kwargs_minimal(cls):
    hdlr = cls(host="localhost", port=0, receivers=["me@example.com"], subject="Some logging")
    assert hdlr.email.host == 'localhost'
    assert hdlr.email.port == 0
    assert hdlr.email.receivers == ["me@example.com"]
    assert hdlr.email.subject == "Some logging"


@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_construct_kwargs(cls):
    hdlr = cls(host="localhost", port=0, receivers=["me@example.com"], subject="Some logging", text="Error: {{ msg }}", html="<h1>Error: {{ msg }}</h1>")
    assert hdlr.email.host == 'localhost'
    assert hdlr.email.port == 0
    assert hdlr.email.receivers == ["me@example.com"]
    assert hdlr.email.subject == "Some logging"

    assert hdlr.email.text == "Error: {{ msg }}"
    assert hdlr.email.html == "<h1>Error: {{ msg }}</h1>"

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_kwargs_error_missing(cls):
    # Missing subject
    with pytest.raises(TypeError):
        hdlr = cls(host="localhost", port=0, receivers=["me@example.com"])

    # Missing receivers
    with pytest.raises(TypeError):
        hdlr = cls(host="localhost", port=0, subject="Some logging")

    # Missing host
    with pytest.raises(TypeError):
        hdlr = cls(port=0, receivers=["me@example.com"], subject="Some logging")

    # Missing port
    with pytest.raises(TypeError):
        hdlr = cls(host="localhost", receivers=["me@example.com"], subject="Some logging")

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_kwargs_error_invalid_attr(cls):
    with pytest.raises(AttributeError):
        hdlr = cls(host="localhost", port=0, receivers=["me@example.com"], subject="Some logging", not_existing="something")

# Testing with passing EmailSender
@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_sender_with_kwargs(cls):
    sender = EmailSender(host="localhost", port=0)
    hdlr = cls(email=sender, subject="A log", receivers=["me@example.com"])
    assert hdlr.email is not sender
    assert hdlr.email.subject == "A log"
    assert hdlr.email.receivers == ["me@example.com"]

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_sender(cls):
    sender = EmailSender(host="localhost", port=0)
    sender.subject = "A log"
    sender.receivers = ["me@example.com"]

    hdlr = cls(email=sender)
    assert hdlr.email is not sender
    assert hdlr.email.subject == "A log"
    assert hdlr.email.receivers == ["me@example.com"]

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_sender_with_kwargs_error_invalid_attr(cls):
    sender = EmailSender(host="localhost", port=0)
    with pytest.raises(AttributeError):
        hdlr = cls(email=sender, not_existing="something")

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_sender_error_missing(cls):
    # Missing subject
    sender = EmailSender(host="localhost", port=0)
    with pytest.raises(TypeError):
        hdlr = cls(email=sender, receivers=["me@example.com"])

    # Missing receivers
    with pytest.raises(TypeError):
        hdlr = cls(email=sender, subject="Some logging")

@pytest.mark.parametrize("cls", [EmailHandler, MultiEmailHandler])
def test_sender_invalid_attr(cls):
    sender = EmailSender(host="localhost", port=0)
    with pytest.raises(AttributeError):
        hdlr = cls(email=sender, not_existing="something")