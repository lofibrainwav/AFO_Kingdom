# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Soul Engine Utilities

유틸리티 함수 및 클래스 모음
"""

from __future__ import annotations

from AFO.exponential_backoff import (
    BackoffStrategies,
    ExponentialBackoff,
    retry_with_exponential_backoff,
)

# Circuit Breaker (Phase 5: Monitoring)
try:
    from AFO.circuit_breaker import (
        CircuitBreaker,
        CircuitBreakerOpenError,
        CircuitState,
        get_all_circuit_statuses,
        ollama_circuit,
        qdrant_circuit,
        redis_circuit,
    )

    CIRCUIT_BREAKER_AVAILABLE = True
    # Only add to __all__ if successfully imported
    _circuit_breaker_items = [
        "CircuitBreaker",
        "CircuitBreakerOpenError",
        "CircuitState",
        "get_all_circuit_statuses",
        "ollama_circuit",
        "qdrant_circuit",
        "redis_circuit",
    ]
except ImportError:
    CIRCUIT_BREAKER_AVAILABLE = False
    CircuitBreaker = None
    CircuitBreakerOpenError = None
    CircuitState = None
    get_all_circuit_statuses = None
    ollama_circuit = None
    qdrant_circuit = None
    redis_circuit = None
    _circuit_breaker_items = []

# Prometheus Metrics (Phase 5: Monitoring)
try:
    from AFO.metrics import (
        MetricsMiddleware,
        create_metrics_router,
        get_metrics_response,
        track_llm_call,
        track_ollama_call,
        update_circuit_breaker_metrics,
        update_organ_health,
        update_trinity_scores,
    )

    METRICS_AVAILABLE = True
    # Only add to __all__ if successfully imported
    _metrics_items = [
        "MetricsMiddleware",
        "create_metrics_router",
        "get_metrics_response",
        "track_llm_call",
        "track_ollama_call",
        "update_circuit_breaker_metrics",
        "update_organ_health",
        "update_trinity_scores",
    ]
except ImportError:
    METRICS_AVAILABLE = False
    MetricsMiddleware = None
    create_metrics_router = None
    get_metrics_response = None
    track_llm_call = None
    track_ollama_call = None
    update_circuit_breaker_metrics = None
    update_organ_health = None
    update_trinity_scores = None
    _metrics_items = []

__all__ = [
    "CIRCUIT_BREAKER_AVAILABLE",
    "METRICS_AVAILABLE",
    "BackoffStrategies",
    "ExponentialBackoff",
    "retry_with_exponential_backoff",
] + _circuit_breaker_items + _metrics_items
