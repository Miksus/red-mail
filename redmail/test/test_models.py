
from redmail.models import EmailAddress, Error

import pytest

@pytest.mark.parametrize("addr,expected",
    [
        pytest.param('info@company.com', {'first_name': None, 'last_name': None, 'full_name': 'Info', 'organization': 'Company', 'top_level_domain': '.com'}, id="Not personal"),
        pytest.param('first.last@company.com', {'first_name': "First", 'last_name': "Last", 'full_name': 'First Last', 'organization': 'Company', 'top_level_domain': '.com'}, id="Personal"),
        pytest.param('no-reply@en.company.com', {'first_name': None, 'last_name': None, 'full_name': 'No-reply', 'organization': 'Company', 'top_level_domain': '.com'}, id="Multi-domain-part"),
    ]
)
def test_address(addr, expected):
    address = EmailAddress(addr)

    assert expected['first_name'] == address.first_name
    assert expected['last_name'] == address.last_name
    assert expected['full_name'] == address.full_name
    assert expected['organization'] == address.organization
    assert expected['top_level_domain'] == address.top_level_domain
    assert str(address) == addr

@pytest.mark.parametrize("exc_as", ['current stack', 'passed exception'])
@pytest.mark.parametrize("cont_type,starts,ends",
    [
        pytest.param(
            'text', 
            'Traceback (most recent call last):\n  File "', 
            '\n    raise RuntimeError("deliberate error")\n\nRuntimeError: deliberate error', 
            id="text"
        ),
        pytest.param(
            'html', 
            '<div class="error">\n                <h4 class="header">Traceback (most recent call last):</h4>\n                <pre class="traceback"><code>  File &quot;',
            '\n    raise RuntimeError(&quot;deliberate error&quot;)</code></pre>\n                <div class="exception">\n                    <span class="exception-type">RuntimeError</span>: <span class="exception-value">deliberate error</span>\n                </div>\n            </div>',
            id="html"
        ),
        pytest.param(
            'html-inline', 
            '\n        <div>\n            <h4>Traceback (most recent call last):</h4>\n            <pre><code>  File &quot;', 
            '\nraise RuntimeError(&quot;deliberate error&quot;)</code></pre>\n            <span style="color: red; font-weight: bold">deliberate error</span>: <span>RuntimeError</span>\n        </div>', 
            id="html-inline"
        ),
    ]
)
def test_error(cont_type, starts, ends, exc_as):
    try:
        raise RuntimeError("deliberate error")
    except RuntimeError as exc:
        if exc_as == 'current stack':
            err = Error(content_type=cont_type)
            exc_type = err.exception_type
            exc_value = err.exception_value
            tb = err.traceback
            string = str(err)
            assert bool(err)
        e = exc
    if exc_as == 'passed exception':
        err = Error(content_type=cont_type, exception=e)
        exc_type = err.exception_type
        exc_value = err.exception_value
        tb = err.traceback
        string = str(err)
        assert bool(err)
    
    assert exc_type == 'RuntimeError'
    assert exc_value == 'deliberate error'
    assert len(tb) == 1
    assert tb[0].startswith('  File "')
    assert tb[0].endswith(', in test_error\n    raise RuntimeError("deliberate error")\n')

    assert string.startswith(starts)
    assert string.endswith(ends)
    
def test_error_no_error():
    err = Error()
    assert err.exception_type is None
    assert err.exception_value is None
    assert err.traceback is None

    assert not bool(err)

def test_error_invalid_type():
    err = Error("Not existing")
    with pytest.raises(ValueError):
        str(err)