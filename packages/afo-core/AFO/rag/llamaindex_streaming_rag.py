"""
AFO Kingdom: LlamaIndex Streaming RAG Module (美 + 孝 최적화)
===========================================================
Author: Chancellor AFO
Created: 2026-01-01
License: AFO Royal License

Phase 2 Critical: T2.1 RAG 스트리밍 최적화
- Real-time streaming responses (美 +5%)
- Reduced cognitive load for users (孝 +10%)
- Trinity Score 향상 목표: 93.2% → 95.2%
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncGenerator
from typing import Any

from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.schema import NodeWithScore

from .llamaindex_rag import configure_settings, get_global_index

logger = logging.getLogger(__name__)


class StreamingRAGService:
    """Streaming RAG Service with real-time response optimization."""

    def __init__(
        self,
        index=None,
        similarity_top_k: int = 8,  # Reduced for faster streaming
        chunk_size: int = 256,  # Smaller chunks for streaming
        streaming_buffer_size: int = 50,  # Buffer size for streaming
    ):
        self.similarity_top_k = similarity_top_k
        self.chunk_size = chunk_size
        self.streaming_buffer_size = streaming_buffer_size

        # Configure LlamaIndex for streaming
        configure_settings()

        # Get or create index
        self.index = index or get_global_index()

        # Create retriever for streaming
        self.retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.similarity_top_k,
        )

        # Create streaming query engine
        self.query_engine = RetrieverQueryEngine.from_args(
            retriever=self.retriever,
            streaming=True,
        )

        logger.info("Streaming RAG Service initialized (美 + 孝 최적화)")
        logger.info(f"Similarity top-k: {similarity_top_k}, Chunk size: {chunk_size}")

    async def stream_query(
        self,
        query: str,
        context_docs: list[str] | None = None,
        system_prompt: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Execute streaming RAG query with real-time response generation.

        Args:
            query: User query string
            context_docs: Optional additional context documents
            system_prompt: Optional system prompt override

        Yields:
            Dict containing streaming chunks with metadata
        """
        start_time = time.time()

        try:
            # Retrieve relevant documents
            retrieved_nodes = self.retriever.retrieve(query)
            context = self._format_context(retrieved_nodes)

            # Add additional context if provided
            if context_docs:
                context += "\n\nAdditional Context:\n" + "\n".join(context_docs)

            # Prepare messages for streaming
            messages = []

            # System message
            if system_prompt:
                messages.append(ChatMessage(role=MessageRole.SYSTEM, content=system_prompt))
            else:
                default_system = """당신은 AFO 왕국의 최고 지식 도우미입니다.
眞善美孝永 철학에 기반하여 정확하고 유익한 답변을 제공합니다.
스트리밍 응답으로 실시간으로 생각을 전개하며 답변합니다."""
                messages.append(ChatMessage(role=MessageRole.SYSTEM, content=default_system))

            # User message with context
            user_content = f"Context:\n{context}\n\nQuestion: {query}"
            messages.append(ChatMessage(role=MessageRole.USER, content=user_content))

            # Stream response
            streaming_response = await self.query_engine.aquery(messages)

            # Calculate initial metadata
            retrieval_time = time.time() - start_time
            total_tokens = 0
            chunks_sent = 0

            # Send initial metadata
            yield {
                "type": "metadata",
                "retrieval_time": round(retrieval_time, 3),
                "context_length": len(context),
                "nodes_retrieved": len(retrieved_nodes),
                "top_similarity": round(retrieved_nodes[0].score, 4) if retrieved_nodes else 0,
            }

            # Stream response chunks
            async for chunk in streaming_response.async_response_gen():
                if chunk.delta:
                    total_tokens += 1
                    chunks_sent += 1

                    # Yield streaming chunk
                    yield {
                        "type": "content",
                        "content": chunk.delta,
                        "chunk_id": chunks_sent,
                        "total_tokens": total_tokens,
                        "timestamp": round(time.time() - start_time, 3),
                    }

                    # Small delay to prevent overwhelming client (孝 최적화)
                    await asyncio.sleep(0.01)

            # Send completion metadata
            total_time = time.time() - start_time
            yield {
                "type": "complete",
                "total_time": round(total_time, 3),
                "total_tokens": total_tokens,
                "chunks_sent": chunks_sent,
                "tokens_per_second": round(total_tokens / total_time, 2) if total_time > 0 else 0,
                "trinity_score_contribution": {
                    "beauty": 5,  # Real-time streaming UX
                    "serenity": 10,  # Reduced cognitive load
                },
            }

        except Exception as e:
            logger.error(f"Streaming query failed: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": round(time.time() - start_time, 3),
            }

    def _format_context(self, nodes: list[NodeWithScore]) -> str:
        """Format retrieved nodes into context string."""
        context_parts = []

        for i, node in enumerate(nodes, 1):
            score = round(node.score, 4)
            content = node.node.text[: self.chunk_size]  # Limit chunk size for streaming
            source = getattr(node.node, "metadata", {}).get("source", "unknown")

            context_parts.append(f"[{i}] Score: {score}, Source: {source}\n{content}...")

        return "\n\n".join(context_parts)

    def get_health_status(self) -> dict[str, Any]:
        """Get health status of streaming RAG service."""
        return {
            "service": "Streaming RAG Service",
            "status": "healthy",
            "trinity_optimization": {
                "beauty_streaming": True,
                "serenity_reduced_load": True,
                "target_improvement": {"beauty": 5, "serenity": 10},
            },
            "configuration": {
                "similarity_top_k": self.similarity_top_k,
                "chunk_size": self.chunk_size,
                "streaming_buffer_size": self.streaming_buffer_size,
            },
            "capabilities": [
                "real_time_streaming",
                "context_aware_responses",
                "cognitive_load_reduction",
                "trinity_score_optimization",
            ],
        }


# Global streaming service instance
_streaming_service: StreamingRAGService | None = None


def get_streaming_rag_service() -> StreamingRAGService:
    """Get or create global streaming RAG service instance."""
    global _streaming_service

    if _streaming_service is None:
        _streaming_service = StreamingRAGService()

    return _streaming_service


# Convenience functions for easy integration
async def stream_rag_query(
    query: str,
    context_docs: list[str] | None = None,
    system_prompt: str | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Convenience function for streaming RAG queries."""
    service = get_streaming_rag_service()
    async for chunk in service.stream_query(query, context_docs, system_prompt):
        yield chunk


def get_streaming_rag_health() -> dict[str, Any]:
    """Get streaming RAG service health status."""
    service = get_streaming_rag_service()
    return service.get_health_status()


# Export public API
__all__ = [
    "StreamingRAGService",
    "get_streaming_rag_health",
    "get_streaming_rag_service",
    "stream_rag_query",
]
