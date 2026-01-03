import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from api_server import app


def test_debug_routes():
    """디버깅: 등록된 라우터 확인"""
    routes = []
    for route in app.routes:
        if hasattr(route, "path"):
            routes.append(route.path)
    print(f"Registered routes: {routes}")
    assert "/api/query/stream" in routes


@pytest.mark.asyncio
async def test_rag_streaming_endpoint():
    """
    眞 (Truth): RAG 스트리밍 엔드포인트가 SSE 형식을 준수하고 실제 토큰을 반환하는지 검증
    善 (Goodness): 에러 이벤트만 오는 경우는 실패로 간주 (T2.1 UX 목표달성 검증)
    """
    payload = {
        "query": "Who is the Commander of AFO Kingdom?",
        "use_hyde": False,
        "use_graph": False,
        "use_qdrant": False,
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Use a longer timeout for LLM generation
        async with ac.stream("POST", "/api/query/stream", json=payload, timeout=60.0) as response:
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("text/event-stream")

            events = []
            async for line in response.aiter_lines():
                if line.strip():
                    events.append(line)
                    print(f"Received: {line}")

            # SSE envelope validation (Strict T2.1 Rule)
            # events should contain "event: start", "data: ...", "event: token", etc.

            # Check for specific event types
            has_start = any("event: start" in e for e in events)
            has_token = any("event: token" in e for e in events)
            has_done = any("event: done" in e for e in events)
            has_error = any("event: error" in e for e in events)

            assert has_start, "❌ 'start' 이벤트가 누락되었습니다."
            assert has_token, "❌ 'token' 이벤트가 누락되었습니다. (실제 스트리밍 실패)"
            assert has_done, "❌ 'done' 이벤트가 누락되었습니다."
            assert not has_error, (
                f"❌ 스트림 중 에러가 발생하였습니다: {[e for e in events if 'error' in e]}"
            )

            print("✅ T2.1 RAG Streaming Verification Success (Tokens Received)")
