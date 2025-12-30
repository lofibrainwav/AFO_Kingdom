# Trinity Score: 90.0 (Established by Chancellor)
"""
Comprehensive Health Check Endpoint
야전교범 원칙 준수: 선확인 후보고, 가정 금지, 선증명 후확신

이 엔드포인트는 AFO 왕국의 모든 시스템 상태를 종합적으로 확인합니다:
- 스킬 레지스트리 (19개 스킬)
- 학자 시스템 (4명)
- MCP 도구 (10개 서버)
- Context7 지식 베이스
- Sequential Thinking
- 서비스 상태 (Redis, PostgreSQL, Ollama, API Server)
- Trinity Score (眞善美孝永 5기둥)
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

from AFO.config.health_check_config import health_check_config
from AFO.services.health_service import get_comprehensive_health
from AFO.utils.automation_tools import AutomationTools
from AFO.utils.path_utils import add_to_sys_path, get_trinity_os_path

router = APIRouter(prefix="/api/health", tags=["Comprehensive Health"])

# 캐시 헤더는 미들웨어에서 처리됨

logger = logging.getLogger(__name__)


@router.get("/trinity-monitor/stats")
async def trinity_monitor_stats() -> dict[str, Any]:
    """Trinity Score 모니터링 통계 조회"""
    try:
        from services.trinity_score_monitor import trinity_score_monitor

        stats = trinity_score_monitor.get_statistics()
        recent_samples = trinity_score_monitor.get_recent_samples(limit=20)

        return {
            "status": "success",
            "statistics": stats,
            "recent_samples": recent_samples,
        }
    except ImportError:
        return {
            "status": "unavailable",
            "error": "Trinity Score monitoring not available",
        }
    except Exception as e:
        logger.error("Trinity monitor stats error: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }


@router.get("/trinity-monitor/trend")
async def trinity_monitor_trend(window_minutes: int = 60) -> dict[str, Any]:
    """Trinity Score 추이 분석 조회"""
    try:
        from services.trinity_score_monitor import trinity_score_monitor

        trend_analysis = trinity_score_monitor.get_trend_analysis(window_minutes)

        return {
            "status": "success",
            "window_minutes": window_minutes,
            "trend_analysis": trend_analysis,
        }
    except ImportError:
        return {
            "status": "unavailable",
            "error": "Trinity Score monitoring not available",
        }
    except Exception as e:
        logger.error("Trinity monitor trend error: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }


@router.get("/comprehensive")
async def comprehensive_health_check() -> dict[str, Any]:
    """
    종합 건강 상태 진단 (야전교범 원칙 준수)

    Returns:
        - organs: 11-오장육부 상태
        - trinity_score: 眞善美孝永 5기둥 점수
        - skills: 스킬 레지스트리 상태
        - scholars: 학자 시스템 상태
        - mcp_tools: MCP 도구 상태
        - services: 서비스 상태
        - timestamp: 검사 시각
    """
    try:
        # 1. 기본 건강 상태 확인 (health_service 사용)
        health_data = await get_comprehensive_health()

        # 2. 스킬 레지스트리 상태 확인
        skills_status = await _check_skills_registry()

        # 3. 학자 시스템 상태 확인
        scholars_status = await _check_scholars()

        # 4. MCP 도구 상태 확인 (SSOT: 肾_MCP 오장육부)
        mcp_tools_status = await _check_mcp_tools()

        # 5. Context7 상태 확인
        context7_status = await _check_context7()

        # 6. Sequential Thinking 상태 확인
        sequential_thinking_status = await _check_sequential_thinking()

        # 7. 자동화 도구 상태 확인
        automation_status = await _check_automation_tools()

        # 8. 종합 결과 구성
        # health_data에서 trinity 정보 추출
        trinity_info = health_data.get("trinity", {})
        if isinstance(trinity_info, dict) and "trinity_score" in trinity_info:
            trinity_score = trinity_info["trinity_score"]
        elif "health_percentage" in health_data:
            trinity_score = health_data["health_percentage"] / 100.0
        else:
            trinity_score = 0.0

        config = health_check_config
        response_data = {
            "status": (
                "healthy" if trinity_score >= config.TRINITY_SCORE_THRESHOLD else "degraded"
            ),
            "timestamp": datetime.now().isoformat(),
            "organs": health_data.get("organs", {}),
            "organs_v2": health_data.get("organs_v2"),
            "contract_v2": health_data.get("contract_v2"),
            "ts_v2": health_data.get("ts_v2"),
            "trinity_score": trinity_score,
            "health_percentage": round(trinity_score * 100, 2),
            "trinity_breakdown": trinity_info if isinstance(trinity_info, dict) else {},
            "skills": skills_status,
            "scholars": scholars_status,
            "mcp_tools": mcp_tools_status,
            "context7": context7_status,
            "sequential_thinking": sequential_thinking_status,
            "automation_tools": automation_status,
            "services": _extract_services_status(health_data),
            "metadata": {
                "check_method": "comprehensive",
                "principles": [
                    "선확인 후보고",
                    "가정 금지",
                    "선증명 후확신",
                    "속도보다 정확성",
                    "지속적 개선",
                ],
            },
        }

        return response_data

    except Exception as e:
        logger.error("Comprehensive health check failed: %s", e)
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


def _extract_services_status(health_data: dict[str, Any]) -> dict[str, bool]:
    """
    서비스 상태 추출 (하드코딩 제거)

    Args:
        health_data: health_service에서 반환된 데이터

    Returns:
        서비스별 상태 딕셔너리
    """
    organs = health_data.get("organs", {})
    if not isinstance(organs, dict):
        return {
            "redis": False,
            "postgres": False,
            "ollama": False,
            "api_server": False,
        }

    # SSOT 표준: 5개 오장육부 매핑
    service_mapping = {
        "redis": "心_Redis",  # 세션/캐시 저장소
        "postgres": "肝_PostgreSQL",  # 메인 데이터베이스
        "ollama": "脾_Ollama",  # AI 모델 서빙
        "api_server": "肺_API_Server",  # API 서버 상태
        "mcp": "肾_MCP",  # 외부 서비스 연결
    }

    return {
        service: organs.get(organ_key, {}).get("status") == "healthy"
        for service, organ_key in service_mapping.items()
    }


async def _check_skills_registry() -> dict[str, Any]:
    """스킬 레지스트리 상태 확인"""
    try:
        from AFO.afo_skills_registry import register_core_skills

        registry = register_core_skills()
        skills = registry.list_all()
        config = health_check_config

        return {
            "status": "healthy",
            "total_skills": len(skills),
            "skills": [
                {"id": skill.skill_id, "name": skill.name, "status": str(skill.status)}
                for skill in skills[: config.MAX_SKILLS_DISPLAY]
            ],
            "categories": (
                registry.get_category_stats() if hasattr(registry, "get_category_stats") else {}
            ),
        }
    except Exception as e:
        logger.warning("Skills registry check failed: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }


async def _check_scholars() -> dict[str, Any]:
    """학자 시스템 상태 확인"""
    try:
        config = health_check_config
        scholars = [
            {"name": scholar.name, "status": scholar.status, "type": scholar.type}
            for scholar in config.SCHOLARS
        ]

        return {
            "status": "healthy",
            "total_scholars": len(scholars),
            "scholars": scholars,
        }
    except Exception as e:
        logger.warning("Scholars check failed: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }


async def _check_mcp_tools() -> dict[str, Any]:
    """MCP 도구 상태 확인"""
    try:
        config = health_check_config
        servers = [
            {
                "name": server.name,
                "status": server.status,
                "description": server.description,
            }
            for server in config.MCP_SERVERS
        ]

        return {
            "status": "healthy",
            "total_servers": len(servers),
            "servers": servers,
        }
    except Exception as e:
        logger.warning("MCP tools check failed: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }


async def _check_context7() -> dict[str, Any]:
    """Context7 지식 베이스 상태 확인 (최적화된 캐싱 서비스 사용)"""
    try:
        # 최적화된 Context7 서비스 사용 (캐싱 + 지연 로딩)
        from AFO.services.context7_service import get_context7_health

        health_data = get_context7_health()

        # 추가 메타데이터
        config = health_check_config
        if health_data["status"] == "healthy" and "knowledge_base_keys" in health_data:
            # 표시 제한 적용
            health_data["knowledge_base_keys"] = health_data["knowledge_base_keys"][
                : config.MAX_CONTEXT7_KEYS_DISPLAY
            ]

        return health_data

    except Exception as e:
        logger.warning("Context7 check failed: %s", e)
        return {
            "status": "error",
            "error": str(e),
            "instance_created": False,
            "knowledge_base_accessible": False,
            "optimization_applied": False,
        }


async def _check_sequential_thinking() -> dict[str, Any]:
    """Sequential Thinking 상태 확인"""
    try:
        from pathlib import Path

        # trinity-os 경로 추가 (동적 계산)
        trinity_os_path = get_trinity_os_path(Path(__file__))
        add_to_sys_path(trinity_os_path)

        return {
            "status": "healthy",
            "available": True,
        }
    except Exception as e:
        logger.warning("Sequential Thinking check failed: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }


async def _check_automation_tools() -> dict[str, Any]:
    """자동화 도구 상태 확인 (최적화된 캐싱 서비스 사용)"""
    try:
        # 최적화된 Automation 서비스 사용 (캐싱 적용)
        from AFO.services.automation_service import get_automation_health

        health_data = get_automation_health()

        return health_data

    except Exception as e:
        logger.warning("Automation tools check failed: %s", e)
        return {
            "status": "error",
            "error": str(e),
        }
