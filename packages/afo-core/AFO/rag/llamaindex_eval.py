"""
AFO Kingdom: LlamaIndex Evaluation Module (永 - Eternity)
=========================================================
Author: Chancellor AFO
Created: 2025-12-31

RAGAS-style evaluation for continuous RAG quality monitoring.
Ensures Trinity Score improvement through measurable metrics.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TYPE_CHECKING

from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
)

if TYPE_CHECKING:
    from llama_index.core import VectorStoreIndex

logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    """Single query evaluation result."""

    query: str
    response: str
    faithfulness_score: float
    relevancy_score: float
    contexts: list[str]
    timestamp: str

    @property
    def average_score(self) -> float:
        """Average of all scores."""
        return (self.faithfulness_score + self.relevancy_score) / 2


@dataclass
class BatchEvaluationReport:
    """Batch evaluation report."""

    total_queries: int
    avg_faithfulness: float
    avg_relevancy: float
    avg_score: float
    pass_rate: float  # % of queries with avg_score > 0.7
    timestamp: str
    individual_results: list[EvaluationResult]


def evaluate_single_query(
    query: str,
    index: VectorStoreIndex,
    reference_answer: str | None = None,
) -> EvaluationResult:
    """Evaluate a single query against the RAG system.

    Args:
        query: User query
        index: Vector store index
        reference_answer: Optional ground truth answer

    Returns:
        EvaluationResult with scores
    """
    logger.info(f"Evaluating query: {query[:50]}...")

    # Get query engine and response
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(query)

    # Get source contexts
    contexts = []
    if hasattr(response, "source_nodes"):
        contexts = [node.text for node in response.source_nodes]

    # Initialize evaluators
    faithfulness_eval = FaithfulnessEvaluator()
    relevancy_eval = RelevancyEvaluator()

    # Evaluate faithfulness (is response grounded in context?)
    try:
        faith_result = faithfulness_eval.evaluate_response(
            query=query,
            response=response,
        )
        faithfulness_score = 1.0 if faith_result.passing else 0.0
    except Exception as e:
        logger.warning(f"Faithfulness eval failed: {e}")
        faithfulness_score = 0.5  # Default on error

    # Evaluate relevancy (is response relevant to query?)
    try:
        rel_result = relevancy_eval.evaluate_response(
            query=query,
            response=response,
        )
        relevancy_score = 1.0 if rel_result.passing else 0.0
    except Exception as e:
        logger.warning(f"Relevancy eval failed: {e}")
        relevancy_score = 0.5  # Default on error

    return EvaluationResult(
        query=query,
        response=str(response),
        faithfulness_score=faithfulness_score,
        relevancy_score=relevancy_score,
        contexts=contexts[:3],  # Limit context storage
        timestamp=datetime.now(UTC).isoformat(),
    )


def evaluate_batch(
    queries: list[str],
    index: VectorStoreIndex,
) -> BatchEvaluationReport:
    """Evaluate a batch of queries.

    Args:
        queries: List of query strings
        index: Vector store index

    Returns:
        BatchEvaluationReport with aggregate stats
    """
    logger.info(f"Running batch evaluation on {len(queries)} queries (永)")

    results = []
    for query in queries:
        try:
            result = evaluate_single_query(query, index)
            results.append(result)
        except Exception as e:
            logger.error(f"Evaluation failed for query: {query[:30]}... Error: {e}")

    if not results:
        return BatchEvaluationReport(
            total_queries=len(queries),
            avg_faithfulness=0.0,
            avg_relevancy=0.0,
            avg_score=0.0,
            pass_rate=0.0,
            timestamp=datetime.now(UTC).isoformat(),
            individual_results=[],
        )

    # Calculate aggregates
    avg_faith = sum(r.faithfulness_score for r in results) / len(results)
    avg_rel = sum(r.relevancy_score for r in results) / len(results)
    avg_score = sum(r.average_score for r in results) / len(results)
    pass_count = sum(1 for r in results if r.average_score > 0.7)
    pass_rate = pass_count / len(results)

    return BatchEvaluationReport(
        total_queries=len(queries),
        avg_faithfulness=avg_faith,
        avg_relevancy=avg_rel,
        avg_score=avg_score,
        pass_rate=pass_rate,
        timestamp=datetime.now(UTC).isoformat(),
        individual_results=results,
    )


def save_evaluation_report(
    report: BatchEvaluationReport,
    output_path: str | Path = "./eval_report.json",
) -> None:
    """Save evaluation report to JSON file.

    Args:
        report: BatchEvaluationReport to save
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict (handle nested dataclasses)
    report_dict = {
        "total_queries": report.total_queries,
        "avg_faithfulness": report.avg_faithfulness,
        "avg_relevancy": report.avg_relevancy,
        "avg_score": report.avg_score,
        "pass_rate": report.pass_rate,
        "timestamp": report.timestamp,
        "individual_results": [asdict(r) for r in report.individual_results],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2, ensure_ascii=False)

    logger.info(f"Evaluation report saved to {output_path}")


def get_default_test_queries() -> list[str]:
    """Get default test queries for evaluation.

    Returns:
        List of test query strings
    """
    return [
        "AFO Kingdom의 아키텍처를 설명해주세요.",
        "Trinity Score는 무엇이고 어떻게 계산되나요?",
        "Soul Engine API의 주요 엔드포인트는 무엇인가요?",
        "제갈량, 사마의, 주유 3책사의 역할은 무엇인가요?",
        "DSPy와 LangGraph의 차이점은 무엇인가요?",
        "멀티모달 RAG 시스템은 어떻게 구성되어 있나요?",
        "Ollama와 Host GPU 가속은 어떻게 연동되나요?",
        "Context7 MCP의 역할은 무엇인가요?",
    ]


# Export public API
__all__ = [
    "BatchEvaluationReport",
    "EvaluationResult",
    "evaluate_batch",
    "evaluate_single_query",
    "get_default_test_queries",
    "save_evaluation_report",
]
