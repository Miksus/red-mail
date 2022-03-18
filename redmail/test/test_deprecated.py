
import pytest
from redmail import EmailSender, MultiEmailHandler

def test_user_name():
    "user_name has been deprecated. Testing backward compatibility."

    # Test EmailSender
    with pytest.warns(FutureWarning):
        email = EmailSender(host="localhost", port=0, user_name="testing", password="1234")

    assert email.username == "testing"
    with pytest.warns(FutureWarning):
        assert email.user_name == "testing"

    with pytest.warns(FutureWarning):
        email.user_name = "another"

    assert email.username == "another"
    with pytest.warns(FutureWarning):
        assert email.user_name == "another"

    # Testing in handler
    with pytest.warns(FutureWarning):
        hdlr = MultiEmailHandler(host="localhost", port=0, user_name="testing", password="1234", subject="A log", receivers=["me@example.com"])
    sender = hdlr.email
    assert sender.username == "testing"
    assert sender.password == "1234"