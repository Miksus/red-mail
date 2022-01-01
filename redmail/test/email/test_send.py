
import pytest

from redmail import EmailSender, send_email

def test_send():
    email = EmailSender(host="localhost", port=0)
    # This should fail but we test everything else goes through
    with pytest.raises(ConnectionRefusedError):
        email.send(
            subject="An example",
            receivers=['koli.mikael@example.com']
        )

def test_send_function():
    # This should fail but we test everything else goes through
    with pytest.raises(ConnectionRefusedError):
        send_email(host="localhost", port=0, subject="An example")