.. _sending-emails:

Sending Emails
==============

This section covers the basics of sending emails.
We use an ``EmailSender`` configured in :ref:`configure`.


Sending Email with Text Body
----------------------------

To send an email with plain text message:

.. code-block:: python

   email.send(
       subject='email subject',
       receivers=['first.last@example.com'],
       text="Hi, this is an email."
   )

Sending Email with HTML Body
----------------------------

To send an email with html content:

.. code-block:: python

    email.send(
        subject='email subject',
        receivers=['first.last@example.com'],
        html="""
            <h1>Hi,</h1>
            <p>this is an email.</p>
        """
    )


Sending Email with text and HTML Body
-------------------------------------

You can also include both to your email:

.. code-block:: python

    email.send(
        subject='email subject',
        receivers=['first.last@example.com'],
        text="Hi, this is an email.",
        html="""
            <h1>Hi,</h1>
            <p>this is an email.</p>
        """
    )