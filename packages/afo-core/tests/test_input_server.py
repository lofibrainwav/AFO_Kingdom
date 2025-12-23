import sys
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

# Mock dependencies BEFORE importing input_server to ensure they exist
# This avoids ImportError and allows the module to bind the names
mock_storage = MagicMock()
mock_wallet_module = MagicMock()
sys.modules["input_storage"] = mock_storage
sys.modules["api_wallet"] = mock_wallet_module

# Now import the app
from AFO.input_server import app, parse_env_text

client = TestClient(app)


# 1. Unit Tests for Logic
def test_parse_env_text():
    text = """
    OPENAI_API_KEY=sk-1234
    ANTHROPIC_API_KEY: sk-ant-5678
    "GITHUB_TOKEN": "ghp_abcd"
    N8N_URL "https://n8n.com"
    # Comment line
    INVALID_LINE
    """
    parsed = parse_env_text(text)

    assert len(parsed) == 4
    # Check key mappings
    assert parsed[0] == ("OPENAI_API_KEY", "sk-1234", "openai")
    assert parsed[1] == ("ANTHROPIC_API_KEY", "sk-ant-5678", "anthropic")
    assert parsed[2] == ("GITHUB_TOKEN", "ghp_abcd", "github")
    assert parsed[3] == ("N8N_URL", "https://n8n.com", "n8n")


def test_parse_env_text_quotes():
    text = """KEY_A="value_a"\nKEY_B='value_b'"""
    parsed = parse_env_text(text)
    assert parsed[0][1] == "value_a"
    assert parsed[1][1] == "value_b"


# 2. API Endpoints
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "AFO Input Server",
        "organ": "胃 (Stomach)",
    }


@patch("httpx.AsyncClient.get")
def test_home_page_no_keys(mock_get):
    mock_get.return_value = MagicMock(status_code=500)
    response = client.get("/")
    assert response.status_code == 200
    assert "AFO Input Server" in response.text
    assert "text/html" in response.headers["content-type"]


@patch("httpx.AsyncClient.get")
def test_home_page_with_keys(mock_get):
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {
        "keys": [
            {
                "name": "test_key",
                "provider": "openai",
                "created_at": "2024-01-01T00:00:00",
            }
        ]
    }
    mock_get.return_value = mock_response

    response = client.get("/")
    assert response.status_code == 200
    assert "test_key" in response.text
    assert "openai" in response.text


@patch("httpx.AsyncClient.post")
def test_add_key_success(mock_post):
    mock_post.return_value = MagicMock(status_code=200)

    # Ensure save_input_to_db is mockable via sys.modules or direct attribute
    # Since we mocked input_storage at top, AFO.input_server.save_input_to_db is a Mock

    response = client.post(
        "/add_key",
        data={
            "name": "new_key",
            "provider": "openai",
            "key": "sk-test-key",
            "description": "test key",
        },
    )
    assert response.status_code == 200
    # Capture print output or verify db call
    assert mock_storage.save_input_to_db.called


@patch("httpx.AsyncClient.post")
def test_add_key_wallet_failure(mock_post):
    mock_post.return_value = MagicMock(
        status_code=400, json=lambda: {"detail": "Bad Request"}
    )

    response = client.post(
        "/add_key", data={"name": "fail_key", "provider": "openai", "key": "sk-fail"}
    )
    assert response.status_code == 200


@patch("httpx.AsyncClient.get")
def test_api_status(mock_http_get):
    mock_http_get.return_value = MagicMock(status_code=200)
    mock_storage.get_input_statistics.return_value = {"count": 10}

    # Force INPUT_STORAGE_AVAILABLE to True for this test
    with patch("AFO.input_server.INPUT_STORAGE_AVAILABLE", True):
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["api_wallet_connected"] is True
        assert data["postgres_connected"] is True
        assert data["input_statistics"] == {"count": 10}


# 3. Bulk Import Logic
def test_bulk_import_direct_wallet():
    # Mock APIWallet class
    mock_wallet_instance = MagicMock()
    mock_wallet_module.APIWallet.return_value = mock_wallet_instance

    # Setup get to return None then something (simulate not exists then exists)
    mock_wallet_instance.get.side_effect = [None, "exists"]

    input_text = "NEW_KEY=sk-new\nEXISTING_KEY=sk-old"

    response = client.post("/bulk_import", data={"bulk_text": input_text})

    assert response.status_code == 200
    assert mock_wallet_instance.add.call_count == 1  # Only one added


def test_bulk_import_empty_handling():
    # If empty text passed (but valid param), it should handle it gracefully or invalid
    response = client.post(
        "/bulk_import", data={"bulk_text": " "}
    )  # Space is not empty param
    assert (
        response.status_code == 200
    )  # Redirects with error "파싱된 환경 변수가 없습니다"


def test_get_history():
    mock_storage.get_input_history.return_value = [{"id": 1}]
    with patch("AFO.input_server.INPUT_STORAGE_AVAILABLE", True):
        response = client.get("/api/history")
        assert response.status_code == 200
        assert response.json()["count"] == 1


def test_get_history_unavailable():
    with patch("AFO.input_server.INPUT_STORAGE_AVAILABLE", False):
        response = client.get("/api/history")
        assert response.status_code == 503
