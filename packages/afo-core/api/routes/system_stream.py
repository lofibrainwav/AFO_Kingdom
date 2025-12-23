import asyncio
import json
from collections.abc import AsyncGenerator
from typing import Optional

from fastapi import APIRouter, Request
from redis.asyncio import Redis
from starlette.responses import StreamingResponse

router = APIRouter()


def _redis() -> Redis:
    # REDIS_URL 우선, 없으면 host/port로
    import os

    url = os.environ.get("REDIS_URL")
    if url:
        return Redis.from_url(url, decode_responses=True)
    host = os.environ.get("REDIS_HOST", "127.0.0.1")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    db = int(os.environ.get("REDIS_DB", "0"))
    password = os.environ.get("REDIS_PASSWORD")
    return Redis(host=host, port=port, db=db, password=password, decode_responses=True)


SSE_CHANNEL = "afo:verdicts"


def _sse(event: str | None, data: dict, _id: str | None = None) -> str:
    # SSE 표준: id / event / data
    lines = []
    if _id is not None:
        lines.append(f"id: {_id}")
    if event is not None:
        lines.append(f"event: {event}")
    lines.append(f"data: {json.dumps(data, separators=(',', ':'))}")
    return "\n".join(lines) + "\n\n"


@router.get("/logs/stream")
async def logs_stream(request: Request) -> StreamingResponse:
    r = _redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(SSE_CHANNEL)

    async def gen() -> AsyncGenerator[str, None]:
        # 최초 연결 알림(클라 디버그용)
        yield _sse("system_status", {"stream": "connected", "channel": SSE_CHANNEL})

        # keep-alive (프록시/로드밸런서 대비)
        ping_interval = 15.0
        next_ping = asyncio.get_event_loop().time() + ping_interval

        try:
            while True:
                if await request.is_disconnected():
                    break

                now = asyncio.get_event_loop().time()
                if now >= next_ping:
                    # SSE comment ping
                    yield ": ping\n\n"
                    next_ping = now + ping_interval

                msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if not msg:
                    continue

                # Redis pubsub payload는 string
                raw = msg.get("data")
                if not raw:
                    continue

                # payload는 이미 JSON이라고 가정 (VerdictLogger에서 publish)
                try:
                    payload = json.loads(raw)
                except Exception:
                    payload = {"type": "raw", "raw": raw}

                # event type 분기
                event_type = payload.get("type", "verdict")
                event_id = payload.get("id")  # optional
                yield _sse(event_type, payload, _id=str(event_id) if event_id is not None else None)
        finally:
            try:
                await pubsub.unsubscribe(SSE_CHANNEL)
            except Exception:
                pass
            try:
                await r.close()
            except Exception:
                pass

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # nginx buffering 방지
        },
    )
