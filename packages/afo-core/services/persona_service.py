"""
Persona Service
페르소나 전환 서비스 (PDF 페이지 3: AFO ↔ TRINITY-OS 통합 지점)
"""

import logging
from datetime import datetime
from typing import Any

from AFO.domain.persona import (
    Persona,
    commander,
    creator,
    current_persona,
    family_head,
    jegalryang,
    juyu,
    samaui,
)

logger = logging.getLogger(__name__)

# 페르소나 매핑 (PDF 페이지 4: Personas 시스템)
PERSONA_MAPPING: dict[str, Persona | None] = {
    "commander": commander,
    "family": family_head,
    "family_head": family_head,
    "creator": creator,
    "learner": None,  # TODO: Phase 2에서 구현
    "jegalryang": jegalryang,
    "samaui": samaui,
    "juyu": juyu,
}


class PersonaService:
    """
    페르소나 전환 서비스

    PDF 페이지 3: AFO ↔ TRINITY-OS 통합 지점
    PDF 페이지 4: Personas 시스템
    """

    def __init__(self):
        self._current_persona: Persona = current_persona

    @property
    def current_persona(self) -> Persona:
        """현재 활성화된 페르소나"""
        return self._current_persona

    async def switch_persona(
        self, persona_type: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        형님의 명령으로 페르소나 전환 (PDF 페이지 4: Personas 시스템)

        Args:
            persona_type: 페르소나 타입 (commander, family, creator 등)
            context: 추가 맥락 정보

        Returns:
            전환 결과
        """
        target = PERSONA_MAPPING.get(persona_type.lower())

        if not target:
            raise ValueError(f"알 수 없는 페르소나 타입: {persona_type}")

        if target == self._current_persona:
            return {
                "current_persona": self._current_persona.name,
                "status": "이미 활성화된 페르소나입니다.",
                "trinity_scores": self._current_persona.trinity_scores,
            }

        # 이전 페르소나 비활성화
        self._current_persona.active = False

        # 새 페르소나 활성화
        target.switch_to()

        # 맥락 정보 추가
        if context:
            target.add_context(context)

        # 전역 변수 업데이트
        global current_persona
        current_persona = target
        self._current_persona = target

        # TRINITY-OS 로그 브릿지 전송 (PDF 페이지 3: 로그 브릿지)
        await self._send_log_bridge(target, context)

        logger.info(f"[PersonaService] 페르소나 전환: {self._current_persona.name} → {target.name}")

        return {
            "current_persona": target.name,
            "status": "전환 완료",
            "trinity_scores": target.trinity_scores,
            "last_switched": target.last_switched.isoformat() if target.last_switched else None,
        }

    async def get_current_persona(self) -> dict[str, Any]:
        """현재 활성화된 페르소나 정보 조회"""
        return {
            "id": self._current_persona.id,
            "name": self._current_persona.name,
            "type": self._current_persona.type.value,
            "trinity_scores": self._current_persona.trinity_scores,
            "active": self._current_persona.active,
            "last_switched": self._current_persona.last_switched.isoformat()
            if self._current_persona.last_switched
            else None,
        }

    async def _send_log_bridge(self, persona: Persona, context: dict[str, Any] | None) -> None:
        """
        TRINITY-OS 로그 브릿지 전송 (PDF 페이지 3: 로그 브릿지)

        실제 구현 시:
        - SSE (Server-Sent Events) 또는 WebSocket 사용
        - TRINITY-OS MCP 서버에 페르소나 전환 알림
        """
        log_entry = {
            "event": "persona_switch",
            "persona_id": persona.id,
            "persona_name": persona.name,
            "persona_type": persona.type.value,
            "trinity_scores": persona.trinity_scores,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        # TODO: 실제 TRINITY-OS 로그 브릿지 구현 (Phase 2 확장)
        # 예: MCP 서버 호출 또는 SSE 스트리밍
        logger.info(f"[로그 브릿지] TRINITY-OS에 페르소나 전환 알림: {persona.name}")
        logger.debug(f"[로그 브릿지] 전송 데이터: {log_entry}")

        # 실제 구현 예시 (주석 처리):
        # try:
        #     from scripts.integration.mcp_client import call_trinity_os_tool
        #     await call_trinity_os_tool("persona_switch", log_entry)
        # except Exception as e:
        #     logger.warning(f"로그 브릿지 전송 실패: {e}")


# 싱글톤 인스턴스
persona_service = PersonaService()


# 편의 함수
async def switch_persona(
    persona_type: str, context: dict[str, Any] | None = None
) -> dict[str, Any]:
    """페르소나 전환 편의 함수"""
    return await persona_service.switch_persona(persona_type, context)


async def get_current_persona() -> dict[str, Any]:
    """현재 페르소나 조회 편의 함수"""
    return await persona_service.get_current_persona()
