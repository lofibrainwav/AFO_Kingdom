"""
AFO Kingdom API Configuration Module

Handles FastAPI app configuration, server settings, and lifespan management.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from AFO.api.compat import get_settings_safe

# ============================================================================
# APP CONFIGURATION
# ============================================================================


def get_app_config() -> FastAPI:
    """Create and configure FastAPI application instance."""
    from AFO.api.metadata import get_api_metadata

    metadata = get_api_metadata()

    app = FastAPI(lifespan=get_lifespan_manager, **metadata)

    return app


def get_server_config() -> tuple[str, int]:
    """Get server host and port configuration."""
    settings = get_settings_safe()

    if settings:
        host = getattr(settings, "API_SERVER_HOST", "0.0.0.0")
        port = getattr(settings, "API_SERVER_PORT", 8010)
    else:
        host = os.getenv("API_SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("API_SERVER_PORT", "8010"))

    return host, port


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================


@asynccontextmanager
async def get_lifespan_manager(app=None):  # type: ignore
    """
    Manage application lifecycle with proper initialization and cleanup.

    This replaces the complex lifespan function in the main api_server.py
    with a cleaner, more maintainable approach.

    Args:
        app: FastAPI app instance (optional, for compatibility with FastAPI's lifespan)
    """
    # Import here to avoid circular imports
    from AFO.api.cleanup import cleanup_system
    from AFO.api.initialization import initialize_system

    try:
        # Initialize system components
        await initialize_system()
        yield
    except Exception as e:
        print(f"❌ [Lifespan Error] 런타임 중 치명적 오류 발생: {e}")
        raise
    finally:
        # Cleanup system components
        await cleanup_system()
