from typing import Any

from fastapi import HTTPException

# 중앙 설정 사용
try:
    from AFO.config.settings import get_settings
except ImportError:
    # Fallback for local execution
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import get_settings

# Lazy import asyncpg to avoid startup errors if not installed
try:
    import asyncpg

    ASYNCPG_AVAILABLE = True
except ImportError:
    asyncpg = None
    ASYNCPG_AVAILABLE = False


async def get_db_connection() -> Any:  # type: ignore[no-any-return]
    """비동기 PostgreSQL 연결 함수 (중앙 설정 사용)"""
    if not ASYNCPG_AVAILABLE or asyncpg is None:
        raise HTTPException(status_code=503, detail="PostgreSQL async support not available")

    try:
        settings = get_settings()
        params = settings.get_postgres_connection_params()

        # DATABASE_URL이 있으면 사용, 없으면 개별 파라미터 사용
        if "database_url" in params:
            conn = await asyncpg.connect(params["database_url"])
        else:
            conn = await asyncpg.connect(
                host=params["host"],
                port=params["port"],
                database=params["database"],
                user=params["user"],
                password=params["password"],
            )
        return conn
    except Exception as e:
        print(f"❌ PostgreSQL 연결 실패: {e}")
        raise HTTPException(status_code=500, detail="데이터베이스 연결 실패") from e
