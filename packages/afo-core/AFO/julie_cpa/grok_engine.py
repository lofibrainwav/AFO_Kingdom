# mypy: ignore-errors
"""
Julie CPA Grok Analysis Engine - The Sage from the Stars
Phase 15: Real-time External Intelligence via xAI

Philosophy:
- 智 (Wisdom): 외부 세계의 변화를 인지하고 해석
- 眞 (Truth): 할루시네이션을 최소화한 정성적 분석
- 善 (Goodness): 예측이 빗나갈 수 있음을 겸허히 인정하고 대안 제시

Usage:
    from AFO.julie_cpa.grok_engine import consult_grok
    analysis = await consult_grok(current_budget_data)
"""

import hashlib
import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# xAI API Support
try:
    from openai import AsyncOpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Playwright Support for Web Mode
try:
    from playwright.async_api import async_playwright

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Redis Support
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Configuration
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_BASE_URL = "https://api.x.ai/v1"
GROK_MODEL_BETA = "grok-beta"
GROK_MODEL_FAST = "grok-beta"  # Currently generic, will use specific if available
SESSION_FILE = "secrets/grok_session.json"
SESSION_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "../../", SESSION_FILE
)

# Redis Configuration (Cost Guardian)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL = 3600  # 1 Hour

# Trinity Config
TRINITY_THRESHOLD = 90


def _get_redis_client():
    if not REDIS_AVAILABLE:
        return None
    try:
        return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    except Exception as e:
        logger.warning(f"[GrokEngine] Redis connection failed: {e}")
        return None


async def consult_grok(
    budget_summary: dict[str, Any],
    market_context: str = "general",
    trinity_score: int = 85,  # Default score
) -> dict[str, Any]:
    """
    Grok에게 왕국의 재정 상태에 대한 거시경제적 조언을 구합니다.
    Smart Routing (Cost Guardian) 적용:
    - Cached Response 확인
    - Trinity Score < 90 -> Mock/Ollama (Cost Saving)
    - Trinity Score >= 90 -> Web Session or API (Real Intelligence)
    """

    # 0. Check Cache (Cost Guardian)
    cache_key = _generate_cache_key(budget_summary)
    cached_response = _get_from_cache(cache_key)
    if cached_response:
        logger.info("[GrokEngine] 🛡️ Cache Hit! Saving costs.")
        cached_response["source"] = "Grok (Cached)"
        cached_response["cost_saved"] = True
        return cached_response

    # 1. Smart Routing based on Trinity Score
    use_real_grok = trinity_score >= TRINITY_THRESHOLD
    model_used = GROK_MODEL_FAST if use_real_grok else "mock-ollama"

    if not use_real_grok:
        logger.info(
            f"[GrokEngine] 🛡️ Trinity Score ({trinity_score}) low. Using Mock/Ollama fallback."
        )
        return _mock_grok_analysis(budget_summary, mood="ECONOMY_MODE")

    response = None

    # 2. Check for Web Session (User Preference)
    if os.path.exists(SESSION_PATH) and PLAYWRIGHT_AVAILABLE:
        logger.info("[GrokEngine] Web Session found. Using Browser Bridge Mode.")
        response = await _consult_grok_web(budget_summary)

    # 3. Check for API Key
    elif XAI_API_KEY and OPENAI_AVAILABLE:
        logger.info("[GrokEngine] API Key found. Using Official API Mode.")
        response = await _consult_grok_api(budget_summary)

    # 4. Fallback
    else:
        logger.warning("[GrokEngine] No auth found. Using Mock Mode.")
        response = _mock_grok_analysis(budget_summary)

    # 5. Save to Cache
    if response:
        response["model_used"] = model_used
        _save_to_cache(cache_key, response)

    return response


def _generate_cache_key(data: dict[str, Any]) -> str:
    """Generate a unique hash for the budget data to use as cache key."""
    data_str = json.dumps(data, sort_keys=True)
    return f"grok_analysis:{hashlib.md5(data_str.encode()).hexdigest()}"


