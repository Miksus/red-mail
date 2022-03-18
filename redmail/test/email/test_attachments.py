
from redmail import EmailSender

import base64

from pathlib import Path
import pytest

from resources import get_mpl_fig, get_pil_image
from convert import remove_extra_lines, payloads_to_dict

def to_encoded(s:str):
    return str(base64.b64encode(s.encode()), 'ascii')


def test_with_text():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        text="Hi, this is an email",
        attachments={'data.txt': "Some content"}
    )
    # Validate structure
    assert payloads_to_dict(msg) == {
        'multipart/mixed': {
            'application/octet-stream': 'U29tZSBjb250ZW50\n',
            'text/plain': 'Hi, this is an email\n',
        }
    }

    assert msg.get_content_type() == "multipart/mixed"

    text, attachment = msg.get_payload()
    assert text.get_content_type() == 'text/plain'
    assert attachment.get_content_type() == 'application/octet-stream'
    assert text.get_payload() == "Hi, this is an email\n"

    filename = attachment.get_filename()
    data = attachment.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_with_html():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        html="<h1>Hi, this is an email.</h1>",
        attachments={'data.txt': "Some content"}
    )
    # Validate structure
    assert payloads_to_dict(msg) == {
        'multipart/mixed': {
            'application/octet-stream': 'U29tZSBjb250ZW50\n',
            'multipart/alternative': {
                'text/html': '<h1>Hi, this is an email.</h1>\n'
            }
        }
    }

    assert msg.get_content_type() == "multipart/mixed"

    alternative, attachment = msg.get_payload()
    html = alternative.get_payload()[0]
    assert html.get_content_type() == 'text/html'
    assert attachment.get_content_type() == 'application/octet-stream'

    assert html.get_payload() == "<h1>Hi, this is an email.</h1>\n"

    filename = attachment.get_filename()
    data = attachment.get_payload()
    assert attachment.get_content_type() == 'application/octet-stream'
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_with_text_and_html():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        text="Hi, this is an email.",
        html="<h1>Hi, this is an email.</h1>",
        attachments={'data.txt': "Some content"}
    )
    # Validate structure
    assert payloads_to_dict(msg) == {
        'multipart/mixed': {
            'application/octet-stream': 'U29tZSBjb250ZW50\n',
            'multipart/alternative': {
                'text/html': '<h1>Hi, this is an email.</h1>\n',
                'text/plain': 'Hi, this is an email.\n'
            }
        }
    }
    assert msg.get_content_type() == "multipart/mixed"

    alternative, attachment = msg.get_payload()
    text, html = alternative.get_payload()
    assert text.get_content_type() == "text/plain"
    assert html.get_content_type() == "text/html"
    assert attachment.get_content_type() == 'application/octet-stream'

    assert text.get_payload() == 'Hi, this is an email.\n'
    assert html.get_payload() == '<h1>Hi, this is an email.</h1>\n'

    filename = attachment.get_filename()
    data = attachment.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_no_body():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'data.txt': 'Some content'}
    )
    # Validate structure
    assert payloads_to_dict(msg) == {
        'multipart/mixed': {
            'application/octet-stream': 'U29tZSBjb250ZW50\n',
        }
    }

    assert msg.get_content_type() == "multipart/mixed"
    assert len(msg.get_payload()) == 1

    attachment = msg.get_payload(0)
    assert attachment.get_content_type() == 'application/octet-stream'

    filename = attachment.get_filename()
    data = attachment.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_dict_string():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'data.txt': 'Some content'}
    )
    assert msg.get_content_type() == "multipart/mixed"
    attachment = msg.get_payload(0)
    filename = attachment.get_filename()
    data = attachment.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_dict_bytes():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'data.bin': bytes(10)}
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'data.bin'
    assert base64.b64encode(bytes(10)).decode() == data.replace('\n', '')

def test_dict_path(tmpdir):
    file = tmpdir.join("data.txt")
    file.write("Some content")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myfile.txt': Path(str(file))}
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'myfile.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_dict_dataframe_txt():
    pytest.importorskip("pandas")
    import pandas as pd

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myfile.txt': pd.DataFrame({'a': [1,2,3], 'b': ['1', '2', '3']})}
    )
    expected = str(pd.DataFrame({'a': [1,2,3], 'b': ['1', '2', '3']}))

    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'myfile.txt'
    assert to_encoded(expected) == data.replace('\n', '')

def test_dict_dataframe_csv():
    pytest.importorskip("pandas")
    import pandas as pd

    df = pd.DataFrame({'a': [1,2,3], 'b': ['1', '2', '3']})

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myfile.csv': df}
    )

    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'myfile.csv'
    assert to_encoded(df.to_csv()) == data.replace('\n', '')

