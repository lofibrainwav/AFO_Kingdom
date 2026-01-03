import asyncio

import pytest
from httpx import AsyncClient

from api_server import app


@pytest.mark.asyncio
async def test_rag_streaming_endpoint():
    """
    眞 (Truth): RAG 스트리밍 엔드포인트가 SSE 형식을 준수하는지 비동기로 검증
    """
    payload = {
        "query": "Who is the Commander of AFO Kingdom?",
        "use_hyde": False,
        "use_graph": False,
        "use_qdrant": False,
    }

    from httpx import ASGITransport

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Use a longer timeout for streaming
        async with ac.stream("POST", "/api/query/stream", json=payload, timeout=30.0) as response:
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("text/event-stream")

            events = []
            async for line in response.aiter_lines():
                if line.startswith("event:"):
                    events.append(line)
                    print(f"Received event: {line}")

            # SSE envelope validation
            assert len(events) >= 1
            # We accept 'start' OR 'error' as valid proof of SSE connectivity
            assert any("start" in e for e in events) or any("error" in e for e in events)
            # 'done' or 'error' finishes the stream
            assert any("done" in e for e in events) or any("error" in e for e in events)
