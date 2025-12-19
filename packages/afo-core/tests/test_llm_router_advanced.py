import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from AFO.llm_router import LLMConfig, LLMProvider, LLMRouter, QualityTier, RoutingDecision


# Test Initialization
def test_router_initialization_env_vars():
    # Mock get_settings to return an object with keys
    mock_settings = MagicMock()
    mock_settings.ANTHROPIC_API_KEY = os.getenv("TEST_ANT_KEY", "mock-ant-key")
    mock_settings.OPENAI_API_KEY = os.getenv("TEST_OPENAI_KEY", "mock-openai-key")
    mock_settings.GEMINI_API_KEY = os.getenv("TEST_GEMINI_KEY", "mock-gemini-key")
    mock_settings.GOOGLE_API_KEY = None
    mock_settings.OLLAMA_MODEL = "test-model"
    mock_settings.OLLAMA_BASE_URL = "http://localhost:11434"

    mock_config_module = MagicMock()
    mock_config_module.get_settings.return_value = mock_settings

    # Patch sys.modules to inject mock config
    with patch.dict(
        sys.modules,
        {"config.settings": mock_config_module, "AFO.config.settings": mock_config_module},
    ):
        router = LLMRouter()
        assert LLMProvider.ANTHROPIC in router.llm_configs
        assert LLMProvider.OPENAI in router.llm_configs
        assert LLMProvider.GEMINI in router.llm_configs
        assert router.llm_configs[LLMProvider.OLLAMA].model == "test-model"


# Test Routing Logic: Explicit Provider
def test_route_explicit_provider():
    router = LLMRouter()
    # Mock configs to ensure provider exists
    router.llm_configs[LLMProvider.OPENAI] = LLMConfig(LLMProvider.OPENAI, "gpt-4")

    decision = router.route_request("hi", context={"provider": "openai"})
    assert decision.selected_provider == LLMProvider.OPENAI
    assert "명시적 요청" in decision.reasoning


def test_route_explicit_provider_invalid():
    router = LLMRouter()
    decision = router.route_request("hi", context={"provider": "invalid_provider"})
    # Should fall back to default logic (Ollama if available)
    with patch.object(router, "_is_ollama_available", return_value=True):
        assert decision.selected_provider == LLMProvider.OLLAMA


# Test Routing Logic: Ollama Priority
def test_route_ollama_priority():
    router = LLMRouter()
    with patch.object(router, "_is_ollama_available", return_value=True):
        decision = router.route_request("simple query")
        assert decision.selected_provider == LLMProvider.OLLAMA
        assert decision.confidence == 0.9


# Test Routing Logic: Upgrade to Ultra
def test_route_upgrade_to_ultra():
    router = LLMRouter()
    # Ensure we have an ULTRA provider
    router.llm_configs[LLMProvider.ANTHROPIC] = LLMConfig(
        LLMProvider.ANTHROPIC, "claude-3-opus", quality_tier=QualityTier.ULTRA, cost_per_token=0.01
    )
    router.llm_configs[LLMProvider.OLLAMA] = LLMConfig(LLMProvider.OLLAMA, "local")

    with patch.object(router, "_is_ollama_available", return_value=True):
        # Request ULTRA quality
        decision = router.route_request("hard query", context={"quality_tier": QualityTier.ULTRA})
        assert decision.selected_provider == LLMProvider.ANTHROPIC
        assert "ULTRA 품질 요구사항" in decision.reasoning


# Test Routing Logic: API Selection (No Ollama)
def test_route_api_selection():
    router = LLMRouter()
    # Setup candidates
    router.llm_configs[LLMProvider.OPENAI] = LLMConfig(
        LLMProvider.OPENAI, "gpt-4", quality_tier=QualityTier.ULTRA, latency_ms=100
    )
    router.llm_configs[LLMProvider.ANTHROPIC] = LLMConfig(
        LLMProvider.ANTHROPIC, "claude-3", quality_tier=QualityTier.ULTRA, latency_ms=2000
    )

    with patch.object(router, "_is_ollama_available", return_value=False):
        # Query asking for low latency
        decision = router.route_request("fast query", context={"max_latency_ms": 500})
        assert decision.selected_provider == LLMProvider.OPENAI  # Lower latency matches


