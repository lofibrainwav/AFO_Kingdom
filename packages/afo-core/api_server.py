# mypy: ignore-errors
# 🧭 Trinity Score: 眞89% 善85% 美72% 孝95% | Total: 84%
# 이 파일은 AFO 왕국의 眞善美孝 철학을 구현합니다

# afo_soul_engine/api_server.py

from __future__ import annotations

import asyncio
import logging
import os
import sys
import warnings
from contextlib import asynccontextmanager
from pathlib import Path

# Path setup for imports (must be before AFO imports)
_AFO_ROOT = str(Path(__file__).resolve().parent.parent)
if _AFO_ROOT not in sys.path:
    sys.path.insert(0, _AFO_ROOT)

# Core FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# AFO Kingdom imports via Strangler Fig Facade
from AFO.api.compat import (
    # Core routers
    health_router,
    root_router,
    skills_router,
    streams_router,
    # Feature routers
    pillars_router,
    system_health_router,
    multi_agent_router,
    strangler_router,
    got_router,
    n8n_router,
    wallet_router,
    trinity_policy_router,
    trinity_sbt_router,
    users_router,
    auth_router,
    education_system_router,
    modal_data_router,
    personas_router,
    # Phase-specific routers
    budget_router,
    aicpa_router,
    learning_log_router,
    grok_stream_router,
    voice_router,
    council_router,
    learning_pipeline,
    serenity_router,
    matrix_router,
    rag_query_router,
    finance_router,
    ssot_router,
    chancellor_router,
)

# Configuration and services
from AFO.api.config import get_app_config, get_lifespan_manager
from AFO.api.middleware import setup_middleware
# Import setup_routers from routers.py file (not routers directory)
import importlib.util
from pathlib import Path
_routers_file = Path(__file__).parent / "AFO" / "api" / "routers.py"
if _routers_file.exists():
    spec = importlib.util.spec_from_file_location("AFO.api.router_setup", _routers_file)
    router_setup_module = importlib.util.module_from_spec(spec)
    if spec and spec.loader:
        spec.loader.exec_module(router_setup_module)
        setup_routers = router_setup_module.setup_routers
    else:
        def setup_routers(app):  # type: ignore
            pass
else:
    def setup_routers(app):  # type: ignore
        pass

# Global logger
logger = logging.getLogger(__name__)

# Create FastAPI app with configuration
app = get_app_config()

# Setup middleware (CORS, security, monitoring)
setup_middleware(app)

# Setup all routers in organized manner
setup_routers(app)

# Main execution block
if __name__ == "__main__":
    import uvicorn

    # Get server configuration
    from AFO.api.config import get_server_config
    host, port = get_server_config()

    print(f"🚀 Starting AFO Kingdom API Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, lifespan="on")
