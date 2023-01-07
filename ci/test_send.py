
import argparse
import os, time
import base64, logging
from pathlib import Path
from redmail import EmailSender, EmailHandler, MultiEmailHandler

from dotenv import load_dotenv
load_dotenv()

email = EmailSender(
    host=os.environ['EMAIL_HOST'],
    port=int(os.environ['EMAIL_PORT']),
    username=os.environ['EMAIL_USERNAME'],
    password=os.environ['EMAIL_PASSWORD']
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def send_empty():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Empty email",
    )

def send_text():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with text",
        text="Hi, this is an example email.",
    )

def send_html():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with HTML",
        html="<h2>This is HTML.</h2>",
    )

def send_test_and_html():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with text and HTML",
        text="This is text (with HTML).",
        html="<h2>This is HTML (with text).</h2>",
    )


def send_attachments():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with attachment",
        attachments={"a_file.html": (Path(__file__).parent / "file.html")}
    )

def send_attachments_with_text():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with attachment and text",
        text="This contains an attachment.",
        attachments={"a_file.html": (Path(__file__).parent / "file.html")}
    )

def send_attachments_with_html():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with attachment and HTML",
        html="<h1>This contains an attachment.</h1>",
        attachments={"a_file.html": (Path(__file__).parent / "file.html")}
    )

def send_attachments_with_html_and_image():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with attachment, HTML and inline image",
        html="<h1>This contains an attachment and image.</h1>{{ path_image }}",
        body_images={
            "path_image": Path(__file__).parent.parent / "docs/imgs/email_emb_img.png",
        },
        attachments={"a_file.html": (Path(__file__).parent / "file.html")}
    )

def send_full_features():
    msg = email.send(
        sender=os.environ['EMAIL_SENDER'],
        receivers=os.environ['EMAIL_RECEIVERS'].split(","),
        subject="Email with full features",
        text="Hi, this contains an attachment and image.",
        html="<h1>This contains text, HTML, an attachment and inline image.</h1>{{ path_image }}",
        body_images={
            "path_image": Path(__file__).parent.parent / "docs/imgs/email_emb_img.png",
        },
        attachments={"a_file.html": (Path(__file__).parent / "file.html")}
    )


def send_images():
    img_data = '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oD/2Q=='
    img_bytes = base64.b64decode(img_data)

    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.plot([1,2,3,2,3])

    email.send(
        sender=f"An Alias <{os.environ['EMAIL_SENDER']}>",
        receivers=[os.environ['EMAIL_RECEIVERS']],
        subject="Embedded images",
        html='''
            <p>Dict image (JPEG):</p>
            <br>{{ dict_image }}
            <p>Plot image:</p>
            <br>{{ plot_image }}
            <p>Path image:</p>
            <br>{{ path_image }}
        ''',
        body_images={
            'dict_image': {
                "content": img_bytes,
                'subtype': 'jpg',
            },
            "plot_image": fig,
            "path_image": Path(__file__).parent.parent / "docs/imgs/email_emb_img.png",
            "path_image_str": str((Path(__file__).parent.parent / "docs/imgs/email_emb_img.png").absolute()),
        }
    )

def send_tables():
    import pandas as pd
    df_empty = pd.DataFrame()
    df_simple = pd.DataFrame({"col 1": [1,2,3], "col 2": ["a", "b", "c"]})
    df_multi_index = pd.DataFrame({"col 1": [1,2,3], "col 2": ["a", "b", "c"]})
    email.send(
        receivers=[os.environ['EMAIL_RECEIVER']],
        subject="Embedded tables",
        html='''
            <p>Empty:</p>
            <br>{{ empty }}
            <p>Simple:</p>
            <br>{{ simple }}
            <p>Multi-index:</p>
            <br>{{ multi_index }}
            <p>Multi-index:</p>
            <br>{{ multi_index_and_columns }}
        ''',
        body_tables={
            'empty': pd.DataFrame(),
        }
    )


def log_multi():
    logger.handlers = []

    hdlr = MultiEmailHandler(
        capacity=4,
        email=email,
        subject="Log records: {min_level_name} - {max_level_name}",
        receivers=os.environ["EMAIL_RECEIVERS"].split(","),
        html="""
            {% for record in records %}
            <h2>A log record</h2>
            <ul>
                <li>Logging level: {{ record.levelname }}</li>
                <li>Message: {{ record.msg }}</li>
            </ul>
            {% endfor %}
        """,
    )
    logger.addHandler(hdlr)

    logger.debug("A debug record")
    logger.info("An info record")
    logger.warning("A warning record")

    try:
        raise RuntimeError("Oops")
    except:
        logger.exception("An exception record")

    logger.handlers = []

def log_simple():
    logger.handlers = []

    hdlr = EmailHandler(
        email=email,
        subject="A log record: {record.levelname}",
        receivers=os.environ["EMAIL_RECEIVERS"].split(","),
        html="""
            <h2>A log record</h2>
            <ul>
                <li>Logging level: {{ record.levelname }}</li>
                <li>Message: {{ record.msg }}</li>
            </ul>
        """,
    )
    logger.addHandler(hdlr)

    logger.info("An info record")
    logger.handlers = []

def main():
    funcs = {
        "empty": send_empty,
        "body_with_text": send_text,
        "body_with_html": send_html,
        "body_with_html_and_text": send_test_and_html,
        "full": send_full_features,

        "images": send_images,

        "with_attachments": send_attachments,
        "body_with_text_and_attachments": send_attachments_with_text,
        "body_with_html_and_attachments": send_attachments_with_html,

        "log": log_simple,
        "log_multi": log_multi,
    }

    parser = argparse.ArgumentParser(prog="Redmail tester")
    parser.add_argument(
        'funcs', type=str, nargs='+',
        help=f"Test functions to run. Allowed: {list(funcs)}"
    )

    args = parser.parse_args()

    for func_name in args.funcs:
        func = funcs[func_name]
        func()
        time.sleep(1)


if __name__ == "__main__":
    main()