
import base64
from redmail import EmailSender

import re

from pathlib import Path
from io import BytesIO
import pytest

# Importing Pandas from utils (is None if missing package)
from redmail.email.utils import pd

from resources import get_mpl_fig, get_pil_image
from convert import remove_extra_lines, payloads_to_dict


def compare_image_mime(mime_part, mime_part_html, orig_image:bytes, type_="image/png"):
    assert type_ == mime_part.get_content_type()
    image_bytes = mime_part.get_content()
    assert orig_image == image_bytes

    # Check the HTML mime has the image
    image_info = dict(mime_part.items())
    cid_parts = image_info['Content-ID'][1:-1].split(".")
    cid = "{}.{}.=\n{}.{domain}".format(*cid_parts[:3], domain='.'.join(cid_parts[3:]))
    cid = image_info['Content-ID'][1:-1]

    mime_part_html_cleaned = mime_part_html.get_payload().replace("=\n", "")
    assert f'<img src=3D"cid:{cid}">' in mime_part_html_cleaned or f'<img src="cid:{cid}">' in mime_part_html_cleaned

@pytest.mark.parametrize(
    "get_image_obj", [
        pytest.param(lambda x: str(x), id="Path (str)"),
        pytest.param(lambda x: Path(str(x)), id="Path (pathlib)"),
        pytest.param(lambda x: open(str(x), 'rb').read(), id="Bytes (bytes)"),
        pytest.param(lambda x: BytesIO(open(str(x), 'rb').read()), id="Bytes (BytesIO)"),
        pytest.param(lambda x: {"maintype": "image", "subtype": "png", "content": open(str(x), 'rb').read()}, id="Dict specs"),
    ]
)
def test_with_image_file(get_image_obj, dummy_png):
    with open(str(dummy_png), "rb") as f:
        dummy_bytes = f.read()
    image_obj = get_image_obj(dummy_png)

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html='<h1>Hi,</h1> Nice to meet you. Look at this: {{ my_image }}',
        body_images={"my_image": image_obj}
    )
    
    assert "multipart/mixed" == msg.get_content_type()

    alternative = msg.get_payload()[0]
    related = alternative.get_payload()[0]

    mime_html, mime_image = related.get_payload()

    compare_image_mime(mime_image, mime_html, orig_image=dummy_bytes)

    # Test receivers etc.
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    assert {
        'From': 'me@gmail.com', 
        'Subject': 'Some news', 
        'To': 'you@gmail.com', 
        #'MIME-Version': '1.0', 
        'Content-Type': 'multipart/mixed'
    } == headers

def test_with_image_dict_jpeg():
    img_data = '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oD/2Q=='
    img_bytes = base64.b64decode(img_data)

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html='<h1>Hi,</h1> Nice to meet you. Look at this: {{ my_image }}',
        body_images={
            'my_image': {
                "content": img_bytes,
                'subtype': 'jpg'
            }
        }
    )
    # Validate structure
    structure = payloads_to_dict(msg)
    assert structure == {
        "multipart/mixed": {
            "multipart/alternative": {
                "multipart/related": {
                    "text/html": structure["multipart/mixed"]["multipart/alternative"]["multipart/related"]["text/html"],
                    "image/jpg": structure["multipart/mixed"]["multipart/alternative"]["multipart/related"]["image/jpg"],
                }
            }
        }
    }
    assert "multipart/mixed" == msg.get_content_type()

    alternative = msg.get_payload()[0]
    related = alternative.get_payload()[0]

    mime_html, mime_image = related.get_payload()

    compare_image_mime(mime_image, mime_html, orig_image=img_bytes, type_="image/jpg")

    # Test receivers etc.
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    assert {
        'From': 'me@gmail.com', 
        'Subject': 'Some news', 
        'To': 'you@gmail.com', 
        #'MIME-Version': '1.0', 
        'Content-Type': 'multipart/mixed'
    } == headers


@pytest.mark.parametrize(
    "get_image_obj", [
        pytest.param(get_mpl_fig, id="Matplotlib figure"),
        pytest.param(get_pil_image, id="PIL image"),
    ]
)
def test_with_image_obj(get_image_obj):
    image_obj, image_bytes = get_image_obj()

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html='<h1>Hi,</h1> Nice to meet you. Look at this: <img src="{{ my_image }}">',
        body_images={"my_image": image_obj}
    )
    
    assert "multipart/mixed" == msg.get_content_type()

    alternative = msg.get_payload()[0]
    related = alternative.get_payload()[0]

    mime_html, mime_image = related.get_payload()

    compare_image_mime(mime_image, mime_html, orig_image=image_bytes)

    # Test receivers etc.
    headers = {
        key: val
        for key, val in msg.items()
        if key not in ('Message-ID', 'Date')
    }
    assert {
        'From': 'me@gmail.com', 
        'Subject': 'Some news', 
        'To': 'you@gmail.com', 
        #'MIME-Version': '1.0', 
        'Content-Type': 'multipart/mixed'
    } == headers

