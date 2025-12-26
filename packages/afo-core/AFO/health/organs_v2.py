from __future__ import annotations

import socket
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timezone
from typing import Any, Dict, Optional, Tuple
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class OrganReport:
    status: str
    score: int
    output: str
    probe: str
    latency_ms: int


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _tcp_probe(host: str, port: int, timeout_s: float) -> tuple[bool, int, str]:
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            ms = int((time.perf_counter() - t0) * 1000)
            return True, ms, f"tcp://{host}:{port}"
    except Exception:
        ms = int((time.perf_counter() - t0) * 1000)
        return False, ms, f"tcp://{host}:{port}"


def _http_probe(url: str, timeout_s: float) -> tuple[bool, int, str]:
    t0 = time.perf_counter()
    try:
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout_s) as resp:
            ok = 200 <= int(resp.status) < 400
        ms = int((time.perf_counter() - t0) * 1000)
        return ok, ms, url
    except Exception:
        ms = int((time.perf_counter() - t0) * 1000)
        return False, ms, url


def _mk(
    ok: bool,
    ms: int,
    target: str,
    probe: str,
    ok_score: int,
    bad_score: int,
    ok_msg: str,
    bad_msg: str,
) -> OrganReport:
    if ok:
        return OrganReport(
            status="healthy",
            score=ok_score,
            output=ok_msg,
            probe=f"{probe}:{target}",
            latency_ms=ms,
        )
    return OrganReport(
        status="disconnected",
        score=bad_score,
        output=bad_msg,
        probe=f"{probe}:{target}",
        latency_ms=ms,
    )


def build_organs_v2(
    *,
    host_local: str = "127.0.0.1",
    redis_port: int = 6379,
    postgres_port: int = 5432,
    qdrant_port: int = 6333,
    ollama_port: int = 11434,
    dashboard_port: int = 3000,
    api_port: int = 8010,
    timeout_tcp_s: float = 0.35,
    timeout_http_s: float = 0.6,
) -> dict[str, Any]:
    organs: dict[str, OrganReport] = {}

    ok, ms, t = _tcp_probe(host_local, redis_port, timeout_tcp_s)
    organs["心_Redis"] = _mk(ok, ms, t, "tcp", 98, 40, "Connected", "Disconnected")

    ok, ms, t = _tcp_probe(host_local, postgres_port, timeout_tcp_s)
    organs["肝_PostgreSQL"] = _mk(ok, ms, t, "tcp", 99, 30, "Connected", "Disconnected")

    ok, ms, t = _http_probe(f"http://{host_local}:{api_port}/health", timeout_http_s)
    organs["肺_API_Server"] = _mk(ok, ms, t, "http", 100, 0, "HTTP OK", "No Signal")

    ok, ms, t = _tcp_probe(host_local, ollama_port, timeout_tcp_s)
    organs["脾_Ollama"] = _mk(ok, ms, t, "tcp", 95, 20, "Connected", "Disconnected")

    ok, ms, t = _tcp_probe(host_local, qdrant_port, timeout_tcp_s)
    organs["腎_Qdrant"] = _mk(ok, ms, t, "tcp", 94, 20, "Connected", "Disconnected")

    ok, ms, t = _http_probe(
        f"http://{host_local}:{dashboard_port}/api/kingdom-status", timeout_http_s
    )
    organs["眼_Dashboard"] = _mk(ok, ms, t, "http", 92, 20, "HTTP OK", "No Signal")

    organs["神経_MCP"] = OrganReport(
        status="unknown", score=50, output="Not Probed", probe="static", latency_ms=0
    )
    organs["耳_Observability"] = OrganReport(
        status="unknown", score=50, output="Not Probed", probe="static", latency_ms=0
    )
    organs["口_Docs"] = OrganReport(
        status="unknown", score=50, output="Not Probed", probe="static", latency_ms=0
    )
    organs["骨_CI"] = OrganReport(
        status="unknown", score=50, output="Not Probed", probe="static", latency_ms=0
    )
    organs["免疫_Trinity_Gate"] = OrganReport(
        status="unknown", score=50, output="Not Probed", probe="static", latency_ms=0
    )

    return {
        "ts": _now_iso(),
        "contract": {"version": "organs/v2", "organs_keys_expected": 11},
        "organs": {k: asdict(v) for k, v in organs.items()},
    }
