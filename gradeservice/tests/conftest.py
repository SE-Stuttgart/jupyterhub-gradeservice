import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from gradeservice.main import app


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def testdata():
    return Path(os.path.dirname(__file__), "testdata")
