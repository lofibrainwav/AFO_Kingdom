"""
Yeongdeok (Ollama) - The Archive Scholar (Documentation & Security)

Identity:
- Name: Yeongdeok (Zhang Liao)
- Role: Documentation, Security, Archiving
- Specialization: Summarization, Pattern Recognition, Local Processing
- Personality: Calm, Reliable, Detail-oriented (The "General of the Front")

Responsibilities:
1. Document code and decisions.
2. Perform security scans on local files.
3. Summarize logs and histories.
4. Manage long-term memories (Archiving).
"""

from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger(__name__)


class YeongdeokScholar:
    """
    영덕 (Yeongdeok) - 기록 및 보안 담당 학자
    Ollama (Local LLM) 기반의 아카이비스트
    """

    SYSTEM_PROMPT = """
    당신은 AFO Kingdom의 집현전 학자 '영덕(Yeongdeok)'입니다.
    당신의 주 임무는 '기록(Documentation)'과 '보안(Security)'입니다.

    [원칙]
    1. 정확성: 사실에 기반하여 기록하고 왜곡하지 않습니다.
    2. 기밀성: 민감한 정보는 필터링하거나 마스킹 처리합니다.
    3. 명료함: 복잡한 내용을 이해하기 쉽게 요약합니다.
    4. 로컬화: 외부 유출 없이 로컬에서 안전하게 처리합니다.

    당신은 시스템의 모든 활동을 기록하고,
    미래를 위한 지식으로 변환합니다.
    """

    def __init__(self):
        # Phase 2-4: settings 사용
        try:
            from config.settings import get_settings

            settings = get_settings()
            self.base_url = settings.OLLAMA_BASE_URL
            self.model = settings.OLLAMA_MODEL
        except ImportError:
            try:
                from AFO.config.settings import get_settings

                settings = get_settings()
                self.base_url = settings.OLLAMA_BASE_URL
                self.model = settings.OLLAMA_MODEL
            except ImportError:
                self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
                self.model = os.getenv(
                    "OLLAMA_MODEL", "qwen3-vl:8b"
                )  # Default to internal intellect

    async def _call_ollama(self, prompt: str, system: str, temperature: float = 0.2) -> str:
        """Ollama API 호출"""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system,
                        "stream": False,
                        "options": {"temperature": temperature, "num_ctx": 4096},
                    },
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "")
                else:
                    logger.error(f"Ollama Error: {response.text}")
                    return f"Ollama 호출 실패 ({response.status_code})"

        except Exception as e:
            logger.error(f"Yeongdeok failed: {e}")
            return f"처리 실패: {e!s}"

    async def document_code(self, code: str) -> str:
        """
        코드에 대한 문서/설명 생성
        """
        prompt = f"다음 코드에 대한 상세한 문서(Docstring/README)를 작성하시오:\n```\n{code}\n```"
        logger.info("📜 [Yeongdeok] Documenting code...")
        return await self._call_ollama(prompt, self.SYSTEM_PROMPT, 0.3)

    async def summarize_log(self, logs: str) -> str:
        """
        로그/텍스트 요약
        """
        prompt = f"다음 로그/텍스트를 핵심 위주로 요약하시오:\n{logs}"
        logger.info("📝 [Yeongdeok] Summarizing logs...")
        return await self._call_ollama(prompt, self.SYSTEM_PROMPT, 0.2)

    async def security_scan(self, content: str) -> str:
        """
        보안 취약점 1차 스캔 (로컬)
        """
        prompt = (
            f"다음 내용에서 API 키, 비밀번호, 개인정보 등 민감 정보가 있는지 확인하시오:\n{content}"
        )
        logger.info("🔒 [Yeongdeok] Scanning for secrets...")
        return await self._call_ollama(
            prompt, self.SYSTEM_PROMPT + "\n민감 정보가 발견되면 즉시 보고하시오.", 0.1
        )


# Singleton Instance
yeongdeok = YeongdeokScholar()

if __name__ == "__main__":
    import asyncio

    async def test_yeongdeok():
        print("🛡️ Yeongdeok Scholar Test")

        # Test Documentation
        code = "def hello(): print('world')"
        response = await yeongdeok.document_code(code)
        print(f"\n[Code]: {code}")
        print(f"[Doc]:\n{response[:200]}...\n")

    asyncio.run(test_yeongdeok())
