
.. meta::
   :description: Send templated email in Python using Jinja. 
   :keywords: send, email, Python, jinja, environment

.. _templating:

Jinja Environments
==================

There are two ways of setting a custom Jinja env
to Red Mail: from paths or directly setting the 
envs.

To set the paths and let Red Mail to create the 
environments:

.. code-block:: python

    from redmail import EmailSender
    email = EmailSender(host="localhost", port=0)
    email.set_template_paths(
        html="path/html/templates",
        text="path/text/templates",
    )

To set the Jinja environments:

.. code-block:: python

    import jinja2

    # Create an env
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("path/to/templates"))

    email_sender.templates_html = jinja_env
    email_sender.templates_text = jinja_env

.. note::

    If you are dissatisfied with default HTML and text
    table templates, you can also pass ``html_table``
    and ``text_table`` to specify the templates used
    to render embedded tables:

    .. code-block:: python

        email.set_template_paths(
            html_table="path/html/tables",
            text_table="path/text/tables",
        )
    
    The environments are in the attributes ``templates_html_table`` 
    and ``templates_text_table`` respectively.

Next we will make a simple template, let's call it 
``event_card.html``:

.. code-block:: html

    <h1>Hi {{ participant }}!</h1>
    <p>
        Thank you for being a valuable member of our 
        community! We are organizing an event 
        {{ event_name }} and we would like to invite
        you.
    </p>
    <p>Kind regards,<br>
    <em>{{ organizer }} </em>
    </p>

Then we can use this template:

.. code-block:: python

    email.send(
        subject='email subject',
        receivers=['first.last@example.com'],
        html_template='event_card.html',
        body_params={
            'participant': 'Jack', 
            'event_name': 'Open data',
            'organizer': 'Organization.org'
        }
    )