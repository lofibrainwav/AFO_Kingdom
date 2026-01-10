from __future__ import annotations

import pathlib
import socket
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

"""VERSION: FINAL_TRUTH_1"""


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


def _security_probe(repo_root: pathlib.Path | None = None) -> OrganReport:
    # Check for evidence of security scans using Root Anchor (Option A: Robust)
    sec_found = False
    sec_path = "None"

    candidates = []
    if repo_root:
        candidates = [
            repo_root / "trivy-results.json",
            repo_root / "logs" / "trivy-results.json",
            repo_root / "artifacts" / "trivy-results.json",
        ]
    else:
        # Fallback if no repo_root (should not happen with new logic, but safe)
        candidates = [
            pathlib.Path("trivy-results.json"),
            pathlib.Path("../../trivy-results.json"),
        ]

    ctx_file = next((p for p in candidates if p.exists()), None)
    if ctx_file:
        sec_found = True
        try:
            sec_path = str(ctx_file.relative_to(repo_root)) if repo_root else str(ctx_file)
        except ValueError:
            sec_path = str(ctx_file)

    return OrganReport(
        status="healthy" if sec_found else "unhealthy",
        score=90 if sec_found else 10,
        output=f"Security Scan Verified ({sec_path})"
        if sec_found
        else "No Security Evidence Found",
        probe="file:trivy-results.json",
        latency_ms=0,
    )


