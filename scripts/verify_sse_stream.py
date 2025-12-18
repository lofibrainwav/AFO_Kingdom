# scripts/verify_sse_stream.py
"""
SSE Stream Verification for Trinity Score real-time updates.
Tests connection to /api/trinity/stream endpoint.
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

async def test_sse_stream():
    """Test SSE streaming endpoint."""
    print("=== SSE Stream Verification ===")
    
    try:
        import httpx
    except ImportError:
        print("❌ httpx not installed. Run: pip install httpx")
        return False
    
    # Backend URL
    api_url = os.getenv("API_URL", "http://localhost:8010")
    stream_endpoint = f"{api_url}/api/trinity/stream"
    
    print(f"[Action] Connecting to {stream_endpoint}...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test if endpoint exists
            async with client.stream("GET", stream_endpoint) as response:
                if response.status_code != 200:
                    print(f"❌ Endpoint returned {response.status_code}")
                    print("   SSE endpoint may not be implemented yet.")
                    return False
                
                # Read first few events
                event_count = 0
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        event_count += 1
                        print(f"  ✅ Event {event_count}: {line[:50]}...")
                        if event_count >= 3:
                            break
                
                if event_count > 0:
                    print(f"\n✅ SSE Stream Active: {event_count} events received")
                    return True
                else:
                    print("⚠️ No events received (stream may be idle)")
                    return True  # Endpoint exists but no events
                    
    except httpx.ConnectError:
        print("❌ Cannot connect to API server")
        print(f"   Is the server running at {api_url}?")
        return False
    except Exception as e:
        print(f"⚠️ SSE test incomplete: {e}")
        print("   (Server may not support SSE streaming yet)")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_sse_stream())
    print("\n" + ("✅ PASS" if result else "⚠️ SSE requires implementation"))
