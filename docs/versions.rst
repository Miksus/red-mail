
.. _version-history:

Version history
===============

- ``0.2.1``

    - Fix: If some attachments are specified and only text body or no body at all is set´, sending email no longer crashes
    - Fix: Now embedded images support also non-PNG images using dict format
    - Docs: Added examples of embedding images using dict format
    - Docs: Added an example of sending emails using aliases
    - Docs: Fixed some couple of typos

- ``0.2.0``

    - Docs: Docstrings were rewritten and are more complete
    - Docs: Huge improvement on the official documentation
    - Add: Support for TLS, SSL and other types of protocols
    - Add: Subclassing of ``EmailSender`` has better support allowing for interesting customization
    - Fix: Fixed a couple of minor bugs related to exceptions, format classes and tests
    - Test: Test coverage is now almost 100 %

- ``0.1.1``

    - Package: Dropped Pandas as hard dependency 

- ``0.1.0``

    - First release