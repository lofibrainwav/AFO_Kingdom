import asyncio
import os
from AFO.scholars.yeongdeok import yeongdeok

async def check_system_health():
    print("🏥 AFO Kingdom System Health Check (Post-Restart)")
    print("-" * 50)

    # 1. Env Check
    num_parallel = os.getenv("OLLAMA_NUM_PARALLEL", "Not Set")
    print(f"✅ OLLAMA_NUM_PARALLEL: {num_parallel} (Target: 2)")

    # 2. Sage Connectivity (Refactored Logic Test)
    print("\n🔮 Testing Sage Connectivity...")
    try:
        # Samahwi (Ollama)
        res_samahwi = await yeongdeok.consult_samahwi("Ping")
        print(f"✅ Samahwi (Backend): Alive ({len(res_samahwi)} chars)")

        # Jwaja (MLX)
        res_jwaja = await yeongdeok.consult_jwaja("Ping")
        print(f"✅ Jwaja (Frontend): Alive ({len(res_jwaja)} chars)")

    except Exception as e:
        print(f"❌ Sage Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_system_health())
