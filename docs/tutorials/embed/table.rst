.. meta::
   :description: Send email with table in the body in Python.
   :keywords: send, email, Python, table, content

.. _embedding-tables:

Sending Email with Table in Body
================================

You may include tables simply by turning them 
to raw HTML for example using ``df.to_html()``
in Pandas. However, this often lead to very
ugly tables as SMTP is poor at handling CSS
or styling in general. Here is a comparison
of using ``df.to_html()`` directly vs embedding
via Red Mail:

|pic1| vs |pic2|

.. |pic1| image:: /imgs/table_without_style.png
   :height: 150px
   :align: top
   

.. |pic2| image:: /imgs/table_with_style.png
   :height: 150px
   :align: top


To embed tables, you can simply pass them 
to the send function as Pandas dataframes:

.. code-block:: python

    # Creating a simple dataframe
    import pandas as pd
    df = pd.DataFrame({
        'nums': [1,2,3],
        'strings': ['yes', 'no', 'yes'],
    })

    # Let Red Mail to render the dataframe for you:
    email.send(
        subject='A prettified table',
        receivers=['first.last@example.com'],
        html="<h1>This is a table:</h1> {{ mytable }}",
        body_tables={
            'mytable': df, 
        }
    )


Red Mail uses Jinja and inline HTML styling to make the
tables look nice. Email servers typically don't handle
well CSS.

.. warning::

    Red Email Pandas templating should work on various 
    dataframe strucutres (empty, multi-indexed etc.) but
    sometimes the rendering may be off if the dataframe
    is especially complex in structural sense. There are
    plans to make it even more better.

You may also override the template paths (see 
:ref:`templating`) to create custom templates
if you wish to make your own table prettifying:

.. code-block:: python

    email.set_template_paths(
        html_table="path/to/templates", 
        text_template="path/to/templates"
    )
    email.default_html_theme = "my_table_template.html"
    email.default_text_theme = "my_table_template.txt"

The templates get parameter ``df`` which is the dataframe
to be prettified.
