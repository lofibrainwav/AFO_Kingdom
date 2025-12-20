"""
Prometheus Metrics for AFO Kingdom
Provides observability for the Soul Engine API.
"""

from __future__ import annotations

import time
from functools import wraps

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    print("⚠️ prometheus_client not installed. Run: pip install prometheus-client")

from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

if TYPE_CHECKING:
    from collections.abc import Callable

    from starlette.requests import Request

# ============================================================================
# Core Metrics Definition
# ============================================================================

if PROMETHEUS_AVAILABLE:
    from prometheus_client import REGISTRY

    def get_or_create_metric(metric_class, name, documentation, labelnames=(), **kwargs):
        """Helper to avoid duplicated timeseries error."""
        if name in REGISTRY._names_to_collectors:
            return REGISTRY._names_to_collectors[name]
        return metric_class(name, documentation, labelnames, **kwargs)

    # HTTP Request Metrics
    http_requests_total = get_or_create_metric(
        Counter,
        "afo_http_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "status_code"],
    )

    http_request_duration_seconds = get_or_create_metric(
        Histogram,
        "afo_http_request_duration_seconds",
        "HTTP request duration in seconds",
        ["method", "endpoint"],
        buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    )

    # Circuit Breaker Metrics
    circuit_breaker_state = get_or_create_metric(
        Gauge,
        "afo_circuit_breaker_state",
        "Circuit breaker state (0=CLOSED, 1=OPEN, 2=HALF_OPEN)",
        ["service"],
    )

    circuit_breaker_failures = get_or_create_metric(
        Counter, "afo_circuit_breaker_failures_total", "Total circuit breaker failures", ["service"]
    )

    # Ollama Metrics
    ollama_calls_total = get_or_create_metric(
        Counter,
        "afo_ollama_calls_total",
        "Total Ollama API calls",
        ["status", "model"],  # status: success, failure, timeout
    )

    ollama_request_duration_seconds = get_or_create_metric(
        Histogram,
        "afo_ollama_request_duration_seconds",
        "Ollama request duration in seconds",
        ["model"],
        buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
    )

    # LLM Routing Metrics
    llm_router_calls_total = get_or_create_metric(
        Counter,
        "afo_llm_router_calls_total",
        "Total LLM router calls",
        ["provider", "status"],  # provider: ollama, gemini, claude, openai
    )

    # CRAG Metrics
    crag_queries_total = get_or_create_metric(
        Counter,
        "afo_crag_queries_total",
        "Total CRAG queries",
        ["status"],  # status: success, no_docs, web_fallback
    )

    # Trinity Score Metrics
    trinity_score = get_or_create_metric(
        Gauge,
        "afo_trinity_score",
        "Current Trinity Score",
        ["pillar"],  # pillar: truth, goodness, beauty, serenity, eternity
    )

    trinity_score_total = get_or_create_metric(
        Gauge, "afo_trinity_score_total", "Total weighted Trinity Score"
    )

    # Health Metrics
    organ_health = get_or_create_metric(
        Gauge,
        "afo_organ_health",
        "Health status of organs (1=healthy, 0=unhealthy)",
        ["organ"],  # organ: redis, postgres, ollama, api_server
    )

    # Memory System Metrics
    memory_entries = get_or_create_metric(
        Gauge,
        "afo_memory_entries",
        "Number of memory entries",
        ["store"],  # store: short_term, long_term
    )

