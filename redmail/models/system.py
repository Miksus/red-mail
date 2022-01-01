
import traceback
import sys
from typing import List, Tuple
from textwrap import dedent
import html

class Error:
    """Format class for errors including the exception 
    and traceback.
    
    Parameters
    ----------
        contet_type : str
            Content type for which the error is meant to be rendered
            on.
        exception : Exception
            Exception object. If not passed, current stack trace is used.
    """

    def __init__(self, content_type="text", exception:Exception=None):
        self.content_type = content_type
        self.exception = exception

    def __str__(self):
        if self.content_type == "text":
            return self.as_text()
        elif self.content_type == "html-inline":
            return self.as_html_inline()
        elif self.content_type == "html":
            return self.as_html()
        else:
            raise ValueError(f"Invalid content_type: {self.content_type}")

    def __bool__(self):
        "Return true if there is an error, false if not"
        exc_type, _, _ = self.exc_format()
        return exc_type is not None

    def as_text(self):
        "Format traceback as text"
        exc_type, exc_text, tb_list = self.exc_format()
        tb_text = '\n'.join(tb_list)
        return f"""Traceback (most recent call last):\n{tb_text}\n{exc_type}: {exc_text}"""

    def as_html_inline(self):
        "Format traceback as HTML"
        exc_type, exc_text, tb_list = self.exc_format()
        tb_str = '\n'.join(tb_list)
        if tb_str.endswith('\n'):
            tb_str = tb_str[:-1]
        exc_type, exc_text, tb_str = (html.escape(val) for val in (exc_type, exc_text, tb_str))

        return dedent(
            f"""
            <div>
                <h4>Traceback (most recent call last):</h4>
                <pre><code>{tb_str}</code></pre>
                <span style="color: red; font-weight: bold">{exc_text}</span>: <span>{exc_type}</span>
            </div>"""
        )

    def as_html(self):
        "Format traceback as HTML"
        exc_type, exc_text, tb_list = self.exc_format()
        tb_str = '\n'.join(tb_list)
        if tb_str.endswith('\n'):
            tb_str = tb_str[:-1]
        exc_type, exc_text, tb_str = (html.escape(val) for val in (exc_type, exc_text, tb_str))

        return dedent(
            f"""<div class="error">
                <h4 class="header">Traceback (most recent call last):</h4>
                <pre class="traceback"><code>{tb_str}</code></pre>
                <div class="exception">
                    <span class="exception-type">{exc_type}</span>: <span class="exception-value">{exc_text}</span>
                </div>
            </div>"""
        )

    @property
    def exception_type(self) -> str:
        "str: Type of the exception (as string)"
        type_, _, _ = self.exc_format()
        return type_

    @property
    def exception_value(self) -> str:
        "str: Exception value (as string)"
        _, value, _ = self.exc_format()
        return value

    @property
    def traceback(self) -> List[str]:
        "list str: Traceback (as list of str)"
        _, _, tb = self.exc_format()
        return tb

    def exc_format(self) -> Tuple[str, str, List[str]]:
        if self.exception is None:
            exc_type, exc_value, tb = sys.exc_info()
        else:
            exc_value = self.exception
            exc_type = type(self.exception)
            tb = self.exception.__traceback__
        tb_list = traceback.format_tb(tb) if tb is not None else None
        exc_str = str(exc_value) if exc_value is not None else None
        exc_type_str = exc_type.__name__ if exc_type is not None else None
        return exc_type_str, exc_str, tb_list