def test_with_image_error():
    sender = EmailSender(host=None, port=1234)
    with pytest.raises(ValueError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            html='<h1>Hi,</h1> Nice to meet you. Look at this: <img src="{{ my_image }}">',
            body_images={"my_image": "this is invalid"}
        )

    invalid_type_obj = type("TempClass", (), {})()
    with pytest.raises(TypeError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            html='<h1>Hi,</h1> Nice to meet you. Look at this: <img src="{{ my_image }}">',
            body_images={"my_image": invalid_type_obj}
        )

    with pytest.raises(KeyError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            html='<h1>Hi,</h1> Nice to meet you. Look at this:>',
            body_images={"my_image": {}}
        )


@pytest.mark.parametrize(
    "get_df,", [
        pytest.param(
            lambda: pd.DataFrame(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                columns=pd.Index(["first", "second", "third"]),
            ), 
            id="Simple dataframe"
        ),
        pytest.param(
            lambda: pd.DataFrame(
                [[1], [2], [3]],
                columns=pd.Index(["first"]),
            ), 
            id="Single column datafram"
        ),
        pytest.param(
            lambda: pd.DataFrame(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                columns=pd.Index(["first", "second", "third"]),
                index=pd.Index(["a", "b", "c"], name="category")
            ),   
            id="Simple dataframe with index"
        ),
        pytest.param(
            lambda: pd.DataFrame(
                [[1, 2, 3, "a"], [4, 5, 6, "b"], [7, 8, 9, "c"], [10, 11, 12, "d"]],
                columns=pd.MultiIndex.from_tuples([("parent a", "child a"), ("parent a", "child b"), ("parent b", "child a"), ("parent c", "child a")], names=["lvl 1", "lvl 2"]),
                index=pd.MultiIndex.from_tuples([("row a", "sub a"), ("row a", "sub b"), ("row b", "sub a"), ("row c", "sub a")], names=["cat 1", "cat 2"]),
            ), 
            id="Complex dataframe"
        ),
        pytest.param(
            lambda: pd.DataFrame(
                [[1, 2], [4, 5]],
                columns=pd.MultiIndex.from_tuples([("col a", "child b", "subchild a"), ("col a", "child b", "subchild a")]),
                index=pd.MultiIndex.from_tuples([("row a", "child b", "subchild a"), ("row a", "child b", "subchild a")]),
            ), 
            id="Multiindex end with spanned"
        ),
        pytest.param(
            lambda: pd.DataFrame(
                [[1, 2], [4, 5]],
                columns=pd.MultiIndex.from_tuples([("col a", "child b", "subchild a"), ("col a", "child b", "subchild a")]),
                index=pd.MultiIndex.from_tuples([("row a", "child b", "subchild a"), ("row a", "child b", "subchild a")]),
            ).style.set_caption("A caption"), 
            id="With styler"
        ),
        pytest.param(
            lambda: pd.DataFrame(
                [],
                columns=pd.Index(["first", "second", "third"]),
            ), 
            id="Empty datafram"
        ),
    ]
)
def test_with_html_table_no_error(get_df, tmpdir):
    pytest.importorskip("pandas")
    df = get_df()
    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html='The table {{my_table}}',
        body_tables={"my_table": df}
    )
    
    assert "multipart/mixed" == msg.get_content_type()

    alternative = msg.get_payload()[0]
    mime_html = alternative.get_payload()[0]

    #mime_text = msg.get_payload()[0]
    html = remove_extra_lines(mime_html.get_payload()).replace("=20", "").replace('"3D', "")
    #tmpdir.join("email.html").write(html)

    # TODO: Test the HTML is as required

    assert html


def test_embed_tables_pandas_missing():
    sender = EmailSender(host=None, port=1234)

    from redmail.email import body
    pd_mdl = body.pd # This may be already None if env does not have Pandas
    try:
        # src uses this to reference Pandas (if missing --> None)
        body.pd = None
        with pytest.raises(ImportError):
            msg = sender.get_message(
                sender="me@gmail.com",
                receivers="you@gmail.com",
                subject="Some news",
                html='The table {{my_table}}',
                body_tables={"my_table": [{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]}
            )
    finally:
        body.pd = pd_mdl

def test_styled_tables_dependency_missing():
    pd = pytest.importorskip("pandas")

    sender = EmailSender(host=None, port=1234)

    from redmail.email import body
    mdl = body.css_inline # This may be already None if env does not have Pandas
    try:
        # src uses this to reference Pandas (if missing --> None)
        body.css_inline = None
        style = pd.DataFrame(
            {"col1": ["a", "b", "c"], "col2": [1, 2, 3]}
        ).style.set_caption("A caption")
        with pytest.raises(ImportError):
            msg = sender.get_message(
                sender="me@gmail.com",
                receivers="you@gmail.com",
                subject="Some news",
                html='The table {{my_table}}',
                body_tables={"my_table": style}
            )
    finally:
        body.css_inline = mdl