def _get_from_cache(key: str) -> dict[str, Any] | None:
    r = _get_redis_client()
    if not r:
        return None
    try:
        data = r.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None


def _save_to_cache(key: str, data: dict[str, Any]):
    r = _get_redis_client()
    if not r:
        return
    try:
        r.setex(key, CACHE_TTL, json.dumps(data))
    except Exception as e:
        logger.warning(f"[GrokEngine] Failed to cache: {e}")


async def _consult_grok_web(budget_summary: dict[str, Any]) -> dict[str, Any]:
    """
    Uses Playwright to interact with Grok Web Interface using saved session.
    """
    try:
        async with async_playwright() as p:
            # 1. Setup Browser
            # Note: We assume chromium is installed.
            browser = await p.chromium.launch(headless=True)  # Headless mode
            context = await browser.new_context()

            # 2. Load Cookies
            with open(SESSION_PATH) as f:
                cookies_dict = json.load(f)
                # Playwright expects list of cookie objects
                cookies_list = []
                for k, v in cookies_dict.items():
                    cookies_list.append({"name": k, "value": v, "domain": ".x.com", "path": "/"})
                await context.add_cookies(cookies_list)

            page = await context.new_page()

            # 3. Navigate & Verify
            await page.goto("https://x.com/i/grok")

            try:
                # Check for input box or drawer to verify login
                # Timeout 30s
                await page.wait_for_selector('[data-testid="GrokDrawer"]', timeout=30000)
                logger.info("[GrokEngine] Web Login Verified!")

                # Mocking the actual chat for MVP stability
                return _mock_grok_analysis(budget_summary, error_msg=None, mood="WEB_AUTHENTICATED")

            except Exception as e:
                logger.error(f"[GrokEngine] Web Login Verification Failed: {e}")
                return _mock_grok_analysis(budget_summary, error_msg=f"Web Auth Failed: {e}")
            finally:
                await browser.close()

    except Exception as e:
        logger.error(f"[GrokEngine] Web Bridge Error: {e}")
        return _mock_grok_analysis(budget_summary, error_msg=str(e))


async def _consult_grok_api(budget_summary: dict[str, Any]) -> dict[str, Any]:
    # (Original API Logic with Smart Model Selection would go here)
    system_prompt = (
        "You are 'The Sage from the Stars', a cynical but brilliant economic strategist..."
    )
    user_prompt = f"Analyze budget: {json.dumps(budget_summary)}"

    # Use grok-beta (or fast if available in future SDK)
    model = GROK_MODEL_FAST

    client = AsyncOpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def _mock_grok_analysis(
    budget_summary: dict[str, Any], error_msg: str | None = None, mood: str = "MOCK"
) -> dict[str, Any]:
    """
    Simulates Grok's analysis result.
    """
    total_forecast = budget_summary.get("summary", {}).get("total", 0)

    advice = "Grok is currently reviewing galaxy charts. "

    if mood == "WEB_AUTHENTICATED":
        advice = "🚀 [WEB MODE] Authentication successful! I see your universe clearly. (Actual inference skipped in MVP)"
        score = 90
    elif mood == "ECONOMY_MODE":
        advice = "💰 [COST GUARDIAN] Using standard logic to save API costs. Improve Trinity Score to unlock full Grok."
        score = 80
    else:
        if error_msg:
            advice += f"(Connection Error: {error_msg})"
        else:
            advice += "Using cached interstellar wisdom."
        score = 75

    return {
        "is_mock": True,
        "sentiment": "bullish" if total_forecast > 500000 else "bearish",
        "score": score,
        "analysis": f"[{mood}] forecast of ${total_forecast:,} requires bold action. The stars suggest optimizing operational expenses.",
        "action_items": [
            "Review global subscription dependencies",
            "Invest in automated efficiency (Phase 16)",
            "Maintain High Serenity (孝)",
        ],
        "message": advice,
        "model_used": "mock-ollama" if mood == "ECONOMY_MODE" else "grok-beta",
    }
