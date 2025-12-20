"""
Multimodal RAG Engine for AFO Kingdom (Phase 2)
Handles multimodal content (images, audio, video) in RAG pipelines.
"""

import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class MultimodalDocument:
    """A document that can contain text, images, or other media."""

    content: str
    content_type: str = "text"  # text, image, audio, video
    metadata: dict[str, Any] | None = None
    embedding: list[float] | None = None

    def __post_init__(self):
        try:
            if self.metadata is None:
                self.metadata = {}
        except Exception:
            self.metadata = {}


class MultimodalRAGEngine:
    """
    Multimodal RAG Engine supporting text, images, and other media.
    """

    def __init__(self, embedding_model: str = "default", **kwargs: Any):
        self.embedding_model = embedding_model
        self.documents: list[MultimodalDocument] = []
        self.supported_types = ["text", "image", "audio", "video"]

    def add_document(
        self, content: str, content_type: str = "text", metadata: dict[str, Any] | None = None
    ) -> None:
        """Add a document to the RAG index."""
        try:
            doc = MultimodalDocument(
                content=content, content_type=content_type, metadata=metadata or {}
            )
            self.documents.append(doc)
        except Exception:
            pass

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
        except Exception:
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
        except Exception as e:
            return {"error": str(e), "results": [], "count": 0}

    def process_image(self, image_path: str) -> dict[str, Any]:
        """Process an image for RAG indexing."""
        try:
            path = Path(image_path)
            if not path.exists():
                return {"error": f"Image not found: {image_path}"}

            return {
                "path": str(path),
                "name": path.name,
                "size": path.stat().st_size,
                "type": path.suffix,
                "indexed": True,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_stats(self) -> dict[str, Any]:
        """Get engine statistics."""
        try:
            type_counts: dict[str, int] = {}
            for doc in self.documents:
                type_counts[doc.content_type] = type_counts.get(doc.content_type, 0) + 1

            return {
                "total_documents": len(self.documents),
                "by_type": type_counts,
                "embedding_model": self.embedding_model,
            }
        except Exception:
            return {"total_documents": 0}


# Default instance
multimodal_rag_engine = MultimodalRAGEngine()


def get_multimodal_engine() -> MultimodalRAGEngine:
    """Get the default multimodal RAG engine."""
    try:
        return multimodal_rag_engine
    except Exception:
        return MultimodalRAGEngine()
