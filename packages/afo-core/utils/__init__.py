"""
AFO Soul Engine Utilities

유틸리티 함수 및 클래스 모음
"""

from __future__ import annotations

from .exponential_backoff import (
    BackoffStrategies,
    ExponentialBackoff,
    retry_with_exponential_backoff,
)

# Circuit Breaker (Phase 5: Monitoring)
try:
    from .circuit_breaker import (
        CircuitBreaker,
        CircuitBreakerOpenError,
        CircuitState,
        ollama_circuit,
        qdrant_circuit,
        redis_circuit,
        get_all_circuit_statuses,
    )
    CIRCUIT_BREAKER_AVAILABLE = True
except ImportError:
    CIRCUIT_BREAKER_AVAILABLE = False

# Prometheus Metrics (Phase 5: Monitoring)
try:
    from .metrics import (
        MetricsMiddleware,
        track_ollama_call,
        track_llm_call,
        update_circuit_breaker_metrics,
        update_organ_health,
        update_trinity_scores,
        get_metrics_response,
        create_metrics_router,
    )
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False

__all__ = [
    "BackoffStrategies",
    "ExponentialBackoff",
    "retry_with_exponential_backoff",
    "CircuitBreaker",
    "CircuitBreakerOpenError",
    "CircuitState",
    "ollama_circuit",
    "qdrant_circuit",
    "redis_circuit",
    "get_all_circuit_statuses",
    "MetricsMiddleware",
    "track_ollama_call",
    "track_llm_call",
    "update_circuit_breaker_metrics",
    "update_organ_health",
    "update_trinity_scores",
    "get_metrics_response",
    "create_metrics_router",
    "CIRCUIT_BREAKER_AVAILABLE",
    "METRICS_AVAILABLE",
]
