# Trinity Score: 90.0 (Established by Chancellor)
"""Skill Registry Routes (眞善美孝)

이 모듈은 Skill Registry의 FastAPI 라우터를 제공합니다.
5636줄의 거대한 단일 파일에서 분리된 모듈입니다.
"""

from __future__ import annotations

from typing import Any

from afo_soul_engine.api.models.skills import (
    SkillExecuteRequest,
    SkillExecutionResult,
    SkillFilterRequest,
    SkillListResponse,
    SkillRequest,
    SkillResponse,
    SkillStatsResponse,
)
from afo_soul_engine.api.services.skills_service import SkillsService
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

# Create router
router = APIRouter(prefix="/api/skills", tags=["Skill Registry"])


# Dependency injection
def get_skills_service() -> SkillsService:
    """Skills Service 의존성 주입"""
    try:
        return SkillsService()
    except Exception:  # pragma: no cover - 초기화 실패 fallback
        # Service 초기화 실패 시에도 기본 서비스 반환
        # 실제로는 SkillsService가 내부에서 graceful fallback 처리
        return SkillsService()


@router.get("/list", response_model=SkillListResponse, summary="스킬 목록 조회")
async def list_skills(
    category: str | None = Query(None, description="카테고리 필터"),
    status: str | None = Query(None, description="상태 필터"),
    search: str | None = Query(None, description="검색어 (이름/설명)"),
    min_philosophy_avg: float | None = Query(
        None, ge=0, le=100, description="최소 철학 평균 점수"
    ),
    execution_mode: str | None = Query(None, description="실행 모드 필터"),
    offset: int = Query(0, ge=0, description="페이지 시작 위치"),
    limit: int = Query(50, ge=0, le=100, description="페이지 크기"),
    service: SkillsService = Depends(get_skills_service),
) -> SkillListResponse:
    """
    스킬 목록을 조회합니다.

    - **category**: 카테고리별 필터링 (workflow_automation, rag_systems, 등)
    - **status**: 상태별 필터링 (active, deprecated, experimental)
    - **search**: 이름이나 설명에서 검색
    - **min_philosophy_avg**: 최소 철학 평균 점수
    - **execution_mode**: 실행 모드별 필터링
    - **offset**: 페이지 시작 위치
    - **limit**: 한 페이지당 항목 수

    Returns:
        필터링된 스킬 목록과 메타 정보
    """
    try:
        filters = SkillFilterRequest(
            category=category,
            status=status,
            search=search,
            min_philosophy_avg=min_philosophy_avg,
            execution_mode=execution_mode,
            offset=offset,
            limit=limit,
        )

        result = await service.list_skills(filters)
        return result

    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(
            status_code=500, detail=f"스킬 목록 조회 실패: {e!s}"
        ) from e


@router.get("/{skill_id}", response_model=SkillResponse, summary="스킬 상세 조회")
async def get_skill(
    skill_id: str, service: SkillsService = Depends(get_skills_service)
) -> SkillResponse:
    """
    특정 스킬의 상세 정보를 조회합니다.

    - **skill_id**: 조회할 스킬의 고유 ID

    Returns:
        스킬의 상세 정보 (철학 점수, 실행 통계 등 포함)
    """
    try:
        skill = await service.get_skill(skill_id)
        if not skill:
            raise HTTPException(
                status_code=404, detail=f"스킬을 찾을 수 없습니다: {skill_id}"
            )

        return skill

    except HTTPException as e:
        raise e
    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(status_code=500, detail=f"스킬 조회 실패: {e!s}") from e


@router.post("/", response_model=SkillResponse, summary="스킬 등록", status_code=201)
async def register_skill(
    request: SkillRequest, service: SkillsService = Depends(get_skills_service)
) -> JSONResponse:
    """
    새로운 스킬을 등록합니다.

    - **skill_id**: 고유 스킬 ID (필수)
    - **name**: 스킬 이름 (필수)
    - **description**: 스킬 설명 (필수)
    - **category**: 카테고리 (필수)
    - **execution_mode**: 실행 모드 (필수)
    - **parameters**: 실행 파라미터 스키마 (선택)

    Returns:
        등록된 스킬 정보
    """
    try:
        # 스킬 ID 중복 체크
        existing = await service.get_skill(request.skill_id)
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"이미 존재하는 스킬 ID입니다: {request.skill_id}",
            )

        result = await service.register_skill(request)
        return JSONResponse(status_code=201, content=result.model_dump())

    except HTTPException as e:
        raise e
    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(status_code=500, detail=f"스킬 등록 실패: {e!s}") from e


