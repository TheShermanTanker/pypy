import os
import pytest
import sys

disabled = None
THIS_DIR = os.path.dirname(__file__)

if sys.maxsize > 2**32 and sys.platform == 'win32':
    disabled = True

def pytest_ignore_collect(path, config):
    path = str(path)
    if disabled:
        if os.path.commonprefix([path, THIS_DIR]) == THIS_DIR:  # workaround for bug in pytest<3.0.5
            return True

def pytest_collect_file(path, parent):
    if disabled:
        # We end up here when calling py.test .../test_foo.py directly
        # It's OK to kill the whole session with the following line
        pytest.skip("not yet supported on windows 64 bit")
