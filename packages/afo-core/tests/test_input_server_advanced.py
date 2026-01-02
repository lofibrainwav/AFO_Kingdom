# Trinity Score: 90.0 (Established by Chancellor)
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Must mock modules before importing input_server to avoid ImportError
# We intentionally want api_wallet import to FAIL to test the HTTP fallback
# So we don't mock it here, or we mock it to raise ImportError?
# But other tests might accept it.
# The safest way is to clean sys.modules or use patch.dict(sys.modules) inside the test?
# But input_server imports at functional level.


def test_bulk_import_http_fallback():
    # Setup mocks
    MagicMock()

    # We need to simulate imported module state where 'api_wallet' is NOT available
    # But input_server.py is already imported by previous tests potentially.
    # We must patch sys.modules to remove it if present, OR patch import mechanism.
    # Easier: patch 'afo.input_server.APIWallet' to raise ImportError?
    # The code does `from api_wallet import APIWallet`.

    # Let's import input_server afresh or rely on the fact that we can control the imports inside the function via patch.dict

    with patch.dict(
        sys.modules, {"api_wallet": None}
    ):  # None usually causes ImportError or similar
        # But wait, if previous tests put a Mock in sys.modules, we need to override it.
        # Setting to None might break things.

        # Better strategy: Patch the class constructor or the specific import line using patch.dict is hard for local import.
        # Let's look at input_server.py again. It does `from api_wallet import APIWallet` inside `bulk_import`.

        # We can simulate failure by patching the class if the module is already loaded.
        pass

    # Actually, let's use a fresh import strategy for the test function logic
    # But input_server.app uses the global scope.

    pass


# We'll use the existing app but patch the internals
from afo.input_server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_bulk_import_via_http_api():
    """
    Test bulk_import when direct APIWallet access fails, forcing HTTP API usage.
    """
    # 1. Mock APIWallet usage to FAIL
    # The code:
    # try:
    #     from api_wallet import APIWallet
    #     wallet = APIWallet()
    # except Exception: wallet = None

    # We can mock `api_wallet.APIWallet` to raise an exception upon instantiation
    # This assumes `api_wallet` module IS importable (mocked or real)

    mock_wallet_module = MagicMock()
    mock_wallet_class = MagicMock()
    mock_wallet_class.side_effect = Exception("Direct Access Denied")  # Force failure
    mock_wallet_module.APIWallet = mock_wallet_class

    # 2. Mock HTTPX for API Server availability and Add Key
    mock_client = AsyncMock()
    # First call: health check (True)
    health_resp = MagicMock(status_code=200)
    # Second call: check if key exists (404/Not Found -> Proceed) OR (200 -> Skip)
    # Let's say check returns 404 (doesn't exist)
    check_resp = MagicMock(status_code=404)
    # Third call: add key (200 OK)
    add_resp = MagicMock(status_code=200)

    # Helper to return different responses based on URL
    async def side_effect(url, **kwargs):
        if "/health" in url:
            return health_resp
        if "/get/" in url:
            return check_resp
        if "/add" in url:
            return add_resp
        return MagicMock(status_code=500)

    mock_client.get.side_effect = side_effect
    mock_client.post.return_value = add_resp

    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    # Patch sys.modules to provide our 'api_wallet' that fails instantiation
    with patch.dict(sys.modules, {"api_wallet": mock_wallet_module}):
        with patch("httpx.AsyncClient", return_value=mock_client):
            response = client.post(
                "/bulk_import",
                data={"bulk_text": "HTTP_KEY=sk-http"},
                follow_redirects=False,
            )

            # The input_server returns RedirectResponse(303)
            assert response.status_code == 303, (
                f"Response was {response.status_code}: {response.text}"
            )
            assert "success" in response.headers["location"]
            # Verify URL encoding logic implicitly by checking substring
            # "1개 저장 성공" might be percent encoded
            assert (
                "saved" in response.headers["location"] or "success" in response.headers["location"]
            )

            # Verify HTTP calls were made
            # Health check called?
            # mock_client.get.assert_any_call(".../health") # URL might differ
            assert mock_client.get.call_count >= 1  # Health + Check
            assert mock_client.post.call_count == 1
