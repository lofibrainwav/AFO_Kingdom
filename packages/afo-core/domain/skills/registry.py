# Trinity Score: 95.0 (Established by Chancellor)
"""
AFO Skill Registry (domain/skills/registry.py)

Centralized management and filtering of AFO skills.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from .models import AFOSkillCard, ExecutionMode, SkillCategory, SkillStatus

# = ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Filter Models
# = ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


class SkillFilterParams(BaseModel):
    """
    Query parameters for filtering skills

    Uses FastAPI 0.115+ Pydantic Query Parameter Models
    """

    category: SkillCategory | None = Field(
        default=None, description="Filter by category"
    )
    status: SkillStatus | None = Field(default=None, description="Filter by status")
    tags: list[str] | None = Field(
        default=None, description="Filter by tags (OR logic)"
    )
    search: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Search in name/description",
    )
    min_philosophy_avg: int | None = Field(
        default=None, ge=0, le=100, description="Minimum average philosophy score"
    )
    execution_mode: ExecutionMode | None = Field(
        default=None, description="Filter by execution mode"
    )
    limit: int = Field(default=100, ge=1, le=500, description="Maximum results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")


# = ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Skill Registry (Singleton)
# = ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


class SkillRegistry:
    """
    Central skill registry for AFO system

    Pattern: Singleton with in-memory storage + optional persistence
    """

    _instance = None
    _skills: ClassVar[dict[str, AFOSkillCard]] = {}

    def __new__(cls) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, skill: AFOSkillCard) -> bool:
        """Register a skill"""
        try:
            if skill.skill_id in self._skills:
                # Update existing skill
                self._skills[skill.skill_id] = skill
                return False  # Not a new registration
            else:
                self._skills[skill.skill_id] = skill
                return True  # New registration
        except Exception:
            return False

    def get(self, skill_id: str) -> AFOSkillCard | None:
        """Get skill by ID"""
        try:
            return self._skills.get(skill_id)
        except Exception:
            return None

    def list_all(self) -> list[AFOSkillCard]:
        """List all skills"""
        try:
            return list(self._skills.values())
        except Exception:
            return []

    def filter(self, params: SkillFilterParams) -> list[AFOSkillCard]:
        """Filter skills by parameters"""
        try:
            results = self.list_all()

            # Category filter
            if params.category:
                results = [s for s in results if s.category == params.category]

            # Status filter
            if params.status:
                results = [s for s in results if s.status == params.status]

            # Tags filter (OR logic)
            if params.tags:
                tag_set = {tag.lower() for tag in params.tags}
                results = [s for s in results if any(tag in tag_set for tag in s.tags)]

            # Search filter
            if params.search:
                search_lower = params.search.lower()
                results = [
                    s
                    for s in results
                    if search_lower in s.name.lower()
                    or search_lower in s.description.lower()
                ]

            # Philosophy score filter
            if params.min_philosophy_avg:
                results = [
                    s
                    for s in results
                    if s.philosophy_scores.average >= params.min_philosophy_avg
                ]

            # Execution mode filter
            if params.execution_mode:
                results = [
                    s for s in results if s.execution_mode == params.execution_mode
                ]

            # Pagination
            start = params.offset
            end = params.offset + params.limit
            return results[start:end]
        except Exception as e:
            print(f"⚠️ Skill filtering failed: {e}")
            return []

    def get_categories(self) -> list[str]:
        """Get all unique categories"""
        try:
            return [cat.value for cat in SkillCategory]
        except Exception:
            return []

    def get_category_stats(self) -> dict[str, int]:
        """Get category statistics (category -> count)"""
        try:
            stats: dict[str, int] = {}
            for skill in self._skills.values():
                category = skill.category.value
                if category not in stats:
                    stats[category] = 0
                stats[category] += 1
            return stats
        except Exception:
            return {}

    def count(self) -> int:
        """Total skill count"""
        return len(self._skills)

    def clear(self) -> None:
        """Clear all skills (for testing)"""
        self._skills.clear()

    @property
    def skills(self) -> dict[str, AFOSkillCard]:
        """Expose registry storage for backwards compatibility"""
        return self._skills
