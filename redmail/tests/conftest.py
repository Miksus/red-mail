
import pytest
from pathlib import Path
import os, sys

# add helpers to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

def copy_file_to_tmpdir(tmpdir, source_file, target_path=None):
    "Utility to copy file from test_files to temporary directory"
    source_path = Path(os.path.dirname(__file__)) / "test_files" / source_file

    fh = tmpdir.join(Path(target_path).name if target_path is not None else source_path.name)
    with open(source_path, 'rb') as f:
        fh.write_binary(f.read())
    return fh

@pytest.fixture
def dummy_png(tmpdir):
    return copy_file_to_tmpdir(tmpdir, source_file="dummy.png")