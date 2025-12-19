"""
AFO 설정 테스트
"""

from AFO.config.settings import get_settings


def test_get_settings():
    """설정 로드 테스트"""
    settings = get_settings()
    assert settings is not None
    assert hasattr(settings, "POSTGRES_HOST")
    assert hasattr(settings, "REDIS_URL")
    assert hasattr(settings, "QDRANT_URL")


def test_settings_defaults():
    """설정 기본값 테스트"""
    settings = get_settings()
    assert settings.POSTGRES_HOST == "localhost"
    assert settings.POSTGRES_PORT == 15432
    assert settings.REDIS_URL.startswith("redis://")


def test_get_postgres_connection_params():
    """PostgreSQL 연결 파라미터 테스트"""
    settings = get_settings()
    params = settings.get_postgres_connection_params()
    assert "host" in params or "database_url" in params
    assert "port" in params or "database_url" in params


def test_get_redis_url():
    """Redis URL 테스트"""
    settings = get_settings()
    redis_url = settings.get_redis_url()
    assert redis_url.startswith("redis://")
