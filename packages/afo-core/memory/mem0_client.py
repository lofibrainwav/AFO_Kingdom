"""
Mem0 Client Wrapper 모듈

AFO 왕국을 위한 Mem0 통합 wrapper입니다.
- user-level personalization 지원
- session/thread 기반 메모리 관리
- Trinity Score 연동 (永 1.0 목표)
"""

import time
from typing import Any

from mem0 import Memory


class AFO_MemoryClient:
    """
    AFO 왕국 전용 Mem0 클라이언트 wrapper

    기능:
    - 사용자별 메모리 관리 (personalization)
    - 세션 기반 메모리 그룹화
    - 메모리 검색 및 업데이트
    - 성능 모니터링
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Mem0 클라이언트 초기화

        Args:
            config: Mem0 설정 (backend, API key 등)
        """
        self.config = config or {
            # 로컬 백엔드 설정 (LanceDB 사용)
            "vector_store": {
                "provider": "lancedb",
                "config": {
                    "collection_name": "afo_memory",
                    "uri": "./data/lancedb/afo_memory.lance",  # LanceDB 파일 경로
                },
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-3.5-turbo",  # 기본 모델
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "openai_api_key": "dummy_key",  # 더미 키 (실제로는 사용되지 않음)
                },
            },
        }

        # Mem0 초기화 시도 (실패해도 graceful degradation)
        try:
            self.memory = Memory.from_config(self.config)
            self.initialized = True
        except Exception as e:
            # Mem0 초기화 실패 시 mock 객체 사용
            print(f"Mem0 initialization failed: {e}. Using mock mode.")
            self.memory = None
            self.initialized = False
            self.mock_memories: dict[str, list[dict[str, Any]]] = {}
        self.performance_stats = {
            "add_calls": 0,
            "search_calls": 0,
            "total_latency_ms": 0,
            "last_operation": None,
        }

    def add_memory(
        self,
        content: str,
        user_id: str,
        metadata: dict | None = None,
        session_id: str | None = None,
        run_id: str | None = None,
    ) -> dict[str, Any]:
        """
        메모리 추가

        Args:
            content: 메모리 내용
            user_id: 사용자 식별자 (personalization용)
            metadata: 추가 메타데이터
            session_id: 세션 식별자
            run_id: 실행 식별자

        Returns:
            Dict: 추가 결과
        """
        start_time = time.time()

        try:
            # user_id 기반 메모리 추가
            enriched_metadata = metadata or {}
            if session_id:
                enriched_metadata["session_id"] = session_id
            if run_id:
                enriched_metadata["run_id"] = run_id

            if self.initialized and self.memory:
                result = self.memory.add(content, user_id=user_id, metadata=enriched_metadata)
            else:
                # Mock 모드: 인메모리 저장
                if user_id not in self.mock_memories:
                    self.mock_memories[user_id] = []
                memory_id = f"mock_{len(self.mock_memories[user_id])}"
                mock_memory = {
                    "id": memory_id,
                    "memory": content,
                    "metadata": enriched_metadata,
                    "user_id": user_id,
                    "created_at": time.time(),
                }
                self.mock_memories[user_id].append(mock_memory)
                result = memory_id

            # 성능 통계 업데이트
            latency = (time.time() - start_time) * 1000
            self.performance_stats["add_calls"] += 1
            self.performance_stats["total_latency_ms"] += latency
            self.performance_stats["last_operation"] = "add"

            return {"success": True, "result": result, "latency_ms": latency, "user_id": user_id}

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {"success": False, "error": str(e), "latency_ms": latency, "user_id": user_id}

    def search_memory(
        self, query: str, user_id: str, limit: int = 5, session_id: str | None = None
    ) -> dict[str, Any]:
        """
        메모리 검색

        Args:
            query: 검색 쿼리
            user_id: 사용자 식별자
            limit: 최대 결과 개수
            session_id: 세션 필터링 (선택)

        Returns:
            Dict: 검색 결과
        """
        start_time = time.time()

        try:
            if self.initialized and self.memory:
                # Mem0 검색
                results = self.memory.search(query, user_id=user_id)
            else:
                # Mock 모드: 간단한 텍스트 매칭
                user_memories = self.mock_memories.get(user_id, [])
                results = []
                query_lower = query.lower()

                for memory in user_memories:
                    memory_text = memory.get("memory", "").lower()
                    if query_lower in memory_text:
                        # Mock 검색 결과 포맷
                        results.append(
                            {
                                "id": memory["id"],
                                "memory": memory["memory"],
                                "metadata": memory["metadata"],
                                "score": 0.9,  # Mock 점수
                            }
                        )

            # 세션 필터링 (선택)
            if session_id:
                results = [
                    r for r in results if r.get("metadata", {}).get("session_id") == session_id
                ]

            # 제한 적용
            filtered_results = results[:limit] if limit > 0 else results

            # 성능 통계 업데이트
            latency = (time.time() - start_time) * 1000
            self.performance_stats["search_calls"] += 1
            self.performance_stats["total_latency_ms"] += latency
            self.performance_stats["last_operation"] = "search"

            return {
                "success": True,
                "results": filtered_results,
                "total_found": len(results),
                "returned": len(filtered_results),
                "latency_ms": latency,
                "user_id": user_id,
            }

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {"success": False, "error": str(e), "latency_ms": latency, "user_id": user_id}

    def get_all_memories(self, user_id: str, session_id: str | None = None) -> dict[str, Any]:
        """
        모든 메모리 조회

        Args:
            user_id: 사용자 식별자
            session_id: 세션 필터링 (선택)

        Returns:
            Dict: 메모리 목록
        """
        start_time = time.time()

        try:
            if self.initialized and self.memory:
                memories = self.memory.get_all(user_id=user_id)
            else:
                # Mock 모드: 저장된 메모리 반환
                memories = self.mock_memories.get(user_id, [])

            # 세션 필터링
            if session_id:
                memories = [
                    m for m in memories if m.get("metadata", {}).get("session_id") == session_id
                ]

            latency = (time.time() - start_time) * 1000

            return {
                "success": True,
                "memories": memories,
                "count": len(memories),
                "latency_ms": latency,
                "user_id": user_id,
            }

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {"success": False, "error": str(e), "latency_ms": latency, "user_id": user_id}

    def get_performance_stats(self) -> dict[str, Any]:
        """
        성능 통계 조회

        Returns:
            Dict: 성능 통계
        """
        stats: dict[str, Any] = self.performance_stats.copy()

        # 타입 보장: 초기값이 0으로 설정되어 있는지 확인
        add_calls = stats.get("add_calls", 0) or 0
        search_calls = stats.get("search_calls", 0) or 0
        total_latency_ms = stats.get("total_latency_ms", 0) or 0

        # 평균 latency 계산
        total_calls = add_calls + search_calls
        if total_calls > 0:
            stats["avg_latency_ms"] = total_latency_ms / total_calls
        else:
            stats["avg_latency_ms"] = 0

        # Trinity Score 계산
        avg_latency = stats.get("avg_latency_ms", 0)
        if avg_latency < 50:  # 50ms 이내
            trinity_eternity = 1.0
        elif avg_latency < 100:  # 100ms 이내
            trinity_eternity = 0.8
        elif avg_latency < 200:  # 200ms 이내
            trinity_eternity = 0.6
        else:
            trinity_eternity = 0.4

        stats["trinity_score"] = {
            "eternity": trinity_eternity,  # 영원한 상태 보존
            "truth": 0.9,  # 정확한 메모리 관리
            "goodness": 0.95,  # 안정적 상태 공유
            "beauty": 0.9,  # Clean Architecture 통합
            "serenity": 1.0,  # 형님 평온 유지
        }

        return stats

    def reset_stats(self):
        """성능 통계 초기화"""
        self.performance_stats = {
            "add_calls": 0,
            "search_calls": 0,
            "total_latency_ms": 0,
            "last_operation": None,
        }


# 전역 클라이언트 인스턴스
_default_client = None


def get_memory_client(config: dict[str, Any] | None = None) -> AFO_MemoryClient:
    """
    전역 Mem0 클라이언트 인스턴스 반환

    Args:
        config: 클라이언트 설정 (최초 호출 시에만 사용)

    Returns:
        AFO_MemoryClient: 클라이언트 인스턴스
    """
    global _default_client

    if _default_client is None:
        _default_client = AFO_MemoryClient(config)

    return _default_client
    return _default_client