def build_organs_final(
    *,
    redis_host: str | None = None,
    redis_port: int = 6379,
    postgres_host: str | None = None,
    postgres_port: int = 5432,
    qdrant_host: str | None = None,
    qdrant_port: int = 6333,
    ollama_host: str | None = None,
    ollama_port: int = 11434,
    timeout_tcp_s: float = 0.35,
) -> dict[str, Any]:
    import os
    import pathlib

    # 1. Determine Repo Root (SSOT Anchor)
    # Using TICKETS.md as the kingdom root marker
    current_path = pathlib.Path(__file__).resolve()
    repo_root = None

    for parent in current_path.parents:
        if (parent / "TICKETS.md").exists():
            repo_root = parent
            break

    # 2. Config & Env + Infra Mode Detection (메타인지 최적화)
    def detect_infra_mode() -> str:
        """인프라 모드 자동 감지 (메타인지 기반)"""
        # 1. 명시적 설정 우선
        infra_mode = os.getenv("INFRA_MODE")
        if infra_mode:
            return infra_mode

        # 2. Docker 환경 감지
        if os.path.exists("/.dockerenv") or os.getenv("DOCKER_CONTAINER"):
            return "docker"

        # 3. 로컬 서비스 연결성으로 감지
        try:
            import socket
            with socket.create_connection(("localhost", 6379), timeout=0.1):
                return "local"
        except:
            pass

        # 4. 아무것도 없으면 minimal 모드
        return "minimal"

    infra_mode = detect_infra_mode()
    print(f"🔧 Infra Mode Detected: {infra_mode}", flush=True)

    # 모드별 기본 설정
    mode_configs = {
        "local": {
            "redis_host": "localhost",
            "postgres_host": "localhost",
            "timeout_tcp_s": 0.2,
            "skip_if_missing": False,
        },
        "docker": {
            "redis_host": "afo-redis",
            "postgres_host": "afo-postgres",
            "timeout_tcp_s": 0.35,
            "skip_if_missing": False,
        },
        "minimal": {
            "redis_host": "localhost",
            "postgres_host": "localhost",
            "timeout_tcp_s": 0.1,
            "skip_if_missing": True,  # 연결 실패해도 organ 점수 유지
        },
        "hybrid": {
            "redis_host": "afo-redis",  # Docker 우선
            "postgres_host": "localhost",  # 로컬 우선
            "timeout_tcp_s": 0.25,
            "skip_if_missing": False,
        }
    }

    mode_config = mode_configs.get(infra_mode, mode_configs["minimal"])
    timeout_tcp_s = mode_config["timeout_tcp_s"]

    try:
        from config.settings import get_settings

        settings = get_settings()
        redis_host = redis_host or settings.REDIS_HOST or os.getenv("REDIS_HOST", mode_config["redis_host"])
        postgres_host = (
            postgres_host or settings.POSTGRES_HOST or os.getenv("POSTGRES_HOST", mode_config["postgres_host"])
        )
        qdrant_host = qdrant_host or os.getenv("QDRANT_HOST", "afo-qdrant")
        # Extract hostname from OLLAMA_BASE_URL if available
        ollama_base = settings.OLLAMA_BASE_URL
        if ollama_base and "://" in ollama_base:
            ollama_host = ollama_host or ollama_base.split("://")[1].split(":")[0].split("/")[0]
        else:
            ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "afo-ollama")
    except ImportError:
        redis_host = redis_host or os.getenv("REDIS_HOST", mode_config["redis_host"])
        postgres_host = postgres_host or os.getenv("POSTGRES_HOST", mode_config["postgres_host"])
        qdrant_host = qdrant_host or os.getenv("QDRANT_HOST", "afo-qdrant")
        ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "afo-ollama")

    organs: dict[str, OrganReport] = {}

    # 3. Dynamic Host Probes (Environment Aware)
    ok, ms, t = _tcp_probe(redis_host, redis_port, timeout_tcp_s)
    organs["心_Redis"] = _mk(ok, ms, t, "tcp", 98, 40, "Connected", "Disconnected")

    ok, ms, t = _tcp_probe(postgres_host, postgres_port, timeout_tcp_s)
    organs["肝_PostgreSQL"] = _mk(ok, ms, t, "tcp", 99, 30, "Connected", "Disconnected")

    # ABSOLUTE TRUTH: Self-check (Brain) -> Honest Loopback/Env Probe
    # Using SOUL_ENGINE_HOST/PORT env vars to support Docker/K8s topologies
    soul_host = os.getenv("SOUL_ENGINE_HOST", "localhost")
    soul_port = int(os.getenv("SOUL_ENGINE_PORT", "8010"))

    ok, ms, t = _tcp_probe(soul_host, soul_port, 0.2)
    organs["腦_Soul_Engine"] = _mk(
        ok,
        ms,
        t,
        "self-tcp",
        100,
        0,
        "Sovereign Orchestration Active",
        f"Soul Engine Unresponsive ({soul_host}:{soul_port})",
    )

    # Print status for debug
    print(f"SOUL ENGINE STATUS: {organs['腦_Soul_Engine']}", flush=True)

    ok, ms, t = _tcp_probe(ollama_host, ollama_port, timeout_tcp_s)
    organs["舌_Ollama"] = _mk(ok, ms, t, "tcp", 95, 20, "Connected", "Disconnected")

    # 벡터 DB 건강도 체크 (환경변수 기반)
    vector_db_type = os.getenv("VECTOR_DB", "lancedb").lower()

    if vector_db_type == "lancedb":
        # LanceDB: 파일 기반 체크
        lancedb_path = os.getenv("LANCEDB_PATH", "./data/lancedb")
        lancedb_table = os.path.join(lancedb_path, "afokingdom_knowledge.lance")
        lancedb_ok = os.path.exists(lancedb_table)

        organs["肺_Vector_DB"] = _mk(
            lancedb_ok, 0, f"file:{lancedb_table}", "file",
            94, 20, "LanceDB Connected", "LanceDB Disconnected"
        )
    else:
        # Qdrant: TCP 기반 체크 (기존 호환성)
        ok, ms, t = _tcp_probe(qdrant_host, qdrant_port, timeout_tcp_s)
        organs["肺_Vector_DB"] = _mk(ok, ms, t, "tcp", 94, 20, "Qdrant Connected", "Qdrant Disconnected")

    # Dashboard: Defaults to localhost, fallback to docker hostname if needed
    dash_host = os.getenv("DASHBOARD_HOST", "localhost")
    dash_ok, dash_ms, dash_t = _tcp_probe(dash_host, 3000, timeout_tcp_s)
    # If explicit env not set/broken, try fallback
    if not dash_ok and dash_host == "localhost":
        dash_ok, dash_ms, dash_t = _tcp_probe("afo-dashboard", 3000, timeout_tcp_s)

    organs["眼_Dashboard"] = _mk(
        dash_ok, dash_ms, dash_t, "tcp", 92, 10, "Visual OK", "Dashboard Disconnected"
    )

    # MCP: Check configured servers count
    try:
        from config.health_check_config import health_check_config

        # Handle both list and object patterns for robustness
        if hasattr(health_check_config, "MCP_SERVERS"):
            mcp_count = len(health_check_config.MCP_SERVERS)
        else:
            mcp_count = len(getattr(health_check_config, "mcp_servers", []))

        mcp_score = 85 + (mcp_count * 2)
        if mcp_score > 98:
            mcp_score = 98
        mcp_msg = f"Active MCP: {mcp_count}"
        if mcp_count == 0:
            mcp_score = 40
            mcp_msg = "No MCP Configured"

        organs["腎_MCP"] = OrganReport(
            status="healthy" if mcp_count > 0 else "unhealthy",
            score=mcp_score,
            output=mcp_msg,
            probe="config:health_check_config",
            latency_ms=0,
        )
    except Exception as e:
        organs["腎_MCP"] = OrganReport(
            status="unhealthy", score=10, output=str(e), probe="error", latency_ms=0
        )

    # Observability: Check if Prometheus client is importable
    try:
        import prometheus_client

        organs["耳_Observability"] = OrganReport(
            status="healthy",
            score=90,
            output="Prometheus Client Loaded",
            probe="module:import",
            latency_ms=0,
        )
    except ImportError:
        organs["耳_Observability"] = OrganReport(
            status="unhealthy",
            score=20,
            output="Prometheus Missing",
            probe="module:import",
            latency_ms=0,
        )

    # 4. File Probes with Root Anchor (Robust)

    # Docs: Check existence of SSOT file (SSOT 永)
    if repo_root:
        ssot_file = repo_root / "docs" / "AFO_FINAL_SSOT.md"
        ssot_found = ssot_file.exists()
        ssot_msg = (
            f"SSOT Canon Found at {ssot_file}" if ssot_found else f"SSOT Missing at {ssot_file}"
        )
    else:
        ssot_found = False
        ssot_msg = "Repo Root Not Found"

    organs["口_Docs"] = OrganReport(
        status="healthy" if ssot_found else "unhealthy",
        score=95 if ssot_found else 10,
        output=ssot_msg,
        probe="file:docs/AFO_FINAL_SSOT.md",
        latency_ms=0,
    )

    # CI: Check for github/workflows directory (Self-awareness)
    ci_active = False
    if repo_root:
        ci_active = (repo_root / ".github" / "workflows").exists()

    organs["骨_CI"] = OrganReport(
        status="healthy" if ci_active else "unhealthy",
        score=90 if ci_active else 40,
        output="Workflows Active" if ci_active else "No Workflows",
        probe="fs:.github/workflows",
        latency_ms=0,
    )

    # Evolution Gate (Gallbladder)
    evo_active = False
    if repo_root:
        evo_active = (repo_root / "docs" / "AFO_EVOLUTION_LOG.md").exists()

    organs["胱_Evolution_Gate"] = OrganReport(
        status="healthy" if evo_active else "unhealthy",
        score=95 if evo_active else 30,
        output="Evolution Log Found" if evo_active else "Evolution Log Missing",
        probe="fs:docs/AFO_EVOLUTION_LOG.md",
        latency_ms=0,
    )

    # 5. Security (Immunity) - Separated from Organs to keep count at 11 (Option A)
    security_report = _security_probe(repo_root)

    # Define Explicit Contract (11 Keys)
    EXPECTED_ORGANS = [
        "心_Redis",
        "肝_PostgreSQL",
        "腦_Soul_Engine",
        "舌_Ollama",
        "肺_Vector_DB",
        "眼_Dashboard",
        "腎_MCP",
        "耳_Observability",
        "口_Docs",
        "骨_CI",
        "胱_Evolution_Gate",
    ]

    return {
        "ts": _now_iso(),
        "contract": {
            "version": "organs/v2",
            "organs_keys_expected": 11,
            "organs_keys": EXPECTED_ORGANS,
        },
        # Exclude Security from organs dict to match 11-Contract
        "organs": {k: asdict(v) for k, v in organs.items() if k in EXPECTED_ORGANS},
        # Pass Security separately for Goodness calculation (SSOT)
        "security": asdict(security_report),
    }
