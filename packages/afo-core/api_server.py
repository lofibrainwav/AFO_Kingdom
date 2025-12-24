# mypy: ignore-errors
# 🧭 Trinity Score: 眞89% 善85% 美72% 孝95% | Total: 84%
# 이 파일은 AFO 왕국의 眞善美孝 철학을 구현합니다

# afo_soul_engine/api_server.py

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Path setup for imports (must be before AFO imports)
_AFO_ROOT = str(Path(__file__).resolve().parent.parent)
if _AFO_ROOT not in sys.path:
    sys.path.insert(0, _AFO_ROOT)

# Core FastAPI imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

# AFO Kingdom imports via Strangler Fig Facade

# Configuration and services
# Import setup_routers from routers.py file (not routers directory)
import importlib.util
from pathlib import Path

from AFO.api.config import get_app_config
from AFO.api.middleware import setup_middleware

_routers_file = Path(__file__).parent / "api" / "routers.py"
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
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
    uvicorn.run(app, host=host, port=port)
