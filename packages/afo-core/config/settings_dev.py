"""
AFO Development Settings
Phase 2-5: 환경별 설정 분리 - Development 환경
"""

from .settings import AFOSettings


class AFOSettingsDev(AFOSettings):
    """
    Development 환경 설정
    기본 설정을 상속받고 개발 환경에 맞게 오버라이드
    """

    # Development 환경 기본값
    MOCK_MODE: bool = True  # 개발 시 Mock 모드 활성화
    ASYNC_QUERY_ENABLED: bool = True

    # Development 환경 로깅
    LOG_LEVEL: str = "DEBUG"

    # Development 환경 데이터베이스 (로컬)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 15432

    # Development 환경 Redis (로컬)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Development 환경 서비스 URL (로컬)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    QDRANT_URL: str = "http://localhost:6333"
    N8N_URL: str = "http://localhost:5678"
    API_WALLET_URL: str = "http://localhost:8000"
    MCP_SERVER_URL: str = "http://localhost:8787"

    # Development 환경 API Keys (선택적, .env에서 로드)
    # 실제 키는 .env 파일에서 관리

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = False
