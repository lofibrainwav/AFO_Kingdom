import pytest
from AFO.api_server import app
from starlette.testclient import TestClient


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
