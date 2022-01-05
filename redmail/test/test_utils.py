
import pytest
from redmail.utils import import_from_string

def test_import_from_string():
    my_pkg = import_from_string("pathlib", if_missing="ignore")
    assert my_pkg is not None
    assert hasattr(my_pkg, "Path")

def test_import_from_string_ignore():
    my_pkg = import_from_string("non_existent_package", if_missing="ignore")
    assert my_pkg is None

def test_import_from_string_raise():
    with pytest.raises(ImportError):
        my_pkg = import_from_string("non_existent_package", if_missing="raise")
