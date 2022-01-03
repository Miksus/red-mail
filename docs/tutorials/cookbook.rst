.. _cookbook:

Cookbook
=========

This section provides various examples for various 
needs.


.. _cookbook-campaign:

Email Campaign
--------------

In case you have a list of clients or customers you 
wish to send personalized emails, you may benefit from
templating. It may help to make the templates to an HTML
file, polish them and after then send:

.. code-block:: python

    from redmail import EmailSender
    
    email = EmailSender(...)
    email.receivers = ['we@example.com']
    email.set_template_paths(
        html="path/to/campaigns"
    )

Then make a HTML file, for example ``path/to/campaigns/summer_sale.html``:

.. code-block:: html

    <img src="{{ company_logo }}" width=200 height=100>
    <h1>Thank you, {{ customer }}, for being awesome!</h1>
    <p>
        We are pleased to inform you that we have a lot of products
        in huge discounts.
    </p>
    <ul>
    {% for product, discount, in discounts.items() %}
        <li>{{ product }}: {{ '{:.0f} %'.format(discount * 100) }}</li>
    {% endfor %}
    </ul>
    <p>Kind regards, We Ltd.</p>

Finally send the emails:

.. code-block:: python

    discounts = {'shoes': 0.2, 'shirts': 0.4}
    customers = ['cust1@example.com', 'cust2@example.com', ...]
    for customer in customers:
        email.send(
            subject="Summer Sale!",
            html_template="summer_sale.html",
            body_params={
                "customer": customer,
                "discounts": discounts
            },
            body_images={
                "company_logo": "path/to/logo.png"
            }
        )

.. _cookbook-alerts:

Error Alerts
------------

If you are building long running program (ie. web app) you can make a
templated error alerts that include the full traceback:

.. code-block:: python

    from redmail import EmailSender
    
    error_email = EmailSender(...)
    error_email.sender = 'me@example.com'
    error_email.receivers = ['me@example.com']
    error_email.html = """
        <h2>An error encountered</h2>
        {{ error }}
    """

    try:
        raise RuntimeError("Oops")
    except:
        # Send an email including the traceback
        error_email.send(subject="Fail: doing stuff failed")

.. note::

    The ``error`` formatting object identifies which body it is being
    attached to. If you wish to use text body, ``error`` will show up
    similarly as Python errors you see on terminals. See more from
    :class:`redmail.models.Error`

.. _cookbook-stats:

Stats Reports
-------------

As demonstrated :ref:`here <embedding-plt>`, embedding Matplotlib 
figures to the HTML bodies is trivial. Therefore you can easily
create diagnostic reports or automatic analyses. Just create 
the plots and let Red Mail send them to you:

.. code-block:: python

    from redmail import EmailSender
    
    stats_report = EmailSender(...)
    stats_report.sender = 'no-reply@example.com'
    stats_report.receivers = ['me@example.com']

    # Create a plot
    import matplotlib.pyplot as plt
    fig_performance = plt.Figure()
    plt.plot([1,2,3,2,3])

    # Create summary table
    import pandas as pd
    df = pd.DataFrame(...)
    df_summary = df.describe()

    # Send the report
    stats_report.send(
        subject="System Diagnostics",
        html="""
            <h1>System Diagnostics ({{ now }})</h1>
            <hr>
            <h2>Performance</h2>
            {{ perf_plot }}
            <h2>Summary Statistics</h2>
            {{ tbl_summary }}
            <hr>
            <p>System running on {{ node }}</p>
        """,
        body_images={
            "perf_plot": fig_performance,
        },
        body_tables={
            "tbl_summary": df_summary
        }
    )