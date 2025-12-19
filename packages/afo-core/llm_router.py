"""
AFO LLM Router - 하이브리드 멀티-LLM 통합 시스템
Ollama (내부 지력) + API LLM (외부 무력) 간 동적 라우팅

기능:
- Latency 기반 자동 fallback
- Cost 최적화 라우팅
- Quality 요구사항 기반 선택
- Graceful degradation
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import time
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import Any

# API wrapper imports
# [장자] 무용지용 - 불필요한 주석은 제거하여 진실을 드러냄
try:
    from AFO.llms.claude_api import claude_api
    from AFO.llms.gemini_api import gemini_api
    from AFO.llms.openai_api import openai_api

    API_WRAPPERS_AVAILABLE = True
except ImportError as e:
    API_WRAPPERS_AVAILABLE = False
    logging.warning(f"⚠️ API wrappers not available: {e}")

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM 제공자 타입"""

    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OPENAI = "openai"


class QualityTier(Enum):
    """품질 등급"""

    BASIC = "basic"  # 기본 응답
    STANDARD = "standard"  # 표준 품질
    PREMIUM = "premium"  # 고품질
    ULTRA = "ultra"  # 최고 품질


@dataclass
class LLMConfig:
    """LLM 설정"""

    provider: LLMProvider
    model: str
    api_key_env: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1024
    cost_per_token: float = 0.0
    latency_ms: int = 1000
    quality_tier: QualityTier = QualityTier.STANDARD
    context_window: int = 4096  # Default context window


@dataclass
class RoutingDecision:
    """라우팅 결정"""

    selected_provider: LLMProvider
    selected_model: str
    reasoning: str
    confidence: float
    estimated_cost: float
    estimated_latency: int
    fallback_providers: list[LLMProvider]


