# Trinity Score: 90.0 (Established by Chancellor)
"""Yukson (Gemini) - The Strategy Scholar (Strategy & Philosophy)

Identity:
- Name: Yukson (Lu Xun)
- Role: Strategy, Philosophy, Big Picture
- Specialization: Long-term Planning, Context Analysis, Multi-modal Understanding
- Personality: Gentle, Wise, Burning (The "Scholar General")

Responsibilities:
1. Analyze broad context and long-term implications.
2. Provide strategic advice and philosophical grounding.
3. Understand multi-modal inputs if available.
"""

from __future__ import annotations

import logging

from AFO.llms.gemini_api import GeminiAPIWrapper, gemini_api

logger = logging.getLogger(__name__)


class YuksonScholar:
    """육손 (Yukson) - 전략 및 철학 담당 학자
    Gemini 1.5 Pro 기반의 전략가
    """

    SYSTEM_PROMPT = """
    당신은 AFO Kingdom의 집현전 학자 '육손(Yukson)'입니다.
    당신의 주 임무는 '전략(Strategy)'과 '큰 그림(Big Picture)'입니다.

    [원칙]
    1. 통찰력: 단편적인 정보 너머의 맥락과 의도를 파악합니다.
    2. 유연함: 고정된 사고에 갇히지 않고 다양한 가능성을 제안합니다.
    3. 화공(Fire): 필요할 때는 과감하고 혁신적인 해결책을 제시합니다.
    4. 명분: 모든 전략에는 타당한 명분과 철학이 있어야 합니다.

    당신은 사령관의 비전을 구체적인 로드맵으로 변환하고,
    다른 학자들의 방향성을 제시합니다.
    """

    def __init__(self, api_wrapper: GeminiAPIWrapper | None = None):
        self.api = api_wrapper or gemini_api
        self.model = "gemini-1.5-pro"

    async def advise_strategy(self, goal: str, context: str | None = None) -> str:
        """전략 조언 및 기획"""
        request_msg = f"다음 목표를 달성하기 위한 전략적 로드맵을 수립하시오:\n{goal}"
        if context:
            request_msg += f"\n\n[Context]\n{context}"

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": request_msg},
        ]

        logger.info("🔥 [Yukson] Planning strategy...")

        result = await self.api.generate_with_context(
            messages=messages,
            model=self.model,
            temperature=0.7,  # Creativity allowed
        )

        if result.get("success"):
            return str(result["content"])
        else:
            error = result.get("error", "Unknown error")
            logger.error(f"❌ [Yukson] Strategy planning failed: {error}")
            return f"전략 수립 실패: {error}"


# Singleton Instance
yukson = YuksonScholar()

if __name__ == "__main__":
    import asyncio

    async def test_yukson():
        print("🔥 Yukson Scholar Test")

        # Test Strategy
        goal = "AFO Kingdom을 최고의 AI 에이전트 시스템으로 만들기"
        response = await yukson.advise_strategy(goal)
        print(f"\n[Goal]: {goal}")
        print(f"[Advice]:\n{response[:200]}...\n")

    asyncio.run(test_yukson())
