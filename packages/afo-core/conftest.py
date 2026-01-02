# Trinity Score: 90.0 (Established by Chancellor)
import pytest
from starlette.testclient import TestClient

from AFO.api_server import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
