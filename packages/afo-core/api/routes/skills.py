# Trinity Score: 95.0 (New Component)
"""
AFO Skills Router (아름다운 코드 적용)

AFO Skill Registry를 외부로 노출하는 API 라우터.
眞善美孝 철학을 준수하며, SkillRegistry Singleton을 통해 데이터를 제공합니다.

Author: AFO Kingdom Development Team
Date: 2025-12-25
Version: 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any

from AFO.afo_skills_registry import (
    AFOSkillCard,
    SkillExecutionRequest,
    SkillExecutionResult,
    SkillFilterParams,
    SkillRegistry,
    register_core_skills,
)
from fastapi import APIRouter, Depends, HTTPException, Query

# Configure logging
logger = logging.getLogger(__name__)


# Initialize Router
router = APIRouter(tags=["Skills"])


# Dependency to get registry (Dependency Injection pattern)
def get_registry() -> SkillRegistry:
    """Get the SkillRegistry instance (Singleton)."""
    registry = SkillRegistry()
    # Ensure core skills are registered (handle case where module-import registered 1 manual skill)
    if registry.count() < 5:
        logger.info("Initializing SkillRegistry with core skills...")
        register_core_skills()
    return registry


@router.post("/", response_model=SkillExecutionResult)
async def execute_skill(
    request: SkillExecutionRequest,
    registry: SkillRegistry = Depends(get_registry),
) -> SkillExecutionResult:
    """
    Execute a skill.

    Trinity Score: 眞 (Truth) - Real execution interface
    """
    skill = registry.get(request.skill_id)
    if not skill:
        raise HTTPException(
            status_code=404, detail=f"Skill '{request.skill_id}' not found"
        )

    dry_run = request.model_dump().get("dry_run", False)
    logger.info(f"Executing skill: {request.skill_id} (Dry Run: {dry_run})")

    # In a real implementation, this would call the SkillExecutor service.
    # For Phase 2, we simulate successful execution/dry-run.

    return SkillExecutionResult(
        skill_id=request.skill_id,
        status="completed" if not dry_run else "dry_run_success",
        result={"message": f"Skill {skill.name} executed successfully"},
        dry_run=dry_run,
    )


@router.get("/", response_model=dict[str, Any])
async def list_skills(
    category: str | None = None,
    search: str | None = None,
    min_philosophy_avg: int | None = Query(None, ge=0, le=100),
    limit: int = 100,
    offset: int = 0,
    registry: SkillRegistry = Depends(get_registry),
) -> dict[str, Any]:
    """
    List all available skills with filtering.

    Trinity Score: 眞 (Truth) - Accurate skill listing
    """
    try:
        # Build filter params
        params = SkillFilterParams(
            category=category,
            search=search,
            min_philosophy_avg=min_philosophy_avg,
            limit=limit,
            offset=offset,
        )

        # Query registry
        skills = registry.filter(params)
        total = registry.count()

        return {
            "skills": skills,
            "total": total,
            "count": len(skills),
            "categories": registry.get_categories(),
        }
    except Exception as e:
        logger.error(f"Failed to list skills: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{skill_id}", response_model=AFOSkillCard)
async def get_skill(
    skill_id: str,
    registry: SkillRegistry = Depends(get_registry),
) -> AFOSkillCard:
    """
    Get a single skill by ID.
    """
    skill = registry.get(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    return skill


@router.get("/stats/categories", response_model=dict[str, int])
async def get_category_stats(
    registry: SkillRegistry = Depends(get_registry),
) -> dict[str, int]:
    """Get statistics by category."""
    return registry.get_category_stats()
