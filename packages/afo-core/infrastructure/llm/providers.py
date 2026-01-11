# Trinity Score: 92.0 (Established by Chancellor)
"""
AFO LLM Providers (infrastructure/llm/providers.py)

Implementation of provider-specific LLM calling logic.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from .models import LLMConfig, LLMProvider, RoutingDecision

logger = logging.getLogger(__name__)

# Optional imports for LLM wrappers
try:
    from AFO.llms.claude_api import claude_api
    from AFO.llms.cli_wrapper import CLIWrapper
    from AFO.llms.gemini_api import gemini_api
    from AFO.llms.openai_api import openai_api

    from services.ollama_service import ollama_service

    API_WRAPPERS_AVAILABLE = True
except ImportError:
    API_WRAPPERS_AVAILABLE = False
    claude_api = None  # type: ignore
    CLIWrapper = None  # type: ignore
    openai_api = None  # type: ignore
    gemini_api = None  # type: ignore
    ollama_service = None  # type: ignore


async def call_llm(
    decision: RoutingDecision,
    query: str,
    context: dict[str, Any] | None,
    llm_configs: dict[LLMProvider, LLMConfig],
) -> str:
    """Dispatches call to the appropriate LLM provider"""
    provider = decision.selected_provider
    config = llm_configs.get(provider)

    if not config:
        raise ValueError(f"No configuration found for provider: {provider}")

    try:
        if provider == LLMProvider.OLLAMA:
            return await call_ollama(query, config, context)
        elif provider == LLMProvider.GEMINI:
            return await query_google(query, config, context)
        elif provider == LLMProvider.ANTHROPIC:
            return await call_anthropic(query, config, context)
        elif provider == LLMProvider.OPENAI:
            return await call_openai(query, config, context)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    except Exception as e:
        logger.error(f"LLM call failed for {provider}: {e}")
        raise


async def call_ollama(
    query: str, config: LLMConfig, context: dict[str, Any] | None = None
) -> str:
    """Ollama API 호출 (Ollama API Call)"""
    import httpx

    base_url = config.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    timeout = float((context or {}).get("ollama_timeout_seconds", 30))
    model = (context or {}).get("ollama_model", config.model)

    # Robust Switching Protocol (if available)
    try:
        from AFO.config.settings import get_settings

        settings = get_settings()
        if (
            settings.OLLAMA_SWITCHING_PROTOCOL_ENABLED
            and ollama_service
            and hasattr(ollama_service, "ensure_model")
        ):
            await ollama_service.ensure_model(model)
    except Exception:  # nosec
        pass

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
            payload = {
                "model": model,
                "prompt": query,
                "stream": False,
                "options": {
                    "temperature": (context or {}).get(
                        "temperature", config.temperature
                    ),
                    "num_predict": (context or {}).get("max_tokens", config.max_tokens),
                    "num_ctx": (context or {}).get(
                        "ollama_num_ctx", config.context_window
                    ),
                },
            }
            response = await client.post(f"{base_url}/api/generate", json=payload)
            response.raise_for_status()
            return str(response.json().get("response", ""))
    except Exception:
        # Fallback to CLI Wrapper
        if CLIWrapper and CLIWrapper.is_available("ollama"):
            res = await CLIWrapper.execute_ollama(query)
            if res["success"]:
                return str(res["content"])
        raise


async def query_google(
    query: str, config: LLMConfig, context: dict[str, Any] | None
) -> str:
    """Google Gemini API 호출 (Gemini API Call)"""
    if not gemini_api or not gemini_api.is_available():
        raise RuntimeError("Gemini API not available")

    models_to_try = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]
    last_error = None
    ctx = context or {}

    for model_name in models_to_try:
        try:
            result = await gemini_api.generate(
                query,
                model=model_name,
                temperature=ctx.get("temperature", 0.7),
                max_tokens=ctx.get("max_tokens", 1000),
            )
            if result.get("success"):
                return str(result.get("content", ""))
            last_error = Exception(result.get("error", "Unknown error"))
        except Exception as e:
            last_error = e

    raise last_error or RuntimeError("All Gemini models failed")


async def call_anthropic(
    query: str, config: LLMConfig, context: dict[str, Any] | None
) -> str:
    """Anthropic Claude API 호출 (Claude API Call)"""
    if claude_api and claude_api.is_available():
        result = await claude_api.generate(query, max_tokens=1024)
        if result.get("success"):
            return str(result.get("content", ""))

    if CLIWrapper and CLIWrapper.is_available("claude"):
        res = await CLIWrapper.execute_claude(query)
        if res["success"]:
            return str(res["content"])

    raise RuntimeError("Anthropic provider unavailable")


async def call_openai(
    query: str, config: LLMConfig, context: dict[str, Any] | None
) -> str:
    """OpenAI API 호출 (OpenAI API Call)"""
    if openai_api and openai_api.is_available():
        result = await openai_api.generate(query, max_tokens=1024)
        if result.get("success"):
            return str(result.get("content", ""))

    if CLIWrapper and CLIWrapper.is_available("codex"):
        res = await CLIWrapper.execute_codex(query)
        if res["success"]:
            return str(res["content"])

    raise RuntimeError("OpenAI provider unavailable")
