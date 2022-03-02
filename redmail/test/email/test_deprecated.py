
import pytest
from redmail import EmailSender

def test_user_name():
    "user_name has been deprecated. Testing backward compatibility."
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
