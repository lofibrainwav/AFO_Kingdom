from __future__ import annotations

import socket
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timezone
from typing import Any, Optional
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
        # urlopen 보안 강화: http/https 스키마만 허용
        if not url.startswith(("http://", "https://")):
            return False, 0, f"Invalid scheme: {url}"

        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout_s) as resp:  # nosec B310
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


def _security_probe() -> OrganReport:
    import json
    import os
    from glob import glob

    base_dir = "/AFO/packages/afo-core/artifacts/ph19_security"
    latest_scan = sorted(glob(os.path.join(base_dir, "*")))
    if not latest_scan:
        return OrganReport("unknown", 50, "No security scans found", "security:scan", 0)

    latest_dir = latest_scan[-1]
    bandit_file = os.path.join(latest_dir, "bandit.json")
    pip_audit_file = os.path.join(latest_dir, "pip_audit.json")

    # Bandit score (Base 50, -5 per HIGH, -2 per MEDIUM)
    # Pip-Audit score (Base 50, -10 per VULN)
    score = 100
    details = []

    try:
        if os.path.exists(bandit_file):
            with open(bandit_file) as f:
                data = json.load(f)
                high = sum(1 for r in data.get("results", []) if r.get("issue_severity") == "HIGH")
                med = sum(1 for r in data.get("results", []) if r.get("issue_severity") == "MEDIUM")
                score -= (high * 10) + (med * 2)
                details.append(f"Bandit:{high}H/{med}M")
        else:
            score -= 10
            details.append("Bandit:Missing")

        if os.path.exists(pip_audit_file):
            with open(pip_audit_file) as f:
                data = json.load(f)
                vulns = sum(len(d.get("vulns", [])) for d in data.get("dependencies", []))
                # Exclude Windows-only nbconvert and pdfminer pickle if we want to be lenient,
                # but for perfection we keep them.
                score -= vulns * 15
                details.append(f"PipAudit:{vulns}V")
        else:
            score -= 10
            details.append("PipAudit:Missing")

    except Exception as e:
        details.append(f"Error:{e!s}")
        score = 0

    score = max(0, min(100, score))
    status = "healthy" if score >= 90 else "warning" if score >= 60 else "danger"

    return OrganReport(
        status=status,
        score=score,
        output=" | ".join(details),
        probe="security:gate",
        latency_ms=0,
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

    # Static / Semi-static Organs
    organs["眼_Dashboard"] = OrganReport(
        status="healthy", score=92, output="Visual OK", probe="static", latency_ms=0
    )

    organs["神経_MCP"] = OrganReport(
        status="healthy", score=85, output="Tools Active", probe="static", latency_ms=0
    )
    organs["耳_Observability"] = OrganReport(
        status="healthy", score=80, output="Listening", probe="static", latency_ms=0
    )
    organs["口_Docs"] = OrganReport(
        status="healthy", score=90, output="Manifesto OK", probe="static", latency_ms=0
    )
    organs["骨_CI"] = OrganReport(
        status="healthy", score=88, output="Pipeline Green", probe="static", latency_ms=0
    )

    # Security Pillar (PH19 Integration)
    organs["免疫_Trinity_Gate"] = _security_probe()

    return {
        "ts": _now_iso(),
        "contract": {"version": "organs/v2", "organs_keys_expected": 11},
        "organs": {k: asdict(v) for k, v in organs.items()},
    }
