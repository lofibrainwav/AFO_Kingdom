"""
Compatibility Layer (Strangler Fig Pattern)
-------------------------------------------
Centralizes conditional imports and legacy support logic.
Ensures 'api_server.py' remains clean and type-safe (Truth 100%).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

# 1. Environment & Settings
if TYPE_CHECKING:
    from AFO.config.settings import AFOSettings

try:
    from dotenv import load_dotenv as _real_load_dotenv
    _load_dotenv: Any = _real_load_dotenv
except ImportError:
    _load_dotenv = None


def load_dotenv_safe() -> bool:
    """Safe wrapper for dotenv.load_dotenv"""
    if _load_dotenv is not None:
        return bool(_load_dotenv(dotenv_path=str(Path.cwd() / ".env"), override=True))
    return False


_get_settings_func: Any = None

try:
    from AFO.config.settings import get_settings as _real_get_settings

    _get_settings_func = _real_get_settings
except ImportError:
    try:
        # [대학] 격물치지 - 사물을 궁구하여 지식을 얻음
        from config.settings import (
            get_settings as _fallback_get_settings,
        )

        _get_settings_func = _fallback_get_settings
    except ImportError:
        pass

# [노자] 도가도비상도 - 완벽한 타입 정의는 변화를 담지 못함
def get_settings_safe() -> Any:
    """Safe wrapper for get_settings"""
    if _get_settings_func is not None:
        try:
            return _get_settings_func()
        except Exception:
            return None
    return None

get_settings = get_settings_safe


# 2. Lazy Imports (External Libs)
class LazyModules:
    """Facade for optionally installed modules"""
    
    anthropic: Any = None
    chromadb: Any = None
    crewai: Any = None
    langchain: Any = None
    qdrant_client: Any = None
    sentry_sdk: Any = None

    @classmethod
    def load(cls):
        try:
            # [주역] 무극이태극 - 무에서 유가 나옴
            from afo_soul_engine.utils.lazy_imports import (
                anthropic,
                chromadb,
                crewai,
                langchain,
                qdrant_client,
            )
            cls.anthropic = anthropic
            cls.chromadb = chromadb
            cls.crewai = crewai
            cls.langchain = langchain
            cls.qdrant_client = qdrant_client
        except ImportError:
            pass

        try:
            import sentry_sdk
            cls.sentry_sdk = sentry_sdk
        except ImportError:
            pass

LazyModules.load()


# 3. Hybrid RAG Services
class HybridRAG:
    """Facade for Hybrid RAG services"""
    
    available: bool = False
    blend_results_async: Any = None
    generate_answer_async: Any = None
    get_embedding_async: Any = None
    query_pgvector_async: Any = None
    query_redis_async: Any = None
    select_context: Any = None

    @classmethod
    def load(cls):
        try:
            from AFO.services.hybrid_rag import (
                blend_results_async,
                generate_answer_async,
                get_embedding_async,
                query_pgvector_async,
                query_redis_async,
                select_context,
            )
            cls.available = True
            cls.blend_results_async = blend_results_async
            cls.generate_answer_async = generate_answer_async
            cls.get_embedding_async = get_embedding_async
            cls.query_pgvector_async = query_pgvector_async
            cls.query_redis_async = query_redis_async
            cls.select_context = select_context
        except ImportError:
            cls.available = False

HybridRAG.load()


# 4. Router Exports (Strangler Fig Facade)
def _get_fallback_router() -> Any:
    try:
        from fastapi import APIRouter
        return APIRouter()
    except ImportError:
        return None

# Initial Fallbacks
auth_router = _get_fallback_router()
chancellor_router = _get_fallback_router()
family_router = _get_fallback_router()
health_router = _get_fallback_router()
julie_router = _get_fallback_router()
personas_router = _get_fallback_router()
root_router = _get_fallback_router()
streams_router = _get_fallback_router()
users_router = _get_fallback_router()
skills_router = _get_fallback_router()
trinity_router = _get_fallback_router()
rag_router = _get_fallback_router()
system_health_router = _get_fallback_router()
trinity_policy_router = _get_fallback_router()
trinity_sbt_router = _get_fallback_router()
multi_agent_router = _get_fallback_router()
education_system_router = _get_fallback_router()
modal_data_router = _get_fallback_router()
n8n_router = _get_fallback_router()
wallet_router = _get_fallback_router()
# [손자병법] 지피지기 - thoughts_router는 왕국의 사고를 투명하게 드러내는 창
thoughts_router = _get_fallback_router()

# Flags
ANTHROPIC_AVAILABLE: bool = LazyModules.anthropic is not None
OPENAI_AVAILABLE: bool = False

# Functions
def calculate_trinity(*args, **kwargs): return None

# Metrics
# [노자] 도가도비상도 - 진실은 하나이나 표현은 여럿, trinity_metrics로 통합
try:
    from AFO.domain.metrics.trinity import TrinityMetrics
except ImportError:
    class TrinityMetrics:  # type: ignore
        trinity_score: float = 0.0
        truth: float = 0.0
        goodness: float = 0.0
        beauty: float = 0.0
        filial_serenity: float = 0.0
        eternity: float = 0.0
        balance_status: str = "Unknown"

        def to_dict(self) -> dict:
            return {}

# Try to load known routers
# [논어] 학이시습지 - 반복적으로 시도하여 지식을 쌓음
def load_routers():
    global auth_router, family_router, health_router, personas_router, root_router, streams_router, users_router, chancellor_router, julie_router, skills_router, trinity_router, thoughts_router
    
    try:
        from AFO.api.routers.auth import router as auth
        auth_router = auth
    except ImportError: pass

    try:
        from AFO.api.routers.family import router as family
        family_router = family
    except ImportError: pass

    try:
        from AFO.api.routers.health import router as health
        health_router = health
    except ImportError: pass

    try:
        from AFO.api.routers.personas import router as personas
        personas_router = personas
    except ImportError: pass

    try:
        from AFO.api.routers.root import router as root
        root_router = root
    except ImportError: pass

    try:
        from AFO.api.routes.streams import router as streams
        streams_router = streams
    except ImportError: pass

    try:
        from AFO.api.routers.users import router as users
        users_router = users
    except ImportError: pass

    try:
        from AFO.api.routers.chancellor_router import router as chancellor
        chancellor_router = chancellor
    except ImportError: pass
    
    try:
        from AFO.api.routers.julie_royal import router as julie
        julie_router = julie
    except ImportError: pass

    # Try to load others if possible
    # (Assuming paths based on naming convention)
    # If not found, they remain fallback routers (Safe)
    
    try:
        from AFO.api.routers.thoughts import router as thoughts
        global thoughts_router
        thoughts_router = thoughts
    except ImportError: pass

load_routers()
# Legacy Router Aliases - [노자] 유무상생 = 있음과 없음은 서로 기댐
got_router: Any = None
pillars_router: Any = None
strangler_router: Any = None


# 5. Antigravity Facade (Pure Control)
def get_antigravity_control() -> Any:
    """
    [Pure] Get Antigravity Governance Controller
    Returns the singleton instance via facade.
    """
    try:
        from AFO.config.antigravity import antigravity
        return antigravity
    except ImportError:
        return None

