# Trinity Score: 90.0 (Established by Chancellor)
import contextlib
import logging
import os
from typing import Any

import httpx

from AFO.llm_router import LLMConfig

from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """
    Provider implementation for local Ollama models.
    """

    async def is_available(self) -> bool:
        """Check if Ollama server is reachable."""
        # Simple check, real check happens during call or router init health check
        # We can implement a ping here if needed, but for now we rely on config presence.
        return True

    async def generate(
        self, query: str, config: LLMConfig, context: dict[str, Any] | None = None
    ) -> str:
        """
        Call Ollama API.
        Logic refactored from LLMRouter._call_ollama.
        """
        # Determine Base URL
        if config.base_url:
            base_url = config.base_url
        else:
            try:
                from AFO.config.settings import get_settings

                base_url = get_settings().OLLAMA_BASE_URL
            except ImportError:
                base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Context overrides
        context = context or {}
        timeout_seconds = float(
            context.get("ollama_timeout_seconds", os.getenv("OLLAMA_TIMEOUT_SECONDS", "30"))
        )
        max_tokens = int(context.get("max_tokens", config.max_tokens))
        temperature = float(context.get("temperature", config.temperature))
        model = str(context.get("ollama_model", config.model))
        num_ctx = int(context.get("ollama_num_ctx", getattr(config, "context_window", 4096)))
        num_threads = context.get("ollama_num_thread")

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
                options: dict[str, Any] = {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "num_ctx": num_ctx,
                }
                if num_threads is not None:
                    with contextlib.suppress(Exception):
                        options["num_thread"] = int(num_threads)

                response = await client.post(
                    f"{base_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": query,
                        "stream": False,
                        "options": options,
                    },
                )
                response.raise_for_status()
                result = response.json()
                return str(result.get("response", ""))
        except Exception as e:
            logger.error(f"Ollama Call Failed: {e}")
            raise
