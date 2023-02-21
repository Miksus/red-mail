
.. _version-history:

Version history
===============

- ``0.6.0``

    - Fix: Line breaks according to RFC 5322 (credit Waghabond)
    - Add: Support for Pandas styler (thanks ejbills!)

- ``0.5.0``

    - Add: Option to set custom email headers.
    - Add: New header, ``Message-ID: ...``. Sending emails via Gmail may fail without it as of 2022. 
    - Add: New header, ``Date: ...``.
    - Fix: Capitalized email headers including ``From``, ``To`` and ``Subject``.
    - Update: Content-IDs (used in the embedded images in the HTML body) now uses fully qualified domain name
      (FQDN) by default. Can be customized by setting ``domain`` attribute in the sender.
    - Package: Now Red Mail is built using pyproject.toml and CI pipelines were updated.

- ``0.4.2``

    - Docs: Changed docs style.

- ``0.4.1``

    - Add: Mypy stubs (thanks Waghabond!)
    - Docs: Improved embedded content page.

- ``0.4.0``

    - Rename: Changed ``user_name`` to ``username`` in ``redmail.EmailSender``. ``user_name`` still works but issues a warning.
    - Add: ``redmail.EmailSender.send`` now has new argument ``use_jinja`` (by default True) to disable Jinja templating.
    - Fix: Now the MIME structure is more defined and more likely renders emails properly across email providers.
    - Fix: Embedded images for aliased senders.
    - Docs: Added examples of how to test Red Mail's messages.

- ``0.3.1``

    - Package: Added the license as a classifier to setup.py. Some pipelines may require such. 

- ``0.3.0``

    - Add: Logging handlers (:class:`.EmailHandler`, :class:`.MultiEmailHandler`)
    - Add: Outlook pre-configured sender
    - Add: Multiple emails can be sent without closing the connection using context manager in :class:`EmailSender`

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