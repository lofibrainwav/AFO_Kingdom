# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Kingdom AntiGravity Configuration Settings
Step 0: The Core configuration for governed autonomous scaling.

Integrated with AGENTS.md (SSOT for Trinity Pillars)
"""

import logging
from pathlib import Path
from typing import Any, Literal, cast

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

# AGENTS.md 파일 경로 (루트 기준)
AGENTS_MD_PATH = Path(__file__).resolve().parent.parent.parent.parent / "AGENTS.md"

# Trinity Score 가중치 (AGENTS.md Ⅲ. 5기둥 철학 및 SSOT 가중치)
AGENTS_MD_TRINITY_WEIGHTS = {
    "truth": 0.35,
    "goodness": 0.35,
    "beauty": 0.20,
    "serenity": 0.08,
    "eternity": 0.02,
}

# Thresholds from AGENTS.md (Rule #1)
AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD = 80
AGENTS_MD_AUTO_RUN_RISK_THRESHOLD = 3

# Risk Score 가이드를 위한 맵핑 (AGENTS.md Ⅵ)
AGENTS_MD_RISK_SCORE_GUIDE = {
    "no_risk": 0,
    "low_risk": 1,
    "medium_risk": 2,
    "high_risk": 3,
    "block": 4,
}


class AntiGravitySettings(BaseSettings):
    """
    AntiGravity Governing Settings
    - Trinity Weights: AGENTS_MD_TRINITY_WEIGHTS
    - Threshholds: AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD, AGENTS_MD_AUTO_RUN_RISK_THRESHOLD
    - Risk Score Guide: AGENTS_MD_RISK_SCORE_GUIDE
    """

    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"  # 환경 자동 감지
    AUTO_DEPLOY: bool = True  # 자동 배포 활성화 (孝: 운영 마찰 제거)
    DRY_RUN_DEFAULT: bool = True  # 기본 DRY_RUN (善: 안전 우선)
    CENTRAL_CONFIG_SYNC: bool = True  # 중앙 설정 동기화 (永: 영속성)
    AUTO_SYNC: bool = False  # 자동 동기화 비활성화 (임시 복구용)
    SELF_EXPANDING_MODE: bool = True  # 자율 확장 모드 (永: 창조자 트랙 활성화)

    # [Phase A] 언어 정책 설정 (SSOT)
    REPORT_LANGUAGE: Literal["ko", "en"] = "ko"
    USE_PROTOCOL_OFFICER: bool = True  # Protocol Officer 사용 여부

    # [AGENTS.md 통합] AGENTS.md 파일 존재 확인
    @property
    def agents_md_exists(self) -> bool:
        """AGENTS.md 파일 존재 여부 확인"""
        return AGENTS_MD_PATH.exists()

    @property
    def agents_md_path(self) -> Path:
        """AGENTS.md 파일 경로 반환"""
        return AGENTS_MD_PATH

    @property
    def trinity_weights(self) -> dict[str, float]:
        """Trinity Score 가중치 반환 (AGENTS.md SSOT)"""
        return AGENTS_MD_TRINITY_WEIGHTS.copy()

    @property
    def auto_run_trinity_threshold(self) -> int:
        """AUTO_RUN Trinity Score 임계값 (AGENTS.md Rule #1)"""
        return AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD

    @property
    def auto_run_risk_threshold(self) -> int:
        """AUTO_RUN Risk Score 임계값 (AGENTS.md Rule #1)"""
        return AGENTS_MD_AUTO_RUN_RISK_THRESHOLD

    @property
    def risk_score_guide(self) -> dict[str, int]:
        """Risk Score 가이드 반환 (AGENTS.md Ⅵ)"""
        return AGENTS_MD_RISK_SCORE_GUIDE.copy()

    # [NEW] Phase 0: Logging Level Enforcement (眞: 관찰 강화)
    @property
    def LOG_LEVEL(self) -> str:
        return "DEBUG" if self.ENVIRONMENT == "dev" else "INFO"

    class Config:
        env_file = str(Path(__file__).parent / ".env.antigravity")  # 절대 경로로 수정
        case_sensitive = False
        extra = "allow"

    def auto_sync(self) -> str:
        """
        자동 동기화 실행 (孝: Serenity) - Hot Reload Implementation

        Reads .env.antigravity and updates the singleton instance in-place.
        """
        if not self.AUTO_SYNC:
            return "[孝: 자동 동기화] 비활성화됨"

        try:
            # 1. Create a fresh instance to read new env values
            new_settings = cast("Any", AntiGravitySettings)(_env_file=".env.antigravity")

            # 2. Update current instance attributes
            # effectively becoming the new settings while keeping the same object reference
            changes = []
            for key, value in new_settings.model_dump().items():
                old_value = getattr(self, key, None)
                if old_value != value:
                    setattr(self, key, value)
                    changes.append(f"{key}: {old_value} -> {value}")

            if changes:
                log_msg = f"[孝: 자동 동기화] 설정 업데이트 완료: {', '.join(changes)}"
                logger.info(log_msg)
                return log_msg
            else:
                return "[孝: 자동 동기화] 변경 사항 없음"
        except Exception as e:
            error_msg = f"[孝: 자동 동기화] 업데이트 실패: {e}"
            logger.error(error_msg)
            return error_msg


# 글로벌 설정 인스턴스 (SSOT)
antigravity = AntiGravitySettings()
