# Trinity Score: 90.0 (Established by Chancellor)
"""
Chancellor Stream SSE (Server-Sent Events) Endpoint
Real-time log streaming for AFO Kingdom monitoring

Provides live log streaming via Redis Pub/Sub to SSE clients.
Implements 眞善美孝永 principles for reliable real-time communication.
"""

import asyncio
import json
import logging
from typing import Any

import redis
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

logger = logging.getLogger(__name__)
router = APIRouter()


async def publish_thought(content: dict | None = None, **kwargs) -> None:
    """
    Publish thought to Chancellor Stream via Redis.

    Args:
        content: Thought content dict with message, level, source, timestamp
        **kwargs: Additional thought parameters
    """
    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        redis_url = settings.REDIS_URL
        redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

        # Merge content dict with kwargs
        if content is None:
            content = {}
        if kwargs:
            content.update(kwargs)

        # Ensure timestamp is included
        if "timestamp" not in content:
            content["timestamp"] = asyncio.get_event_loop().time()

        # Publish to Redis channel
        redis_client.publish("kingdom:logs:stream", json.dumps(content))

        logger.debug(f"Published thought to Chancellor Stream: {content.get('message', '')[:100]}...")

    except Exception as e:
        logger.error(f"Failed to publish thought: {e}")
        # Don't raise exception - logging should not break business logic


# SSE event generator
async def log_stream_generator() -> Any:
    """Generate SSE events from Redis Pub/Sub messages."""
    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        redis_url = settings.REDIS_URL
        # Parse redis_url to pass to redis.Redis if needed, or use from_url
        redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        redis_client.ping()  # Test connection
    except Exception as e:
        logger.error(f"Redis connection failed for Chancellor Stream: {e}")
        yield 'data: {"error": "Redis unavailable", "level": "ERROR"}\n\n'
        return

    pubsub = redis_client.pubsub()
    pubsub.subscribe("kingdom:logs:stream")

    try:
        logger.info("Chancellor Stream SSE connection established")

        # Send initial connection message
        initial_msg = {
            "message": "[SSE CONNECTED] Chancellor Stream 실시간 모니터링 시작",
            "level": "SUCCESS",
            "source": "Chancellor Stream",
            "timestamp": asyncio.get_event_loop().time(),
        }
        yield f"data: {json.dumps(initial_msg)}\n\n"

        # Listen for messages
        while True:
            try:
                message = pubsub.get_message(timeout=1.0)
                if message and message["type"] == "message":
                    # Parse and forward Redis message
                    try:
                        data = json.loads(message["data"])
                        yield f"data: {json.dumps(data)}\n\n"
                    except json.JSONDecodeError:
                        # Handle non-JSON messages
                        yield f'data: {{"message": "{message["data"]}", "level": "INFO"}}\n\n'

                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting

            except Exception as e:
                logger.error(f"Chancellor Stream error: {e}")
                error_msg = {
                    "message": f"[STREAM ERROR] {e!s}",
                    "level": "ERROR",
                    "source": "Chancellor Stream",
                }
                yield f"data: {json.dumps(error_msg)}\n\n"
                await asyncio.sleep(1.0)

    except Exception as e:
        logger.error(f"Chancellor Stream generator failed: {e}")
    finally:
        pubsub.close()
        logger.info("Chancellor Stream SSE connection closed")


@router.get("/logs/stream")
async def logs_stream_endpoint(request: Request) -> StreamingResponse:
    """
    Chancellor Stream SSE endpoint.

    Provides real-time log streaming via Server-Sent Events.
    Connected clients receive live updates from Redis kingdom:logs:stream channel.

    Trinity Score: 美 (Beauty) - Clean, reliable real-time communication
    """
    logger.info(
        f"Chancellor Stream connection from {request.client.host if request.client else 'unknown'}"
    )

    return EventSourceResponse(
        log_stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Cache-Control",
        },
    )
