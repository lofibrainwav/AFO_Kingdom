from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# We need to test the lifespan context manager in api_server.py
# The lifespan function depends on global variables in api_server.py
# that are imported at module level.
# To test the "Component Not Available" branches, we need to ensure those globals are None.


@pytest.mark.asyncio
async def test_lifespan_components_enabled():
    # Test the "Available" branches (partial)
    # We verify that if components ARE present, they are initialized

    # Yeongdeok needs async methods
    mock_yeongdeok_instance = MagicMock()
    mock_yeongdeok_instance.close_eyes = AsyncMock()
    # If open_eyes or similar is awaited on startup, mock that too.
    # Checking code: initialization seems synchronous constructor?

    mock_registry_instance = MagicMock()
    mock_registry_instance.count = lambda: 10

    mock_query_expander = MagicMock()
    mock_multimodal = MagicMock()

    patches = {
        "QueryExpander": MagicMock(return_value=mock_query_expander),
        "MultimodalRAGEngine": MagicMock(return_value=mock_multimodal),
        "YeongdeokComplete": MagicMock(return_value=mock_yeongdeok_instance),
        "register_core_skills": MagicMock(return_value=mock_registry_instance),
    }

    # We need to construct this carefully because api_server.py might have already imported "None"
    # if optional deps are missing in this environment.
    # So we patch the Names in AFO.api_server.

    from AFO import api_server

    with patch.multiple(api_server, **patches):
        # We also need to patch settings to avoid config errors if they are read in lifespan
        mock_settings = MagicMock()
        mock_settings.MOCK_MODE = True
        mock_settings.N8N_URL = "http://test"

        # Also patch DB connections to avoid real connection attempts if not fully mocked
        # It seems PG_POOL and REDIS_CLIENT are initialized inside lifespan too?
        # Lines 778 global definition.
        # Lines 949 PG_POOL = SimpleConnectionPool(...)

        with patch("AFO.api_server.get_settings", return_value=mock_settings):
            with patch("AFO.api_server.SimpleConnectionPool", MagicMock()):
                with patch("AFO.api_server.redis.Redis", MagicMock()):
                    with TestClient(api_server.app):
                        pass
                        # Verify initializations happened
                        # Since we mocked the classes, we expect their constructors to be called.
                        patches["QueryExpander"].assert_called()
                        patches["MultimodalRAGEngine"].assert_called()
