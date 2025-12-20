"""
Prometheus Middleware for AFO Kingdom (Phase 20)
Collects metrics for all incoming requests: Latency, Count, Errors.
"""

import time

from fastapi import FastAPI, Request
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Metrics Definitions
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP request latency", ["endpoint"])
DB_CONNECTIONS = Gauge("db_connections", "Current DB connections")
TRINITY_SCORE = Gauge("trinity_score", "Current Trinity Score")
RISK_SCORE = Gauge("risk_score_current", "Current System Risk Score")


def setup_prometheus_metrics(app: FastAPI, port: int = 8001):
    """
    Starts Prometheus HTTP Server on separate port and adds middleware.
    """
    try:
        start_http_server(port)
        print(f"✅ Prometheus Metrics Exporter started on port {port}")
    except Exception as e:
        print(f"⚠️ Prometheus Exporter failed to start (might satisfy multiple workers): {e}")

    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        start_time = time.time()
        method = request.method
        # Simplify endpoint to avoid high cardinality
        endpoint = request.url.path

        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise e
        finally:
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()

        return response
