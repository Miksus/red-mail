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

As demonstrated :ref:`here <embedding-images-plt>`, embedding Matplotlib 
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


Distribution Lists
------------------

There might be a situation in which you would like to 
specify some sets of pre-defined distribution lists
for which you will send emails to depending on situation. 
To accomplish this, you can create subclass the :class:`.EmailSender`
and create cystin distribution list logic:  

.. code-block:: python

    from redmail import EmailSender

    class DistributionSender(EmailSender):
        "Send email using pre-defined distribution lists"

        def __init__(self, *args, distributions:dict, **kwargs):
            super().__init__(*args, **kwargs)
            self.distributions = distributions

        def get_receivers(self, receiver_list):
            if receiver_list:
                return self.distributions[receiver_list]

        def get_cc(self, receiver_list):
            if receiver_list:
                return self.distributions[receiver_list]

        def get_bcc(self, receiver_list):
            if receiver_list:
                return self.distributions[receiver_list]

Then to use it:

.. code-block:: python

    email = DistributionSender(
        host="localhost", port=0,
        distributions={
            "managers": ["boss1@example.com", "boss2@example.com"],
            "developers": ["dev1@example.com", "dev2@example.com"]
        }
    )

    email.send(
        subject="Important news",
        receivers="developers",
        cc="managers",
        ...
    )

You can also accomplish this without subclassing to limited extent:

.. code-block:: python

    managers = EmailSender(host="localhost", port=0)
    managers.receivers = ["boss1@example.com", "boss2@example.com"]

    developers = EmailSender(host="localhost", port=0)
    developers.receivers = ["dev1@example.com", "dev2@example.com"]

    # Send an email to the developers
    developers.send(
        subject="Important news"
    )