# Trinity Score: 95.0 (Established by Chancellor)
"""
AFO Infrastructure LLM Package (infrastructure/llm/__init__.py)

Core infrastructure for LLM routing and execution.
"""

from .models import LLMConfig, LLMProvider, QualityTier, RoutingDecision
from .providers import call_llm, call_ollama, query_google
from .router import LLMRouter

__all__ = [
    "LLMConfig",
    "LLMProvider",
    "QualityTier",
    "RoutingDecision",
    "call_llm",
    "call_ollama",
    "query_google",
    "LLMRouter",
]
