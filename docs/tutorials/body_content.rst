
.. _embedded:

Embedding Content
=================

Red Mail allows to embed images and tables to the
HTML bodies of emails. By default, tables often 
look outdated and ugly in emails but Red Mail
has pre-made table templates that render nicer
looking tables from Pandas dataframes.

.. _embedding-tables:

Embedded Tables
---------------

You may include tables simply by turning them 
to raw HTML for example using ``df.to_html()``
in Pandas. However, this often lead to very
ugly tables as SMTP is poor at handling CSS
or styling in general. Here is a comparison
of using ``df.to_html()`` directly vs embedding
via Red Mail:

|pic1| -- |pic2|

.. |pic1| image:: /imgs/table_unrendered.png
   :height: 150px
   :align: top
   

.. |pic2| image:: /imgs/table_rendered.png
   :height: 150px
   :align: top


To embed tables, you can si  mply pass them 
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
        subject='Some attachments',
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
    development plans to make it even more better.

.. _embedding-images:

Embedded Images
---------------

You can also embed images straight to the HTML body 
of the email:

.. code-block:: python

    email.send(
        subject='Some attachments',
        receivers=['first.last@example.com'],
        html="<h1>This is an image:</h1> {{ myimage }}",
        body_images={
            'myimage': 'path/to/image.png', 
        }
    )

The image will be rendered as ``<img src="cid:...">``.
In case you need to control the image (like the size)
you can also create the ``img`` tag yourself:

.. code-block:: python

    email.send(
        subject='Some attachments',
        receivers=['first.last@example.com'],
        html='<h1>This is an image:</h1> <img src="{{ myimage.src }}">',
        body_images={
            'myimage': 'path/to/image.png', 
        }
    )

In addition to paths as strings, the following are supported:

- ``pathlib.Path``
- ``bytes`` (the image as raw bytes)
- ``matplotlib.pyplot.Figure``
- ``PIL.Image``
