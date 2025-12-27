# Trinity Score: 90.0 (Established by Chancellor)
import logging
from typing import Any

from AFO.llm_router import LLMConfig

from .base import BaseLLMProvider

# Late import to minimize top-level dependencies, or standard import
try:
    from AFO.llms.gemini_api import gemini_api
except ImportError:
    gemini_api = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


class GoogleProvider(BaseLLMProvider):
    """
    Provider implementation for Google Gemini models via REST API wrapper.
    """

    async def is_available(self) -> bool:
        return gemini_api is not None and gemini_api.is_available()

    async def generate(
        self, query: str, config: LLMConfig, context: dict[str, Any] | None = None
    ) -> str:
        """
        Call Gemini API.
        Logic refactored from LLMRouter._query_google.
        """
        if not self.is_available():
            raise ValueError("Gemini API Wrapper not available available")

        context = context or {}
        # Models to try - logic preserved from original router
        models_to_try = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]

        # If config specifies a model, prioritize it
        if config.model and config.model in models_to_try:
            # Move to front
            models_to_try.remove(config.model)
            models_to_try.insert(0, config.model)
        elif config.model:
            # Just try what's configured first
            models_to_try.insert(0, config.model)

        last_error = None

        for model_name in models_to_try:
            try:
                # Using the existing gemini_api wrapper which handles the REST details
                result = await gemini_api.generate(
                    query,
                    model=model_name,
                    temperature=context.get("temperature", config.temperature),
                    max_tokens=int(context.get("max_tokens", config.max_tokens)),
                )

                if result.get("success"):
                    content = result.get("content", "")
                    return str(content) if content is not None else ""
                else:
                    error_msg = result.get("error", "Unknown error")
                    logger.warning(f"⚠️ Gemini Model ({model_name}) Failed: {error_msg}")
                    last_error = Exception(str(error_msg))
                    continue

            except Exception as e:
                logger.warning(f"⚠️ Gemini Model ({model_name}) Failed: {e}")
                last_error = e
                continue

        if last_error:
            raise last_error

        raise RuntimeError("All Gemini models failed")
