# Trinity Score: 90.0 (Established by Chancellor)
"""Skill Registry Service (眞善美孝)

이 모듈은 AFO Skill Registry의 비즈니스 로직을 제공합니다.
5636줄의 거대한 단일 파일에서 분리된 모듈입니다.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections import defaultdict
from datetime import datetime
from typing import TYPE_CHECKING, Any

from afo_soul_engine.api.core.base_service import BaseService
from afo_soul_engine.api.models.skills import (
    PhilosophyScores,
    SkillCategoryStats,
    SkillExecuteRequest,
    SkillExecutionResult,
    SkillFilterRequest,
    SkillListResponse,
    SkillRequest,
    SkillResponse,
    SkillStatsResponse,
)

# Trinity Score Evaluator (동적 점수 계산)
try:
    from AFO.services.mcp_tool_trinity_evaluator import mcp_tool_trinity_evaluator

    TRINITY_EVALUATOR_AVAILABLE = True
except ImportError:
    mcp_tool_trinity_evaluator = None  # type: ignore
    TRINITY_EVALUATOR_AVAILABLE = False

# Import skill registry components for runtime
try:
    from AFO.afo_skills_registry import (
        ExecutionMode,
        SkillCategory,
        SkillFilterParams,
        SkillRegistry,
        SkillStatus,
        register_core_skills,
    )
    from AFO.afo_skills_registry import PhilosophyScore as RegistryPhilosophyScores

    SKILL_REGISTRY_AVAILABLE = True
except ImportError:
    SkillRegistry = None  # type: ignore
    SkillFilterParams = None  # type: ignore
    SkillCategory = None  # type: ignore
    ExecutionMode = None  # type: ignore
    SkillStatus = None  # type: ignore
    RegistryPhilosophyScores = None  # type: ignore
    register_core_skills = None  # type: ignore
    SKILL_REGISTRY_AVAILABLE = False

# Import types for type checking only
if TYPE_CHECKING:
    from AFO.afo_skills_registry import AFOSkillCard, SkillRegistry
else:
    # Runtime fallback
    try:
        from AFO.afo_skills_registry import AFOSkillCard
    except ImportError:
        AFOSkillCard = None  # type: ignore


class SkillsService(BaseService):
    """Skill Registry 비즈니스 로직 서비스 (眞善美孝)"""

    def __init__(self) -> None:
        super().__init__()
        self.skill_registry: SkillRegistry | None = None
        self.execution_stats: dict[str, dict[str, Any]] = defaultdict(dict)
        self._initialize_registry()

    def _initialize_registry(self) -> None:
        """Skill Registry 초기화"""
        # 직접 스킬 레지스트리 초기화
        try:
            # 직접 스킬 레지스트리 초기화
            from AFO.afo_skills_registry import register_core_skills

            self.skill_registry = register_core_skills()
            skill_count = (
                len(self.skill_registry._skills)
                if hasattr(self.skill_registry, "_skills")
                else 0
            )
            self.logger.info("✅ Skill Registry 초기화됨: %d개 스킬", skill_count)

            # 카테고리 통계 로깅
            if self.skill_registry and hasattr(
                self.skill_registry, "get_category_stats"
            ):
                category_stats = self.skill_registry.get_category_stats()
                self.logger.info("📊 카테고리 통계: %s", category_stats)

        except Exception as e:
            self.logger.error("❌ Skill Registry 초기화 실패: %s", e)
            self.skill_registry = None

    async def register_skill(self, request: SkillRequest) -> SkillResponse:
        """
        스킬 등록

        Args:
            request: 스킬 등록 요청

        Returns:
            등록된 스킬 정보

        Raises:
            ValueError: 등록 실패 시
        """
        try:
            if not self.skill_registry:
                raise ValueError("Skill Registry not available")

            if AFOSkillCard is None:
                raise ValueError(
                    "AFOSkillCard not available - skill registry module not loaded"
                )

            # AFOSkillCard 생성
            # 문자열을 enum으로 변환
            if SkillCategory is None or ExecutionMode is None:
                raise ValueError(
                    "SkillCategory or ExecutionMode not available - skill registry module not loaded"
                )

            category_enum = SkillCategory(request.category)
            execution_mode_enum = ExecutionMode(request.execution_mode)

            # PhilosophyScores는 afo_skills_registry의 것을 사용해야 함
            if RegistryPhilosophyScores is None:
                raise ValueError(
                    "RegistryPhilosophyScores not available - skill registry module not loaded"
                )

            skill_card = AFOSkillCard(
                skill_id=request.skill_id,
                name=request.name,
                description=request.description,
                category=category_enum,
                execution_mode=execution_mode_enum,
                version="1.0.0",
                parameters=request.parameters or {},
                philosophy_scores=RegistryPhilosophyScores(
                    truth=85,
                    goodness=80,
                    beauty=75,
                    serenity=90,
                ),
            )

            # 레지스트리에 등록
            self.skill_registry.skills[request.skill_id] = skill_card

            self.logger.info("✅ 스킬 등록됨: %s", request.skill_id)

            # skill_card.philosophy는 RegistryPhilosophyScores이므로
            # api.models.skills.PhilosophyScores로 변환 필요
            # Pydantic 모델의 실제 값을 가져오기 위해 model_dump 사용
            skill_card_dict = skill_card.model_dump()
            registry_philosophy = skill_card_dict.get("philosophy")
            if registry_philosophy and isinstance(registry_philosophy, dict):
                api_philosophy = PhilosophyScores(
                    truth=registry_philosophy.get("truth", 85.0),
                    goodness=registry_philosophy.get("goodness", 80.0),
                    beauty=registry_philosophy.get("beauty", 75.0),
                    serenity=registry_philosophy.get("serenity", 90.0),
                )
            elif registry_philosophy and hasattr(registry_philosophy, "truth"):
                # 이미 인스턴스인 경우
                api_philosophy = PhilosophyScores(
                    truth=float(registry_philosophy.truth),
                    goodness=float(registry_philosophy.goodness),
                    beauty=float(registry_philosophy.beauty),
                    serenity=float(registry_philosophy.serenity),
                )
            else:
                api_philosophy = PhilosophyScores(
                    truth=85.0, goodness=80.0, beauty=75.0, serenity=90.0
                )

            return SkillResponse(
                skill_id=skill_card.skill_id,
                name=skill_card.name,
                description=skill_card.description,
                category=skill_card.category,
                execution_mode=skill_card.execution_mode,
                philosophy=api_philosophy,
                parameters=skill_card.parameters,
                execution_count=0,
            )

        except Exception as e:
            self.logger.error("❌ 스킬 등록 실패: %s", e)
            raise ValueError(f"Failed to register skill: {e!s}") from e

    async def get_skill(self, skill_id: str) -> SkillResponse | None:
        """
        스킬 조회

        Args:
            skill_id: 조회할 스킬 ID

        Returns:
            스킬 정보 또는 None
        """
        try:
            if not self.skill_registry:
                return None

            skill = self.skill_registry.get(skill_id)
            if not skill:
                return None

            return SkillResponse(
                skill_id=skill.skill_id,
                name=skill.name,
                description=skill.description,
                category=skill.category,
                execution_mode=skill.execution_mode,
                status=skill.status,
                philosophy=PhilosophyScores(
                    truth=getattr(skill.philosophy_scores, "truth", 85.0),
                    goodness=getattr(skill.philosophy_scores, "goodness", 80.0),
                    beauty=getattr(skill.philosophy_scores, "beauty", 75.0),
                    serenity=getattr(skill.philosophy_scores, "serenity", 90.0),
                ),
                tags=skill.tags,
                parameters=skill.parameters,
                execution_count=getattr(skill, "execution_count", 0),
                created_at=(
                    skill.created_at
                    if hasattr(skill, "created_at")
                    else datetime.utcnow()
                ),
                updated_at=(
                    skill.updated_at
                    if hasattr(skill, "updated_at")
                    else datetime.utcnow()
                ),
            )

        except Exception as e:
            self.logger.error("❌ 스킬 조회 실패: %s", e)
            return None

    async def list_skills(
        self, filters: SkillFilterRequest | None = None
    ) -> SkillListResponse:
        """
        스킬 목록 조회 (필터링 지원)

        Args:
            filters: 필터링 조건

        Returns:
            필터링된 스킬 목록
        """
        try:
            if not self.skill_registry:
                return SkillListResponse(
                    skills=[],
                    total_count=0,
                    filtered_count=0,
                    offset=filters.offset if filters else 0,
                    limit=filters.limit if filters else 50,
                )

            # 필터 파라미터 변환
            if filters:
                if (
                    SkillFilterParams is None
                    or SkillCategory is None
                    or ExecutionMode is None
                    or SkillStatus is None
                ):
                    raise ValueError(
                        "SkillFilterParams or enum types not available - skill registry module not loaded"
                    )

                # 문자열을 enum으로 변환
                category_enum = (
                    SkillCategory(filters.category) if filters.category else None
                )
                status_enum = SkillStatus(filters.status) if filters.status else None
                execution_mode_enum = (
                    ExecutionMode(filters.execution_mode)
                    if filters.execution_mode
                    else None
                )

                filter_params = SkillFilterParams(
                    category=category_enum,
                    status=status_enum,
                    tags=filters.tags,
                    search=filters.search,
                    min_philosophy_avg=(
                        int(filters.min_philosophy_avg)
                        if filters.min_philosophy_avg
                        else None
                    ),
                    execution_mode=execution_mode_enum,
                    offset=filters.offset,
                    limit=filters.limit,
                )
                filtered_skills = self.skill_registry.filter(filter_params)
            else:
                filtered_skills = self.skill_registry.list_all()

            # 응답 변환 (DRY: list comprehension)
            skills = [
                SkillResponse(
                    skill_id=skill.skill_id,
                    name=skill.name,
                    description=skill.description,
                    category=skill.category,
                    execution_mode=skill.execution_mode,
                    status=skill.status,
                    philosophy=PhilosophyScores(
                        truth=getattr(skill.philosophy_scores, "truth", 85.0),
                        goodness=getattr(skill.philosophy_scores, "goodness", 80.0),
                        beauty=getattr(skill.philosophy_scores, "beauty", 75.0),
                        serenity=getattr(skill.philosophy_scores, "serenity", 90.0),
                    ),
                    tags=skill.tags,
                    parameters=skill.parameters,
                    execution_count=getattr(skill, "execution_count", 0),
                    created_at=getattr(skill, "created_at", datetime.utcnow()),
                    updated_at=getattr(skill, "updated_at", datetime.utcnow()),
                )
                for skill in filtered_skills
            ]

            return SkillListResponse(
                skills=skills,
                total_count=len(self.skill_registry.skills),
                filtered_count=len(skills),
                offset=filters.offset if filters else 0,
                limit=filters.limit if filters else 50,
            )

        except Exception as e:
            self.logger.error("❌ 스킬 목록 조회 실패: %s", e)
            return SkillListResponse(
                skills=[],
                total_count=0,
                filtered_count=0,
                offset=filters.offset if filters else 0,
                limit=filters.limit if filters else 50,
            )

    async def execute_skill(self, request: SkillExecuteRequest) -> SkillExecutionResult:
        """
        스킬 실행

        Args:
            request: 스킬 실행 요청

        Returns:
            실행 결과

        Raises:
            ValueError: 실행 실패 시
        """
        start_time = time.time()

        try:
            if not self.skill_registry:
                raise ValueError("Skill Registry not available")

            skill = self.skill_registry.get(request.skill_id)
            if not skill:
                raise ValueError(f"Skill not found: {request.skill_id}")

            # 실제 스킬 실행 로직 (현재는 mock)
            result = await self._execute_skill_logic(skill, request.parameters or {})

            execution_time = (time.time() - start_time) * 1000

            # 실행 통계 업데이트
            if hasattr(self.skill_registry, "increment_execution_count"):
                self.skill_registry.increment_execution_count(request.skill_id)
            else:
                # Fallback: execution_stats에 직접 기록
                if request.skill_id not in self.execution_stats:
                    self.execution_stats[request.skill_id] = {}
                self.execution_stats[request.skill_id]["execution_count"] = (
                    self.execution_stats[request.skill_id].get("execution_count", 0) + 1
                )

            # 동적 Trinity Score 계산 (眞善美孝永 5기둥)
            dynamic_trinity_score = None
            base_philosophy_scores = None

            # 기본 철학 점수 추출 (정적 점수)
            if skill.philosophy_scores and hasattr(skill.philosophy_scores, "truth"):
                base_philosophy_scores = {
                    "truth": getattr(skill.philosophy_scores, "truth", 85),
                    "goodness": getattr(skill.philosophy_scores, "goodness", 80),
                    "beauty": getattr(skill.philosophy_scores, "beauty", 75),
                    "serenity": getattr(skill.philosophy_scores, "serenity", 90),
                }

            # 실행 결과를 문자열로 변환하여 분석
            result_str = json.dumps(result) if isinstance(result, dict) else str(result)
            is_error = False

            # 동적 Trinity Score 계산
            if TRINITY_EVALUATOR_AVAILABLE and mcp_tool_trinity_evaluator:
                try:
                    trinity_eval = mcp_tool_trinity_evaluator.evaluate_execution_result(
                        tool_name=request.skill_id,
                        execution_result=result_str,
                        execution_time_ms=execution_time,
                        is_error=is_error,
                        base_philosophy_scores=base_philosophy_scores,
                    )
                    dynamic_trinity_score = PhilosophyScores(
                        truth=trinity_eval["trinity_scores"]["truth"] * 100,
                        goodness=trinity_eval["trinity_scores"]["goodness"] * 100,
                        beauty=trinity_eval["trinity_scores"]["beauty"] * 100,
                        serenity=trinity_eval["trinity_scores"]["filial_serenity"]
                        * 100,
                    )
                except Exception as e:
                    self.logger.warning(
                        "Trinity Score 계산 실패, 정적 점수 사용: %s", e
                    )
                    dynamic_trinity_score = None

            # 동적 점수가 없으면 정적 점수 사용
            final_philosophy_score = dynamic_trinity_score
            if final_philosophy_score is None:
                final_philosophy_score = (
                    PhilosophyScores(
                        truth=(
                            base_philosophy_scores["truth"]
                            if base_philosophy_scores
                            else 85.0
                        ),
                        goodness=(
                            base_philosophy_scores["goodness"]
                            if base_philosophy_scores
                            else 80.0
                        ),
                        beauty=(
                            base_philosophy_scores["beauty"]
                            if base_philosophy_scores
                            else 75.0
                        ),
                        serenity=(
                            base_philosophy_scores["serenity"]
                            if base_philosophy_scores
                            else 90.0
                        ),
                    )
                    if base_philosophy_scores
                    else None
                )

            # 실행 결과 생성
            execution_result = SkillExecutionResult(
                skill_id=request.skill_id,
                success=True,
                status="success",
                result=result,
                execution_time_ms=execution_time,
                philosophy_score=final_philosophy_score,
                error=None,
            )

            # 실행 통계 기록
            self._record_execution_stats(request.skill_id, execution_result)

            self.logger.info(
                "✅ 스킬 실행 완료: %s (%.2fms)", request.skill_id, execution_time
            )

            return execution_result

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            error_msg = str(e)

            execution_result = SkillExecutionResult(
                skill_id=request.skill_id,
                success=False,
                status="error",
                result={},
                execution_time_ms=execution_time,
                error=error_msg,
                philosophy_score=None,
            )

            self.logger.error("❌ 스킬 실행 실패: %s - %s", request.skill_id, error_msg)
            return execution_result

    async def _execute_skill_logic(
        self, skill: Any, parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """
        실제 스킬 실행 로직 (현재는 mock 구현)

        Args:
            skill: 실행할 스킬
            parameters: 실행 파라미터

        Returns:
            실행 결과
        """
        # 현재는 mock 구현 - 실제로는 각 스킬의 execution_mode에 따라 다르게 처리
        await asyncio.sleep(0.1)  # 모의 실행 시간

        # execution_mode는 ExecutionMode enum이므로 .value로 비교
        execution_mode_value = (
            skill.execution_mode.value
            if hasattr(skill.execution_mode, "value")
            else str(skill.execution_mode)
        )

        if execution_mode_value == "local_function":
            # 로컬 함수 실행 (예: skill_002_trinity_analysis)
            return await self._execute_local_function(skill, parameters)
        elif execution_mode_value == "n8n_workflow":
            # n8n 워크플로우 실행
            return await self._execute_n8n_workflow(skill, parameters)
        elif execution_mode_value == "browser_script":
            # 브라우저 스크립트 실행
            return await self._execute_browser_script(skill, parameters)
        elif execution_mode_value == "api_call":
            # API 호출
            return await self._execute_api_call(skill, parameters)
        else:
            return {"message": f"Executed skill {skill.skill_id} with mock result"}

    async def _execute_local_function(
        self, skill: Any, parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """로컬 함수 실행"""
        # 실제로는 skill.local_function_name을 import해서 실행
        return {"message": f"Executed local function for {skill.skill_id}"}

    async def _execute_n8n_workflow(
        self, skill: Any, parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """n8n 워크플로우 실행"""
        # 실제로는 n8n API 호출
        return {"message": f"Executed n8n workflow for {skill.skill_id}"}

    async def _execute_browser_script(
        self, skill: Any, parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """브라우저 스크립트 실행"""
        # 실제로는 브라우저 자동화
        return {"message": f"Executed browser script for {skill.skill_id}"}

    async def _execute_api_call(
        self, skill: Any, parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """API 호출 실행"""
        # 실제로는 HTTP 요청
        return {"message": f"Executed API call for {skill.skill_id}"}

    def _record_execution_stats(
        self, skill_id: str, result: SkillExecutionResult
    ) -> None:
        """실행 통계 기록"""
        self.execution_stats[skill_id].update(
            {
                "last_execution": datetime.utcnow(),
                "success_rate": 1.0 if result.status == "success" else 0.0,
                "avg_execution_time": result.execution_time_ms,
            }
        )

    async def delete_skill(self, skill_id: str) -> bool:
        """
        스킬 삭제

        Args:
            skill_id: 삭제할 스킬 ID

        Returns:
            삭제 성공 여부
        """
        try:
            if not self.skill_registry:
                return False

            if skill_id in self.skill_registry.skills:
                del self.skill_registry.skills[skill_id]
                self.logger.info("✅ 스킬 삭제됨: %s", skill_id)
                return True

            return False

        except Exception as e:
            self.logger.error("❌ 스킬 삭제 실패: %s", e)
            return False

    async def get_stats(self) -> SkillStatsResponse:
        """
        스킬 통계 조회

        Returns:
            스킬 통계 정보
        """
        try:
            if not self.skill_registry:
                return SkillStatsResponse(
                    total_skills=0,
                    active_skills=0,
                    recent_executions=0,
                    avg_execution_time=0.0,
                    philosophy_distribution={},
                )

            total_skills = len(self.skill_registry.__class__._skills)
            all_skills = list(self.skill_registry.__class__._skills.values())
            # status는 SkillStatus enum이므로 .value로 비교하거나 enum 직접 비교
            if SkillStatus is not None and hasattr(SkillStatus, "ACTIVE"):
                active_skills = sum(
                    1
                    for s in all_skills
                    if (hasattr(s.status, "value") and s.status.value == "active")
                    or (s.status == SkillStatus.ACTIVE)
                    or str(s.status) == "active"
                )
            else:
                # SkillStatus가 없을 때는 문자열 비교
                active_skills = sum(
                    1
                    for s in all_skills
                    if (hasattr(s.status, "value") and s.status.value == "active")
                    or str(s.status) == "active"
                )

            # 카테고리별 통계
            category_stats = self.skill_registry.get_category_stats()
            self.logger.info("🔍 Raw category stats: %s", category_stats)

            # dict[str, int]를 SkillCategoryStats로 변환
            categories = []
            for cat_name, count in category_stats.items():
                # 해당 카테고리의 스킬들 가져오기
                category_skills = [
                    skill
                    for skill in self.skill_registry._skills.values()
                    if skill.category == cat_name
                ]

                # 평균 철학 점수 계산
                avg_philosophy = 0.0
                if category_skills:
                    total_philosophy = sum(
                        skill.philosophy_scores.average for skill in category_skills
                    )
                    avg_philosophy = total_philosophy / len(category_skills)

                # 실행 횟수 계산 (실제로는 execution_stats에서 가져와야 함)
                execution_count = self.execution_stats.get(cat_name, {}).get(
                    "execution_count", 0
                )

                cat_stat = SkillCategoryStats(
                    category=cat_name,
                    count=count,
                    avg_philosophy=round(avg_philosophy, 2),
                    execution_count=execution_count,
                    description=_get_category_description(cat_name),
                )
                categories.append(cat_stat)
                self.logger.info(
                    "📊 Category %s: %d skills, avg philosophy: %.2f",
                    cat_name,
                    count,
                    avg_philosophy,
                )

            # 철학 점수 분포 계산
            philosophy_distribution = self._calculate_philosophy_distribution()

            return SkillStatsResponse(
                total_skills=total_skills,
                active_skills=active_skills,
                categories=categories,
                recent_executions=self._get_recent_executions(),
                avg_execution_time=self._get_avg_execution_time(),
                philosophy_distribution=philosophy_distribution,
            )

        except Exception as e:
            self.logger.error("❌ 스킬 통계 조회 실패: %s", e)
            return SkillStatsResponse(
                total_skills=0,
                active_skills=0,
                categories=[],
                recent_executions=0,
                avg_execution_time=0.0,
                philosophy_distribution={},
            )

    def _calculate_philosophy_distribution(self) -> dict[str, int]:
        """철학 점수 분포 계산"""
        distribution = {"90-95": 0, "95-100": 0}

        if not self.skill_registry:
            return distribution

        for skill in self.skill_registry.__class__._skills.values():
            avg_score = skill.philosophy_scores.average
            if 90 <= avg_score < 95:
                distribution["90-95"] += 1
            elif 95 <= avg_score <= 100:
                distribution["95-100"] += 1

        return distribution

    def _get_recent_executions(self) -> int:
        """최근 24시간 실행 횟수"""
        # 실제로는 타임스탬프 기반 계산 필요
        return sum(
            stats.get("execution_count", 0) for stats in self.execution_stats.values()
        )

    def _get_avg_execution_time(self) -> float:
        """평균 실행 시간"""
        times = [
            stats.get("avg_execution_time", 0)
            for stats in self.execution_stats.values()
        ]
        return sum(times) / len(times) if times else 0.0

    async def health_check(self) -> dict[str, Any]:
        """서비스 헬스 체크"""
        return {
            "service": "skills",
            "status": "healthy" if self.skill_registry else "degraded",
            "philosophy": "眞善美孝",
            "registry_available": self.skill_registry is not None,
            "total_skills": (
                len(self.skill_registry.__class__._skills) if self.skill_registry else 0
            ),
        }


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
        "health_monitoring": "시스템 건강 모니터링 (11-오장육부)",
        "strategic_command": "전략적 명령 처리 (LangGraph)",
        "memory_management": "메모리 시스템 관리",
    }
    return descriptions.get(category, f"{category} 카테고리")
