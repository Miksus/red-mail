
.. meta::
   :description: Send templated email in Python using Jinja. 
   :keywords: send, email, Python, jinja, environment

.. _templating:

Using Templates
===============

As templating relies on Jinja, you can set the 
template path to a custom folder and 

.. code-block:: python

    from redmail import EmailSender
    email = EmailSender(host="localhost", port=0)
    email.set_template_paths(
        html="path/html/templates",
        text="path/text/templates",
    )

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