# Trinity Score: 90.0 (Established by Chancellor)
"""
Multimodal RAG Engine for AFO Kingdom (Phase 2)
Handles multimodal content (images, audio, video) in RAG pipelines.
Strangler Fig: 메모리 관리 및 문서 제한 추가
"""

import contextlib
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# 로깅 설정
logger = logging.getLogger(__name__)

# Strangler Fig: 메모리 관리 추가 (善: Goodness 안전성)
_memory_config = {
    "max_documents": 1000,  # 최대 문서 수
    "max_memory_mb": 500.0,  # 최대 메모리 사용량 (MB)
    "cleanup_threshold": 0.8,  # 정리 임계값 (80%)
    "lru_enabled": True,  # LRU 정리 활성화
}
_memory_lock = threading.Lock()


@dataclass
class MultimodalDocument:
    """A document that can contain text, images, or other media."""

    content: str
    content_type: str = "text"  # text, image, audio, video
    metadata: dict[str, Any] | None = None
    embedding: list[float] | None = None
    created_at: float | None = None  # LRU용 타임스탬프

    def __post_init__(self) -> None:
        try:
            if self.metadata is None:
                self.metadata = {}
            if self.created_at is None:
                self.created_at = time.time()
        except (ValueError, TypeError) as e:
            logger.debug("MultimodalDocument 초기화 중 값 설정 실패: %s", str(e))
            self.metadata = {}
            self.created_at = time.time()
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("MultimodalDocument 초기화 중 예상치 못한 에러: %s", str(e))
            self.metadata = {}
            self.created_at = time.time()


