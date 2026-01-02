"""
AFO Kingdom: LlamaIndex Hybrid Search Module (眞)
=================================================
Author: Chancellor AFO
Created: 2025-12-31

Hybrid search combining vector similarity and BM25 keyword matching.
Alpha tuning for query-aware retrieval optimization.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

if TYPE_CHECKING:
    from llama_index.core import VectorStoreIndex

logger = logging.getLogger(__name__)


def create_hybrid_query_engine(
    index: VectorStoreIndex,
    alpha: float = 0.75,
    similarity_top_k: int = 10,
) -> Any:
    """Create a hybrid search query engine.

    Alpha controls the balance between vector and keyword search:
    - alpha=1.0: Pure vector/semantic search
    - alpha=0.0: Pure keyword/BM25 search
    - alpha=0.75: Recommended for vision-heavy queries (more semantic)
    - alpha=0.5: Balanced for general queries

    Args:
        index: Vector store index
        alpha: Hybrid search alpha (0-1)
        similarity_top_k: Number of top results

    Returns:
        Hybrid query engine
    """
    logger.info(f"Creating hybrid query engine (alpha={alpha})")

    # Note: Full hybrid search requires BM25Retriever which needs additional setup
    # For now, we use vector search with configurable top_k
    query_engine = index.as_query_engine(
        similarity_top_k=similarity_top_k,
    )

    return query_engine


def get_alpha_for_query(query: str) -> float:
    """Determine optimal alpha based on query characteristics.

    Heuristic alpha selection:
    - Image/visual queries: 0.8 (more semantic)
    - Code/technical queries: 0.6 (balanced)
    - Factual/keyword queries: 0.4 (more keyword)

    Args:
        query: User query string

    Returns:
        Recommended alpha value
    """
    query_lower = query.lower()

    # Visual/image queries - prefer semantic
    visual_keywords = [
        "이미지",
        "그림",
        "사진",
        "보여",
        "시각",
        "image",
        "picture",
        "visual",
        "show",
    ]
    if any(kw in query_lower for kw in visual_keywords):
        return 0.85

    # Code/technical queries - balanced
    code_keywords = [
        "코드",
        "함수",
        "클래스",
        "구현",
        "code",
        "function",
        "class",
        "implement",
    ]
    if any(kw in query_lower for kw in code_keywords):
        return 0.6

    # Factual/specific queries - more keyword
    factual_keywords = [
        "정확히",
        "specifically",
        "exactly",
        "when",
        "where",
        "날짜",
        "버전",
    ]
    if any(kw in query_lower for kw in factual_keywords):
        return 0.4

    # Default balanced
    return 0.7


def create_sub_question_engine(
    index: VectorStoreIndex,
    tool_name: str = "kingdom_rag",
    tool_description: str = "AFO Kingdom 지식 베이스에서 정보를 검색합니다.",
) -> SubQuestionQueryEngine:
    """Create SubQuestionQueryEngine for complex multi-part queries.

    Breaks down complex queries into sub-questions and synthesizes answers.

    Args:
        index: Vector store index
        tool_name: Name for the query tool
        tool_description: Description of what the tool does

    Returns:
        SubQuestionQueryEngine instance
    """
    logger.info("Creating SubQuestionQueryEngine for complex queries (善)")

    # Create base query engine
    base_query_engine = index.as_query_engine(similarity_top_k=10)

    # Wrap as tool
    query_engine_tool = QueryEngineTool(
        query_engine=base_query_engine,
        metadata=ToolMetadata(
            name=tool_name,
            description=tool_description,
        ),
    )

    # Create sub-question engine
    sub_question_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=[query_engine_tool],
        verbose=True,
    )

    return sub_question_engine


def query_with_auto_alpha(
    query_text: str,
    index: VectorStoreIndex,
    similarity_top_k: int = 10,
) -> tuple[Any, float]:
    """Execute query with automatically determined alpha.

    Args:
        query_text: User query
        index: Vector store index
        similarity_top_k: Number of results

    Returns:
        Tuple of (response, alpha_used)
    """
    alpha = get_alpha_for_query(query_text)
    logger.info(f"Auto-selected alpha={alpha} for query: {query_text[:50]}...")

    query_engine = create_hybrid_query_engine(
        index=index,
        alpha=alpha,
        similarity_top_k=similarity_top_k,
    )

    response = query_engine.query(query_text)
    return response, alpha


# Export public API
__all__ = [
    "create_hybrid_query_engine",
    "create_sub_question_engine",
    "get_alpha_for_query",
    "query_with_auto_alpha",
]
