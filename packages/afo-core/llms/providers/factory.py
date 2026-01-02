# Trinity Score: 90.0 (Established by Chancellor)
import logging

from AFO..llm_router import import LLMProvider

from AFO.anthropic import import AnthropicProvider
from AFO.base import import BaseLLMProvider
from AFO.google import import GoogleProvider
from AFO.ollama import import OllamaProvider
from AFO.openai import import OpenAIProvider

logger = logging.getLogger(__name__)


class ProviderFactory:
    """
    Factory to get appropriate provider instance.
    """

    import typing

    _providers: typing.ClassVar[dict[LLMProvider, BaseLLMProvider]] = {}

    @classmethod
    def get_provider(cls, provider_type: LLMProvider) -> BaseLLMProvider:
        if provider_type in cls._providers:
            return cls._providers[provider_type]

        # Lazy initialization
        if provider_type == LLMProvider.OLLAMA:
            instance = OllamaProvider()
        elif provider_type == LLMProvider.GEMINI:
            instance = GoogleProvider()  # type: ignore[assignment]
        elif provider_type == LLMProvider.OPENAI:
            instance = OpenAIProvider()  # type: ignore[assignment]
        elif provider_type == LLMProvider.ANTHROPIC:
            instance = AnthropicProvider()  # type: ignore[assignment]
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")

        cls._providers[provider_type] = instance
        return instance
