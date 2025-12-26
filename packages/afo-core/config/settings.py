# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO 왕국 중앙 집중식 설정 관리
Phase 1 리팩토링: 하드코딩 제거 및 환경 변수 통합
"""

import os
import sys
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .antigravity import antigravity
from .julie import JulieConfig, julie_config
from .trinity import TrinityConfig


class AFOSettings(BaseSettings):
    """
    AFO 왕국 중앙 설정 클래스
    모든 환경 변수와 기본값을 한 곳에서 관리
    """

    # ============================================================================
    # AntiGravity Integration (Phase 1)
    # ============================================================================
    antigravity_mode: bool = Field(
        default=antigravity.AUTO_DEPLOY,
        description="AntiGravity 자동 배포 모드 (True: 활성화)",
    )

    # ============================================================================
    # Sub-Configurations (Phase 6A Centralization)
    # ============================================================================
    # Trinity SSOT (Class-based constant, not Pydantic)
    TRINITY: ClassVar[type[TrinityConfig]] = TrinityConfig

    # Julie CPA Config (Nested Pydantic)
    julie: JulieConfig = Field(default_factory=lambda: julie_config)

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ============================================================================
    # Database Settings (PostgreSQL)
    # ============================================================================
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL 호스트")
    POSTGRES_PORT: int = Field(default=15432, description="PostgreSQL 포트")
    POSTGRES_DB: str = Field(
        default="afo_memory", description="PostgreSQL 데이터베이스 이름"
    )
    POSTGRES_USER: str = Field(default="afo", description="PostgreSQL 사용자")
    POSTGRES_PASSWORD: str = Field(
        default="afo_secret_change_me", description="PostgreSQL 비밀번호"
    )
    DATABASE_URL: str | None = Field(
        default=None, description="PostgreSQL 연결 URL (선택적, 개별 설정보다 우선)"
    )

    # ============================================================================
    # Redis Settings
    # ============================================================================
    REDIS_URL: str = Field(
        default="redis://localhost:6379", description="Redis 연결 URL"
    )
    REDIS_HOST: str = Field(
        default="localhost", description="Redis 호스트 (REDIS_URL이 없을 때 사용)"
    )
    REDIS_PORT: int = Field(
        default=6379, description="Redis 포트 (REDIS_URL이 없을 때 사용)"
    )

    # ============================================================================
    # Qdrant Settings
    # ============================================================================
    QDRANT_URL: str = Field(
        default="http://localhost:6333", description="Qdrant 벡터 DB URL"
    )

    # ============================================================================
    # Ollama Settings
    # ============================================================================
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434", description="Ollama LLM 서버 URL"
    )
    OLLAMA_MODEL: str = Field(default="qwen3-vl:8b", description="Ollama 기본 모델")

    # ============================================================================
    # N8N Settings
    # ============================================================================
    N8N_URL: str = Field(
        default="http://localhost:5678", description="N8N 워크플로우 자동화 서버 URL"
    )

    # ============================================================================
    # API Wallet Settings
    # ============================================================================
    API_WALLET_URL: str = Field(
        default="http://localhost:8000", description="API Wallet 서버 URL"
    )

    # ============================================================================
    # MCP Server Settings
    # ============================================================================
    MCP_SERVER_URL: str = Field(
        default="http://localhost:8787",
        description="MCP (Model Context Protocol) 서버 URL",
    )

    # ============================================================================
    # API Keys
    # ============================================================================
    API_YUNGDEOK: str = Field(default="default_yungdeok_key", description="영덕 API 키")
    OPENAI_API_KEY: str | None = Field(default=None, description="OpenAI API 키")
    ANTHROPIC_API_KEY: str | None = Field(
        default=None, description="Anthropic (Claude) API 키"
    )
    GEMINI_API_KEY: str | None = Field(default=None, description="Google Gemini API 키")
    GOOGLE_API_KEY: str | None = Field(
        default=None, description="Google API 키 (GEMINI_API_KEY 대체용)"
    )
    CHATGPT_SESSION_TOKEN_1: str | None = Field(
        default=None, description="ChatGPT 세션 토큰 1"
    )
    CHATGPT_SESSION_TOKEN_2: str | None = Field(
        default=None, description="ChatGPT 세션 토큰 2"
    )
    CHATGPT_SESSION_TOKEN_3: str | None = Field(
        default=None, description="ChatGPT 세션 토큰 3"
    )
    CURSOR_ACCESS_TOKEN: str | None = Field(
        default=None, description="Cursor 액세스 토큰"
    )
    REDIS_PASSWORD: str | None = Field(default=None, description="Redis 비밀번호")

    # ============================================================================
    # Application Settings
    # ============================================================================
    AFO_API_VERSION: str = Field(default="v1", description="AFO API 버전")
    INPUT_SERVER_PORT: int = Field(default=4200, description="Input Server 포트")
    INPUT_SERVER_HOST: str = Field(default="0.0.0.0", description="Input Server 호스트")
    DASHBOARD_URL: str = Field(
        default="http://localhost:3000",
        description="프론트엔드 대시보드 URL (GenUI 등)",
    )

    # ============================================================================
    # API Server Settings
    # ============================================================================
    API_SERVER_PORT: int = Field(
        default=8010, description="API Server 포트 (Soul Engine)"
    )
    API_SERVER_HOST: str = Field(default="0.0.0.0", description="API Server 호스트")
    SOUL_ENGINE_PORT: int = Field(
        default=8010, description="Soul Engine 포트 (5 Pillars 등)"
    )
    ASYNC_QUERY_ENABLED: bool = Field(
        default=True, description="비동기 쿼리 활성화 여부"
    )
    MOCK_MODE: bool = Field(default=False, description="Mock 모드 활성화 여부")
    SENTRY_DSN: str | None = Field(
        default=None, description="Sentry DSN (에러 모니터링)"
    )
    VAULT_ENABLED: bool = Field(default=False, description="Vault KMS 사용 여부")
    API_WALLET_ENCRYPTION_KEY: str | None = Field(
        default=None, description="API Wallet 암호화 키 (Fernet, 44자)"
    )
    # Vault Settings (Phase 3)
    VAULT_URL: str = Field(
        default="http://localhost:8200", description="Vault 서버 URL"
    )
    VAULT_TOKEN: str | None = Field(default=None, description="Vault 액세스 토큰")
    TAVILY_API_KEY: str | None = Field(
        default=None, description="Tavily API 키 (웹 검색)"
    )
    REDIS_RAG_INDEX: str = Field(
        default="rag_docs", description="Redis RAG 인덱스 이름"
    )
    AFO_HOME: str | None = Field(default=None, description="AFO 홈 디렉토리 경로")
    AFO_SOUL_ENGINE_HOME: str | None = Field(
        default=None, description="AFO Soul Engine 홈 디렉토리 경로"
    )
    BASE_DIR: str = Field(
        default=os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ),
        description="프로젝트 루트 디렉토리",
    )

    # ============================================================================
    # Chancellor Configuration (Optimization)
    # ============================================================================
    CHANCELLOR_AUTO_RUN_THRESHOLD: float = Field(
        default=90.0, description="자동 실행(AUTO_RUN)을 위한 최소 Trinity Score"
    )
    CHANCELLOR_RISK_THRESHOLD: float = Field(
        default=10.0, description="자동 실행(AUTO_RUN)을 위한 최대 Risk Score"
    )
    CHANCELLOR_MAX_MEMORY_ITEMS: int = Field(
        default=10, description="Chancellor 메모리 요약 트리거 임계값"
    )

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def get_postgres_connection_params(self) -> dict:
        """PostgreSQL 연결 파라미터 반환"""
        if self.DATABASE_URL:
            return {"database_url": self.DATABASE_URL}

        return {
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
        }

    def get_redis_url(self) -> str:
        """Redis URL 반환"""
        if self.REDIS_URL and not self.REDIS_URL.startswith("redis://localhost"):
            return self.REDIS_URL
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


# 전역 설정 인스턴스 (싱글톤 패턴)
_settings: AFOSettings | None = None


def get_settings(env: str | None = None) -> AFOSettings:
    """
    전역 설정 인스턴스 반환 (싱글톤)

    Args:
        env: 환경 이름 ("dev", "prod", "test"). None이면 AFO_ENV 환경 변수 사용

    Returns:
        AFOSettings 인스턴스 (환경에 따라 AFOSettingsDev, AFOSettingsProd, AFOSettingsTest)
    """
    global _settings

    # 환경 변수에서 환경 확인 (Phase 2-5)
    if env is None:
        env = os.getenv("AFO_ENV", "dev").lower()

    # 환경별 설정 클래스 로드
    settings_class: type[AFOSettings]

    if env == "prod" or env == "production":
        try:
            from .settings_prod import AFOSettingsProd

            settings_class = AFOSettingsProd
        except ImportError:
            # Fallback: 기본 설정 사용
            settings_class = AFOSettings
    elif env == "test" or env == "testing":
        try:
            from .settings_test import AFOSettingsTest

            settings_class = AFOSettingsTest
        except ImportError:
            # Fallback: 기본 설정 사용
            settings_class = AFOSettings
    else:  # dev 또는 기본값
        try:
            from .settings_dev import AFOSettingsDev

            settings_class = AFOSettingsDev
        except ImportError:
            # Fallback: 기본 설정 사용
            settings_class = AFOSettings

    # 싱글톤 인스턴스 생성
    if _settings is None:
        _settings = settings_class()

        # Context7 trinity-os 패키지 경로 추가 (Python Path 확장)
        trinity_os_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'trinity-os'))
        if trinity_os_path not in sys.path:
            sys.path.insert(0, trinity_os_path)
            print(f"✅ Context7 trinity-os 경로 추가: {trinity_os_path}")

        print(f"✅ AFO 설정 로드 완료: {env} 환경 ({settings_class.__name__})")

    return _settings


# 편의를 위한 전역 인스턴스
settings = get_settings()
