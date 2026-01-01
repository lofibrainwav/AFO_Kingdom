"""
AFO Kingdom: LlamaIndex RAG Package
====================================
Unified exports for LlamaIndex Multimodal Hybrid RAG system.
"""

from afo.rag.llamaindex_eval import (
    BatchEvaluationReport,
    EvaluationResult,
    evaluate_batch,
    evaluate_single_query,
    get_default_test_queries,
    save_evaluation_report,
)
from afo.rag.llamaindex_hybrid import (
    create_hybrid_query_engine,
    create_sub_question_engine,
    get_alpha_for_query,
    query_with_auto_alpha,
)
from afo.rag.llamaindex_rag import (
    build_index,
    configure_settings,
    create_query_engine,
    get_chroma_client,
    get_global_index,
    query,
)
from afo.rag.llamaindex_reranker import (
    create_reranked_query_engine,
    create_similarity_filtered_engine,
    rerank_results,
)
from afo.rag.llamaindex_vision import analyze_image, analyze_images_batch, get_vision_models

__all__ = [
    "BatchEvaluationReport",
    # Evaluation
    "EvaluationResult",
    # Vision
    "analyze_image",
    "analyze_images_batch",
    "build_index",
    # Core RAG
    "configure_settings",
    # Hybrid Search
    "create_hybrid_query_engine",
    "create_query_engine",
    # Reranker
    "create_reranked_query_engine",
    "create_similarity_filtered_engine",
    "create_sub_question_engine",
    "evaluate_batch",
    "evaluate_single_query",
    "get_alpha_for_query",
    "get_chroma_client",
    "get_default_test_queries",
    "get_global_index",
    "get_vision_models",
    "query",
    "query_with_auto_alpha",
    "rerank_results",
    "save_evaluation_report",
]
