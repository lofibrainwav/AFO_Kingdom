# Trinity Score: 90.0 (Established by Chancellor)
"""
Streams Router (孝 - Serenity)
------------------------------
Server-Sent Events (SSE) router for real-time dashboard updates.
Reduces friction by providing visible system thought processes.
"""

import json
from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


@router.get("/mcp/thoughts")
async def stream_thoughts(request: Request) -> EventSourceResponse:
    """
    Stream real-time thoughts from the Chancellor (Matrix Style).
    Connection stays open to push updates instantly.
    """

    from afo.utils.redis_connection import get_shared_async_redis_client

    async def event_generator() -> AsyncGenerator[dict[str, str], None]:
        # Initial greeting
        yield {
            "event": "message",
            "data": json.dumps(
                {
                    "source": "System",
                    "message": "Neural Link Established... Waiting for Chancellor.",
                    "type": "info",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
            ),
        }

        try:
            redis = await get_shared_async_redis_client()
            pubsub = redis.pubsub()
            await pubsub.subscribe("chancellor_thought_stream")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    payload = message["data"]
                    # If payload is string (JSON), yield it.
                    # Frontend expects: {id, source, message, timestamp, type}
                    # Publisher sends: {source, message, type, timestamp}
                    # We just pass it through data.
                    yield {"event": "message", "data": payload}

        except Exception as e:
            yield {
                "event": "message",
                "data": json.dumps(
                    {
                        "source": "System",
                        "message": f"Stream Error: {e}",
                        "type": "error",
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    }
                ),
            }
            if "pubsub" in locals():
                await pubsub.unsubscribe("chancellor_thought_stream")

    return EventSourceResponse(event_generator())
