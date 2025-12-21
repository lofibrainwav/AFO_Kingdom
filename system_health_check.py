import asyncio
import os

from AFO.scholars.yeongdeok import yeongdeok


async def check_system_health():

    # 1. Env Check
    os.getenv("OLLAMA_NUM_PARALLEL", "Not Set")

    # 2. Sage Connectivity (Refactored Logic Test)
    try:
        # Samahwi (Ollama)
        await yeongdeok.consult_samahwi("Ping")

        # Jwaja (MLX)
        await yeongdeok.consult_jwaja("Ping")

    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(check_system_health())
