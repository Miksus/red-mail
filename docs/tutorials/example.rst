
.. _examples-simple:

Examples
========

Simple Example
--------------

.. code-block:: python

    from redmail import EmailSender

    email = EmailSender(
        host='localhost', 
        port=0, 
        user_name='me@example.com', 
        password='<PASSWORD>'
    )
    email.send(
        subject="An email",
        sender="me@example.com",
        receivers=['you@example.com'],
        test="Hi, this is an email.",
        html="<h1>Hi, </h1><p>this is an email.</p>"
    )

.. _examples-mega:

Super Example
-------------

This example covers the most interesting 
features of Red Mail:

.. code-block:: python

    from pathlib import Path
    from redmail import EmailSender

    import pandas as pd
    from PIL import Image
    import matplotlib.pyplot as plt

    fig = plt.figure()
    plt.plot([1, 2, 3])

    df = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 3]})

    byte_content = Path("a_file.bin").read_bytes()

    email = EmailSender(
        host='localhost', 
        port=0, 
        user_name='me@example.com', 
        password='<PASSWORD>'
    )

    # Send an email
    email.send(
        subject="A lot of stuff!",
        sender="me@example.com",

        # Receivers
        receivers=["you@example.com"],
        cc=['also@example.com'],
        bcc=['external@example.com'],

        # Bodies
        text="""Hi {{ friend }},
        This email has a lot of stuff!
        Use HTML to view the awesome content.
        """,
        html="""<h1>Hi {{ friend }},</h1>
        <p>This email has a lot of stuff!</p>
        <p>Like this image:</p>
        {{ my_image }}
        <p>or this image:</p>
        {{ my_pillow }}
        <p>or this plot:</p>
        {{ my_plot }}
        <p>or this table:</p>
        {{ my_table }}
        <p>or this loop:</p>
        <ul>
        {% for value in container %}
            {% if value > 5 %}
                <li>{{ value }}</li>
            {% else %}
                <li style="color: red">{{ value }}</li>
            {% endif %}
        {% endfor %}
        </ul>
        """,

        # Embedded content
        body_images={
            "my_image": "path/to/image.png",
            "my_pillow": Image.new('RGB', (100, 30), color = (73, 109, 137))
            "my_plot": fig,
        },
        body_tables={
            "my_table": df,
        },
        body_params={
            "friend": "Jack",
            "container": [1, 3, 5, 7, 9],
        },
        attachments={
            "data.csv": df,
            "file.txt": "This is file content",
            "file.html": Path("path/to/a_file.html"),
            "file.bin": byte_content,
        }
    )