
.. _examples:

Examples
========

This is a collection of various examples of 
sending emails. Remember to initiate the 
sender object as:

.. code-block:: python

    from redmail import EmailSender

    email = EmailSender(
        host='localhost', 
        port=0, 
        username='me@example.com', 
        password='<PASSWORD>'
    )

.. _examples-simple:

Simple Example
--------------

.. code-block:: python

    email.send(
        subject="An email",
        sender="me@example.com",
        receivers=['you@example.com'],
        text="Hi, this is an email.",
        html="<h1>Hi, </h1><p>this is an email.</p>"
    )

.. _examples-attachments:

Attachments
-----------

.. code-block:: python

    from pathlib import Path
    import pandas as pd

    email.send(
        subject="Email subject",
        sender="me@example.com",
        receivers=["you@example.com"],
        text="Hi, this is a simple email.",
        attachments={
            'myfile.csv': Path("path/to/data.csv"),
            'myfile.xlsx': pd.DataFrame({'A': [1, 2, 3]}),
            'myfile.html': '<h1>This is content of an attachment</h1>'
        }
    )

.. _examples-embed-image:

Embedded Images
---------------

.. code-block:: python

    import pandas as pd

    email.send(
        subject="Email subject",
        sender="me@example.com",
        receivers=["you@example.com"],
        html="""
            <h1>Hi,</h1> 
            <p>have you seen this?</p> 
            {{ myimg }}
        """,
        body_images={"myimg": "path/to/my/image.png"}
    )

.. _examples-embed-plot:

Embedded Plots
--------------

.. code-block:: python

    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.plot([1,2,3,2,3])

    email.send(
        subject="Email subject",
        sender="me@example.com",
        receivers=["you@example.com"],
        html="""
            <h1>Hi,</h1> 
            <p>have you seen this?</p> 
            {{ myplot }}
        """,
        body_images={"myplot": fig}
    )

.. _examples-embed-table:

Embedded Tables
---------------

.. code-block:: python

    import pandas as pd

    email.send(
        subject="Email subject",
        sender="me@example.com",
        receivers=["you@example.com"],
        html="""
            <h1>Hi,</h1> 
            <p>have you seen this?</p> 
            {{ mytable }}
        """,
        body_tables={"mytable": pd.DataFrame({'a': [1,2,3], 'b': [1,2,3]})}
    )

.. _examples-parametrized:

Parametrization
---------------

.. code-block:: python

    email.send(
        subject="Email subject",
        sender="me@example.com",
        receivers=["you@example.com"],
        text="Hi {{ friend }}, nice to meet you.",
        html="<h1>Hi {{ friend }}, nice to meet you</h1>",
        body_params={
            "friend": "Jack"
        }
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
