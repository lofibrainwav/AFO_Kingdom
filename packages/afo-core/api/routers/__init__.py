"""
AFO API Routers
Phase 2 리팩토링: 라우터 분리
"""

# Import setup_routers from parent routers module
import sys
from pathlib import Path

from .health import router as health_router
from .root import router as root_router

# Add parent directory to path to import routers.py
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

try:
    # Import from AFO.api.routers (the file, not the directory)
    import importlib.util

    routers_file = _parent_dir / "routers.py"
    if routers_file.exists():
        spec = importlib.util.spec_from_file_location(
            "AFO.api.routers_module", routers_file
        )
        routers_module = importlib.util.module_from_spec(spec)
        if spec and spec.loader:
            spec.loader.exec_module(routers_module)
            setup_routers = routers_module.setup_routers
            __all__ = ["health_router", "root_router", "setup_routers"]
        else:
            __all__ = ["health_router", "root_router"]
    else:
        __all__ = ["health_router", "root_router"]
except Exception:
    __all__ = ["health_router", "root_router"]
