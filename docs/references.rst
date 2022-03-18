References
==========

Sender
------

.. autoclass:: redmail.EmailSender
    :members:


Format Classes
--------------

.. autoclass:: redmail.models.EmailAddress

.. autoclass:: redmail.models.Error

Logging Classes
---------------

.. autoclass:: redmail.EmailHandler

.. autoclass:: redmail.MultiEmailHandler


.. _email_structure:

Email Strucure (MIME)
---------------------

This section covers how Red Mail structures emails with MIME parts.
You may need this information if you are creating unit tests or 
if you face problems with rendering your emails by your email provider.

Empty Email
^^^^^^^^^^^

Empty email has no MIME parts attached. It only has the headers.


Email with a text body
^^^^^^^^^^^^^^^^^^^^^^

* text/plain


Email with an HTML body
^^^^^^^^^^^^^^^^^^^^^^^

* multipart/mixed

    * multipart/alternative

        * text/html


Email with an HTML body and inline JPG image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* multipart/mixed

    * multipart/alternative

        * multipart/related

            * text/html
            * image/jpg


Email with an attachment
^^^^^^^^^^^^^^^^^^^^^^^^

* multipart/mixed

    * application/octet-stream


Email with all elements
^^^^^^^^^^^^^^^^^^^^^^^

* multipart/mixed

    * multipart/alternative

        * text/plain
        * multipart/related

            * text/html
            * image/jpg

    * application/octet-stream