class MultimodalRAGEngine:
    """
    Multimodal RAG Engine supporting text, images, and other media.
    Strangler Fig: 메모리 관리 및 자동 정리 기능 추가
    """

    def __init__(self, embedding_model: str = "default", **kwargs: Any):
        self.embedding_model = embedding_model
        self.documents: list[MultimodalDocument] = []
        self.supported_types = ["text", "image", "audio", "video"]
        self._current_memory_mb = 0.0
        self._last_access_times: dict[int, float] = {}  # 문서 ID별 마지막 접근 시간

    def _estimate_document_memory(
        self, content: str, content_type: str, metadata: dict[str, Any]
    ) -> float:
        """
        문서의 메모리 사용량 추정 (MB)

        Args:
            content: 문서 내용
            content_type: 콘텐츠 타입
            metadata: 메타데이터

        Returns:
            예상 메모리 사용량 (MB)
        """
        try:
            # 기본 텍스트 크기
            text_size = len(content.encode("utf-8"))

            # 멀티모달 콘텐츠 추가 크기
            if content_type == "image":
                # 이미지 메타데이터 (실제 이미지 데이터는 파일 경로만 저장)
                text_size += len(str(metadata.get("path", "")).encode("utf-8"))
            elif content_type in ["audio", "video"]:
                # 미디어 파일 메타데이터
                text_size += len(str(metadata).encode("utf-8")) * 2

            # 임베딩 벡터 크기 (1536차원 float32 ≈ 6KB)
            if content_type == "text":
                text_size += 1536 * 4  # float32 = 4 bytes

            # Python 객체 오버헤드 (약 3배)
            return text_size * 3 / (1024 * 1024)

        except (UnicodeEncodeError, ValueError, TypeError) as e:
            logger.debug("문서 메모리 사용량 추정 실패: %s", str(e))
            return 1.0  # 기본 1MB 추정
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("문서 메모리 사용량 추정 중 예상치 못한 에러: %s", str(e))
            return 1.0  # 기본 1MB 추정

    def _cleanup_old_documents(self, required_space_mb: float) -> int:
        """
        오래된 문서 정리 (LRU 기반)

        Args:
            required_space_mb: 필요한 공간 (MB)

        Returns:
            정리된 문서 수
        """
        if not _memory_config["lru_enabled"]:
            return 0

        try:
            # 접근 시간으로 정렬 (오래된 것부터)
            docs_with_times = []
            for i, doc in enumerate(self.documents):
                access_time = self._last_access_times.get(id(doc), doc.created_at or 0)
                docs_with_times.append((access_time, i, doc))

            docs_with_times.sort(key=lambda x: x[0])  # 접근 시간 오름차순

            cleaned = 0
            freed_space = 0.0

            for _, index, doc in docs_with_times:
                if freed_space >= required_space_mb:
                    break

                # 메모리 사용량 추정
                doc_memory = self._estimate_document_memory(
                    doc.content, doc.content_type, doc.metadata or {}
                )

                # 문서 제거
                self.documents.pop(index - cleaned)  # 인덱스 조정
                self._current_memory_mb -= doc_memory
                freed_space += doc_memory
                cleaned += 1

                # 접근 시간 제거
                doc_id = id(doc)
                self._last_access_times.pop(doc_id, None)

            if cleaned > 0:
                logger.warning(
                    "메모리 부족으로 %d개 문서 정리 (해방: %.2fMB)",
                    cleaned,
                    freed_space,
                )

            return cleaned

        except (IndexError, ValueError) as e:
            logger.warning("문서 정리 중 인덱스/값 에러: %s", str(e))
            return 0
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("문서 정리 중 예상치 못한 에러: %s", str(e))
            return 0

    def add_document(
        self,
        content: str,
        content_type: str = "text",
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        문서를 RAG 인덱스에 추가 (Strangler Fig 메모리 관리 적용)

        Args:
            content: 문서 내용
            content_type: 콘텐츠 타입
            metadata: 메타데이터

        Returns:
            추가 성공 여부
        """
        try:
            with _memory_lock:
                # 1. 문서 수 제한 확인
                if len(self.documents) >= _memory_config["max_documents"]:
                    logger.warning(
                        "문서 수 제한 초과: %d/%d",
                        len(self.documents),
                        _memory_config["max_documents"],
                    )
                    return False

                # 2. 메모리 사용량 추정
                doc_memory_mb = self._estimate_document_memory(
                    content, content_type, metadata or {}
                )

                # 3. 메모리 제한 확인 및 정리
                if self._current_memory_mb + doc_memory_mb > _memory_config["max_memory_mb"]:
                    # 임계값 도달 시 자동 정리
                    threshold_memory = (
                        _memory_config["max_memory_mb"] * _memory_config["cleanup_threshold"]
                    )
                    if self._current_memory_mb >= threshold_memory:
                        self._cleanup_old_documents(doc_memory_mb)

                    # 여전히 메모리 부족하면 실패
                    if self._current_memory_mb + doc_memory_mb > _memory_config["max_memory_mb"]:
                        logger.warning(
                            "메모리 제한 초과: %.2fMB 요청, 현재 %.2fMB 사용",
                            doc_memory_mb,
                            self._current_memory_mb,
                        )
                        return False

                # 4. 문서 생성 및 추가
                doc = MultimodalDocument(
                    content=content, content_type=content_type, metadata=metadata or {}
                )

                self.documents.append(doc)
                self._current_memory_mb += doc_memory_mb

                # 5. 접근 시간 초기화
                self._last_access_times[id(doc)] = time.time()

                logger.info(
                    "문서 추가: %s (%.2fMB, 총 %.2fMB)",
                    content_type,
                    doc_memory_mb,
                    self._current_memory_mb,
                )
                return True

        except (ValueError, TypeError, MemoryError) as e:
            logger.error("문서 추가 실패 (값/타입/메모리 에러): %s", str(e))
            return False
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.error("문서 추가 실패 (예상치 못한 에러): %s", str(e))
            return False

    def add_image(self, image_path: str, description: str = "") -> None:
        """Add an image document."""
        with contextlib.suppress(Exception):
            self.add_document(
                content=description or f"Image: {image_path}",
                content_type="image",
                metadata={"path": image_path},
            )

    def search(
        self, query: str, top_k: int = 5, content_types: list[str] | None = None
    ) -> list[MultimodalDocument]:
        """Search for relevant documents."""
        try:
            # Filter by content type if specified
            candidates = self.documents
            if content_types:
                candidates = [d for d in candidates if d.content_type in content_types]

            # Simple keyword matching (would use embeddings in production)
            query_lower = query.lower()
            scored = []
            for doc in candidates:
                score = sum(1 for word in query_lower.split() if word in doc.content.lower())
                if score > 0:
                    scored.append((score, doc))

            # Sort by score and return top_k
            scored.sort(key=lambda x: x[0], reverse=True)
            return [doc for _, doc in scored[:top_k]]
        except (AttributeError, ValueError, IndexError) as e:
            logger.warning("문서 검색 중 에러: %s", str(e))
            return []
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("문서 검색 중 예상치 못한 에러: %s", str(e))
            return []

    def retrieve_with_context(
        self, query: str, context: dict[str, Any] | None = None, top_k: int = 5
    ) -> dict[str, Any]:
        """Retrieve documents with context awareness."""
        try:
            results = self.search(query, top_k)
            return {
                "query": query,
                "results": results,
                "count": len(results),
                "context_used": context is not None,
            }
        except (AttributeError, ValueError) as e:
            logger.warning("컨텍스트 기반 검색 실패: %s", str(e))
            return {"error": str(e), "results": [], "count": 0}
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("컨텍스트 기반 검색 중 예상치 못한 에러: %s", str(e))
            return {"error": str(e), "results": [], "count": 0}

    def process_image(self, image_path: str) -> dict[str, Any]:
        """Process an image for RAG indexing."""
        try:
            path = Path(image_path)
            if not path.exists():
                logger.warning("이미지 파일 없음: %s", image_path)
                return {"error": f"Image not found: {image_path}"}

            return {
                "path": str(path),
                "name": path.name,
                "size": path.stat().st_size,
                "type": path.suffix,
                "indexed": True,
            }
        except (FileNotFoundError, OSError, PermissionError) as e:
            logger.warning("이미지 처리 실패 (파일 시스템 에러): %s", str(e))
            return {"error": str(e)}
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("이미지 처리 중 예상치 못한 에러: %s", str(e))
            return {"error": str(e)}

    def get_stats(self) -> dict[str, Any]:
        """
        엔진 통계 및 메모리 상태 반환 (Strangler Fig 메모리 모니터링)
        """
        try:
            type_counts: dict[str, int] = {}
            for doc in self.documents:
                type_counts[doc.content_type] = type_counts.get(doc.content_type, 0) + 1

            return {
                "total_documents": len(self.documents),
                "max_documents": _memory_config["max_documents"],
                "documents_utilization": len(self.documents) / _memory_config["max_documents"],
                "by_type": type_counts,
                "embedding_model": self.embedding_model,
                "memory_stats": {
                    "current_memory_mb": round(self._current_memory_mb, 2),
                    "max_memory_mb": _memory_config["max_memory_mb"],
                    "memory_utilization": round(
                        self._current_memory_mb / _memory_config["max_memory_mb"], 3
                    ),
                    "cleanup_threshold": _memory_config["cleanup_threshold"],
                    "lru_enabled": _memory_config["lru_enabled"],
                    "tracked_access_times": len(self._last_access_times),
                },
                "health_status": self._get_health_status(),
            }
        except (AttributeError, ValueError, KeyError) as e:
            logger.warning("통계 수집 실패: %s", str(e))
            return {"total_documents": 0, "error": "stats collection failed"}
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("통계 수집 중 예상치 못한 에러: %s", str(e))
            return {"total_documents": 0, "error": "stats collection failed"}

    def _get_health_status(self) -> str:
        """
        엔진 건강 상태 평가

        Returns:
            건강 상태 문자열
        """
        try:
            doc_util = len(self.documents) / _memory_config["max_documents"]
            mem_util = self._current_memory_mb / _memory_config["max_memory_mb"]

            if doc_util > 0.95 or mem_util > 0.95:
                return "critical"
            elif doc_util > 0.8 or mem_util > 0.8:
                return "warning"
            elif doc_util > 0.5 or mem_util > 0.5:
                return "normal"
            else:
                return "healthy"
        except (ZeroDivisionError, ValueError, TypeError) as e:
            logger.warning("건강 상태 평가 실패: %s", str(e))
            return "unknown"
        except Exception as e:  # - Intentional fallback for unexpected errors
            logger.debug("건강 상태 평가 중 예상치 못한 에러: %s", str(e))
            return "unknown"


# Default instance
multimodal_rag_engine = MultimodalRAGEngine()


def get_multimodal_engine() -> MultimodalRAGEngine:
    """Get the default multimodal RAG engine."""
    try:
        return multimodal_rag_engine
    except (AttributeError, NameError) as e:
        logger.warning("기본 엔진 인스턴스 접근 실패, 새 인스턴스 생성: %s", str(e))
        return MultimodalRAGEngine()
    except Exception as e:  # - Intentional fallback for unexpected errors
        logger.debug("엔진 인스턴스 접근 중 예상치 못한 에러: %s", str(e))
        return MultimodalRAGEngine()
