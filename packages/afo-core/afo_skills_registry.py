# Trinity Score: 98.0 (Established by Chancellor)
# afo_soul_engine/afo_skills_registry.py
"""
AFO Skill Registry System (Strangler Fig Facade)

This module now serves as a facade for the modularized domain/skills package.
All core models and registry logic have been moved to domain/skills/.
"""

from __future__ import annotations

import os
import sys

# Add package root to sys.path to ensure 'domain' is importable
package_root = os.path.dirname(os.path.abspath(__file__))
if package_root not in sys.path:
    sys.path.append(package_root)

# Import from core domain package (Strangler Fig)
try:
    from domain.skills import (AFOSkillCard, ExecutionMode, MCPConfig,
                               PhilosophyScore, SkillCategory,
                               SkillExecutionRequest, SkillExecutionResult,
                               SkillFilterParams, SkillIOSchema,
                               SkillParameter, SkillRegistry, SkillStatus,
                               register_core_skills)
except ImportError:
    # Fallback for different execution contexts
    from AFO.domain.skills import ExecutionMode  # type: ignore
    from AFO.domain.skills import (AFOSkillCard, MCPConfig, PhilosophyScore,
                                   SkillCategory, SkillExecutionRequest,
                                   SkillExecutionResult, SkillFilterParams,
                                   SkillIOSchema, SkillParameter,
                                   SkillRegistry, SkillStatus,
                                   register_core_skills)

# ============================================================================
# Global Registry Instance
# ============================================================================

skills_registry: SkillRegistry = register_core_skills()

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "AFOSkillCard",
    "ExecutionMode",
    "MCPConfig",
    "PhilosophyScore",
    "SkillCategory",
    "SkillExecutionRequest",
    "SkillExecutionResult",
    "SkillFilterParams",
    "SkillIOSchema",
    "SkillParameter",
    "SkillRegistry",
    "SkillStatus",
    "register_core_skills",
    "skills_registry",
]

# ============================================================================
# Self-Test
# ============================================================================

if __name__ == "__main__":
    import asyncio

    async def self_test() -> None:
        print("=" * 70)
        print("AFO Skill Registry - Facade Self-Test")
        print("=" * 70)

        # 1. Registration Test
        count = skills_registry.count()
        print(f"\n📋 Total skills registered: {count}")

        # 2. Filter Test
        print("\n🔍 Filter check: RAG Systems...")
        rag_skills = skills_registry.filter(
            SkillFilterParams(category=SkillCategory.RAG_SYSTEMS)
        )
        for s in rag_skills:
            print(f"  - {s.name} ({s.skill_id})")

        # 3. Model Rebuild Test (Ensure Pydantic is healthy)
        try:
            AFOSkillCard.model_rebuild()
            print("\n✅ Pydantic model rebuild successful!")
        except Exception as e:  # nosec
            print(f"\n❌ Model rebuild failed: {e}")

        print("\n✅ Facade self-test completed successfully!")

    asyncio.run(self_test())
