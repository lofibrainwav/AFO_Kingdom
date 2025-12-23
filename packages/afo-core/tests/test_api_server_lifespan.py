from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# We need to test the lifespan context manager in api_server.py
# The lifespan function depends on global variables in api_server.py
# that are imported at module level.
# To test the "Component Not Available" branches, we need to ensure those globals are None.


@pytest.mark.asyncio
async def test_lifespan_manager_calls_init_cleanup():
    """Test that lifespan manager calls initialize and cleanup systems."""
    from AFO.api.config import get_lifespan_manager
    from fastapi import FastAPI

    app = FastAPI()

    # We patch import inside the function to avoid strict dependency issues if modules are missing
    # But since we are testing flow, we just patch the imported functions in AFO.api.config

    # We need to patch where they are IMPORTED in AFO.api.config
    # Usually this is tricky if they are imported inside the function.
    # Looking at config.py:
    #     from AFO.api.cleanup import cleanup_system
    #     from AFO.api.initialization import initialize_system

    # We can patch the source modules 'AFO.api.cleanup.cleanup_system' and 'AFO.api.initialization.initialize_system'

    with patch(
        "AFO.api.initialization.initialize_system", new_callable=AsyncMock
    ) as mock_init:
        with patch(
            "AFO.api.cleanup.cleanup_system", new_callable=AsyncMock
        ) as mock_cleanup:
            async with get_lifespan_manager(app):
                mock_init.assert_awaited_once()
                mock_cleanup.assert_not_awaited()

            mock_cleanup.assert_awaited_once()
