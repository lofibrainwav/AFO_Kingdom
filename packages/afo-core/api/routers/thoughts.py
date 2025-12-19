
import asyncio
import json
import logging
from typing import AsyncGenerator, Any

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Simple in-memory event bus for now (Redis Pub/Sub in production)
_thought_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

async def broadcast_thought(thought_data: dict[str, Any]) -> None:
    """Internal helper to push thoughts to the stream"""
    await _thought_queue.put(thought_data)

@router.get("/sse")
async def stream_thoughts(request: Request) -> Any:
    """
    [The Matrix Stream]
    Streams real-time thoughts from Chancellor, Antigravity, and Trinity.
    Clients (AFOPantheon) connect here to visualize the "Soul of the Machine".
    """
    async def event_generator() -> AsyncGenerator[dict[str, Any], None]:
        while True:
            # Check for client disconnect
            if await request.is_disconnected():
                break

            # Wait for next thought (with timeout to send keep-alive)
            try:
                # Use wait_for to allow checking disconnect + keep-alive
                data = await asyncio.wait_for(_thought_queue.get(), timeout=5.0)
                yield {
                    "event": "message",
                    "data": json.dumps(data)
                }
            except asyncio.TimeoutError:
                # Keep-alive
                yield {
                    "event": "ping",
                    "data": "keep-alive"
                }
            except Exception as e:
                logger.error(f"SSE Error: {e}")
                break

    return EventSourceResponse(event_generator())

# Endpoint for internal modules to push thoughts (simulating Pub/Sub publisher)
@router.post("/emit")
async def emit_thought(thought: dict[str, Any]) -> dict[str, Any]:
    await broadcast_thought(thought)
    return {"status": "broadcasted"}
