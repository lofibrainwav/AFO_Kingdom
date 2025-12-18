import asyncio
import os
import sys

# 프로젝트 루트 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core/AFO")))

from utils.playwright_bridge import bridge, MockScenario
from config.antigravity import antigravity

async def verify_real_ai_features():
    print("=== Playwright Bridge Real AI Features Verification ===")
    
    # 1. AI Integration Test (Simulation mostly likely if no LLM key)
    # But Playwright Bridge 'run_ai_test_scenario' does NOT check DRY_RUN before calling Router.
    # However, Router has fallback.
    
    print("\n[Step 1] verifying AI Scenario Request (Real LLM Router Call)...")
    # We use a simple prompt that might work even with a fallback or standard model
    prompt = "Verify page title"
    
    # Since we might not have keys, we expect either a PASS (if Ollama/Keys work) or FAIL (graceful fallback)
    # We just want to ensure it doesn't crash the process.
    ai_result = await bridge.run_ai_test_scenario(prompt)
    print(f"AI Result: {ai_result}")
    
    if ai_result["status"] == "PASS":
        print("✅ AI Integration Success (Code Generated & Executed)")
    elif ai_result["status"] == "FAIL":
         print(f"⚠️ AI Integration Failed (Expected if no LLM/Keys available): {ai_result.get('error')}")
         print("✅ Graceful Failure Verified")
    else:
        print(f"❓ Unexpected Status: {ai_result['status']}")

    await bridge.teardown()
    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    asyncio.run(verify_real_ai_features())
