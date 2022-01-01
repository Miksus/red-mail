
from redmail.models import EmailAddress

import pytest

@pytest.mark.parametrize("addr,expected",
    [
        pytest.param('info@company.com', {'first_name': None, 'last_name': None, 'full_name': 'Info', 'organization': 'Company'}, id="Not personal"),
        pytest.param('first.last@company.com', {'first_name': "First", 'last_name': "Last", 'full_name': 'First Last', 'organization': 'Company'}, id="Personal"),
        pytest.param('no-reply@en.company.com', {'first_name': None, 'last_name': None, 'full_name': 'No-reply', 'organization': 'Company'}, id="Multi-domain-part"),
    ]
)
def test_address(addr, expected):
    address = EmailAddress(addr)

    assert expected['first_name'] == address.first_name
    assert expected['last_name'] == address.last_name
    assert expected['full_name'] == address.full_name
    assert expected['organization'] == address.organization
    assert str(address) == addr