@router.post(
    "/{skill_id}/execute", response_model=SkillExecutionResult, summary="스킬 실행"
)
async def execute_skill(
    skill_id: str,
    parameters: dict[str, Any] | None = None,
    timeout: int | None = Query(30, ge=1, le=300, description="실행 타임아웃(초)"),
    service: SkillsService = Depends(get_skills_service),
) -> SkillExecutionResult:
    """
    스킬을 실행합니다.

    - **skill_id**: 실행할 스킬의 ID
    - **parameters**: 실행 파라미터 (스킬별로 다름)
    - **timeout**: 실행 타임아웃 (초, 기본 30초)

    Returns:
        실행 결과 (성공/실패, 실행 시간, 결과 데이터)
    """
    try:
        # 스킬 존재 여부 확인
        skill = await service.get_skill(skill_id)
        if not skill:
            raise HTTPException(
                status_code=404, detail=f"실행할 스킬을 찾을 수 없습니다: {skill_id}"
            )

        request = SkillExecuteRequest(
            skill_id=skill_id, parameters=parameters or {}, timeout=timeout
        )

        result = await service.execute_skill(request)
        return result

    except HTTPException as e:
        raise e
    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(status_code=500, detail=f"스킬 실행 실패: {e!s}") from e


@router.delete("/{skill_id}", summary="스킬 삭제", status_code=204)
async def delete_skill(
    skill_id: str, service: SkillsService = Depends(get_skills_service)
) -> JSONResponse:
    """
    스킬을 삭제합니다.

    - **skill_id**: 삭제할 스킬의 ID

    Returns:
        삭제 성공 시 204 No Content
    """
    try:
        success = await service.delete_skill(skill_id)
        if not success:
            raise HTTPException(
                status_code=404, detail=f"삭제할 스킬을 찾을 수 없습니다: {skill_id}"
            )

        return JSONResponse(status_code=204, content=None)

    except HTTPException as e:
        raise e
    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(status_code=500, detail=f"스킬 삭제 실패: {e!s}") from e


@router.get("/stats", response_model=SkillStatsResponse, summary="스킬 통계 조회")
async def get_skill_stats(
    service: SkillsService = Depends(get_skills_service),
) -> SkillStatsResponse:
    """
    스킬 시스템의 통계 정보를 조회합니다.

    Returns:
        전체 스킬 수, 활성 스킬 수, 카테고리별 통계, 실행 통계 등
    """
    try:
        stats = await service.get_stats()
        return stats

    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(
            status_code=500, detail=f"스킬 통계 조회 실패: {e!s}"
        ) from e


@router.get("/categories", summary="카테고리 목록 조회")
async def get_categories(
    service: SkillsService = Depends(get_skills_service),
) -> dict[str, Any]:
    """
    사용 가능한 스킬 카테고리 목록을 조회합니다.

    Returns:
        카테고리 목록과 각 카테고리의 스킬 수
    """
    try:
        stats = await service.get_stats()
        categories = [
            {
                "category": cat.category,
                "name": cat.category.replace("_", " ").title(),
                "count": cat.count,
                "description": _get_category_description(cat.category),
            }
            for cat in stats.categories
        ]

        return {"categories": categories, "total_categories": len(categories)}

    except Exception as e:  # pragma: no cover - 예외 상황
        raise HTTPException(
            status_code=500, detail=f"카테고리 목록 조회 실패: {e!s}"
        ) from e


def _get_category_description(category: str) -> str:
    """카테고리 설명 반환"""
    descriptions = {
        "workflow_automation": "워크플로우 자동화 (n8n, Zapier 등)",
        "rag_systems": "RAG 시스템 (검색-증강 생성)",
        "browser_automation": "브라우저 자동화 (스크래핑, 테스트)",
        "data_processing": "데이터 처리 및 변환",
        "ai_inference": "AI 추론 및 예측",
        "monitoring": "모니터링 및 알림",
        "utilities": "유틸리티 및 도구",
        "analysis_evaluation": "분석 및 평가 (Speckit 확장)",
        "integration": "외부 서비스 통합 (Speckit 확장)",
    }
    return descriptions.get(category, f"{category} 카테고리")


@router.get("/health", summary="스킬 서비스 헬스체크")
async def skills_health(
    service: SkillsService = Depends(get_skills_service),
) -> dict[str, Any]:
    """
    스킬 서비스의 헬스 상태를 확인합니다.

    Returns:
        서비스 상태, 철학 점수, 레지스트리 상태 등
    """
    try:
        health = await service.health_check()
        return {
            "service": "skills",
            "status": health.get("status", "unknown"),
            "philosophy": "眞善美孝",
            "registry_available": health.get("registry_available", False),
            "total_skills": health.get("total_skills", 0),
            "timestamp": health.get("timestamp"),
        }

    except Exception as e:  # pragma: no cover - 헬스체크 실패 fallback
        return {
            "service": "skills",
            "status": "error",
            "error": str(e),
            "philosophy": "眞善美孝",
        }
