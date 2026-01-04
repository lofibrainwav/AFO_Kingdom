"""
AFO Authorization Middleware
Minimal stub implementation for CI compatibility.
"""

from typing import Callable


class APIKeyAuthMiddleware:
    """
    API Key Authentication middleware for FastAPI applications.
    Currently a no-op stub for CI compatibility.
    """
    
    def __init__(self, app: Callable = None, **kwargs):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        """ASGI middleware interface"""
        if self.app:
            await self.app(scope, receive, send)
        else:
            # Pass through if no app
            await send(scope)


def install_authz_middleware(app, **kwargs):
    """
    Install authorization middleware on FastAPI app.
    Currently a no-op for CI compatibility.
    """
    return app
