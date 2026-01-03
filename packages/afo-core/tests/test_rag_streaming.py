"""
Test RAG Streaming API Endpoints (Ticket-075 Phase 3)

Tests for /api/query/stream endpoint and related streaming functionality.
"""
from fastapi.testclient import TestClient
from AFO.api_server import app


def test_debug_routes():
    """Test that /api/query/stream route is registered."""
    client = TestClient(app)

    # Get all registered routes
    routes = [route.path for route in app.routes if hasattr(route, "path")]
    print(f"Registered routes: {routes}")

    # Check that the streaming route is registered
    assert "/api/query/stream" in routes, f"/api/query/stream not found in routes: {routes}"


def test_stream_endpoint_basic():
    """Test basic streaming endpoint functionality."""
    client = TestClient(app)

    # Test the endpoint exists and returns proper response
    response = client.get("/api/query/stream")
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")

    # Check for SSE format in response
    content = response.text
    assert "event: ping" in content
    assert "data: ok" in content
