
.. meta::
   :description: Send email with attachment in Python.
   :keywords: send, email, Python, attachment

.. _attachments:

Sending Email with Attachments
------------------------------

Red Mail also provides a convenient way to include
attachments to the emails, for example:

.. code-block:: python

    import pandas as pd
    from pathlib import Path

    email.send(
        subject='Some attachments',
        receivers=['first.last@example.com'],
        attachments={
            'data.csv': Path('path/to/file.csv'), 
            'data.xlsx': pd.DataFrame(...), 
            'raw_file.html': '<h1>Just some HTML</h1>',
        }
    )

As seen, Red Mail allows passing various objects to the 
attachments. You may pass a list, a single object or 
a dict. If you pass a dict, the key is used to determine
the name of the attachment and possibly the type.

Here is a list of supported value formats if ``dict`` is passed to attachments:

================ =============== =================================================================
Value type       Dict key        Dict value
================ =============== =================================================================
``pd.Series``    Attachment name Turned to CSV, XLSX, HTML etc. depending on file extension in key
``pd.DataFrame`` Attachment name Turned to CSV, XLSX, HTML etc. depending on file extension in key           
``str``          Attachment name Attachment content as raw text
``bytes``        Attachment name Attachment content as raw bytes
``pathlib.Path`` Attachment name Path to a file that is attached (using key as the file name)
================ =============== =================================================================

Here is a list of supported value formats if ``list`` or single object is passed to attachments:

================ =============== =========================================================
Type             Attachment name Value
================ =============== =========================================================
``pathlib.Path`` From file name  Content of the file read as the content of the attachment
``str``          From file name  Considered as file path, handled the same as above
================ =============== =========================================================

