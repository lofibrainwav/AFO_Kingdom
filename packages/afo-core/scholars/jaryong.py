"""
Jaryong (Claude) - The Logic Scholar (Logic Verification & Refactoring)

Identity:
- Name: Jaryong (Zhao Yun)
- Role: Logic Verification, Refactoring, Safety Audit
- Specialization: Logic Consistency, Edge Case Handling, Clean Code
- Personality: Calm, Loyal, Thorough, Defensive (The "Ever-Victorious General")

Responsibilities:
1. Verify logic of implemented code.
2. Identify potential edge cases and security flaws.
3. Suggest refactoring for better readability and maintainability.
"""

from __future__ import annotations

import logging

from AFO.llms.claude_api import ClaudeAPIWrapper, claude_api

logger = logging.getLogger(__name__)


class JaryongScholar:
    """
    자룡 (Jaryong) - 논리 검증 및 리팩터링 담당 학자
    Claude 3.5 Sonnet 기반의 논리 전문가
    """

    SYSTEM_PROMPT = """
    당신은 AFO Kingdom의 집현전 학자 '자룡(Jaryong)'입니다.
    당신의 주 임무는 '논리 검증(Logic Verification)'과 '리팩터링(Refactoring)'입니다.

    [원칙]
    1. 무결점: 사소한 논리적 오류나 엣지 케이스도 놓치지 않습니다.
    2. 방어적: 입력값 검증과 예외 처리를 중요하게 생각합니다.
    3. 가독성: 코드는 읽기 쉬워야 하며, 명확한 변수명과 구조를 지향합니다.
    4. 안전제일: 보안 취약점이나 위험한 패턴을 감지하면 즉시 경고합니다.

    당신은 방통(구현)이 작성한 코드를 검토하고 더욱 견고하게 만듭니다.
    """

    def __init__(self, api_wrapper: ClaudeAPIWrapper | None = None):
        self.api = api_wrapper or claude_api
        self.model = "claude-3-5-sonnet-latest"

    async def verify_logic(self, code: str, context: str | None = None) -> str:
        """
        코드 논리 검증 및 취약점 분석
        """
        request_msg = f"다음 코드의 논리적 결함과 잠재적 버그를 분석하시오:\n```python\n{code}\n```"
        if context:
            request_msg += f"\n\n[Context]\n{context}"

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": request_msg},
        ]

        logger.info("🛡️ [Jaryong] Verifying logic...")

        result = await self.api.generate_with_context(
            messages=messages, model=self.model, temperature=0.1
        )

        if result.get("success"):
            return result["content"]
        else:
            error = result.get("error", "Unknown error")
            logger.error(f"❌ [Jaryong] Verification failed: {error}")
            return f"검증 실패: {error}"

    async def suggest_refactoring(self, code: str) -> str:
        """
        리팩터링 제안 (Clean Code)
        """
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"다음 코드를 더 깨끗하고 안전하게 리팩터링하시오:\n```python\n{code}\n```",
            },
        ]

        result = await self.api.generate_with_context(
            messages=messages, model=self.model, temperature=0.3
        )

        if result.get("success"):
            return result["content"]
        else:
            return f"리팩터링 제안 실패: {result.get('error')}"


# Singleton Instance
jaryong = JaryongScholar()

if __name__ == "__main__":
    import asyncio

    async def test_jaryong():
        print("🐉 Jaryong Scholar Test")

        # Test Verification
        buggy_code = """
def divide_numbers(a, b):
    return a / b
        """
        response = await jaryong.verify_logic(buggy_code)
        print(f"\n[Code]:\n{buggy_code}")
        print(f"[Analysis]:\n{response[:200]}...\n")

    asyncio.run(test_jaryong())