def test_dict_dataframe_html():
    pytest.importorskip("pandas")
    import pandas as pd

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myfile.html': pd.DataFrame({'a': [1,2,3], 'b': ['1', '2', '3']})}
    )
    expected = '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>a</th>\n      <th>b</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>1</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>2</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>3</td>\n      <td>3</td>\n    </tr>\n  </tbody>\n</table>'

    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload().replace('\n', '')

    assert filename == 'myfile.html'
    assert to_encoded(expected) == data

def test_dict_dataframe_invalid():
    pytest.importorskip("pandas")
    import pandas as pd

    sender = EmailSender(host=None, port=1234)
    with pytest.raises(ValueError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            attachments={'myfile.something': pd.DataFrame({'a': [1,2,3], 'b': ['1', '2', '3']})}
        )

def test_dict_dataframe_excel_no_error():
    pytest.importorskip("pandas")
    pytest.importorskip("openpyxl")
    import pandas as pd

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myfile.xlsx': pd.DataFrame({'a': [1,2,3], 'b': ['1', '2', '3']})}
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'myfile.xlsx'
    # Excels are harder to verify

def test_dict_pil_no_error():
    pil, bytes_img = get_pil_image()

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myimg.png': pil}
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'myimg.png'
    assert str(base64.b64encode(bytes_img), 'ascii') == data.replace('\n', '')

def test_dict_matplotlib_no_error():
    fig, bytes_fig = get_mpl_fig()

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'myimg.png': fig}
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'myimg.png'
    assert str(base64.b64encode(bytes_fig), 'ascii') == data.replace('\n', '')

def test_dict_invalid():

    sender = EmailSender(host=None, port=1234)
    with pytest.raises(TypeError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            attachments={'myimg.png': sender}
        )

def test_dict_invalid_key():
    fig, bytes_fig = get_mpl_fig()

    sender = EmailSender(host=None, port=1234)
    with pytest.raises(TypeError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            attachments={sender: 'something'}
        )

def test_dict_multiple(tmpdir):
    file1 = tmpdir.join("file_1.txt")
    file1.write("Some content 1")

    file2 = tmpdir.join("file_2.txt")
    file2.write("Some content 2")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments={'data_1.txt': Path(file1), 'data_2.txt': Path(file2)}
    )
    assert msg.get_content_type() == "multipart/mixed"
    expected = [('data_1.txt', 'Some content 1'), ('data_2.txt', 'Some content 2')]
    for payload, expected in zip(msg.iter_attachments(), expected):
        filename = payload.get_filename()
        data = payload.get_payload()
        assert filename == expected[0]
        assert to_encoded(expected[1]) == data.replace('\n', '')



# List attachments
# ----------------

def test_list_path(tmpdir):
    file = tmpdir.join("data.txt")
    file.write("Some content")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments=[Path(str(file))]
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_list_string_path(tmpdir):
    file = tmpdir.join("data.txt")
    file.write("Some content")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments=[str(file)]
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_list_string_error():

    sender = EmailSender(host=None, port=1234)
    with pytest.raises(ValueError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            attachments=['just something']
        )

def test_list_multiple(tmpdir):
    file1 = tmpdir.join("data_1.txt")
    file1.write("Some content 1")

    file2 = tmpdir.join("data_2.txt")
    file2.write("Some content 2")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments=[Path(str(file1)), Path(str(file2))]
    )
    assert msg.get_content_type() == "multipart/mixed"
    expected = [('data_1.txt', 'Some content 1'), ('data_2.txt', 'Some content 2')]
    for payload, expected in zip(msg.iter_attachments(), expected):
        filename = payload.get_filename()
        data = payload.get_payload()
        assert filename == expected[0]
        assert to_encoded(expected[1]) == data.replace('\n', '')

def test_list_invalid():

    sender = EmailSender(host=None, port=1234)
    with pytest.raises(TypeError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            attachments=[sender]
        )

def test_string_path(tmpdir):
    file = tmpdir.join("data.txt")
    file.write("Some content")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments=str(file)
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')

def test_string_error():
    sender = EmailSender(host=None, port=1234)
    with pytest.raises(ValueError):
        msg = sender.get_message(
            sender="me@gmail.com",
            receivers="you@gmail.com",
            subject="Some news",
            attachments="just something"
        )

def test_path(tmpdir):
    file = tmpdir.join("data.txt")
    file.write("Some content")

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@gmail.com",
        receivers="you@gmail.com",
        subject="Some news",
        attachments=Path(file)
    )
    assert msg.get_content_type() == "multipart/mixed"
    payload = msg.get_payload(0)
    filename = payload.get_filename()
    data = payload.get_payload()
    assert filename == 'data.txt'
    assert to_encoded("Some content") == data.replace('\n', '')