# ============================================================================
# Metrics Middleware
# ============================================================================


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically collect HTTP metrics."""

    async def dispatch(self, request: Request, call_next):
        if not PROMETHEUS_AVAILABLE:
            return await call_next(request)

        # Skip metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)

        start_time = time.perf_counter()
        status_code = 500  # Default in case of exception

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration = time.perf_counter() - start_time
            endpoint = self._normalize_endpoint(request.url.path)

            http_requests_total.labels(
                method=request.method, endpoint=endpoint, status_code=status_code
            ).inc()

            http_request_duration_seconds.labels(method=request.method, endpoint=endpoint).observe(
                duration
            )

    def _normalize_endpoint(self, path: str) -> str:
        """Normalize endpoint to avoid high cardinality."""
        # Replace UUIDs and IDs with placeholders
        parts = path.split("/")
        normalized = []
        for part in parts:
            # Check if it looks like an ID (UUID or numeric)
            if self._is_id(part):
                normalized.append("{id}")
            else:
                normalized.append(part)
        return "/".join(normalized)

    def _is_id(self, part: str) -> bool:
        """Check if a path part looks like an ID."""
        if not part:
            return False
        # UUID pattern
        if len(part) == 36 and part.count("-") == 4:
            return True
        # Numeric ID
        return bool(part.isdigit() and len(part) > 3)


# ============================================================================
# Decorator for Function Metrics
# ============================================================================


def track_ollama_call(model: str = "default"):
    """Decorator to track Ollama call metrics."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not PROMETHEUS_AVAILABLE:
                return await func(*args, **kwargs)

            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                ollama_calls_total.labels(status="success", model=model).inc()
                return result
            except TimeoutError:
                ollama_calls_total.labels(status="timeout", model=model).inc()
                raise
            except Exception:
                ollama_calls_total.labels(status="failure", model=model).inc()
                raise
            finally:
                duration = time.perf_counter() - start_time
                ollama_request_duration_seconds.labels(model=model).observe(duration)

        return wrapper

    return decorator


def track_llm_call(provider: str):
    """Decorator to track LLM router calls."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not PROMETHEUS_AVAILABLE:
                return await func(*args, **kwargs)

            try:
                result = await func(*args, **kwargs)
                llm_router_calls_total.labels(provider=provider, status="success").inc()
                return result
            except Exception:
                llm_router_calls_total.labels(provider=provider, status="failure").inc()
                raise

        return wrapper

    return decorator


# ============================================================================
# Circuit Breaker Metrics Integration
# ============================================================================


def update_circuit_breaker_metrics(service: str, state: str):
    """Update circuit breaker metrics."""
    if not PROMETHEUS_AVAILABLE:
        return

    state_value = {"closed": 0, "open": 1, "half_open": 2}.get(state.lower(), 0)
    circuit_breaker_state.labels(service=service).set(state_value)


def record_circuit_breaker_failure(service: str):
    """Record a circuit breaker failure."""
    if not PROMETHEUS_AVAILABLE:
        return

    circuit_breaker_failures.labels(service=service).inc()


# ============================================================================
# Health & Trinity Metrics
# ============================================================================


def update_organ_health(organ: str, is_healthy: bool):
    """Update organ health metric."""
    if not PROMETHEUS_AVAILABLE:
        return

    organ_health.labels(organ=organ).set(1 if is_healthy else 0)


def update_trinity_scores(scores: dict):
    """Update Trinity Score metrics."""
    if not PROMETHEUS_AVAILABLE:
        return

    for pillar, value in scores.items():
        if pillar != "total":
            trinity_score.labels(pillar=pillar).set(value)

    if "total" in scores:
        trinity_score_total.set(scores["total"])


def update_memory_metrics(short_term: int, long_term: int):
    """Update memory system metrics."""
    if not PROMETHEUS_AVAILABLE:
        return

    memory_entries.labels(store="short_term").set(short_term)
    memory_entries.labels(store="long_term").set(long_term)


# ============================================================================
# Metrics Endpoint Handler
# ============================================================================


async def get_metrics_response() -> Response:
    """Generate Prometheus metrics response."""
    if not PROMETHEUS_AVAILABLE:
        return Response(content="# prometheus_client not installed", media_type="text/plain")

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ============================================================================
# FastAPI Router
# ============================================================================


def create_metrics_router():
    """Create a FastAPI router for metrics endpoint."""
    from fastapi import APIRouter

    router = APIRouter(tags=["Metrics"])

    @router.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        return await get_metrics_response()

    return router
