# Trinity Score: 90.0 (Established by Chancellor)
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException

if TYPE_CHECKING:
    import asyncpg

# 중앙 설정 사용
# 중앙 설정 사용
from AFO.config.settings import get_settings

# Lazy import asyncpg to avoid startup errors if not installed
try:
    import asyncpg

    ASYNCPG_AVAILABLE = True
except ImportError:
    asyncpg = None
    ASYNCPG_AVAILABLE = False


# [論語]學而不思則罔 - 배우되 생각하지 않으면 어둡다
async def get_db_connection() -> Any:
    """
    비동기 PostgreSQL 연결 함수 (중앙 설정 사용)

    Returns:
        asyncpg.Connection: PostgreSQL 연결 객체
    """
    if not ASYNCPG_AVAILABLE or asyncpg is None:
        raise HTTPException(
            status_code=503, detail="PostgreSQL async support not available"
        )

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
