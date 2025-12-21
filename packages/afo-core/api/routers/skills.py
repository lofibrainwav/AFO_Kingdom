"""
Skills Router
AFO Kingdom Skills API - Phase 2.5 Skills Registry Integration
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Skills Registry
try:
    from afo_skills_registry import SkillRegistry, register_core_skills

    SKILLS_REGISTRY_AVAILABLE = True
except ImportError:
    SkillRegistry = None
    register_core_skills = None
    SKILLS_REGISTRY_AVAILABLE = False

router = APIRouter(tags=["Skills"])


# Mock Skills Registry for development
class MockSkillRegistry:
    """Mock Skills Registry for development/testing"""

    def __init__(self):
        self.skills = [
            {
                "id": "truth_evaluate",
                "name": "Truth Evaluation",
                "description": "Technical accuracy and fact verification",
                "category": "truth",
                "status": "active",
                "philosophy_score": 35.0,
            },
            {
                "id": "goodness_review",
                "name": "Goodness Review",
                "description": "Safety and ethics assessment",
                "category": "goodness",
                "status": "active",
                "philosophy_score": 35.0,
            },
            {
                "id": "beauty_optimize",
                "name": "Beauty Optimization",
                "description": "UX and design improvements",
                "category": "beauty",
                "status": "active",
                "philosophy_score": 20.0,
            },
            {
                "id": "serenity_deploy",
                "name": "Serenity Deployment",
                "description": "Smooth automated deployment",
                "category": "serenity",
                "status": "active",
                "philosophy_score": 8.0,
            },
            {
                "id": "eternity_log",
                "name": "Eternity Logging",
                "description": "Comprehensive audit trails",
                "category": "eternity",
                "status": "active",
                "philosophy_score": 2.0,
            },
        ]

    def list_skills(self):
        """List all available skills"""
        return self.skills

    def get_skill(self, skill_id: str):
        """Get skill by ID"""
        for skill in self.skills:
            if skill["id"] == skill_id:
                # Convert to object-like structure
                class MockSkill:
                    def __init__(self, data):
                        for key, value in data.items():
                            setattr(self, key, value)

                return MockSkill(skill)
        return None

    async def execute_skill(self, skill_id: str, parameters: dict, timeout_seconds: int = 30):
        """Execute a skill with mock response"""
        skill = self.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found")

        # Simulate processing time
        import asyncio

        await asyncio.sleep(0.1)

        # Return mock execution result
        return {
            "skill_id": skill_id,
            "skill_name": skill.name,
            "category": skill.category,
            "philosophy_score": skill.philosophy_score,
            "parameters": parameters,
            "result": f"Executed {skill.name} successfully",
            "timestamp": "2025-12-21T11:42:57Z",
        }


# Initialize registry
if SKILLS_REGISTRY_AVAILABLE and register_core_skills:
    registry = register_core_skills()
elif SkillRegistry:
    registry = SkillRegistry()
else:
    registry = MockSkillRegistry()


class SkillInfo(BaseModel):
    """Skill 정보 모델"""

    id: str = Field(..., description="Skill 고유 ID")
    name: str = Field(..., description="Skill 이름")
    description: str = Field(..., description="Skill 설명")
    category: str = Field(..., description="Skill 카테고리")
    status: str = Field(..., description="Skill 상태")
    philosophy_score: float = Field(default=0.0, description="철학 점수")


class SkillExecutionRequest(BaseModel):
    """Skill 실행 요청 모델"""

    skill_id: str = Field(..., description="실행할 Skill ID")
    parameters: dict[str, Any] = Field(default_factory=dict, description="실행 파라미터")
    timeout_seconds: int = Field(default=30, ge=1, le=300, description="실행 제한 시간")


class SkillExecutionResponse(BaseModel):
    """Skill 실행 응답 모델"""

    skill_id: str = Field(..., description="실행된 Skill ID")
    result: Any = Field(..., description="실행 결과")
    execution_time: float = Field(..., description="실행 시간")
    success: bool = Field(..., description="실행 성공 여부")
    error: str | None = Field(None, description="오류 메시지")


@router.get("/list")
async def list_skills() -> dict[str, Any]:
    """
    등록된 모든 Skills 목록 조회
    """
    try:
        if SkillRegistry is None:
            raise HTTPException(status_code=503, detail="Skills Registry not available")

        # Skills Registry 초기화
        if register_core_skills:
            registry = register_core_skills()
        else:
            registry = SkillRegistry()

        skills = registry.list_skills()
        skills_data = []

        for skill in skills:
            skill_info = SkillInfo(
                id=skill.id,
                name=skill.name,
                description=skill.description,
                category=getattr(skill, "category", "general"),
                status=getattr(skill, "status", "active"),
                philosophy_score=getattr(skill, "philosophy_score", 0.0),
            )
            skills_data.append(skill_info.dict())

        return {"skills": skills_data, "total": len(skills_data), "status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list skills: {e!s}")


@router.get("/detail/{skill_id}")
async def get_skill_detail(skill_id: str) -> dict[str, Any]:
    """
    특정 Skill의 상세 정보 조회
    """
    try:
        if SkillRegistry is None:
            raise HTTPException(status_code=503, detail="Skills Registry not available")

        # Skills Registry 초기화
        if register_core_skills:
            registry = register_core_skills()
        else:
            registry = SkillRegistry()

        skill = registry.get_skill(skill_id)
        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill {skill_id} not found")

        skill_info = SkillInfo(
            id=skill.id,
            name=skill.name,
            description=skill.description,
            category=getattr(skill, "category", "general"),
            status=getattr(skill, "status", "active"),
            philosophy_score=getattr(skill, "philosophy_score", 0.0),
        )

        return {"skill": skill_info.dict(), "status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get skill detail: {e!s}")


@router.post("/execute")
async def execute_skill(request: SkillExecutionRequest) -> SkillExecutionResponse:
    """
    Skill 실행
    """
    try:
        if SkillRegistry is None:
            raise HTTPException(status_code=503, detail="Skills Registry not available")

        # Skills Registry 초기화
        if register_core_skills:
            registry = register_core_skills()
        else:
            registry = SkillRegistry()

        import time

        start_time = time.time()

        try:
            result = await registry.execute_skill(
                request.skill_id, request.parameters, timeout_seconds=request.timeout_seconds
            )

            execution_time = time.time() - start_time

            return SkillExecutionResponse(
                skill_id=request.skill_id,
                result=result,
                execution_time=execution_time,
                success=True,
            )

        except Exception as exec_error:
            execution_time = time.time() - start_time

            return SkillExecutionResponse(
                skill_id=request.skill_id,
                result=None,
                execution_time=execution_time,
                success=False,
                error=str(exec_error),
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute skill: {e!s}")


@router.get("/health")
async def skills_health() -> dict[str, Any]:
    """
    Skills 시스템 건강 상태 확인
    """
    try:
        health_status = {
            "service": "skills_registry",
            "status": "unknown",
            "skills_count": 0,
            "registry_available": False,
            "details": {},
        }

        if SkillRegistry is None:
            health_status["status"] = "unhealthy"
            health_status["details"]["error"] = "Skills Registry not available"
            return health_status

        # Skills Registry 초기화
        try:
            if register_core_skills:
                registry = register_core_skills()
            else:
                registry = SkillRegistry()

            skills = registry.list_skills()
            health_status["skills_count"] = len(skills)
            health_status["registry_available"] = True
            health_status["status"] = "healthy"

            # 각 skill 상태 확인
            skill_statuses = {}
            for skill in skills:
                skill_statuses[skill.id] = {
                    "name": skill.name,
                    "status": getattr(skill, "status", "active"),
                    "philosophy_score": getattr(skill, "philosophy_score", 0.0),
                }

            health_status["details"]["skills"] = skill_statuses

        except Exception as e:
            health_status["status"] = "degraded"
            health_status["details"]["error"] = str(e)

        return health_status

    except Exception as e:
        return {"service": "skills_registry", "status": "error", "error": str(e)}
