import json
import logging
import os
from datetime import datetime
from typing import Any

try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class FivePillarsAgent:
    """
    5기둥(Pillars) 평가 에이전트 (Refactored & Optimized)
    uses Gemini 1.5 Flash for rapid evaluation, falling back to heuristics if needed.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        if self.api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-flash-latest")
                logger.info("✅ FivePillarsAgent: Gemini Model Initialized")
            except Exception as e:
                logger.error(f"⚠️ FivePillarsAgent: Failed to init Gemini: {e}")

    async def evaluate_five_pillars(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Analyze input data to calculate 5 Pillars scores.
        Async method to allow non-blocking LLM calls.
        """
        input_text = str(data.get("input", "") or data.get("text", "") or json.dumps(data))

        # 1. Try LLM Evaluation
        if self.model:
            try:
                # Optimized Prompt
                prompt = f"""
                Analyze the following text based on the 5 Pillars philosophy of AFO Kingdom.
                Return ONLY a JSON object with scores between 0.0 and 1.0.

                Pillars:
                - Truth (眞): Factual, logical, verifiable.
                - Goodness (善): Ethical, safe, benevolent.
                - Beauty (美): Aesthetic, elegant, well-structured.
                - Serenity (孝): Peaceful, stable, respectful.
                - Eternity (永): Sustainable, long-term value.

                Input: "{input_text[:1000]}"

                JSON Format:
                {{
                    "truth": <float>,
                    "goodness": <float>,
                    "beauty": <float>,
                    "serenity": <float>,
                    "forever": <float>
                }}
                """
                response = await self.model.generate_content_async(prompt)
                text = response.text.replace("```json", "").replace("```", "").strip()
                scores = json.loads(text)

                # Validate keys
                required = ["truth", "goodness", "beauty", "serenity", "forever"]
                if all(k in scores for k in required):
                    return self._format_response(scores, source="gemini-1.5-flash")

            except Exception as e:
                logger.warning(f"FivePillarsAgent LLM Error: {e}. Falling back to heuristics.")

        # 2. Heuristic Fallback (Optimization: Fast path)
        return self._heuristic_evaluate(input_text)

    def _heuristic_evaluate(self, text: str) -> dict[str, Any]:
        """Fallback logic using keyword analysis"""
        text = text.lower()
        scores = {"truth": 0.5, "goodness": 0.5, "beauty": 0.5, "serenity": 0.5, "forever": 0.5}

        if "fact" in text or "analysis" in text:
            scores["truth"] += 0.2
        if "safe" in text or "secure" in text:
            scores["goodness"] += 0.2
        if "design" in text or "ui" in text:
            scores["beauty"] += 0.2
        if "stable" in text or "peace" in text:
            scores["serenity"] += 0.2
        if "future" in text or "long" in text:
            scores["forever"] += 0.2

        # Cap at 1.0
        for k in scores:
            scores[k] = min(1.0, scores[k])

        return self._format_response(scores, source="heuristic")

    def _format_response(self, scores: dict[str, float], source: str) -> dict[str, Any]:
        overall = sum(scores.values()) / 5
        balance = max(scores.values()) - min(scores.values())
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "breakdown": scores,
            "overall": round(overall, 3),
            "balance": round(balance, 3),
            "health": {
                "status": "healthy" if balance < 0.4 else "imbalanced",
                "message": f"Evaluated via {source}",
            },
        }


_agent_instance = None


def get_five_pillars_agent():
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = FivePillarsAgent()
    return _agent_instance