class LLMRouter:
    """
    하이브리드 LLM 라우터
    Ollama 우선 → API LLM fallback
    """

    def __init__(self) -> None:
        self.llm_configs: dict[LLMProvider, LLMConfig] = {}
        self._initialize_configs()
        self.routing_history: list[dict[str, Any]] = []
        # Simple LRU Cache
        self._response_cache: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._cache_max_size = 100
        self._cache_ttl = 300  # 5 minutes

    def _initialize_configs(self) -> None:
        """LLM 설정 초기화"""
        # Phase 2-4: settings 사용
        try:
            from AFO.config.settings import get_settings

            settings = get_settings()
        except ImportError:
            try:
                # [맹자] 득도다조 = 여러 길을 시도하여 도움을 구함
                from config.settings import get_settings  # type: ignore[assignment]

                settings = get_settings()
            except ImportError:
                settings = None

        # Ollama (내부 지력)
        ollama_model = (
            settings.OLLAMA_MODEL if settings else os.getenv("OLLAMA_MODEL", "qwen3-vl:8b")
        )
        ollama_base_url = (
            settings.OLLAMA_BASE_URL
            if settings
            else os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )

        self.llm_configs[LLMProvider.OLLAMA] = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model=ollama_model,  # Phase 2-4: settings 사용
            base_url=ollama_base_url,  # Phase 2-4: settings 사용
            temperature=0.7,
            max_tokens=2048,
            cost_per_token=0.0,  # 무료
            latency_ms=500,  # 로컬이므로 빠름
            quality_tier=QualityTier.PREMIUM,
            context_window=8192,  # Qwen3-VL-8B supports larger context
        )

        # Vault Integration - [손자] 지피지기 - 비밀을 아는 자가 승리함
        vault: Any = None
        try:
            from AFO.security.vault_manager import vault as _vault
            vault = _vault
        except (ImportError, ValueError):
            try:
                from security.vault_manager import vault as _v2
                vault = _v2
            except ImportError:
                vault = None

        # Helper to get secret
        def get_secret(name: str) -> str | None:
            if vault:
                # Type safe call
                res = vault.get_secret(name)
                return res if isinstance(res, str) else None
            return getattr(settings, name, None) if settings else os.getenv(name)

        # Anthropic (Claude)
        anthropic_key = get_secret("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.llm_configs[LLMProvider.ANTHROPIC] = LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                model="claude-3-sonnet-20240229",
                api_key_env="ANTHROPIC_API_KEY",
                temperature=0.7,
                max_tokens=4096,
                cost_per_token=0.000015,
                latency_ms=2000,
                quality_tier=QualityTier.ULTRA,
            )

        # Google Gemini
        gemini_key = get_secret("GEMINI_API_KEY")
        google_key = get_secret("GOOGLE_API_KEY")
        if gemini_key or google_key:
            self.llm_configs[LLMProvider.GEMINI] = LLMConfig(
                provider=LLMProvider.GEMINI,
                model="gemini-2.0-flash-exp",  # Updated to latest model
                api_key_env="GEMINI_API_KEY" if gemini_key else "GOOGLE_API_KEY",
                temperature=0.7,
                max_tokens=2048,
                cost_per_token=0.0000005,
                latency_ms=500,
                quality_tier=QualityTier.PREMIUM,
            )

        # OpenAI GPT
        openai_key = get_secret("OPENAI_API_KEY")
        if openai_key:
            self.llm_configs[LLMProvider.OPENAI] = LLMConfig(
                provider=LLMProvider.OPENAI,
                model="gpt-4o",
                api_key_env="OPENAI_API_KEY",
                temperature=0.7,
                max_tokens=4096,
                cost_per_token=0.000005,  # 입력 토큰당
                latency_ms=1800,
                quality_tier=QualityTier.ULTRA,
            )

        logger.info(f"✅ LLM Router 초기화: {len(self.llm_configs)}개 LLM 설정됨")
        # Start health check in background implies calling check_connections async,
        # but in sync __init__ we just log.

    async def check_connections(self) -> dict[str, bool]:
        """Startup Health Check for all providers"""
        results = {}
        logger.info("🏥 Running LLM Health Checks...")

        # Check Ollama
        if self._is_ollama_available():
            results["Ollama"] = True
            logger.info("   ✅ Ollama: Online")
        else:
            results["Ollama"] = False
            logger.warning("   ❌ Ollama: Offline or Unreachable")

        return results

    def route_request(self, query: str, context: dict[str, Any] | None = None) -> RoutingDecision:
        """
        쿼리에 대한 최적 LLM 라우팅 결정
        """
        context = context or {}
        quality_requirement = context.get("quality_tier", QualityTier.STANDARD)
        latency_requirement = context.get("max_latency_ms", 5000)
        cost_budget = context.get("max_cost", 1.0)

        # 0. 명시적 프로바이더 요청 처리
        requested_provider = context.get("provider")
        if requested_provider and requested_provider != "auto":
            try:
                target_provider = LLMProvider(requested_provider)
                config = self.llm_configs.get(target_provider)

                if config:
                    return RoutingDecision(
                        selected_provider=target_provider,
                        selected_model=config.model,
                        reasoning=f"사용자 명시적 요청: {requested_provider}",
                        confidence=1.0,
                        estimated_cost=self._estimate_cost(query, config),
                        estimated_latency=config.latency_ms,
                        fallback_providers=[LLMProvider.OLLAMA],
                    )
            except ValueError:
                pass  # 유효하지 않은 provider 문자열은 무시

        # 1. Ollama 우선 선택 (내부 지력)
        if self._is_ollama_available():
            decision = RoutingDecision(
                selected_provider=LLMProvider.OLLAMA,
                selected_model="qwen3-vl:8b",
                reasoning="내부 지력(Ollama) 우선 사용 - 비용 절감 및 속도 최적화",
                confidence=0.9,
                estimated_cost=0.0,
                estimated_latency=500,
                fallback_providers=[LLMProvider.ANTHROPIC, LLMProvider.GEMINI, LLMProvider.OPENAI],
            )

            # 품질 요구사항이 ULTRA인 경우 API LLM으로 업그레이드
            if quality_requirement == QualityTier.ULTRA and self._has_ultra_llm():
                decision = self._upgrade_to_ultra(query, context)

            return decision

        # 2. Ollama 불가 시 API LLM 선택
        return self._select_api_llm(
            query, context, quality_requirement, latency_requirement, cost_budget
        )

    def _is_ollama_available(self) -> bool:
        """Ollama 사용 가능 여부 확인"""
        try:
            # 간단한 헬스 체크 (실제로는 HTTP 요청)
            config = self.llm_configs.get(LLMProvider.OLLAMA)
            return config is not None and config.base_url is not None
        except Exception:
            return False

    def _has_ultra_llm(self) -> bool:
        """ULTRA 품질 LLM 보유 여부"""
        return any(config.quality_tier == QualityTier.ULTRA for config in self.llm_configs.values())

    def _upgrade_to_ultra(self, query: str, context: dict[str, Any]) -> RoutingDecision:
        """ULTRA 품질로 업그레이드"""
        # 가장 저렴한 ULTRA LLM 선택
        ultra_llms = [
            config
            for config in self.llm_configs.values()
            if config.quality_tier == QualityTier.ULTRA
        ]

        if not ultra_llms:
            return self._select_api_llm(query, context, QualityTier.ULTRA, 5000, 1.0)

        # 비용 기준 정렬
        best_llm = min(ultra_llms, key=lambda x: x.cost_per_token)

        return RoutingDecision(
            selected_provider=best_llm.provider,
            selected_model=best_llm.model,
            reasoning=f"ULTRA 품질 요구사항으로 {best_llm.provider.value}로 업그레이드",
            confidence=0.95,
            estimated_cost=self._estimate_cost(query, best_llm),
            estimated_latency=best_llm.latency_ms,
            fallback_providers=[p.provider for p in ultra_llms if p != best_llm],
        )

    def _select_api_llm(
        self,
        query: str,
        context: dict[str, Any],
        quality: QualityTier,
        max_latency: int,
        max_cost: float,
    ) -> RoutingDecision:
        """API LLM 선택 (Ollama 불가 시)"""
        candidates = [
            config
            for config in self.llm_configs.values()
            if config.provider != LLMProvider.OLLAMA
            and config.quality_tier.value >= quality.value
            and config.latency_ms <= max_latency
        ]

        if not candidates:
            # 품질 낮춰서 재시도
            candidates = [
                config
                for config in self.llm_configs.values()
                if config.provider != LLMProvider.OLLAMA
            ]

        if not candidates:
            return RoutingDecision(
                selected_provider=LLMProvider.OLLAMA,  # fallback to Ollama anyway
                selected_model="qwen3-vl:8b",
                reasoning="사용 가능한 LLM 없음 - Ollama로 fallback",
                confidence=0.5,
                estimated_cost=0.0,
                estimated_latency=500,
                fallback_providers=[],
            )

        # 비용-성능 균형으로 선택
        best_llm = self._select_best_llm(candidates, query, context)

        return RoutingDecision(
            selected_provider=best_llm.provider,
            selected_model=best_llm.model,
            reasoning=self._generate_reasoning(best_llm, quality, max_latency, max_cost),
            confidence=0.85,
            estimated_cost=self._estimate_cost(query, best_llm),
            estimated_latency=best_llm.latency_ms,
            fallback_providers=[c.provider for c in candidates if c != best_llm],
        )

    def _select_best_llm(
        self, candidates: list[LLMConfig], query: str, context: dict[str, Any]
    ) -> LLMConfig:
        """최적 LLM 선택 알고리즘"""
        # 점수 기반 선택 (비용, 품질, 지연 시간 균형)
        scored_candidates = []

        for config in candidates:
            score = self._calculate_llm_score(config, query, context)
            scored_candidates.append((config, score))

        # 최고 점수 LLM 선택
        return max(scored_candidates, key=lambda x: x[1])[0]

    def _calculate_llm_score(self, config: LLMConfig, query: str, context: dict[str, Any]) -> float:
        """LLM 점수 계산 (0-1 범위)"""
        # 품질 점수 (0.4 가중치)
        quality_score = {
            QualityTier.BASIC: 0.3,
            QualityTier.STANDARD: 0.6,
            QualityTier.PREMIUM: 0.8,
            QualityTier.ULTRA: 1.0,
        }[config.quality_tier]

        # 비용 점수 (역수, 0.3 가중치) - 저비용일수록 높음
        cost_score = min(1.0, 1.0 / (config.cost_per_token * 1000 + 1))

        # 지연 시간 점수 (역수, 0.3 가중치) - 빠를수록 높음
        latency_score = min(1.0, 2000 / config.latency_ms)

        # 최종 점수 (가중 평균)
        final_score = quality_score * 0.4 + cost_score * 0.3 + latency_score * 0.3

        return final_score

    def _generate_reasoning(
        self, config: LLMConfig, quality: QualityTier, max_latency: int, max_cost: float
    ) -> str:
        """라우팅 이유 생성"""
        reasons = []

        if config.quality_tier.value >= quality.value:
            reasons.append(f"품질 요구사항({quality.value}) 충족")
        else:
            reasons.append(f"품질 제한으로 {config.quality_tier.value} 선택")

        if config.latency_ms <= max_latency:
            reasons.append(f"지연 시간({config.latency_ms}ms) 허용 범위 내")
        else:
            reasons.append("지연 시간 제한 고려됨")

        if config.cost_per_token * 1000 <= max_cost:
            reasons.append("비용 예산 내")
        else:
            reasons.append("최적 비용 선택")

        return f"{config.provider.value} 선택: {', '.join(reasons)}"

    def _estimate_cost(self, query: str, config: LLMConfig) -> float:
        """비용 추정 (근사치)"""
        # 간단한 토큰 수 추정 (문자 수 기반)
        estimated_tokens = len(query) * 0.3  # 대략적인 변환
        return estimated_tokens * config.cost_per_token

    async def execute_with_routing(
        self, query: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        라우팅 결정 후 실제 실행
        """
        # Explicitly return dict[str, Any]
        result: dict[str, Any]
        """
        라우팅 결정 후 실제 실행 (w/ Caching)
        """
        # 1. Check Cache
        cache_key = f"{query}::{context}"
        if cache_key in self._response_cache:
            entry = self._response_cache[cache_key]
            if time.time() - entry["timestamp"] < self._cache_ttl:
                # Move to end (LRU)
                self._response_cache.move_to_end(cache_key)
                logger.info("⚡️ Cache Hit! Returning cached response.")
                # Cast Any to expected dict type for MyPy
                cached_data: dict[str, Any] = entry["data"]
                return cached_data
            else:
                # Expired
                del self._response_cache[cache_key]

        routing_decision = self.route_request(query, context)

        # 라우팅 기록
        self.routing_history.append(
            {
                "timestamp": time.time(),
                "query": query[:100],  # 축약
                "decision": {
                    "provider": routing_decision.selected_provider.value,
                    "model": routing_decision.selected_model,
                    "reasoning": routing_decision.reasoning,
                    "confidence": routing_decision.confidence,
                },
            }
        )

        # 실제 LLM 호출 (여기서는 모의 구현)
        try:
            response = await self._call_llm(routing_decision, query, context)
            response_data = {
                "success": True,
                "response": response,
                "routing": {
                    "provider": routing_decision.selected_provider.value,
                    "model": routing_decision.selected_model,
                    "reasoning": routing_decision.reasoning,
                    "estimated_cost": routing_decision.estimated_cost,
                    "estimated_latency": routing_decision.estimated_latency,
                },
            }

            # Cache Success Response
            self._response_cache[cache_key] = {"timestamp": time.time(), "data": response_data}
            if len(self._response_cache) > self._cache_max_size:
                self._response_cache.popitem(last=False)  # Remove oldest

            return response_data
        except Exception as e:
            # Fallback 시도
            if routing_decision.fallback_providers:
                return await self._try_fallback(
                    routing_decision.fallback_providers[0], query, context
                )
            else:
                return {"success": False, "error": str(e), "routing": routing_decision.__dict__}

    def _get_google_module(self) -> Any:
        """Helper for testability"""
        import google.generativeai as genai

        return genai

    async def _query_google(
        self, query: str, config: LLMConfig, context: dict[str, Any] | None
    ) -> str:
        """Google Gemini 쿼리 실행 (모델 Fallback 적용)"""
        genai = self._get_google_module()

        # Phase 2-4: settings 사용
        vault_client = None
        try:
            from AFO.security.vault_manager import vault as v1_client
            vault_client = v1_client
        except ImportError:
            try:
                # [맹자] 득도다조 - 진실된 경로를 찾으면 도움이 따름
                from security.vault_manager import vault as v2_client
                vault_client = v2_client
            except ImportError:
                vault_client = None

        if vault_client and config.api_key_env:
            api_key = vault_client.get_secret(config.api_key_env)
        else:
            # Fallback
            try:
                from AFO.config.settings import get_settings

                settings = get_settings()
                api_key = getattr(settings, config.api_key_env or "", None)
            except ImportError:
                api_key = os.getenv(config.api_key_env or "")

        if not api_key:
            raise ValueError(f"API Key not found for env var: {config.api_key_env}")

        genai.configure(api_key=api_key)

        # 시도할 모델 목록 (실제 API 조회 결과 기반)
        models_to_try = ["gemini-2.0-flash-exp", "gemini-flash-latest", "gemini-pro-latest"]
        last_error = None

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)

                # 안전 설정 완화
                safety_settings: list[dict[str, str]] = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]

                # context가 None일 수 있으므로 기본값 처리
                context_dict = context or {}
                response = await model.generate_content_async(
                    query,
                    generation_config=genai.types.GenerationConfig(
                        temperature=context_dict.get("temperature", 0.7),
                        max_output_tokens=context_dict.get("max_tokens", 1000),
                    ),
                    safety_settings=safety_settings,
                )

                return str(response.text)
            except Exception as e:
                print(f"⚠️ Gemini 모델({model_name}) 실패: {e}")
                last_error = e  # Update with the actual error
                continue  # 다음 모델 시도

        # 모든 모델 실패 시
        if last_error is not None:
            raise last_error
        raise RuntimeError("All Gemini models failed and no error was captured")

    async def _call_ollama(
        self, query: str, config: LLMConfig, context: dict[str, Any] | None = None
    ) -> str:
        """Ollama API 호출"""
        import httpx

        # Phase 2-4: settings 사용
        if config.base_url:
            base_url = config.base_url
        else:
            try:
                from AFO.config.settings import get_settings

                base_url = get_settings().OLLAMA_BASE_URL
            except ImportError:
                try:
                    from config.settings import get_settings  # type: ignore

                    base_url = get_settings().OLLAMA_BASE_URL
                except ImportError:
                    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        timeout_seconds = float(
            (context or {}).get("ollama_timeout_seconds", os.getenv("OLLAMA_TIMEOUT_SECONDS", "30"))
        )
        max_tokens = int((context or {}).get("max_tokens", config.max_tokens))
        temperature = float((context or {}).get("temperature", config.temperature))
        model = str((context or {}).get("ollama_model", config.model))
        num_ctx = int(
            (context or {}).get("ollama_num_ctx", getattr(config, "context_window", 4096))
        )
        num_threads = (context or {}).get("ollama_num_thread")

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
            logger.error(f"Ollama 호출 실패: {e}")
            raise

    async def _call_llm(
        self, decision: RoutingDecision, query: str, context: dict[str, Any] | None
    ) -> str:
        """실제 LLM 호출"""
        provider = decision.selected_provider

        try:
            if provider == LLMProvider.OLLAMA:
                config = self.llm_configs.get(LLMProvider.OLLAMA)
                if config:
                    return await self._call_ollama(query, config, context)
                return "[Ollama Error] 설정이 없습니다."

            elif provider == LLMProvider.ANTHROPIC and API_WRAPPERS_AVAILABLE:
                if claude_api.is_available():
                    result = await claude_api.generate(query, max_tokens=1024)
                    if result.get("success"):
                        return str(result["content"])
                    else:
                        return f"[Claude Error] {result.get('error', 'Unknown error')}"
                else:
                    return "[Claude Unavailable] API 키가 설정되지 않았습니다."

            elif provider == LLMProvider.GEMINI:
                # Gemini 직접 호출 (Fallback 로직 포함)
                config = self.llm_configs.get(LLMProvider.GEMINI)
                if config:
                    return await self._query_google(query, config, context)
                else:
                    return "[Gemini Unavailable] 설정이 없습니다."

            elif provider == LLMProvider.OPENAI and API_WRAPPERS_AVAILABLE:
                if openai_api.is_available():
                    result = await openai_api.generate(query, max_tokens=1024)
                    if result.get("success"):
                        return str(result["content"])
                    else:
                        return f"[OpenAI Error] {result.get('error', 'Unknown error')}"
                else:
                    return "[OpenAI Unavailable] API 키가 설정되지 않았습니다."

            else:
                # Fallback 모의 응답
                return f"[{provider.value}] {query}에 대한 응답입니다. (API wrapper unavailable)"

        except Exception as e:
            logger.error(f"LLM 호출 중 예외: {e}")
            raise

    async def _try_fallback(
        self, fallback_provider: LLMProvider, query: str, context: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Fallback LLM 시도"""
        try:
            config = self.llm_configs.get(fallback_provider)
            if not config:
                raise ValueError(f"설정되지 않은 provider: {fallback_provider}")

            # 간단한 fallback 호출
            response = f"[Fallback {fallback_provider.value}] {query}에 대한 응답입니다."

            return {
                "success": True,
                "response": response,
                "routing": {
                    "provider": fallback_provider.value,
                    "model": config.model,
                    "reasoning": "Primary LLM 실패로 fallback 사용",
                    "is_fallback": True,
                },
            }
        except Exception as e:
            return {"success": False, "error": f"Fallback도 실패: {e!s}"}

    def get_routing_stats(self) -> dict[str, Any]:
        """라우팅 통계"""
        if not self.routing_history:
            return {"total_requests": 0}

        total_requests = len(self.routing_history)
        provider_usage: dict[str, Any] = {}

        for record in self.routing_history[-100:]:  # 최근 100개
            provider = record["decision"]["provider"]
            provider_usage[provider] = provider_usage.get(provider, 0) + 1

        return {
            "total_requests": total_requests,
            "provider_usage": provider_usage,
            "average_confidence": sum(
                r["decision"]["confidence"] for r in self.routing_history[-100:]
            )
            / min(100, len(self.routing_history)),
            "ollama_preference_ratio": provider_usage.get("ollama", 0) / total_requests
            if total_requests > 0
            else 0,
        }


# 글로벌 LLMRouter 인스턴스
llm_router = LLMRouter()


async def route_and_execute(query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    LLM 라우팅 및 실행 인터페이스
    """
    return await llm_router.execute_with_routing(query, context)


if __name__ == "__main__":
    # 테스트
    async def test_router() -> None:
        router = LLMRouter()

        test_queries = [
            "간단한 질문입니다",
            "고품질 답변이 필요한 복잡한 질문입니다",
            "빠른 응답이 필요한 질문입니다",
        ]

        print("🧭 LLM Router 테스트")
        print("=" * 50)

        for query in test_queries:
            print(f"\n🔍 쿼리: {query}")

            # 라우팅 결정
            decision = router.route_request(query)
            print(f"📋 결정: {decision.selected_provider.value} ({decision.selected_model})")
            print(f"💭 이유: {decision.reasoning}")
            print(f"💰 예상 비용: ${decision.estimated_cost:.4f}")
            print(f"⏱️  예상 지연: {decision.estimated_latency}ms")
            # 실제 실행 (모의)
            result = await router.execute_with_routing(query)
            print(f"✅ 결과: {result['success']}")
            if result["success"]:
                print(f"💬 응답: {result['response'][:50]}...")

        # 통계
        stats = router.get_routing_stats()
        print(f"\n📊 통계: {stats}")

    asyncio.run(test_router())
