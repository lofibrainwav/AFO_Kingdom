from unittest.mock import patch

import pytest
from AFO.afo_skills_registry import (
    AFOSkillCard,
    PhilosophyScore,
    SkillCategory,
    SkillRegistry,
)


class TestSkillRegistry:
    def setup_method(self):
        # Reset registry before each test
        SkillRegistry._instance = None
        SkillRegistry._skills = {}

    def test_singleton(self):
        r1 = SkillRegistry()
        r2 = SkillRegistry()
        assert r1 is r2

    def test_register_and_get(self):
        registry = SkillRegistry()
        skill = AFOSkillCard(
            skill_id="skill_999_test",
            name="Test Skill",
            description="A test skill description that is long enough",
            category=SkillCategory.INTEGRATION,
            version="1.0.0",
            philosophy_scores=PhilosophyScore(truth=10, goodness=10, beauty=10, serenity=10),
        )
        assert registry.register(skill) is True
        # Register again returns False
        assert registry.register(skill) is False

        fetched = registry.get("skill_999_test")
        assert fetched == skill
        assert fetched.name == "Test Skill"

    def test_filter_category(self):
        registry = SkillRegistry()
        s1 = AFOSkillCard(
            skill_id="skill_001_s1",
            name="Skill One",
            description="Desc for S1.........",
            category=SkillCategory.INTEGRATION,
            version="1.0.0",
            philosophy_scores=PhilosophyScore(truth=10, goodness=10, beauty=10, serenity=10),
        )
        s2 = AFOSkillCard(
            skill_id="skill_002_s2",
            name="Skill Two",
            description="Desc for S2.........",
            category=SkillCategory.HEALTH_MONITORING,
            version="1.0.0",
            philosophy_scores=PhilosophyScore(truth=10, goodness=10, beauty=10, serenity=10),
        )
        registry.register(s1)
        registry.register(s2)

        from AFO.afo_skills_registry import SkillFilterParams

        results = registry.filter(SkillFilterParams(category=SkillCategory.INTEGRATION))
        assert len(results) == 1
        assert results[0].skill_id == "skill_001_s1"

    def test_filter_search(self):
        registry = SkillRegistry()
        s1 = AFOSkillCard(
            skill_id="skill_001_s1",
            name="Apple Skill",
            description="A red fruit description",
            category=SkillCategory.INTEGRATION,
            version="1.0.0",
            philosophy_scores=PhilosophyScore(truth=10, goodness=10, beauty=10, serenity=10),
        )
        registry.register(s1)

        from AFO.afo_skills_registry import SkillFilterParams

        # Match name
        assert len(registry.filter(SkillFilterParams(search="Apple"))) == 1
        # Match desc
        assert len(registry.filter(SkillFilterParams(search="fruit"))) == 1
        # No match
        assert len(registry.filter(SkillFilterParams(search="banana"))) == 0

    def test_philosophy_score_properties(self):
        score = PhilosophyScore(truth=100, goodness=50, beauty=50, serenity=0)
        assert score.average == 50.0
        # Check for Chinese characters as per implementation
        assert "眞" in score.summary

    def test_validation_logic(self):
        from pydantic import ValidationError

        # Test invalid semantic version
        with pytest.raises(ValidationError):
            AFOSkillCard(
                skill_id="skill_000_bad",
                name="Bad Skill",
                description="Bad desc.....",
                category=SkillCategory.INTEGRATION,
                version="v1.0",  # Invalid pattern
                philosophy_scores=PhilosophyScore(truth=0, goodness=0, beauty=0, serenity=0),
            )

    def test_stats(self):
        registry = SkillRegistry()
        registry.register(
            AFOSkillCard(
                skill_id="skill_001_stat_test",
                name="Skill Stats",
                description="D1..........",
                category=SkillCategory.INTEGRATION,
                version="1.0.0",
                philosophy_scores=PhilosophyScore(truth=0, goodness=0, beauty=0, serenity=0),
            )
        )
        assert registry.count() == 1
        stats = registry.get_category_stats()
        assert stats[SkillCategory.INTEGRATION.value] == 1

    def test_built_in_registration(self):
        from AFO.afo_skills_registry import register_core_skills

        # Mock settings if needed, or rely on defaults/env
        with patch("AFO.afo_skills_registry._get_mcp_server_url", return_value="http://mock-mcp"):
            registry = register_core_skills()
            assert registry.count() > 0
            assert registry.get("skill_001_youtube_spec_gen") is not None
