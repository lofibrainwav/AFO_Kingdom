"""
AFO Kingdom: LlamaIndex RAG Package
====================================
Unified exports for LlamaIndex Multimodal Hybrid RAG system.
"""

from AFO.rag.llamaindex_eval import (
    BatchEvaluationReport,
    EvaluationResult,
    evaluate_batch,
    evaluate_single_query,
    get_default_test_queries,
    save_evaluation_report,
)
from AFO.rag.llamaindex_hybrid import (
    create_hybrid_query_engine,
    create_sub_question_engine,
    get_alpha_for_query,
    query_with_auto_alpha,
)
from AFO.rag.llamaindex_rag import (
    build_index,
    configure_settings,
    create_query_engine,
    get_chroma_client,
    get_global_index,
    query,
)
from AFO.rag.llamaindex_reranker import (
    create_reranked_query_engine,
    create_similarity_filtered_engine,
    rerank_results,
)
from AFO.rag.llamaindex_vision import (
    analyze_image,
    analyze_images_batch,
    get_vision_models,
)

__all__ = [
    # Core RAG
    "configure_settings",
    "build_index",
    "create_query_engine",
    "query",
    "get_global_index",
    "get_chroma_client",
    # Vision
    "analyze_image",
    "analyze_images_batch",
    "get_vision_models",
    # Hybrid Search
    "create_hybrid_query_engine",
    "get_alpha_for_query",
    "create_sub_question_engine",
    "query_with_auto_alpha",
    # Reranker
    "create_reranked_query_engine",
    "create_similarity_filtered_engine",
    "rerank_results",
    # Evaluation
    "EvaluationResult",
    "BatchEvaluationReport",
    "evaluate_single_query",
    "evaluate_batch",
    "save_evaluation_report",
    "get_default_test_queries",
]
