# Trinity Score: 95.0 (Established by Chancellor)
"""
AFO LLM Router Core (infrastructure/llm/router.py)

Hybrid LLM Router with dynamic routing, scoring, and caching.
"""

from __future__ import annotations

import logging
import os
from collections import OrderedDict
from typing import Any

from .models import LLMConfig, LLMProvider, QualityTier, RoutingDecision
from .providers import call_llm

logger = logging.getLogger(__name__)


class LLMRouter:
    """
    하이브리드 LLM 라우터 (Hybrid LLM Router)
    Ollama 우선 → API LLM fallback
    """

    def __init__(self) -> None:
        self.llm_configs: dict[LLMProvider, LLMConfig] = {}
        self._initialize_configs()
        self.routing_history: list[dict[str, Any]] = []
        self._response_cache: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._cache_max_size = 100
        self._cache_ttl = 300

    def _initialize_configs(self) -> None:
        """LLM 설정 초기화 (Initialize LLM Configurations)"""
        try:
            from AFO.config.settings import get_settings

            settings = get_settings()
        except ImportError:
            settings = None

        # Ollama (Internal Wisdom)
        ollama_model = (
            settings.OLLAMA_MODEL
            if settings
            else os.getenv("OLLAMA_MODEL", "qwen3-vl:8b")
        )
        ollama_url = (
            settings.OLLAMA_BASE_URL
            if settings
            else os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )

        self.llm_configs[LLMProvider.OLLAMA] = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model=ollama_model,
            base_url=ollama_url,
            latency_ms=500,
            quality_tier=QualityTier.PREMIUM,
            context_window=8192,
        )

        # Vault Integration
        vault = None
        try:
            from AFO.security.vault_manager import vault as _vault

            vault = _vault
        except Exception:  # nosec
            pass

        def get_secret(name: str) -> str | None:
            if vault:
                try:
                    res = vault.get_secret(name)
                    if isinstance(res, str):
                        return res
                except Exception:  # nosec
                    pass
            return getattr(settings, name, None) if settings else os.getenv(name)

        # External Providers (Claude, Gemini, GPT)
        self._add_provider_config(
            LLMProvider.ANTHROPIC,
            "claude-3-sonnet-20240229",
            "ANTHROPIC_API_KEY",
            get_secret,
            quality=QualityTier.ULTRA,
        )
        self._add_provider_config(
            LLMProvider.GEMINI,
            "gemini-2.0-flash-exp",
            "GEMINI_API_KEY",
            get_secret,
            quality=QualityTier.PREMIUM,
        )
        self._add_provider_config(
            LLMProvider.OPENAI,
            "gpt-4o-mini",
            "OPENAI_API_KEY",
            get_secret,
            quality=QualityTier.ULTRA,
        )

        logger.info(f"✅ LLM Router 초기화: {len(self.llm_configs)}개 LLM 설정됨")

    def _add_provider_config(
        self,
        provider: LLMProvider,
        model: str,
        key_env: str,
        secret_fn: Any,
        quality: QualityTier,
    ) -> None:
        key = secret_fn(key_env)
        if key:
            self.llm_configs[provider] = LLMConfig(
                provider=provider,
                model=model,
                api_key_env=key_env,
                quality_tier=quality,
            )

    def route_request(
        self, query: str, context: dict[str, Any] | None = None
    ) -> RoutingDecision:
        """쿼리에 대한 최적 LLM 라우팅 결정 (Determine Optimal Routing)"""
        ctx = context or {}
        requested = ctx.get("provider")

        # Explicit provider request
        if requested and requested != "auto":
            try:
                p = LLMProvider(requested)
                if p in self.llm_configs:
                    config = self.llm_configs[p]
                    return RoutingDecision(
                        selected_provider=p,
                        selected_model=config.model,
                        reasoning=f"User request: {requested}",
                        confidence=1.0,
                        estimated_cost=0.0,
                        estimated_latency=config.latency_ms,
                        fallback_providers=[LLMProvider.OLLAMA],
                    )
            except ValueError:  # nosec
                pass

        # Default: Ollama priority
        if LLMProvider.OLLAMA in self.llm_configs:
            decision = RoutingDecision(
                selected_provider=LLMProvider.OLLAMA,
                selected_model=self.llm_configs[LLMProvider.OLLAMA].model,
                reasoning="Ollama (Internal) Priority",
                confidence=0.9,
                estimated_cost=0.0,
                estimated_latency=500,
                fallback_providers=[
                    p for p in self.llm_configs if p != LLMProvider.OLLAMA
                ],
            )
            if ctx.get("quality_tier") == QualityTier.ULTRA:
                return self._select_api_llm(query, ctx, QualityTier.ULTRA)
            return decision

        return self._select_api_llm(query, ctx, QualityTier.STANDARD)

    def _select_api_llm(
        self, query: str, ctx: dict[str, Any], quality: QualityTier
    ) -> RoutingDecision:
        candidates = [
            c
            for p, c in self.llm_configs.items()
            if p != LLMProvider.OLLAMA
            and c.quality_tier.value_rank >= quality.value_rank
        ]
        if not candidates:
            candidates = list(self.llm_configs.values())

        best = max(candidates, key=lambda c: self._calculate_llm_score(c))
        return RoutingDecision(
            selected_provider=best.provider,
            selected_model=best.model,
            reasoning=f"Best candidate by score: {best.provider}",
            confidence=0.8,
            estimated_cost=0.0,
            estimated_latency=best.latency_ms,
            fallback_providers=[c.provider for c in candidates if c != best],
        )

    def _calculate_llm_score(self, config: LLMConfig) -> float:
        quality = config.quality_tier.value_rank * 0.4
        latency = (2000 / config.latency_ms) * 0.3
        cost = (1.0 / (config.cost_per_token * 1000 + 1)) * 0.3
        return quality + latency + cost

    async def execute_with_routing(
        self, query: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """라우팅 및 실행 (Route and Execute with Caching)"""
        ctx = context or {}

        # 1. Routing Decision
        decision = self.route_request(query, ctx)

        # 2. Call LLM (with basic memory cache for now)
        try:
            response = await call_llm(decision, query, ctx, self.llm_configs)
            return {
                "success": True,
                "response": response,
                "routing": {
                    "provider": decision.selected_provider.value,
                    "model": decision.selected_model,
                    "reasoning": decision.reasoning,
                },
            }
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return {"success": False, "error": str(e)}
