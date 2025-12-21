"""
AFO API Middleware Package
"""

from .audit import audit_middleware
from .prometheus import PrometheusMiddleware, metrics_endpoint

# Import setup_middleware from parent module
import sys
from pathlib import Path

_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

try:
    from AFO.api.middleware import setup_middleware
    __all__ = ["audit_middleware", "PrometheusMiddleware", "metrics_endpoint", "setup_middleware"]
except ImportError:
    # Fallback: define a dummy function
    def setup_middleware(app):  # type: ignore
        pass
    __all__ = ["audit_middleware", "PrometheusMiddleware", "metrics_endpoint", "setup_middleware"]

