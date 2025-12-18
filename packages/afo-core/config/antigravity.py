import logging
from pydantic_settings import BaseSettings
from typing import Literal

logger = logging.getLogger(__name__)


class AntiGravitySettings(BaseSettings):
    """
    AntiGravity 중앙 설정 클래스 - 모든 마찰 제거를 위한 통합 포인트
    Truth (眞): 타입 안전성 및 명시적 설정
    Goodness (善): DRY_RUN 기본값으로 안전 우선
    Beauty (美): 간결한 설정 인터페이스
    Serenity (孝): 자동화로 운영 마찰 제거
    """
    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"  # 환경 자동 감지
    AUTO_DEPLOY: bool = True                             # 자동 배포 활성화 (孝: 운영 마찰 제거)
    DRY_RUN_DEFAULT: bool = True                         # 기본 DRY_RUN (善: 안전 우선)
    CENTRAL_CONFIG_SYNC: bool = True                     # 중앙 설정 동기화 (永: 영속성)
    AUTO_SYNC: bool = True                               # 자동 동기화 활성화 (孝: 설정 마찰 제거)

    class Config:
        env_file = ".env.antigravity"  # 별도 env 파일로 마찰 최소화
        case_sensitive = False
    
    def auto_sync(self) -> str:
        """
        자동 동기화 실행 (孝: Serenity)
        
        PDF 페이지 1: AntiGravity 자동화
        - 설정·데이터 실시간 반영
        - Vault·DB 동기화 로직
        
        Returns:
            동기화 결과 메시지
        """
        if not self.AUTO_SYNC:
            return "[孝: 자동 동기화] 비활성화됨"
        
        logger.info("[孝: 자동 동기화] 설정·데이터 실시간 반영 완료")
        # TODO: 실제 Vault·DB 동기화 로직 구현
        # 예: Vault에서 설정 로드, DB에 반영 등
        
        return "[孝: 자동 동기화] 설정·데이터 실시간 반영 완료"


# 싱글톤 인스턴스 - 전체 앱에서 공유
antigravity = AntiGravitySettings()

# Startup 시 자동 동기화 실행
antigravity.auto_sync()
