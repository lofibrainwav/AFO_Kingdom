"""
AFO API Middleware Package
"""

# Import setup_middleware from parent module (AFO.api.middleware.py)
# Note: This is a file, not a package, so we need to import from the parent package
import importlib.util
from pathlib import Path

from .audit import audit_middleware
from .prometheus import PrometheusMiddleware, metrics_endpoint

_parent_file = Path(__file__).parent.parent / "middleware.py"
if _parent_file.exists():
    spec = importlib.util.spec_from_file_location("AFO.api.middleware_module", _parent_file)
    if spec and spec.loader:
        middleware_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(middleware_module)
        setup_middleware = getattr(middleware_module, "setup_middleware", None)
        if setup_middleware:
            __all__ = [
                "PrometheusMiddleware",
                "audit_middleware",
                "metrics_endpoint",
                "setup_middleware",
            ]
        else:

            def setup_middleware(app):  # type: ignore
                pass

            __all__ = [
                "PrometheusMiddleware",
                "audit_middleware",
                "metrics_endpoint",
                "setup_middleware",
            ]
    else:

        def setup_middleware(app):  # type: ignore
            pass

        __all__ = [
            "PrometheusMiddleware",
            "audit_middleware",
            "metrics_endpoint",
            "setup_middleware",
        ]
else:

    def setup_middleware(app):  # type: ignore
        pass

    __all__ = [
        "PrometheusMiddleware",
        "audit_middleware",
        "metrics_endpoint",
        "setup_middleware",
    ]