# Test Execution Caching
@pytest.mark.asyncio
async def test_execution_caching():
    router = LLMRouter()
    router._call_llm = AsyncMock(return_value="Response")

    # 1st call
    await router.execute_with_routing("test query", {"key": "value"})
    assert router._call_llm.call_count == 1

    # 2nd call (Same)
    await router.execute_with_routing("test query", {"key": "value"})
    assert router._call_llm.call_count == 1  # Cached

    # 3rd call (Different context)
    await router.execute_with_routing("test query", {"key": "other"})
    assert router._call_llm.call_count == 2


# Test Provider Execution: Gemini (Google) with Retry
@pytest.mark.asyncio
async def test_call_gemini_retry():
    router = LLMRouter()
    config = LLMConfig(LLMProvider.GEMINI, "gemini-pro", api_key_env="GEMINI_API_KEY")

    # Mock google.generativeai module
    mock_genai_module = MagicMock()
    model_mock = MagicMock()
    mock_genai_module.GenerativeModel.return_value = model_mock

    # Setup failure then success
    model_mock.generate_content_async = AsyncMock(
        side_effect=[Exception("Error1"), MagicMock(text="Success")]
    )

    # Mock settings
    mock_settings = MagicMock()
    mock_settings.GEMINI_API_KEY = "fake-key"
    mock_config_module = MagicMock()
    mock_config_module.get_settings.return_value = mock_settings

    # Patch _get_google_module to return our mock
    # Also patch settings to avoid import errors
    with patch.object(router, "_get_google_module", return_value=mock_genai_module):
        with patch.object(router, "_is_ollama_available", return_value=False):
            with patch.dict(
                sys.modules,
                {"config.settings": mock_config_module, "AFO.config.settings": mock_config_module},
            ):
                response = await router._query_google("query", config, None)

                assert response == "Success"
                # Verify it retried
                assert model_mock.generate_content_async.call_count == 2
                # Verify models tried: first fails, second succeeds
                mock_genai_module.GenerativeModel.assert_any_call("gemini-2.0-flash-exp")
                mock_genai_module.GenerativeModel.assert_any_call("gemini-flash-latest")


# Test Provider Execution: Ollama
@pytest.mark.asyncio
async def test_call_ollama():
    router = LLMRouter()
    config = LLMConfig(LLMProvider.OLLAMA, "llama3")

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200, json=lambda: {"response": "Ollama Response"}
        )

        response = await router._call_ollama("hi", config)
        assert response == "Ollama Response"


# Test Provider Execution: Anthropic
@pytest.mark.asyncio
async def test_call_anthropic():
    router = LLMRouter()
    router.llm_configs[LLMProvider.ANTHROPIC] = LLMConfig(LLMProvider.ANTHROPIC, "claude")

    decision = RoutingDecision(LLMProvider.ANTHROPIC, "claude-3", "reason", 1.0, 0.0, 100, [])

    # Mock claude_api wrapper
    with patch("AFO.llm_router.claude_api") as mock_api:
        mock_api.is_available.return_value = True
        mock_api.generate = AsyncMock(return_value={"success": True, "content": "Claude Response"})

        # Mock API_WRAPPERS_AVAILABLE
        with patch("AFO.llm_router.API_WRAPPERS_AVAILABLE", True):
            response = await router._call_llm(decision, "hi", None)
            assert response == "Claude Response"


# Test Fallback
@pytest.mark.asyncio
async def test_fallback_execution():
    router = LLMRouter()
    router.llm_configs[LLMProvider.OLLAMA] = LLMConfig(LLMProvider.OLLAMA, "backup")

    # Make primary fail
    router._call_llm = AsyncMock(side_effect=Exception("Primary Failed"))

    # Test _try_fallback
    result = await router._try_fallback(LLMProvider.OLLAMA, "query", None)
    assert result["success"] is True
    assert "ollama" in result["response"].lower()
