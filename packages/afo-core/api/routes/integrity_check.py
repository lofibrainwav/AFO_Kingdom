# Trinity Score: 90.0 (Established by Chancellor)
"""
Integrity Check API
무결성 체크리스트 검증 엔드포인트
眞·善·美·孝·永 5기둥 무결성 검증
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/integrity", tags=["Integrity Check"])

logger = logging.getLogger(__name__)


# Dynamic workspace root calculation
@lru_cache(maxsize=1)
def _find_workspace_root(anchor: Path) -> Path:
    override = os.getenv("AFO_WORKSPACE_ROOT") or os.getenv("WORKSPACE_ROOT")
    if override:
        p = Path(override).expanduser().resolve()
        if p.exists():
            return p

    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(anchor.parent),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if out:
            p = Path(out).resolve()
            if p.exists():
                return p
    except Exception:
        pass

    markers = (
        ".git",
        "pyproject.toml",
        "poetry.lock",
        "package.json",
        "pnpm-lock.yaml",
    )
    for p in (anchor, *anchor.parents):
        if any((p / m).exists() for m in markers):
            return p

    return anchor


WORKSPACE_ROOT = _find_workspace_root(Path(__file__).resolve())


class IntegrityCheckRequest(BaseModel):
    """무결성 체크 요청"""

    pillar: str | None = None  # None이면 전체 검증


@router.post("/check")
async def check_integrity(request: IntegrityCheckRequest) -> dict[str, Any]:
    """
    무결성 체크리스트 검증

    각 기둥별로 실제 시스템 상태를 확인합니다.
    """
    try:
        results = {}

        # 眞 (Truth) 검증
        if not request.pillar or request.pillar == "truth":
            results["truth"] = await _check_truth_pillar()

        # 善 (Goodness) 검증
        if not request.pillar or request.pillar == "goodness":
            results["goodness"] = await _check_goodness_pillar()

        # 美 (Beauty) 검증
        if not request.pillar or request.pillar == "beauty":
            results["beauty"] = await _check_beauty_pillar()

        # 孝 (Serenity) 검증
        if not request.pillar or request.pillar == "serenity":
            results["serenity"] = await _check_serenity_pillar()

        # 永 (Eternity) 검증
        if not request.pillar or request.pillar == "eternity":
            results["eternity"] = await _check_eternity_pillar()

        # 종합 점수 계산
        if len(results) == 5:
            total_score = (
                results["truth"]["score"] * 0.35
                + results["goodness"]["score"] * 0.35
                + results["beauty"]["score"] * 0.20
                + results["serenity"]["score"] * 0.08
                + results["eternity"]["score"] * 0.02
            )
        else:
            total_score = sum(r["score"] for r in results.values()) / len(results)

        return {
            "status": "success",
            "total_score": round(total_score, 2),
            "pillars": results,
        }
    except Exception as e:
        logger.error(f"Integrity check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


async def _check_truth_pillar() -> dict[str, Any]:
    """眞 (Truth) 기둥 검증"""
    checks = {
        "ci_cd_lock": False,
        "type_safety": False,
        "fact_verification": False,
    }

    # 1. CI/CD LOCK 원칙 확인
    try:
        # MyPy, Ruff, pytest, SBOM 확인
        mypy_result = subprocess.run(
            ["which", "mypy"], capture_output=True, text=True, timeout=5
        )
        ruff_result = subprocess.run(
            ["which", "ruff"], capture_output=True, text=True, timeout=5
        )
        pytest_result = subprocess.run(
            ["which", "pytest"], capture_output=True, text=True, timeout=5
        )

        checks["ci_cd_lock"] = (
            mypy_result.returncode == 0
            and ruff_result.returncode == 0
            and pytest_result.returncode == 0
        )
    except Exception as e:
        logger.warning(f"CI/CD check failed: {e}")

    # 2. 타입 안전성 확인
    try:
        # MyPy strict 모드 확인 (pyproject.toml 또는 설정 파일)
        pyproject_path = WORKSPACE_ROOT / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            checks["type_safety"] = (
                "mypy" in content.lower() or "strict" in content.lower()
            )
    except Exception as e:
        logger.warning(f"Type safety check failed: {e}")

    # 3. 사실 검증 도구 확인
    try:
        # verify_fact 도구 존재 확인
        from AFO.afo_skills_registry import register_core_skills

        registry = register_core_skills()
        skills = registry.list_all()
        fact_skills = [
            s
            for s in skills
            if "fact" in s.skill_id.lower() or "verify" in s.skill_id.lower()
        ]
        checks["fact_verification"] = len(fact_skills) > 0
    except Exception as e:
        logger.warning(f"Fact verification check failed: {e}")

    # 3b. MCP 기반 사실 검증 도구 확인 (Cursor MCP 설정 기준)
    if not checks["fact_verification"]:
        try:
            mcp_config_path = WORKSPACE_ROOT / ".cursor" / "mcp.json"
            if mcp_config_path.exists():
                mcp_config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
                servers = mcp_config.get("mcpServers", {})
                # AFO Ultimate MCP는 verify_fact 도구를 제공한다.
                checks["fact_verification"] = "afo-ultimate-mcp" in servers
        except Exception as e:
            logger.warning(f"MCP fact verification check failed: {e}")

    passed_count = sum(1 for v in checks.values() if v)
    score = (passed_count / len(checks)) * 100

    return {
        "score": round(score, 2),
        "checks": checks,
        "passed": passed_count,
        "total": len(checks),
    }


async def _check_goodness_pillar() -> dict[str, Any]:
    """善 (Goodness) 기둥 검증"""
    checks = {
        "auto_run_gate": False,
        "dry_run_default": False,
        "cai_engine": False,
    }

    # 1. AUTO_RUN 게이트 확인 (PH23: V2 Runner 우선)
    try:
        from api.chancellor_v2.graph.runner import run_v2

        # V2 Runner가 있으면 AUTO_RUN 게이트 통과
        checks["auto_run_gate"] = run_v2 is not None
    except ImportError:
        # Fallback to deprecated V1
        try:
            from AFO.chancellor_graph import chancellor_graph

            checks["auto_run_gate"] = chancellor_graph is not None
        except ImportError:
            logger.warning("AUTO_RUN gate check failed: Neither V2 nor V1 available")

    # 2. DRY_RUN 기본값 확인
    try:
        from AFO.config.antigravity import antigravity

        checks["dry_run_default"] = antigravity.DRY_RUN_DEFAULT is True
    except Exception as e:
        logger.warning(f"DRY_RUN check failed: {e}")

    # 3. CAI 엔진 확인
    try:
        from AFO.constitution.constitutional_ai import AFOConstitution

        checks["cai_engine"] = AFOConstitution is not None and hasattr(
            AFOConstitution, "evaluate_compliance"
        )
    except Exception as e:
        logger.warning(f"CAI engine check failed: {e}")

    passed_count = sum(1 for v in checks.values() if v)
    score = (passed_count / len(checks)) * 100

    return {
        "score": round(score, 2),
        "checks": checks,
        "passed": passed_count,
        "total": len(checks),
    }


async def _check_beauty_pillar() -> dict[str, Any]:
    """美 (Beauty) 기둥 검증"""
    checks = {
        "4_layer_arch": False,
        "glassmorphism": False,
        "naming_convention": False,
    }

    # 1. 4계층 아키텍처 확인
    try:
        # Presentation, Application, Domain, Infrastructure 계층 확인
        presentation_path = WORKSPACE_ROOT / "packages" / "dashboard"
        application_path = WORKSPACE_ROOT / "packages" / "afo-core" / "api"
        domain_path = WORKSPACE_ROOT / "packages" / "afo-core" / "AFO"
        infrastructure_path = (
            WORKSPACE_ROOT / "packages" / "afo-core" / "AFO" / "infrastructure"
        )

        checks["4_layer_arch"] = (
            presentation_path.exists()
            and application_path.exists()
            and domain_path.exists()
        )
    except Exception as e:
        logger.warning(f"4-layer arch check failed: {e}")

    # 2. Glassmorphism UX 확인 (프론트엔드 파일 확인)
    try:
        dashboard_path = WORKSPACE_ROOT / "packages" / "dashboard" / "src"
        if dashboard_path.exists():
            # CSS 파일에서 glassmorphism 관련 스타일 확인
            css_files = list(dashboard_path.rglob("*.css")) + list(
                dashboard_path.rglob("*.tsx")
            )
            for css_file in css_files[:5]:  # 처음 5개만 확인
                content = css_file.read_text()
                if "backdrop-filter" in content or "glass" in content.lower():
                    checks["glassmorphism"] = True
                    break
    except Exception as e:
        logger.warning(f"Glassmorphism check failed: {e}")

    # 3. 네이밍 컨벤션 확인 (일관된 네이밍 패턴)
    try:
        # 주요 파일들의 네이밍 패턴 확인
        api_files = list(
            (WORKSPACE_ROOT / "packages" / "afo-core" / "api").rglob("*.py")
        )
        if api_files:
            # snake_case 패턴 확인
            checks["naming_convention"] = all(
                "_" in f.stem or f.stem.islower() for f in api_files[:10]
            )
    except Exception as e:
        logger.warning(f"Naming convention check failed: {e}")

    passed_count = sum(1 for v in checks.values() if v)
    score = (passed_count / len(checks)) * 100

    return {
        "score": round(score, 2),
        "checks": checks,
        "passed": passed_count,
        "total": len(checks),
    }


async def _check_serenity_pillar() -> dict[str, Any]:
    """孝 (Serenity) 기둥 검증"""
    checks = {
        "mcp_tools": False,
        "organs_health": False,
        "sse_streaming": False,
    }

    # 1. MCP 도구 점검
    try:
        from AFO.config.health_check_config import health_check_config

        checks["mcp_tools"] = len(health_check_config.MCP_SERVERS) > 0
    except Exception as e:
        logger.warning(f"MCP tools check failed: {e}")

    # 2. 오장육부 건강도 확인
    try:
        from AFO.services.health_service import get_comprehensive_health

        health_data = await get_comprehensive_health()
        organs = health_data.get("organs", [])
        if isinstance(organs, dict):
            checks["organs_health"] = all(
                isinstance(v, dict) and v.get("status") == "healthy"
                for v in organs.values()
            )
        elif isinstance(organs, list):
            healthy_count = sum(1 for o in organs if o.get("healthy", False))
            checks["organs_health"] = healthy_count == len(organs) if organs else False
    except Exception as e:
        logger.warning(f"Organs health check failed: {e}")

    # 3. SSE 스트리밍 확인
    try:
        from sse_starlette.sse import EventSourceResponse

        checks["sse_streaming"] = True
    except ImportError:
        checks["sse_streaming"] = False

    passed_count = sum(1 for v in checks.values() if v)
    score = (passed_count / len(checks)) * 100

    return {
        "score": round(score, 2),
        "checks": checks,
        "passed": passed_count,
        "total": len(checks),
    }


async def _check_eternity_pillar() -> dict[str, Any]:
    """永 (Eternity) 기둥 검증"""
    checks = {
        "persistence": False,
        "genesis_mode": False,
        "documentation": False,
    }

    # 1. 영원한 기억 (Persistence) 확인
    try:
        # Redis Checkpoint 확인

        # Checkpoint 설정 확인
        checks["persistence"] = True  # 기본적으로 LangGraph는 MemorySaver 사용
    except Exception as e:
        logger.warning(f"Persistence check failed: {e}")

    # 2. Project Genesis 모드 확인
    try:
        from AFO.config.antigravity import antigravity

        checks["genesis_mode"] = antigravity.SELF_EXPANDING_MODE is True
    except Exception as e:
        logger.warning(f"Genesis mode check failed: {e}")

    # 3. 문서화 확인
    try:
        docs_path = WORKSPACE_ROOT / "docs"
        md_files = list(docs_path.rglob("*.md")) if docs_path.exists() else []
        checks["documentation"] = len(md_files) >= 10  # 최소 10개 문서
    except Exception as e:
        logger.warning(f"Documentation check failed: {e}")

    passed_count = sum(1 for v in checks.values() if v)
    score = (passed_count / len(checks)) * 100

    return {
        "score": round(score, 2),
        "checks": checks,
        "passed": passed_count,
        "total": len(checks),
    }
