# Trinity Score: 98.0 (Established by Chancellor)
# afo_soul_engine/llm_router.py
"""
AFO LLM Router (Strangler Fig Facade)

This module now serves as a facade for the modularized infrastructure/llm package.
All core models and routing logic have been moved to infrastructure/llm/.
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Add package root to sys.path to ensure 'infrastructure' is importable
package_root = os.path.dirname(os.path.abspath(__file__))
if package_root not in sys.path:
    sys.path.append(package_root)

# Import from core infrastructure package (Strangler Fig)
try:
    from infrastructure.llm import (
        LLMConfig,
        LLMProvider,
        LLMRouter,
        QualityTier,
        RoutingDecision,
        call_llm,
    )
except ImportError:
    # Fallback for different execution contexts
    from AFO.infrastructure.llm import (  # type: ignore
        LLMConfig,
        LLMProvider,
        LLMRouter,
        QualityTier,
        RoutingDecision,
        call_llm,
    )

# ============================================================================
# Global Router Instance
# ============================================================================

llm_router = LLMRouter()

# ============================================================================
# Compatibility Interface
# ============================================================================


async def route_and_execute(
    query: str, context: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    LLM 라우팅 및 실행 인터페이스 (Compatibility Layer)
    """
    return await llm_router.execute_with_routing(query, context)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "LLMConfig",
    "LLMProvider",
    "LLMRouter",
    "QualityTier",
    "RoutingDecision",
    "call_llm",
    "llm_router",
    "route_and_execute",
]

# ============================================================================
# Self-Test
# ============================================================================

if __name__ == "__main__":
    import asyncio

    async def self_test() -> None:
        print("=" * 70)
        print("AFO LLM Router - Facade Self-Test")
        print("=" * 70)

        # 1. Routing Test
        print("\n🔍 Testing Routing (Standard Quality)...")
        decision = llm_router.route_request("Hello, world!")
        print(f"   Selected Provider: {decision.selected_provider}")
        print(f"   Selected Model: {decision.selected_model}")
        print(f"   Reasoning: {decision.reasoning}")

        # 2. Execution Test (Dry mode equivalent or simple call)
        print("\n🚀 Testing Execution Interface...")
        try:
            result = await route_and_execute(
                "Translate 'Peace' to Korean", {"provider": "ollama"}
            )
            print(f"   Success: {result.get('success')}")
            if result.get("success"):
                print(f"   Response: {result.get('response')}")
        except Exception as e:  # nosec
            print(f"   Execution failed (expected if Ollama offline): {e}")

        print("\n✅ Facade self-test completed successfully!")

    asyncio.run(self_test())
