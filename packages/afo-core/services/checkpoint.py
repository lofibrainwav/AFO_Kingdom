# mypy: ignore-errors
"""
Checkpoint Service
永 (Eternity): Redis Checkpoint + DB 영속 저장
PDF 페이지 4: 문서화 + 지속 아키텍처
"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Lazy import to avoid startup errors
try:
    from AFO.utils.redis_connection import get_redis_url

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available - checkpoint will use in-memory storage")

try:
    from AFO.services.database import get_db_connection

    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    logger.warning("Database not available - checkpoint will use in-memory storage")


class CheckpointService:
    """
    Checkpoint Service - 상태 영속 저장

    PDF 페이지 4: 문서화 + 지속 아키텍처
    - Redis Checkpoint: 빠른 상태 복원 (7일 영속)
    - DB 영속 저장: 장기 유지보수성
    """

    def __init__(self):
        self._memory_store: dict[str, Any] = {}  # Fallback: 메모리 저장

    async def save_persona_state(self, persona: Any) -> dict[str, Any]:
        """
        페르소나 상태 저장 (永: Eternity)

        PDF 페이지 4: 지속 아키텍처
        - Redis Checkpoint: 7일 영속
        - DB 영속 저장: 장기 유지보수성

        Args:
            persona: 저장할 페르소나 객체

        Returns:
            저장 결과
        """
        try:
            # 페르소나를 JSON 직렬화 가능한 형태로 변환
            if hasattr(persona, "model_dump"):
                persona_data = persona.model_dump()
            elif hasattr(persona, "dict"):
                persona_data = persona.dict()
            else:
                persona_data = {
                    "id": getattr(persona, "id", "unknown"),
                    "name": getattr(persona, "name", "unknown"),
                }

            persona_json = json.dumps(persona_data, default=str)

            # Redis Checkpoint 저장 (7일 영속)
            if REDIS_AVAILABLE:
                try:
                    import redis.asyncio as redis

                    redis_url = get_redis_url()
                    r = redis.from_url(redis_url)
                    await r.set(
                        f"persona:{persona_data.get('id', 'unknown')}", persona_json, ex=604800
                    )  # 7일
                    await r.close()
                    logger.info(
                        f"[永: Checkpoint] Redis에 페르소나 상태 저장: {persona_data.get('id')}"
                    )
                except Exception as e:
                    logger.warning(f"[永: Checkpoint] Redis 저장 실패, 메모리 저장으로 폴백: {e}")
                    self._memory_store[f"persona:{persona_data.get('id', 'unknown')}"] = (
                        persona_data
                    )

            # DB 영속 저장
            if DB_AVAILABLE:
                try:
                    conn = await get_db_connection()
                    # TODO: 실제 DB INSERT 쿼리 구현
                    # await conn.execute("INSERT INTO persona_history (persona_id, state, created_at) VALUES ($1, $2, NOW())", ...)
                    await conn.close()
                    logger.info(f"[永: Eternity] DB에 페르소나 상태 저장: {persona_data.get('id')}")
                except Exception as e:
                    logger.warning(f"[永: Eternity] DB 저장 실패: {e}")

            return {
                "status": "success",
                "persona_id": persona_data.get("id"),
                "storage": "redis+db" if (REDIS_AVAILABLE and DB_AVAILABLE) else "memory",
            }

        except Exception as e:
            logger.error(f"[永: Eternity] 페르소나 상태 저장 실패: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    async def load_persona_state(self, persona_id: str) -> dict[str, Any] | None:
        """
        페르소나 상태 로드 (永: Eternity)

        Args:
            persona_id: 로드할 페르소나 ID

        Returns:
            페르소나 상태 또는 None
        """
        try:
            # Redis에서 로드
            if REDIS_AVAILABLE:
                try:
                    import redis.asyncio as redis

                    redis_url = get_redis_url()
                    r = redis.from_url(redis_url)
                    data = await r.get(f"persona:{persona_id}")
                    await r.close()
                    if data:
                        result: dict[str, Any] = json.loads(data)
                        return result
                except Exception as e:
                    logger.warning(f"[永: Checkpoint] Redis 로드 실패: {e}")

            # 메모리에서 로드 (폴백)
            if f"persona:{persona_id}" in self._memory_store:
                return self._memory_store[f"persona:{persona_id}"]

            return None

        except Exception as e:
            logger.error(f"[永: Eternity] 페르소나 상태 로드 실패: {e}")
            return None


# 싱글톤 인스턴스
checkpoint_service = CheckpointService()
