import socket
from redmail import EmailSender

import pytest

from convert import remove_extra_lines, payloads_to_dict
from getpass import getpass, getuser
from platform import node
import base64, re

from convert import remove_email_extra

def test_empty():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
    )
    structure = payloads_to_dict(msg)
    assert structure == {}

def test_text():

    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        text="Text content",
    )
    structure = payloads_to_dict(msg)
    assert structure == {
        'text/plain': 'Text content\n'
    }

def test_html():
    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        html="<h1>HTML content</h1>",
    )
    structure = payloads_to_dict(msg)
    assert structure == {
        "multipart/mixed": {
            'multipart/alternative': {
                'text/html': '<h1>HTML content</h1>\n'
            }
        }
    }

def test_text_and_html():
    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        text="Text content",
        html="<h1>HTML content</h1>",
    )
    structure = payloads_to_dict(msg)
    assert structure == {
        "multipart/mixed": {
            'multipart/alternative': {
                'text/plain': 'Text content\n',
                'text/html': '<h1>HTML content</h1>\n'
            }
        }
    }

def test_attachment():
    sender = EmailSender(host=None, port=1234)
    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        attachments={'data.txt': "Some content"}
    )
    structure = payloads_to_dict(msg)
    assert structure == {
        "multipart/mixed": {
            'application/octet-stream': 'U29tZSBjb250ZW50\n'
        }
    }

def test_html_inline():
    img_data = '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oD/2Q=='
    img_bytes = base64.b64decode(img_data)

    sender = EmailSender(host=None, port=1234)

    # CI may have long domain name thus we set it to such
    # that's shorter but looks realistic
    host = "REDMAIL-1234.mail.com"
    sender.domain = host

    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        html='<p>HTML content</p> \n{{ my_image }}',
        body_images={
            "my_image": {
                "content": img_bytes,
                'subtype': 'jpg'
            }
        },
    )

    structure = payloads_to_dict(msg)
    cid = re.search('(?<=cid:).+(?=@)', structure["multipart/mixed"]["multipart/alternative"]["multipart/related"]["text/html"]).group()
    assert structure == {
        "multipart/mixed": {
            "multipart/alternative": {
                "multipart/related": {
                    'text/html': f'<p>HTML content</p> \n<img src="cid:{cid}@{host}">\n',
                    'image/jpg': '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcG\nBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwM\nDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooo\nr8DP9oD/2Q==\n',
                }
            },
        }
    }

def test_text_html_inline_attachment():
    img_data = '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oD/2Q=='
    img_bytes = base64.b64decode(img_data)

    sender = EmailSender(host=None, port=1234)

    # CI may have long domain name thus we set it to such
    # that's shorter but looks realistic
    host = "REDMAIL-1234.mail.com"
    sender.domain = host

    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        text="Text content",
        html='<p>HTML content</p> \n{{ my_image }}',
        body_images={
            "my_image": {
                "content": img_bytes,
                'subtype': 'jpg'
            }
        },
        attachments={'data.txt': "Some content"},
    )

    structure = payloads_to_dict(msg)
    cid = re.search('(?<=cid:).+(?=@)', structure["multipart/mixed"]["multipart/alternative"]["multipart/related"]["text/html"]).group()
    assert structure == {
        "multipart/mixed": {
            "multipart/alternative": {
                'text/plain': 'Text content\n',
                "multipart/related": {
                    'text/html': f'<p>HTML content</p> \n<img src="cid:{cid}@{host}">\n',
                    'image/jpg': '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcG\nBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwM\nDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooo\nr8DP9oD/2Q==\n',
                }
            },
            # Attachments
            'application/octet-stream': 'U29tZSBjb250ZW50\n'
        }
    }

def test_text_html_inline_attachment_multiple():
    img_data = '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oD/2Q=='
    img_bytes = base64.b64decode(img_data)

    sender = EmailSender(host=None, port=1234)

    # CI may have long domain name thus we set it to such
    # that's shorter but looks realistic
    host = "REDMAIL-1234.mail.com"
    sender.domain = host

    msg = sender.get_message(
        sender="me@example.com",
        receivers="you@example.com",
        subject="An example",
        text="Text content",
        html='<p>HTML content</p> \n{{ my_image_1 }}\n{{ my_image_2 }}',
        body_images={
            "my_image_1": {
                "content": img_bytes,
                'subtype': 'jpg'
            },
            "my_image_2": {
                "content": img_bytes,
                'subtype': 'jpg'
            },
        },
        attachments={
            'data_1.txt': "Some content 1",
            "data_2.txt": "Some content 2",
        },
    )

    structure = payloads_to_dict(msg)
    cid_1, cid_2 = re.findall('(?<=cid:).+(?=@)', structure["multipart/mixed"]["multipart/alternative"]["multipart/related"]["text/html"])
    assert structure == {
        "multipart/mixed": {
            "multipart/alternative": {
                'text/plain': 'Text content\n',
                "multipart/related": {
                    'text/html': f'<p>HTML content</p> \n<img src="cid:{cid_1}@{host}">\n<img src="cid:{cid_2}@{host}">\n',
                    'image/jpg':   '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcG\nBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwM\nDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooo\nr8DP9oD/2Q==\n',
                    'image/jpg_1': '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcG\nBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwM\nDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooo\nr8DP9oD/2Q==\n',
                }
            },
            # Attachments
            'application/octet-stream': 'U29tZSBjb250ZW50IDE=\n',
            'application/octet-stream_1': 'U29tZSBjb250ZW50IDI=\n'
        }
    }