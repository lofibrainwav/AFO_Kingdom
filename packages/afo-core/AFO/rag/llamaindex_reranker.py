"""
AFO Kingdom: LlamaIndex Reranker Module (眞)
============================================
Author: Chancellor AFO
Created: 2025-12-31

LLM-based reranking for improved retrieval precision.
"""

from __future__ import annotations

import logging
from typing import Any

from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import LLMRerank, SimilarityPostprocessor

logger = logging.getLogger(__name__)


def create_reranked_query_engine(
    index: VectorStoreIndex,
    top_n_initial: int = 10,
    top_n_final: int = 3,
    rerank_model: str | None = None,
) -> Any:
    """Create query engine with LLM-based reranking.

    Two-stage retrieval:
    1. Initial retrieval: Get top_n_initial candidates
    2. Rerank: Use LLM to select top_n_final most relevant

    Args:
        index: Vector store index
        top_n_initial: Number of candidates for initial retrieval
        top_n_final: Number of results after reranking
        rerank_model: Optional specific model for reranking

    Returns:
        Reranked query engine
    """
    logger.info(f"Creating reranked query engine (top_k={top_n_initial} → top_n={top_n_final})")

    # LLM Reranker - uses the configured Settings.llm
    reranker = LLMRerank(
        top_n=top_n_final,
    )

    # Similarity threshold postprocessor (fallback filter)
    similarity_filter = SimilarityPostprocessor(
        similarity_cutoff=0.5,  # Minimum similarity score
    )

    query_engine = index.as_query_engine(
        similarity_top_k=top_n_initial,
        node_postprocessors=[similarity_filter, reranker],
    )

    return query_engine


def create_similarity_filtered_engine(
    index: VectorStoreIndex,
    similarity_cutoff: float = 0.6,
    top_k: int = 10,
) -> Any:
    """Create query engine with similarity threshold filtering.

    Args:
        index: Vector store index
        similarity_cutoff: Minimum similarity score (0-1)
        top_k: Number of results

    Returns:
        Filtered query engine
    """
    logger.info(f"Creating similarity-filtered engine (cutoff={similarity_cutoff})")

    postprocessor = SimilarityPostprocessor(
        similarity_cutoff=similarity_cutoff,
    )

    query_engine = index.as_query_engine(
        similarity_top_k=top_k,
        node_postprocessors=[postprocessor],
    )

    return query_engine


def rerank_results(
    query: str,
    nodes: list[Any],
    top_n: int = 3,
) -> list[Any]:
    """Manually rerank a list of retrieved nodes.

    Args:
        query: Original query
        nodes: List of retrieved nodes
        top_n: Number of results to return

    Returns:
        Reranked nodes list
    """
    if not nodes:
        return []

    reranker = LLMRerank(top_n=top_n)

    logger.info(f"Reranking {len(nodes)} nodes → top {top_n}")

    # Create mock query bundle for reranking
    from llama_index.core.schema import QueryBundle

    query_bundle = QueryBundle(query_str=query)

    reranked = reranker.postprocess_nodes(
        nodes=nodes,
        query_bundle=query_bundle,
    )

    return reranked


# Export public API
__all__ = [
    "create_reranked_query_engine",
    "create_similarity_filtered_engine",
    "rerank_results",
]
