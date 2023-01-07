
.. _testing:

How to Test
===========

For testing purposes, it might be useful to prevent
sending the actual email. This is especially preferable
with unit tests. There are several ways to do this.

.. note::

    Red Mail extends :stdlib:`email.message.EmailMessage <email.message.html#email.message.EmailMessage>`
    from standard library. You may use its attributes and
    methods for testing the contents of your messages. 
    
    See :ref:`email_structure` for how Red Mail's
    emails are structured.

Using get_message
-----------------

All of the arguments in method :py:meth:`.EmailSender.send`
are passed to :py:meth:`.EmailSender.get_message` method 
which generates the message itself. Therefore, the simplest
solution is to use this method instead of :py:meth:`.EmailSender.send`
in tests:

.. code-block:: python

    from redmail import EmailSender

    # Just put something as host and port
    email = EmailSender(host="localhost", port=0)

    msg = email.get_message(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hi, this is an email.",
    )

    assert str(msg) == """From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <167294165062.31860.1664530310632362057@LAPTOP-1234GML0>
    Date: Sun, 31 Jan 2021 06:56:46 -0000
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    Hi, nice to meet you.
    """

Mock Server
-----------

In case changing to method :py:meth:`.EmailSender.get_message` 
is inconvenient or it does not suit to your testing, you may
also create a mock SMTP server that imitates an actual SMTP
server instance:

.. code-block:: python

    class MockSMTP:

        messages = []

        def __init__(self, host, port):
            self.host = host
            self.port = port

        def starttls(self):
            # Called only if use_startls is True
            return

        def login(self, username, password):
            # Log in to the server (if credentials passed)
            self.username = username
            self.password = password
            return

        def send_message(self, msg):
            # Instead of sending, we just store the message
            self.messages.append(msg)

        def quit(self):
            # Closing the connection
            return

Then to use this mock:

.. code-block:: python

    from redmail import EmailSender

    email = EmailSender(
        host="localhost", 
        port=0, 
        username="me@example.com", 
        password="1234", 
        cls_smtp=MockServer
    )

    email.send(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hi, this is an email.",
    )

    msgs = MockServer.messages
    assert msgs == ["""From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <167294165062.31860.1664530310632362057@LAPTOP-1234GML0>
    Date: Sun, 31 Jan 2021 06:56:46 -0000
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    Hi, nice to meet you.
    """]

Note that an instance of ``MockServer`` is created 
for each connection, often per sent email.

Subclass Sender
---------------

Another option is to just subclass the sender and 
change the email sending there:

.. code-block:: python

    from redmail import EmailSender

    class MockSender(EmailSender):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.messages = []

        def send_message(self, msg):
            self.messages.append(msg)

Then to use this class:

.. code-block:: python

    # Just put something as host and port
    email = MockSender(host="localhost", port=0)

    email.send(
        subject='email subject',
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hi, this is an email.",
    )

    msgs = email.messages
    assert msgs == ["""From: me@example.com
    Subject: Some news
    To: you@example.com
    Message-ID: <167294165062.31860.1664530310632362057@LAPTOP-1234GML0>
    Date: Sun, 31 Jan 2021 06:56:46 -0000
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    MIME-Version: 1.0

    Hi, nice to meet you.
    """]
