import json
import os

import requests


def verify_active_rag():
    url = "http://localhost:8010/api/chat/message"

    # Complex query requiring System 2 thinking
    payload = {
        "message": "What is the current Trinity Score philosophy and formula?",
        "provider": "openai",  # Force high quality
        "quality_tier": "premium",
        "system_prompt": "You are the AFO Chancellor.",
    }

    try:
        print(f"🚀 Sending Active RAG request to {url}...")
        response = requests.post(url, json=payload)
        response.raise_for_status()

        data = response.json()

        print("\n✅ Response Received:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Validation
        if data["success"] is True and "routing" in data:
            routing = data["routing"]
            if routing.get("agent") == "RagActiveAgent":
                print("\n🎉 VERIFIED: RagActiveAgent handled the request.")
                print(f"🧠 Thought Process: {routing.get('thought_process')[:100]}...")
                return

        print("\n⚠️  WARNING: Response format did not match Active RAG signature.")

    except Exception as e:
        print(f"\n❌ REQUEST FAILED: {e}")
        # If server is down, we might need to rely on static analysis or manual check
        # But for 'verify', we assume server is running or we can't verify 'active' behavior.


if __name__ == "__main__":
    verify_active_rag()
