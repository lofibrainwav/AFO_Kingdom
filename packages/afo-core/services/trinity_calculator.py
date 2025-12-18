"""
Trinity Score Calculator
동적 Trinity Score 계산기 - 실시간 행동·상태 반영
PDF 페이지 1: Trinity Score 계산기, 페이지 3: 5대 가치 동적 평가
"""

import logging
from typing import Any

from AFO.config.antigravity import antigravity
from AFO.domain.persona import current_persona

logger = logging.getLogger(__name__)


class TrinityCalculator:
    """
    동적 Trinity Score 계산기 - 실시간 행동·상태 반영
    
    PDF 페이지 1: Trinity Score 계산기
    PDF 페이지 3: 5대 가치 동적 평가
    """
    
    BASE_SCORES = {  # 기본 점수 (PDF 페이지 3: 5대 가치 구현 기준)
        "truth": 100.0,
        "goodness": 100.0,
        "beauty": 100.0,
        "serenity": 100.0,
        "eternity": 100.0,
    }
    
    def calculate_dynamic(self, action: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        동적 점수 계산 - 행동에 따라 변동
        
        PDF 페이지 1: Trinity Score 계산기
        PDF 페이지 3: 5대 가치 동적 평가
        
        Args:
            action: 수행한 행동 (예: "receipt", "safe", "summary", "auto", "checkpoint")
            context: 추가 맥락 정보
            
        Returns:
            계산된 Trinity Scores 및 총점
        """
        if context is None:
            context = {}
        
        scores = self.BASE_SCORES.copy()
        
        # 眞 (Truth): 증거 기반 행동 시 가점
        if "receipt" in action.lower() or "verified" in action.lower():
            scores["truth"] = min(100.0, scores["truth"] + 5.0)
            logger.debug(f"[眞: Truth] 증거 기반 행동 감지: +5점")
        
        # 善 (Goodness): DRY_RUN 또는 안전 행동 시 가점
        if antigravity.DRY_RUN_DEFAULT or "safe" in action.lower():
            scores["goodness"] = min(100.0, scores["goodness"] + 10.0)
            logger.debug(f"[善: Goodness] DRY_RUN/안전 행동 감지: +10점")
        
        # 美 (Beauty): 우아한 응답(3줄 요약) 시 가점
        response_length = len(context.get("response", ""))
        if "summary" in action.lower() or response_length < 300:
            scores["beauty"] = min(100.0, scores["beauty"] + 8.0)
            logger.debug(f"[美: Beauty] 우아한 응답 감지: +8점")
        
        # 孝 (Serenity): 마찰 제거 행동 시 가점
        if "auto" in action.lower() or antigravity.AUTO_DEPLOY:
            scores["serenity"] = min(100.0, scores["serenity"] + 10.0)
            logger.debug(f"[孝: Serenity] 자동화 행동 감지: +10점")
        
        # 永 (Eternity): 영속 저장 행동 시 가점
        if "checkpoint" in action.lower() or "save" in action.lower():
            scores["eternity"] = min(100.0, scores["eternity"] + 5.0)
            logger.debug(f"[永: Eternity] 영속 저장 행동 감지: +5점")
        
        total = sum(scores.values())
        # 상한 초과 시 500으로 클립
        if total > 500.0:
            logger.warning(f"[TrinityCalculator] 총점 상한 초과: {total} → 500으로 클립")
            total = 500.0
        
        return {
            "scores": scores,
            "total": total,
            "max": 500.0,
            "persona": current_persona.name if current_persona else "unknown",
        }


# 싱글톤 인스턴스
trinity_calculator = TrinityCalculator()

