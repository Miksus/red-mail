
import importlib
import io
import os

def import_from_string(imp_str, if_missing="raise"):
    try:
        return importlib.import_module(imp_str)
    except ImportError:
        if if_missing == "ignore":
            return None
        raise


def is_filelike(value):
    """Is file-like object or string of file path
    
    See: https://stackoverflow.com/a/1661354/13696660"""
    try:
        return hasattr(value, "read") or os.path.isfile(value)
    except TypeError:
        return False

def is_bytes(value):
    return isinstance(value, (bytes, bytearray))

def is_pathlike(value):
    "Check if the value is path-like"
    return isinstance(value, os.PathLike)