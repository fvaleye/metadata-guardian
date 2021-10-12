import os

import pytest


@pytest.fixture
def local_file(request) -> str:
    return os.path.join(os.path.dirname(__file__), "resources", request.param)
