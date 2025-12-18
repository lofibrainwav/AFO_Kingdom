"""
Universal Model Adapter Interface (Eternity Pillar)
Part of the "100% Score" Strategy.

Purpose:
Define a standard Protocol for ALL AI models (current and future).
This guarantees that Trinity OS can adapt to GPT-5, Gemini 2, or any future architecture
without refactoring the core logic, ensuring "Eternity".
"""

from collections.abc import AsyncIterator
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class UniversalModelInterface(Protocol):
    """
    The Eternity Contract:
    Any model that implements this interface can be plug-and-played into Trinity OS.
    """

    async def ask(self, prompt: str, **kwargs: Any) -> str:
        """Standard synchronous-like request"""
        ...

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        """Standard streaming response"""
        ...

    async def embed(self, text: str) -> list[float]:
        """Standard embedding generation"""
        ...

    def get_metadata(self) -> dict[str, Any]:
        """Return model capabilities, cost per token, and context window"""
        ...


# Example Stub Implementation (Proof of Concept)
class MockUniversalAdapter:
    def get_metadata(self) -> dict[str, Any]:
        return {"name": "mock-adapter", "version": "0.1"}

    async def ask(self, prompt: str, **kwargs: Any) -> str:
        return f"Mock answer to: {prompt[:20]}..."

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncIterator[str]:
        yield "Mock "
        yield "stream"

    async def embed(self, text: str) -> list[float]:
        return [0.0] * 1536
