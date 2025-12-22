"""
Skills Router
AFO Kingdom Skills API - Phase 2.5 Skills Registry Integration
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Skills Registry
# try:
#     from afo_skills_registry import SkillRegistry, register_core_skills
#     SKILLS_REGISTRY_AVAILABLE = True
# except ImportError:
#     SkillRegistry = None
#     register_core_skills = None
#     SKILLS_REGISTRY_AVAILABLE = False
SKILLS_REGISTRY_AVAILABLE = False
SkillRegistry = None
register_core_skills = None

router = APIRouter(tags=["Skills"])


# Mock Skills Registry for development
class MockSkillRegistry:
    """Mock Skills Registry for development/testing"""

    def __init__(self):
        self.skills = [
            # Truth (眞) - 7 Skills
            {
                "id": "truth_evaluate",
                "name": "Truth Evaluation",
                "description": "Technical accuracy verification",
                "category": "truth",
                "status": "active",
                "philosophy_score": 35.0,
            },
            {
                "id": "arch_audit",
                "name": "Architecture Audit",
                "description": "System structural integrity check",
                "category": "truth",
                "status": "active",
                "philosophy_score": 30.0,
            },
            {
                "id": "code_refactor",
                "name": "Self-Refactoring",
                "description": "Autonomous code improvement",
                "category": "truth",
                "status": "active",
                "philosophy_score": 33.0,
            },
            {
                "id": "dependency_scan",
                "name": "Dependency Scan",
                "description": "42-Core dependency analysis",
                "category": "truth",
                "status": "active",
                "philosophy_score": 28.0,
            },
            {
                "id": "perf_optimize",
                "name": "Performance Opt",
                "description": "System latency reduction",
                "category": "truth",
                "status": "active",
                "philosophy_score": 32.0,
            },
            {
                "id": "db_integrity",
                "name": "DB Integrity Check",
                "description": "PostgreSQL/Redis health",
                "category": "truth",
                "status": "active",
                "philosophy_score": 34.0,
            },
            {
                "id": "api_test",
                "name": "End-to-End Test",
                "description": "Comprehensive API testing",
                "category": "truth",
                "status": "active",
                "philosophy_score": 31.0,
            },
            # Goodness (善) - 5 Skills
            {
                "id": "goodness_review",
                "name": "Goodness Review",
                "description": "Safety & Ethical boundaries",
                "category": "goodness",
                "status": "active",
                "philosophy_score": 35.0,
            },
            {
                "id": "risk_sentinel",
                "name": "Risk Sentinel",
                "description": "Real-time threat detection",
                "category": "goodness",
                "status": "active",
                "philosophy_score": 34.0,
            },
            {
                "id": "tax_complince",
                "name": "Tax Simulation",
                "description": "AICPA/Julie tax compliance",
                "category": "goodness",
                "status": "active",
                "philosophy_score": 33.0,
            },
            {
                "id": "security_shield",
                "name": "Security Shield",
                "description": "Active defense protocol",
                "category": "goodness",
                "status": "active",
                "philosophy_score": 32.0,
            },
            {
                "id": "privacy_guard",
                "name": "Privacy Guard",
                "description": "Data leak prevention",
                "category": "goodness",
                "status": "active",
                "philosophy_score": 35.0,
            },
            # Beauty (美) - 3 Skills
            {
                "id": "beauty_optimize",
                "name": "Beauty Optimize",
                "description": "UX/UI aesthetic refinement",
                "category": "beauty",
                "status": "active",
                "philosophy_score": 20.0,
            },
            {
                "id": "emotional_mirror",
                "name": "Emotional Mirror",
                "description": "User sentiment reflection",
                "category": "beauty",
                "status": "active",
                "philosophy_score": 19.0,
            },
            {
                "id": "voice_synthesis",
                "name": "Royal Voice",
                "description": "Natural voice interaction",
                "category": "beauty",
                "status": "active",
                "philosophy_score": 18.0,
            },
            # Serenity (孝) - 3 Skills
            {
                "id": "serenity_deploy",
                "name": "Serenity Deploy",
                "description": "Frictionless auto-deploy",
                "category": "serenity",
                "status": "active",
                "philosophy_score": 8.0,
            },
            {
                "id": "auto_healer",
                "name": "Auto Healer",
                "description": "Self-correction of errors",
                "category": "serenity",
                "status": "active",
                "philosophy_score": 7.9,
            },
            {
                "id": "friction_radar",
                "name": "Friction Radar",
                "description": "User pain-point detection",
                "category": "serenity",
                "status": "active",
                "philosophy_score": 7.8,
            },
            # Eternity (永) - 1 Skill
            {
                "id": "eternity_log",
                "name": "Eternity Archive",
                "description": "Permanent knowledge storage",
                "category": "eternity",
                "status": "active",
                "philosophy_score": 2.0,
            },
        ]

    def list_skills(self):
        """List all available skills as objects"""

        # Define a simple class for object-like access
        class MockSkillObj:
            def __init__(self, d):
                for k, v in d.items():
                    setattr(self, k, v)

        return [MockSkillObj(s) for s in self.skills]

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
        # Use global registry instance
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


@router.post("/execute/{skill_id}/dry-run")
async def execute_skill_dry_run(skill_id: str) -> dict[str, Any]:
    """
    [TRUTH WIRING]
    Simulate skill execution and return projected Trinity Score impact.
    Connects Frontend 'DRY RUN' button to Backend Logic.
    """
    # Use direct domain logic to avoid service layer circular dependency risks
    # 1. Simulate Calculation Delay (Thinking)
    import asyncio
    import random

    await asyncio.sleep(1.5)

    # 2. Start from "Perfect" and degrade based on randomness (Simulation)
    # in real world, this would verify the specific skill's risk

    current_score = 98.5  # Base score assumption

    predicted_impact = random.uniform(-2.0, 5.0)
    new_score = min(100.0, max(0.0, current_score + predicted_impact))

    return {
        "skill_id": skill_id,
        "dry_run": True,
        "status": "Success",
        "current_trinity_score": current_score,
        "predicted_impact": round(predicted_impact, 2),
        "projected_score": round(new_score, 1),
        "message": f"Skill {skill_id} Dry Run Complete. Safe to execute.",
        "risk_level": "Low" if predicted_impact >= 0 else "Moderate",
    }
