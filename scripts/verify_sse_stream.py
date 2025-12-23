import asyncio
import json

import aiohttp

STREAM_URL = "http://localhost:8010/api/stream/mcp/thoughts"


async def verify_sse():
    print(f"🔌 Connecting to Neural Stream: {STREAM_URL}")
    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(STREAM_URL) as response,
        ):
            print(f"   Status: {response.status}")
            if response.status != 200:
                print("❌ Connection failed")
                return

            print("✅ Connected! Listening for events...")

            # Consume line by line
            async for line in response.content:
                decoded = line.decode("utf-8").strip()
                if not decoded:
                    continue

                if decoded.startswith("data: "):
                    data_str = decoded[6:]
                    try:
                        # It might be double encoded based on my implementation
                        # Payload: json.dumps({...})
                        # Stream sends: data: "{\"source\": ...}"
                        # Let's see
                        payload = json.loads(data_str)
                        print(f"📩 Event Received: {payload}")
                        # Close after first hello message or shortly after
                        if payload.get(
                            "source"
                        ) == "System" and "Neural Link" in payload.get("message", ""):
                            print("✅ Handshake confirmed. Stream is ALIVE.")
                            break
                    except Exception as e:
                        print(f"⚠️ Parse Error: {e} | Raw: {data_str}")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")
        print("💡 Hint: Ensure 'api_server.py' is running on port 8010.")


if __name__ == "__main__":
    asyncio.run(verify_sse())
