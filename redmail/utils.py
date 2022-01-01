
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

def is_bytes(value):
    return isinstance(value, (bytes, bytearray))
