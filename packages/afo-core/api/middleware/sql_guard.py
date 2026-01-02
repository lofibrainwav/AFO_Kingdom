# Trinity Score: 90.0 (Established by Chancellor)
from __future__ import annotations

import json
import os
import re
from typing import TYPE_CHECKING, Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

if TYPE_CHECKING:
    from collections.abc import Iterable

    from starlette.requests import Request

_PATTERNS: Iterable[re.Pattern[str]] = (
    re.compile(r"(?i)\bunion\b\s+\bselect\b"),
    re.compile(r"(?i)\bor\b\s+1\s*=\s*1\b"),
    re.compile(r"(?i)\bdrop\b\s+\btable\b"),
    re.compile(r"(?i)\binsert\b\s+\binto\b"),
    re.compile(r"--"),
    re.compile(r"/\*"),
    re.compile(r";\s*$"),
)


def _mode() -> str:
    return os.getenv("AFO_SQL_GUARD_MODE", "log").lower()


def _is_suspicious_text(s: str) -> bool:
    if len(s) > 2000:
        return False
    return any(p.search(s) for p in _PATTERNS)


def _walk_strings(x: Any) -> Iterable[str]:
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            if isinstance(k, str):
                yield k
            yield from _walk_strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _walk_strings(v)


class SqlGuardMiddleware:
    def __init__(self, app: Any):
        self.app = app

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        from starlette.requests import Request

        request = Request(scope, receive)
        mode = _mode()

        if mode == "off":
            await self.app(scope, receive, send)
            return

        suspicious = False
        for k, v in request.query_params.items():
            if _is_suspicious_text(k) or _is_suspicious_text(v):
                suspicious = True
                break

        if not suspicious and request.headers.get("content-type", "").startswith(
            "application/json"
        ):
            # We must be careful about reading the body in ASGI middleware
            # Starlette's Request.body() reads it into memory.
            # To pass it on, we need a custom receive function.
            try:
                raw = await request.body()
                if raw and len(raw) <= 65536:
                    data = json.loads(raw.decode("utf-8"))
                    for s in _walk_strings(data):
                        if _is_suspicious_text(s):
                            suspicious = True
                            break

                async def mocked_receive() -> dict:
                    return {"type": "http.request", "body": raw, "more_body": False}

                if suspicious and mode == "block":
                    response = JSONResponse(
                        {"ok": False, "error": "suspicious_input"}, status_code=400
                    )
                    await response(scope, receive, send)
                    return

                # Continue with the mocked receive channel
                await self.app(scope, mocked_receive, send)
                return
            except Exception:
                pass

        if suspicious and mode == "block":
            response = JSONResponse({"ok": False, "error": "suspicious_input"}, status_code=400)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
