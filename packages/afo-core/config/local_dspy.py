# Trinity Score: 90.0 (Established by Chancellor)
"""AFO Kingdom Local DSPy Configuration (眞善美孝永)

Configure DSPy to use local Ollama LLM without OpenAI API key.
Supports both ollama_chat and openai-compatible providers.

References:
- DSPy LM docs: https://dspy.ai/learn/programming/language_models/
- Ollama OpenAI compatibility: https://docs.ollama.com/api/openai-compatibility
"""

from __future__ import annotations

import logging
import os
from typing import Literal

logger = logging.getLogger(__name__)

# Provider types
ProviderType = Literal["ollama_chat", "openai"]


def configure_dspy_local_lm(
    *,
    model: str | None = None,
    base_url: str | None = None,
    provider: ProviderType | None = None,
) -> None:
    """Configure DSPy to use local Ollama (OpenAI key 불필요).

    Args:
        model: Ollama model name (default: deepseek-r1:14b)
        base_url: Ollama API base URL (default: http://localhost:11434)
        provider: LM provider type
            - "ollama_chat" (default): DSPy-native Ollama provider
            - "openai": OpenAI-compatible endpoint (/v1)

    Environment Variables:
        AFO_DSPY_MODEL: Override model name
        AFO_OLLAMA_BASE_URL: Override base URL
        AFO_DSPY_PROVIDER: Override provider type
        AFO_DRY_RUN: Skip configuration if "true"
    """
    try:
        import dspy
    except ImportError as e:
        raise ImportError("DSPy is not installed. Run: pip install dspy-ai") from e

    # Check DRY_RUN mode
    if os.getenv("AFO_DRY_RUN", "false").lower() == "true":
        logger.info("[DRY_RUN] Skipping LM configuration.")
        print("[DRY_RUN] Skipping LM configuration.")
        return

    # Resolve configuration from args or environment
    model = model or os.getenv("AFO_DSPY_MODEL", "deepseek-r1:14b")
    base_url = base_url or os.getenv("AFO_OLLAMA_BASE_URL", "http://localhost:11434")
    provider = provider or os.getenv("AFO_DSPY_PROVIDER", "ollama_chat")  # type: ignore[assignment]

    # Normalize base_url
    base_url = base_url.rstrip("/")

    try:
        if provider == "openai":
            # Ollama OpenAI-compatible API (requires /v1 suffix)
            api_base = f"{base_url}/v1"
            api_key = os.getenv("AFO_OPENAI_COMPAT_KEY", "ollama")

            lm = dspy.LM(
                f"openai/{model}",
                api_base=api_base,
                api_key=api_key,
            )
            logger.info(f"[AFO] DSPy LM configured: openai-compat @ {api_base}")

        else:
            # DSPy-native Ollama provider (ollama_chat)
            lm = dspy.LM(
                f"ollama_chat/{model}",
                api_base=base_url,
                api_key="",  # Ollama doesn't need API key
            )
            logger.info(f"[AFO] DSPy LM configured: ollama_chat @ {base_url}")

        dspy.configure(lm=lm)
        print(f"[AFO] DSPy configured: provider={provider} model={model} base={base_url}")

    except Exception as e:
        logger.error(f"[AFO] Failed to configure DSPy LM: {e}")
        raise


def get_available_ollama_models() -> list[str]:
    """Get list of available Ollama models.

    Returns:
        List of model names, or empty list if Ollama unavailable.
    """
    import subprocess

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            return [line.split()[0] for line in lines if line.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


__all__ = ["configure_dspy_local_lm", "get_available_ollama_models"]
