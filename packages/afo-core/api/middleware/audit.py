"""
Audit Middleware for AFO Kingdom (Phase 22)
Logs privileged actions (POST/PUT/DELETE) for security auditing.
"""

import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger("AFO.Audit")


async def audit_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    # Only audit state-changing methods
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        user_agent = request.headers.get("user-agent", "unknown")
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        logger.info(
            f"🛡️ [AUDIT] method={request.method} path={path} ip={client_ip} agent={user_agent} status=PENDING"
        )

        start_time = time.time()
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            logger.info(
                f"✅ [AUDIT] method={request.method} path={path} status={response.status_code} duration={duration:.3f}s"
            )
            return response
        except Exception as e:
            logger.error(f"🚨 [AUDIT] method={request.method} path={path} status=ERROR error={e!s}")
            raise e
    else:
        return await call_next(request)
