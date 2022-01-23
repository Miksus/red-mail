
import logging
import pytest

@pytest.fixture
def logger():
    logger = logging.getLogger("_test")
    logger.handlers = []
    return logger