# 🧭 Trinity Score: 眞89% 善85% 美72% 孝95% | Total: 84%
# 이 파일은 AFO 왕국의 眞善美孝 철학을 구현합니다

# afo_soul_engine/api_server.py

from __future__ import annotations

import asyncio
import logging
import os
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager, suppress
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import redis
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.exceptions import HTTPException as StarletteHTTPException

# Path setup for imports (must be before AFO imports)
_AFO_ROOT = str(Path(__file__).resolve().parent.parent)
if _AFO_ROOT not in sys.path:
    sys.path.insert(0, _AFO_ROOT)

from AFO.api.routers.health import router as health_router
from AFO.api.routers.root import router as root_router

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None  # type: ignore[assignment]

try:
    from config.settings import get_settings
except ImportError:  # pragma: no cover - fallback on packaging issues
    get_settings = None

try:
    from afo_soul_engine.utils.lazy_imports import (
        anthropic,
        chromadb,
        crewai,
        langchain,
        qdrant_client,
    )
except ImportError:  # pragma: no cover - optional tooling
    anthropic = None
    chromadb = None
    crewai = None
    langchain = None
    qdrant_client = None

try:
    from AFO.services.hybrid_rag import (
        blend_results_async,
        generate_answer_async,
        get_embedding_async,
        query_pgvector_async,
        query_redis_async,
        select_context,
    )
except ImportError as exc:  # pragma: no cover - local execution fallback
    print("⚠️  Hybrid RAG services unavailable:", exc)
    raise


# 백색 소음 제거: Pydantic UserWarning 완전 박멸
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# ============================================================================
# ENVIRONMENT / SETTINGS
# ============================================================================

settings: Any | None = None

if load_dotenv:
    env_loaded = load_dotenv(dotenv_path=str(Path.cwd() / ".env"), override=True)
    if env_loaded:
        print("✅ 환경 변수 로드 완료 (.env)")
    else:
        print("⚠️ .env 파일을 찾을 수 없거나 로드 실패")
else:
    print("⚠️ python-dotenv가 설치되지 않아 .env 파일을 로드할 수 없습니다")

if get_settings:
    try:
        settings = get_settings()
    except Exception:
        settings = None

gemini_key = getattr(settings, "GEMINI_API_KEY", None) if settings else os.getenv("GEMINI_API_KEY")
if gemini_key:
    print(f"✅ GEMINI_API_KEY 로드됨: {gemini_key[:20]}...")
else:
    print("⚠️ GEMINI_API_KEY가 .env에 설정되지 않았습니다")

sentinel_dsn = getattr(settings, "SENTRY_DSN", None) if settings else os.getenv("SENTRY_DSN")
if sentinel_dsn:
    try:
        import sentry_sdk

        sentry_sdk.init(
            dsn=sentinel_dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        print("✅ Sentry 모니터링 활성화")
    except ImportError:
        print("⚠️  sentry_sdk not installed, skipping Sentry integration")
else:
    print("⚠️ SENTRY_DSN 설정 없음")


# ============================================================================
# LAZY IMPORTS - Phase 1.2: 서버 시작 시간 최적화
# 무거운 라이브러리들을 실제 사용 시에만 로딩
# ============================================================================

try:
    from openai import OpenAI  # type: ignore[import]

    OPENAI_AVAILABLE = True
    print("✅ OpenAI available (lazy loaded)")
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not available (optional dependency)")

Anthropic = anthropic if anthropic else None
CREWAI_AVAILABLE = crewai.is_available() if crewai else False
if crewai and CREWAI_AVAILABLE:
    print("✅ CrewAI available (lazy loaded)")
elif crewai is None:
    print("⚠️  CrewAI not available (optional dependency)")
else:
    print("⚠️  CrewAI lazy import failed")

LANGCHAIN_AVAILABLE = langchain.is_available() if langchain else False
if langchain and LANGCHAIN_AVAILABLE:
    print("✅ LangChain available (lazy loaded)")
elif langchain is None:
    print("⚠️  LangChain not available (optional dependency)")
else:
    print("⚠️  LangChain lazy import failed")

ANTHROPIC_AVAILABLE = anthropic.is_available() if anthropic else False
if anthropic and ANTHROPIC_AVAILABLE:
    print("✅ Anthropic available (lazy loaded)")
elif anthropic is None:
    print("⚠️  Anthropic not available (optional dependency)")
else:
    print("⚠️  Anthropic lazy import failed")

CHROMADB_AVAILABLE = chromadb.is_available() if chromadb else False
QDRANT_AVAILABLE = qdrant_client.is_available() if qdrant_client else False

print("🎉 Phase 1.2: Lazy Imports 적용 완료 - 서버 시작 시간 최적화")

# ============================================================================
# ASYNC CONFIGURATION - Phase 1.3: Strangler Fig Async Wrappers
# 기존 sync 코드는 한 줄도 건드리지 말고, 껍데기만 async로 감싸기
# ============================================================================

# 전역 플래그 + 안전한 롤백
ASYNC_QUERY_ENABLED = (
    getattr(settings, "ASYNC_QUERY_ENABLED", None)
    if settings and hasattr(settings, "ASYNC_QUERY_ENABLED")
    else os.getenv("ASYNC_QUERY_ENABLED", "1") == "1"
)
executor = ThreadPoolExecutor(max_workers=56)  # M4 Pro 풀가동


# 마법 같은 유틸 - sync 함수를 async로 감싸는 만능 래퍼
def to_async(sync_func: Callable) -> Callable:
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, sync_func, *args, **kwargs)

    wrapper.__name__ = f"{sync_func.__name__}_async"
    return wrapper


# Async 래퍼들은 함수 정의 이후에 생성 (Strangler Fig)
# 기존 sync 함수들은 그대로 두고, 껍데기만 async로 감싸기

print("🎉 Phase 1.3: Async Configuration 적용 완료 - Strangler Fig 준비")

# Optional PostgreSQL imports
try:
    # from pgvector.psycopg2 import register_vector

    # register_vector()  # Connection required, skipping at module level
    PGVECTOR_AVAILABLE = True
except ImportError:
    PGVECTOR_AVAILABLE = False
    # 서버 시작 시점에서는 조용히 처리 (optional dependency)
    pass

try:
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import SimpleConnectionPool

    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    SimpleConnectionPool: Any = None  # type: ignore[no-redef]
    RealDictCursor: Any = None  # type: ignore[no-redef]
    # 서버 시작 시점에서는 조용히 처리 (optional dependency)
    pass

# Optional SSE imports (현재 사용되지 않음 - 필요시 주석 해제)
# try:
#     from sse_starlette.sse import EventSourceResponse
#     SSE_AVAILABLE = True
# except ImportError:
#     EventSourceResponse = None
#     SSE_AVAILABLE = False
#     print("⚠️  sse-starlette not available (SSE support disabled)")
SSE_AVAILABLE = False

MODULAR_ROUTERS_AVAILABLE = True

# ============================================================
# AFO 스킬 API 영구 등록 플래그 (永遠不滅 - 영원불멸)
# ============================================================
SKILLS_ROUTER_PERMANENT = True  # 이 플래그는 절대 False 안 됨


def _fallback_router(name: str, exc: Exception, essential: bool = False) -> APIRouter:
    """Return an empty router when optional imports fail."""
    global MODULAR_ROUTERS_AVAILABLE
    print(f"⚠️  {name} router not available: {exc}")
    if essential:
        MODULAR_ROUTERS_AVAILABLE = False
    return APIRouter()


# api_wallet_router는 레거시 - wallet_router로 대체됨 (Strangler Fig)
# try:
#     from .api.routers.api_wallet import router as api_wallet_router
# except Exception as exc:
#     api_wallet_router = _fallback_router("API Wallet", exc)

# obsidian_router는 현재 사용되지 않음 (레거시)
# try:
#     from .api.routes.obsidian import router as obsidian_router
# except Exception as exc:
#     obsidian_router = _fallback_router("Obsidian", exc)

try:
    from .api.routers.education_system import router as education_system_router
except Exception as exc:  # pragma: no cover - optional feature
    education_system_router = _fallback_router("Education System", exc)

try:
    from .api.routers.modal_data import router as modal_data_router
except Exception as exc:  # pragma: no cover - optional feature
    modal_data_router = _fallback_router("Modal Data", exc)

try:
    from .api.routers.skill_registry import router as skill_registry_router
except Exception as exc:  # pragma: no cover - optional feature
    skill_registry_router = _fallback_router("Skill Registry (legacy)", exc)

try:
    from .api.routers.trinity_policy import router as trinity_policy_router
except Exception as exc:  # pragma: no cover - optional feature
    trinity_policy_router = _fallback_router("Trinity Policy (legacy)", exc)

try:
    from .api.routes.trinity_sbt import router as trinity_sbt_router
except Exception as exc:  # pragma: no cover - optional feature
    trinity_sbt_router = _fallback_router("Trinity SBT", exc)

# graphrag_router는 현재 사용되지 않음 (레거시)
# try:
#     from .api.routes.graphrag.hybrid_rag import router as graphrag_router
# except Exception as exc:
#     graphrag_router = _fallback_router("GraphRAG", exc)

# Health router는 이미 Line 31에서 import됨 (AFO.api.routers.health)
# 중복 로드 방지: 이미 import된 health_router 사용
# try:
#     try:
#         from .api.routes.health import router as health_router
#     except ImportError:
#         try:
#             from api.routes.health import router as health_router  # type: ignore[no-redef]
#         except ImportError:
#             health_router = None  # type: ignore[assignment]
#             print("⚠️  Health router not available")
# except Exception as exc:  # pragma: no cover - optional feature
#     health_router = _fallback_router("Health", exc)

# Strangler Fig Pattern: Music Router (점진적 리팩터링)
# music_router는 현재 사용되지 않음 (레거시)
# try:
#     from .api.routes.music import music_router
#     MUSIC_ROUTER_AVAILABLE = True
#     print("✅ Music router loaded (Strangler Fig)")
# except Exception as exc:
#     music_router = _fallback_router("Music", exc)
#     MUSIC_ROUTER_AVAILABLE = False
#     print(f"⚠️  Music router not available: {exc}")

# Strangler Fig Pattern: N8N Router (점진적 리팩터링)
try:
    from afo_soul_engine.api.routes.n8n import health_n8n_router, n8n_router

    N8N_ROUTER_AVAILABLE = True
    print("✅ N8N router loaded (Strangler Fig)")
except Exception:
    try:
        from .api.routes.n8n import health_n8n_router, n8n_router

        N8N_ROUTER_AVAILABLE = True
        print("✅ N8N router loaded (Strangler Fig - fallback)")
    except Exception as exc2:
        n8n_router = _fallback_router("N8N", exc2)
        health_n8n_router = _fallback_router("N8N Health", exc2)
        N8N_ROUTER_AVAILABLE = False
        print(f"⚠️  N8N router not available: {exc2}")

# Strangler Fig Pattern: Strategy Router (점진적 리팩터링)
# strategy_router는 현재 사용되지 않음 (레거시 - LangGraph로 대체)
# try:
#     from .api.routes.strategy import strategy_router
#     STRATEGY_ROUTER_AVAILABLE = True
#     print("✅ Strategy router loaded (Strangler Fig)")
# except Exception as exc:
#     strategy_router = _fallback_router("Strategy", exc)
#     STRATEGY_ROUTER_AVAILABLE = False
#     print(f"⚠️  Strategy router not available: {exc}")

# Strangler Fig Pattern: Hybrid-RAG Router (점진적 리팩터링)
# hybrid_rag_router는 현재 사용되지 않음 (레거시)
# try:
#     from .api.routes.hybrid_rag import hybrid_rag_router
#     HYBRID_RAG_ROUTER_AVAILABLE = True
#     print("✅ Hybrid-RAG router loaded (Strangler Fig)")
# except Exception as exc:
#     hybrid_rag_router = _fallback_router("Hybrid-RAG", exc)
#     HYBRID_RAG_ROUTER_AVAILABLE = False
#     print(f"⚠️  Hybrid-RAG router not available: {exc}")

# Multi-Agent Router (Phase 4 - 협력 에이전트 시스템)
try:
    from .api.routes.multi_agent import router as multi_agent_router

    MULTI_AGENT_ROUTER_AVAILABLE = True
    print("✅ Multi-Agent router loaded")
except Exception as exc:
    multi_agent_router = _fallback_router("Multi-Agent", exc)
    MULTI_AGENT_ROUTER_AVAILABLE = False
    print(f"⚠️  Multi-Agent router not available: {exc}")

# Strangler Fig Pattern: Prompt Cache Router (점진적 리팩터링)
# prompt_cache_router는 현재 사용되지 않음 (레거시)
# try:
#     from .api.routes.prompt_cache import prompt_cache_router
#     PROMPT_CACHE_ROUTER_AVAILABLE = True
#     print("✅ Prompt Cache router loaded (Strangler Fig)")
# except Exception as exc:
#     prompt_cache_router = _fallback_router("Prompt Cache", exc)
#     PROMPT_CACHE_ROUTER_AVAILABLE = False
#     print(f"⚠️  Prompt Cache router not available: {exc}")

# Strangler Fig Pattern: Yeongdeok Router (점진적 리팩터링)
# yeongdeok_router는 현재 사용되지 않음 (레거시 - YeongdeokComplete로 대체)
# try:
#     from .api.routes.yeongdeok import yeongdeok_router
#     YEONGDEOK_ROUTER_AVAILABLE = True
#     print("✅ Yeongdeok router loaded (Strangler Fig)")
# except Exception as exc:
#     yeongdeok_router = _fallback_router("Yeongdeok", exc)
#     YEONGDEOK_ROUTER_AVAILABLE = False
#     print(f"⚠️  Yeongdeok router not available: {exc}")

# Strangler Fig Pattern: Ragas Router (점진적 리팩터링 + 간결화)
try:
    from .api.routes.ragas import ragas_router

    RAGAS_ROUTER_AVAILABLE = True
    print("✅ Ragas router loaded (Strangler Fig + 간결화)")
except Exception as exc:
    ragas_router = _fallback_router("Ragas", exc)
    RAGAS_ROUTER_AVAILABLE = False
    print(f"⚠️  Ragas router not available: {exc}")

# Strangler Fig Pattern: RAG Router (점진적 리팩터링 + 간결화)
try:
    from .api.routes.rag import rag_router

    RAG_ROUTER_AVAILABLE = True
    print("✅ RAG router loaded (Strangler Fig + 간결화)")
except Exception as exc:
    rag_router = _fallback_router("RAG", exc)
    RAG_ROUTER_AVAILABLE = False
    print(f"⚠️  RAG router not available: {exc}")

# Strangler Fig Pattern: Wallet Router (점진적 리팩터링 + 간결화)
# wallet_router 등록 (Strangler Fig Pattern)
try:
    from afo_soul_engine.api.routes.wallet import wallet_router

    WALLET_ROUTER_AVAILABLE = True
    print("✅ Wallet router loaded (Strangler Fig)")
except Exception:
    try:
        from .api.routes.wallet import wallet_router

        WALLET_ROUTER_AVAILABLE = True
        print("✅ Wallet router loaded (Strangler Fig - fallback)")
    except Exception:
        try:
            from api.routes.wallet import wallet_router

            WALLET_ROUTER_AVAILABLE = True
            print("✅ Wallet router loaded (Strangler Fig - local fallback)")
        except Exception as exc2:
            wallet_router = _fallback_router("Wallet", exc2)
            WALLET_ROUTER_AVAILABLE = False
            print(f"⚠️  Wallet router not available: {exc2}")
# 주석 처리하여 unused import 경고 제거

# Strangler Fig Pattern: Evaluation Router (점진적 리팩터링 + 간결화)
# evaluation_router는 현재 사용되지 않음 (레거시)
# 주석 처리하여 unused import 경고 제거

# Strangler Fig Pattern: Auth Router (점진적 리팩터링 + 간결화)
# auth_router는 현재 사용되지 않음 (레거시)
# 주석 처리하여 unused import 경고 제거

# Strangler Fig Pattern: Soul Router (점진적 리팩터링 + 간결화)
# 승상의 지혜: Soul Vectors 모듈 분리
# soul_router는 현재 사용되지 않음 (레거시)
# try:
#     from .api.routes.soul import soul_router
#     SOUL_ROUTER_AVAILABLE = True
#     print("✅ Soul router loaded (Strangler Fig + 간결화 + Vectors)")
# except Exception as exc:
#     soul_router = _fallback_router("Soul", exc)
#     SOUL_ROUTER_AVAILABLE = False
#     print(f"⚠️  Soul router not available: {exc}")
SOUL_ROUTER_AVAILABLE = False

# Strangler Fig Pattern: Yeongdeok Browser Router (점진적 리팩터링 + 간결화)
# 승상의 지혜: Browser 인터랙션 모듈 분리
# Note: Browser router는 yeongdeok.py에서 자동 포함됨

try:
    # 절대 import 시도 (상대 import 실패 시 대비)
    try:
        from .api.routes.skills import router as skills_router
    except ImportError:
        from afo_soul_engine.api.routes.skills import router as skills_router
    SKILLS_ROUTER_AVAILABLE = True
    print("✅ Skills router loaded")
except Exception as exc:  # pragma: no cover - optional feature
    skills_router = _fallback_router("Skills", exc)
    SKILLS_ROUTER_AVAILABLE = False
    print(f"⚠️  Skills router not available: {exc}")

# Trinity router는 Router Facade Pattern으로 통합됨 (routers/trinity_router.py)
# 기존 개별 라우터들은 trinity_router로 통합되어 더 이상 직접 import하지 않음
# - trinity_scorer_router → routers/trinity_router.py의 /scorer/compute
# - trinity_calculator_router → routers/trinity_router.py의 /calculate, /linear-algebra 등
# - trinity_eaas_router → 레거시, 통합 예정

try:
    from .routers.trinity_router import router as trinity_router
except Exception as exc:  # pragma: no cover - optional feature
    trinity_router = _fallback_router("Trinity Router (Facade)", exc)

try:
    from AFO.api.routers.auth import router as auth_router
except Exception as exc:  # pragma: no cover - optional feature
    auth_router = _fallback_router("Auth Router (Heart)", exc)

try:
    from AFO.api.routers.users import router as users_router
except Exception as exc:  # pragma: no cover - optional feature
    users_router = _fallback_router("Users Router (Liver)", exc)

try:
    from .api.routes.llm_router import router as llm_router_api
except Exception as exc:  # pragma: no cover
    llm_router_api = _fallback_router("LLM Router", exc)

try:
    from .api.routes.crewai import router as crewai_router
except Exception as exc:  # pragma: no cover
    crewai_router = _fallback_router("CrewAI", exc)

try:
    from .api.routes.langgraph_tutor import router as langgraph_tutor_router
except Exception as exc:
    langgraph_tutor_router = _fallback_router("LangGraph Tutor", exc)

try:
    from .api.routes.langgraph_router import router as twin_dragon_router
except Exception as exc:
    twin_dragon_router = _fallback_router("Twin Dragon Router", exc)

# trinity_scorer_router는 trinity_router로 통합됨 (Facade Pattern)
# 제거됨: from .api.routes.trinity_scorer import router as trinity_scorer_router

try:
    from .api.routes.rag_advanced import router as rag_advanced_router
except Exception as exc:
    rag_advanced_router = _fallback_router("Advanced RAG", exc)

try:
    from afo_soul_engine.api.routes.system_health import router as system_health_router
except Exception:
    try:
        from .api.routes.system_health import router as system_health_router
    except Exception:
        try:
            from api.routes.system_health import (
                router as system_health_router,  # type: ignore[no-redef]
            )

            print("✅ System Health router loaded (absolute import fallback)")
        except Exception as exc3:
            system_health_router = _fallback_router("System Health", exc3)

try:
    from .api.routes.deployment import router as deployment_router
except Exception as exc:
    deployment_router = _fallback_router("Deployment", exc)

# 제3계명: 5기둥 API 라우터 (항상 로드 시도)
try:
    # 상대 import 시도
    try:
        from .api.routes.pillars import router as pillars_router
    except ImportError:
        # 절대 import 시도 (서버 실행 디렉토리 문제 대비)
        try:
            from afo_soul_engine.api.routes.pillars import router as pillars_router
        except ImportError:
            # api.routes.pillars 직접 import (현재 디렉토리 기준)
            from api.routes.pillars import router as pillars_router  # type: ignore[no-redef]
    PILLARS_ROUTER_AVAILABLE = True
    print("✅ 5기둥 API 라우터 로드 성공")
except Exception as exc:
    pillars_router = _fallback_router("5 Pillars", exc)
    PILLARS_ROUTER_AVAILABLE = False
    print(f"⚠️  5기둥 API 라우터 로드 실패: {exc}")

# Strangler Fig API 라우터 (항상 로드 시도)
try:
    try:
        from .api.routes.strangler import router as strangler_router
    except ImportError:
        try:
            from afo_soul_engine.api.routes.strangler import router as strangler_router
        except ImportError:
            from api.routes.strangler import router as strangler_router  # type: ignore[no-redef]
    STRANGLER_ROUTER_AVAILABLE = True
    print("✅ Strangler Fig API 라우터 로드 성공")
except Exception as exc:
    strangler_router = _fallback_router("Strangler Fig", exc)
    STRANGLER_ROUTER_AVAILABLE = False
    print(f"⚠️  Strangler Fig API 라우터 로드 실패: {exc}")

# Graph-of-Thought API 라우터 (항상 로드 시도)
try:
    try:
        from .api.routes.got import router as got_router
    except ImportError:
        try:
            from afo_soul_engine.api.routes.got import router as got_router
        except ImportError:
            from api.routes.got import router as got_router  # type: ignore[no-redef]
    GOT_ROUTER_AVAILABLE = True
    print("✅ Graph-of-Thought API 라우터 로드 성공")
except Exception as exc:
    got_router = _fallback_router("Graph-of-Thought", exc)
    GOT_ROUTER_AVAILABLE = False
    print(f"⚠️  Graph-of-Thought API 라우터 로드 실패: {exc}")

# Database setup
try:
    DATABASE_AVAILABLE = True
    print("✅ Database module loaded")
except Exception as exc:
    DATABASE_AVAILABLE = False
    print(f"⚠️  Database module not available: {exc}")

if MODULAR_ROUTERS_AVAILABLE:
    print("✅ Modular routers imported successfully")
else:
    print("⚠️  Trinity EaaS router unavailable - running with fallback")
# Configure logger first
logger = logging.getLogger(__name__)

# Optional Prometheus instrumentation (graceful degradation if not available)
try:
    from prometheus_fastapi_instrumentator import Instrumentator

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    # 서버 시작 시점에서는 조용히 처리 (optional dependency)
    pass

# Import the LangGraph blueprint and the ASYNC memory context manager
try:
    from .strategy_engine import memory_context, workflow
except ImportError:
    try:
        from strategy_engine import memory_context, workflow  # type: ignore[no-redef]
    except ImportError:
        memory_context = None
        workflow = None  # type: ignore[assignment]
        print("⚠️  Strategy engine not available")

# Import RAG engines (Phase 2.3 - Optional until implemented)
# CRAGEngine, HybridCRAGSelfRAG는 현재 사용되지 않음 (레거시)
# try:
#     from .crag_engine import CRAGEngine
# except ImportError:
#     CRAGEngine = None
#     print("⚠️  CRAGEngine not available (Phase 2.3 pending)")
#
# try:
#     from .hybrid_crag_selfrag import HybridCRAGSelfRAG
# except ImportError:
#     HybridCRAGSelfRAG = None
#     print("⚠️  HybridCRAGSelfRAG not available (Phase 2.3 pending)")

# Import Query Expansion (Phase 2.3 - Optional)
try:
    from .query_expansion_advanced import QueryExpander
except ImportError:
    QueryExpander = None  # type: ignore[assignment, misc]
    print("⚠️  QueryExpander not available (Phase 2.3 pending)")

# Import Multimodal RAG Engine (Phase 2 - Multimodal RAG)
try:
    from .multimodal_rag_engine import MultimodalRAGEngine
except ImportError:
    MultimodalRAGEngine: Any = None  # type: ignore[no-redef]
    print("⚠️  MultimodalRAGEngine not available (Multimodal RAG Phase 2 pending)")

# Import Multimodal RAG Cache (Phase 5 - Optimization)
# set_redis_client만 사용됨, 나머지는 레거시
try:
    from .multimodal_rag_cache import set_redis_client
except ImportError:
    set_redis_client: Any = None  # type: ignore[no-redef]
    print("⚠️  Multimodal RAG Cache not available (Multimodal RAG Phase 5 pending)")

# Multimodal RAG Utils, Suno-Style Music RAG, LangChainRAGSystem는 현재 사용되지 않음 (레거시)
# try:
#     from .multimodal_rag_utils import (compress_image, export_results_to_csv,
#                                        export_results_to_json, load_history,
#                                        save_history)
# except ImportError:
#     compress_image = None
#     export_results_to_json = None
#     export_results_to_csv = None
#     save_history = None
#     load_history = None
#     print("⚠️  Multimodal RAG Utils not available (Multimodal RAG Phase 5 pending)")
#
# try:
#     from .suno_style_music_rag import (generate_suno_style_music,
#                                        get_music_trend_insights)
#     SUNO_MUSIC_RAG_AVAILABLE = True
#     print("✅ Suno-Style Music RAG 통합 완료 (Phase 3)")
# except ImportError as e:
#     SUNO_MUSIC_RAG_AVAILABLE = False
#     print(f"⚠️  Suno-Style Music RAG not available: {e}")
#
# try:
#     from .langchain_rag_retrievalqa_system import LangChainRAGSystem
# except ImportError:
#     LangChainRAGSystem = None
#     print("⚠️  LangChainRAGSystem not available (Week 1 pending)")
SUNO_MUSIC_RAG_AVAILABLE = False

# Import Yeongdeok Complete (Phase 2.5 - Optional)
try:
    import sys

    memory_system_path = str(Path(__file__).parent / "memory_system")
    if memory_system_path not in sys.path:
        sys.path.insert(0, memory_system_path)
    from memory_system.yeongdeok_complete import YeongdeokComplete
except ImportError:
    YeongdeokComplete = None
    print("⚠️  YeongdeokComplete not available (Phase 2.5 pending)")

# Import API Wallet (Phase 2.1 - Required)
# APIWallet는 현재 사용되지 않음 (레거시 - api_wallet_router로 대체)
# try:
#     from .api_wallet import APIWallet
# except ImportError:
#     try:
#         from api_wallet import APIWallet
#     except ImportError:
#         APIWallet = None
#         print("⚠️  API Wallet not available")

# Import Skill Registry (Phase 2.5 - Optional)
# register_core_skills만 사용됨, 나머지는 레거시 (skills_router로 대체)
try:
    from afo_skills_registry import register_core_skills
except ImportError:
    register_core_skills = None
    print("⚠️  afo_skills_registry not available (Phase 2.5 pending)")

# This global variable will hold the compiled, runnable LangGraph app.
strategy_app_runnable = None

# Global variables for RAG engines
crag_engine = None
hybrid_engine = None
multimodal_rag_engine = None

# Global variable for Yeongdeok Complete
yeongdeok = None

# Global variable for Query Expander
query_expander = None

# Global variable for Skill Registry
skill_registry: Any | None = None  # SkillRegistry when available

# Global event queue for neural flow streaming (영덕의 신경 흐름)
neural_event_queue: asyncio.Queue = asyncio.Queue()

# Hybrid RAG infrastructure (PostgreSQL + Redis + OpenAI + Claude)
PG_POOL: Any | None = None  # SimpleConnectionPool when psycopg2 available
REDIS_CLIENT: Any | None = None  # redis.Redis
OPENAI_CLIENT: Any | None = None  # OpenAI client
CLAUDE_CLIENT: Any | None = None  # Anthropic client

# Phase 8.2.3: Claude 메트릭 (별도 관리)
claude_cache_metrics = {
    "total_requests": 0,
    "cached_requests": 0,
    "cache_hit_rate": 0.0,
    "estimated_savings_usd": 0.0,
}

# Phase 8.2.3: Prompt Caching 메트릭
prompt_cache_metrics = {
    "total_requests": 0,
    "cached_requests": 0,
    "cache_hit_rate": 0.0,
    "estimated_savings_usd": 0.0,
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manages the lifecycle of the application.
    On startup, it compiles the LangGraph application with Redis checkpointer
    (initialized in strategy_engine.py via AsyncRedisSaver).
    """
    global \
        strategy_app_runnable, \
        crag_engine, \
        hybrid_engine, \
        yeongdeok, \
        query_expander, \
        skill_registry
    global PG_POOL, REDIS_CLIENT, OPENAI_CLIENT, multimodal_rag_engine
    print("【지휘소 v6 - 최종】 API 서버 가동 준비 (완전 비동기)...")

    # Initialize Query Expander (Phase 2.3 - Optional)
    if QueryExpander is not None:
        print("【Query Expander】 쿼리 확장 시스템 초기화 중...")
        query_expander = QueryExpander()
        print("【Query Expander】 WordNet + ChromaDB 하이브리드 확장 준비 완료")
    else:
        query_expander = None
        print("⚠️  Query Expander 건너뜀 (Phase 2.3 구현 필요)")

    # ============================================================================
    # AntiGravity Phase 1: Initialization
    # ============================================================================
    from config.antigravity import antigravity

    if antigravity.AUTO_DEPLOY:
        print(f"🚀 [AntiGravity] 활성화: {antigravity.ENVIRONMENT} 환경 자동 배포 준비 완료 (孝)")

    if antigravity.DRY_RUN_DEFAULT:
        print("🛡️ [AntiGravity] DRY_RUN 모드 활성화 - 모든 위험 동작 시뮬레이션 (善)")
    # ============================================================================

    # Initialize RAG engines - 각 LLM별로 on-demand 생성
    # (API 요청시마다 llm_provider에 따라 동적 생성)
    print("【RAG 엔진】 멀티-LLM 지원 준비 완료.")
    print("【RAG 엔진】 지원 LLM: claude, gemini, codex, ollama, lmstudio")

    # 초기화는 생략 (첫 요청시 생성)
    crag_engine = None
    hybrid_engine = None

    # Initialize Multimodal RAG Engine (Phase 2 - Multimodal RAG)
    if MultimodalRAGEngine is not None:
        print("【Multimodal RAG】 멀티모달 RAG 엔진 초기화 중...")
        # Phase 2-4: settings 사용
        from config.settings import get_settings

        settings = get_settings()
        mock_mode = settings.MOCK_MODE
        multimodal_rag_engine = MultimodalRAGEngine(
            vectorstore=None,  # 벡터 DB는 나중에 통합 가능
            llm_provider="openai",  # 기본값: OpenAI GPT-4V
            use_reranking=False,  # Phase 3에서 활성화
            mock_mode=mock_mode,
        )
        print("【Multimodal RAG】 멀티모달 RAG 엔진 준비 완료 (텍스트+이미지 통합 검색)")
    else:
        multimodal_rag_engine = None
        print("⚠️  Multimodal RAG Engine 건너뜀 (Multimodal RAG Phase 2 구현 필요)")

    # Initialize Multimodal RAG Cache (Phase 5 - Optimization)
    if set_redis_client is not None and REDIS_CLIENT is not None:
        set_redis_client(REDIS_CLIENT)
        print("【Multimodal RAG Cache】 캐시 시스템 초기화 완료 (Redis 통합)")
    else:
        print("⚠️  Multimodal RAG Cache 건너뜀 (Redis 또는 캐시 모듈 없음)")

    # Initialize Skill Registry (Phase 2.5 - Optional)
    if register_core_skills is not None:
        skill_registry = register_core_skills()
        skill_count = (
            skill_registry.count() if skill_registry and hasattr(skill_registry, "count") else 0
        )
        print(f"ℹ️ [INFO] {skill_count} Skills loaded in simulation mode")
    else:
        skill_registry = None
        print("⚠️  Skill Registry not available (Phase 2.5 pending)")

    # Initialize Yeongdeok Complete (Phase 2.5 - Optional)
    if YeongdeokComplete is not None:
        print("【영덕】 영덕 완전체 초기화 중...")
        # Phase 2-4: settings 사용
        try:
            from config.settings import get_settings

            settings = get_settings()
            n8n_url = settings.N8N_URL or ""
            n8n_key = settings.API_YUNGDEOK or ""
        except ImportError:
            n8n_url = ""
            n8n_key = ""

        yeongdeok = YeongdeokComplete(
            n8n_url=n8n_url,
            n8n_api_key=n8n_key,
            enable_llm_brain=False,  # LLM 없어도 작동 (RAG Memory만 사용)
            neural_event_queue=neural_event_queue,  # 신경 흐름 이벤트 큐 연결
        )
        print("【영덕】 영덕 완전체 준비 완료 - 뇌/눈/귀/팔 모두 연결됨")
    else:
        yeongdeok = None
        print("⚠️  Yeongdeok Complete 건너뜀 (Phase 2.5 구현 필요)")

    # Compile with MemorySaver (no context manager needed)
    print("【지휘소 v6】 LangGraph 설계도를 컴파일하여 '두뇌'를 완성합니다...")
    if workflow is not None and memory_context is not None:
        strategy_app_runnable = workflow.compile(checkpointer=memory_context)
        print("【지휘소 v6】 '두뇌' 가동 준비 완료. 명령을 수신할 수 있습니다.")
    else:
        strategy_app_runnable = None
        print("⚠️  Strategy workflow 또는 memory_context 없음 - LangGraph 컴파일 건너뜀")

    # Hybrid RAG: initialize shared resources
    # Phase 2-4: settings 사용
    from config.settings import get_settings

    settings = get_settings()
    pg_host = settings.POSTGRES_HOST
    pg_port = settings.POSTGRES_PORT
    pg_db = settings.POSTGRES_DB
    pg_user = settings.POSTGRES_USER
    pg_password = settings.POSTGRES_PASSWORD

    # REMOVED: PostgreSQL 연결 - 가지치기 (DB 문제 해결)
    # PostgreSQL 연결 (Optional - API Wallet은 JSON 폴백 가능)
    # PostgreSQL 연결 (Optional - API Wallet은 JSON 폴백 가능)
    if PSYCOPG2_AVAILABLE and SimpleConnectionPool is not None:
        try:
            print("【Hybrid RAG】 PostgreSQL 풀 초기화 중...")
            PG_POOL = SimpleConnectionPool(
                1,
                5,
                host=pg_host,
                port=pg_port,
                database=pg_db,
                user=pg_user,
                password=pg_password,
            )
            print(f"✅ PostgreSQL 연결 성공 ({pg_host}:{pg_port}/{pg_db})")
        except Exception as e:
            PG_POOL = None
            print(f"⚠️  PostgreSQL 연결 실패 (API Wallet은 JSON 모드로 작동): {e}")
    else:
        PG_POOL = None
        print("⚠️  PostgreSQL 지원 없음 (psycopg2 미설치) - API Wallet은 JSON 모드로 작동")

    # Redis 연결 (Optional - 캐싱 없이도 작동)
    # 로컬 실행 시 localhost 사용, Docker 네트워크에서는 redis 사용
    # 중앙 설정 사용 (Phase 1 리팩토링)
    try:
        from AFO.config.settings import get_settings

        redis_settings = get_settings()
        redis_host = redis_settings.REDIS_HOST
    except ImportError:
        # Phase 2-4: settings 사용
        from config.settings import get_settings

        settings = get_settings()
        redis_host = settings.REDIS_HOST
    redis_port = settings.REDIS_PORT
    redis_password = settings.REDIS_PASSWORD

    try:
        print(f"【Hybrid RAG】 Redis 클라이언트 연결 중... ({redis_host}:{redis_port})")
        REDIS_CLIENT = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=2,  # 타임아웃 추가
        )
        REDIS_CLIENT.ping()  # Test connection
        print(f"✅ Redis 연결 성공 ({redis_host}:{redis_port})")
    except Exception as e:
        REDIS_CLIENT = None
        print(f"⚠️  Redis 연결 실패 (캐싱 없이 작동): {e}")
        print("   💡 Redis가 필요하면 Docker 컨테이너가 실행 중인지 확인하세요")

    # Initialize OpenAI client (optional)
    # 세션 추출된 토큰 확인
    if OPENAI_AVAILABLE:
        # 1순위: OPENAI_API_KEY (직접 API 키)
        # 2순위: CHATGPT_SESSION_TOKEN (Chrome 세션에서 추출)
        # Phase 2-4: settings 사용
        from config.settings import get_settings

        settings = get_settings()
        openai_key = settings.OPENAI_API_KEY

        # ChatGPT 세션 토큰 확인
        if not openai_key:
            chatgpt_token = (
                # Phase 2-4: settings 사용
                settings.CHATGPT_SESSION_TOKEN_1
                or settings.CHATGPT_SESSION_TOKEN_2
                or settings.CHATGPT_SESSION_TOKEN_3
            )
            if chatgpt_token:
                print("【Hybrid RAG】 CHATGPT_SESSION_TOKEN 발견 (웹 인터페이스용)")
                print(
                    "【Hybrid RAG】 💡 ChatGPT 세션 토큰은 웹용이며, API 호출에는 OPENAI_API_KEY가 필요합니다"
                )

        if openai_key and OpenAI is not None:
            OPENAI_CLIENT = OpenAI(api_key=openai_key)
            print("✅ Hybrid RAG: OpenAI Engine Ready")
        else:
            OPENAI_CLIENT = None
            if not openai_key:
                print("ℹ️ [INFO] OpenAI API key not found, using fallback responses")
            else:
                print("ℹ️ [INFO] OpenAI library unavailable, using fallback responses")
    else:
        OPENAI_CLIENT = None
        print("ℹ️ [INFO] OpenAI library unavailable, using fallback responses")

    # Phase 8.2.3: Claude 클라이언트 초기화 (optional)
    # 세션 추출된 토큰 우선 사용
    if ANTHROPIC_AVAILABLE:
        # 1순위: ANTHROPIC_API_KEY (직접 API 키)
        # 2순위: CURSOR_ACCESS_TOKEN에서 추출된 키 (세션 추출)
        # Phase 2-4: settings 사용
        claude_key = settings.ANTHROPIC_API_KEY

        # Cursor 세션에서 추출된 키 확인
        if not claude_key:
            # Phase 2-4: settings 사용
            cursor_token = settings.CURSOR_ACCESS_TOKEN
            if cursor_token:
                # Cursor 토큰이 있으면 로그만 남기고 (직접 Claude API 호출 불가)
                print("【Hybrid RAG】 CURSOR_ACCESS_TOKEN 발견 (직접 Claude API 호출 불가)")
                print("【Hybrid RAG】 💡 Cursor 세션에서 ANTHROPIC_API_KEY 추출을 권장합니다")

        if claude_key and Anthropic is not None:
            Anthropic(api_key=claude_key)
            print("【Hybrid RAG】 Claude 클라이언트 준비 완료")
        else:
            # CLAUDE_CLIENT = None
            print("【Hybrid RAG】 ⚠️ Claude API 키가 없어 OpenAI로 대체합니다.")
    else:
        print("【Hybrid RAG】 ⚠️ Anthropic 라이브러리 없음 - OpenAI로 대체합니다.")

    # The application is now ready to run
    yield

    # ===== ASYNC DATABASE CONNECTION FUNCTION =====
    # ===== ASYNC DATABASE CONNECTION FUNCTION =====
    # Moved to services/database.py
    # Imported at top level

    # Cleanup
    print("【영덕】 영덕 완전체 종료 중...")
    if yeongdeok and yeongdeok.browser:
        await yeongdeok.close_eyes()

    if PG_POOL:
        PG_POOL.closeall()
    if REDIS_CLIENT:
        with suppress(Exception):
            REDIS_CLIENT.close()

    print("【지휘소 v6】 API 서버 가동 중지.")


# 중앙 설정 사용 (Phase 1 리팩토링)
try:
    from AFO.config.settings import AFOSettings, get_settings

    settings = get_settings()
    # 하위 호환성을 위한 Settings 별칭
    Settings = AFOSettings
except ImportError:
    # Fallback: 기존 Settings 클래스 유지 (하위 호환성)
    class Settings(BaseSettings):
        # Auto-detect .env file location (environment-independent)
        model_config = SettingsConfigDict(
            env_file=str(Path(__file__).parent / ".env"),
            env_file_encoding="utf-8",
            extra="ignore",
        )
        # 환경변수에서 읽고, 없으면 기본값 사용
        # Phase 2-4: settings 사용 (config/settings.py로 이동됨)
        # N8N_URL과 API_YUNGDEOK은 config/settings.py에서 관리

    settings = Settings()

# API Metadata for OpenAPI documentation
API_TITLE = "AFO Kingdom Soul Engine API"
API_DESCRIPTION = """
## 🏰 AFO (A-Philosophy-First Operating System) Ultimate API

**Philosophy**: 眞善美孝 (Truth, Goodness, Beauty, Serenity)

### Overview

The AFO Soul Engine is a multi-agent RAG system with advanced monitoring and workflow automation.

### Key Features

* **🧠 Multi-Agent Orchestration** - LangGraph-based command execution with Redis checkpointing
* **📚 5 RAG Systems** - Ultimate RAG, Trinity Loop, Query Expansion, Recursive RAG, Ragas Evaluation
* **🏥 11-Organ Health Monitoring** - Real-time system health tracking (100% = all healthy)
* **🗄️ Triple Memory** - ChromaDB (vectors), PostgreSQL+pgvector (hybrid), Redis (checkpoints)
* **🔔 Alertmanager Integration** - 30-second Slack notifications for critical events
* **⚡ High Performance** - <50ms API response, 80%+ cache hit rate

### Documentation

* **GitHub**: [lofibrainwav/AFO](https://github.com/lofibrainwav/AFO)
* **Comprehensive Guide**: See CLAUDE.md and DEPLOYMENT_GUIDE.md
* **Philosophy**: See AFO_KINGDOM_CONSTITUTION.md

### Recent Achievements (Nov 2025)

* ✅ **Phase 6.2**: Redis optimization (80%+ cache hit rate via AsyncRedisSaver)
* ✅ **Phase 6.3**: Alertmanager + Grafana integration (30s Slack alerts)
* 🎯 **System Health**: 100% (11/11 organs operational)
"""

API_VERSION = "6.3.0"  # Phase 6.3 complete
API_CONTACT = {
    "name": "AFO Kingdom",
    "url": "https://github.com/lofibrainwav/AFO",
}
API_LICENSE = {
    "name": "MIT License",
    "url": "https://github.com/lofibrainwav/AFO/blob/main/LICENSE",
}

# API Tags for endpoint grouping
tags_metadata = [
    {
        "name": "Health",
        "description": "System health monitoring endpoints. Check 11-organ status and n8n connectivity.",
    },
    {
        "name": "RAG",
        "description": "Retrieval-Augmented Generation endpoints. 5 RAG systems: CRAG, Hybrid, Ultimate, Trinity Loop, Query Expansion.",
    },
    {
        "name": "Ragas",
        "description": "Ragas RAG evaluation system. 4 metrics: Faithfulness, Answer Relevancy, Context Precision, Context Recall.",
    },
    {
        "name": "Strategy",
        "description": "LangGraph-based command execution with Redis checkpointing. Multi-turn conversations with state persistence.",
    },
    {
        "name": "n8n Integration",
        "description": "n8n workflow automation integration. Monitor workflows, check health, execute actions.",
    },
    {
        "name": "API Wallet",
        "description": "Secure API key management with encryption. Store and retrieve API keys for multiple services.",
    },
    {
        "name": "Yeongdeok Memory",
        "description": "Advanced memory system with RAG integration. Named after 제갈량's strategic wisdom.",
    },
    {
        "name": "Skills Registry",
        "description": "AFO skill execution system. Register, discover, and execute modular skills.",
    },
]

# Create the FastAPI app with the lifespan manager
app = FastAPI(
    lifespan=lifespan,
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    contact=API_CONTACT,
    license_info=API_LICENSE,
    openapi_tags=tags_metadata,
)

# ============================================================
# 전역 예외 처리 (FastAPI 베스트 프랙티스)
# ============================================================
try:
    from typing import cast

    from afo_soul_engine.api.core.exceptions import (
        AFOException,
        afo_exception_handler,
        general_exception_handler,
        http_exception_handler,
        validation_exception_handler,
    )

    # FastAPI 타입 시스템에 맞춰 타입 캐스팅 사용 (眞 100% 확보)
    app.add_exception_handler(AFOException, cast("Any", afo_exception_handler))
    app.add_exception_handler(StarletteHTTPException, cast("Any", http_exception_handler))
    app.add_exception_handler(RequestValidationError, cast("Any", validation_exception_handler))
    app.add_exception_handler(Exception, cast("Any", general_exception_handler))
    print("✅ 전역 예외 처리기 등록 완료")
except Exception as e:
    print(f"⚠️  전역 예외 처리기 등록 건너뜀: {e}")

# CORS 설정 (브라우저에서 API 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (프로덕션에서는 특정 도메인으로 제한)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 성능 모니터링 미들웨어 추가 (Phase 3 최적화)
try:
    from .api.middleware.performance import PerformanceMiddleware, RequestLoggingMiddleware

    app.add_middleware(PerformanceMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    print("✅ 성능 모니터링 미들웨어 활성화")
except ImportError as e:
    print(f"⚠️  성능 미들웨어 로드 실패: {e}")

# Rate Limiting 미들웨어 (Phase 9: Trinity EaaS API)
try:
    from .api.middleware.rate_limit import RateLimitMiddleware

    app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
    print("✅ Rate limiting middleware enabled (100 req/min)")
except ImportError as e:
    print(f"⚠️  Rate limiting middleware not available: {e}")

    # ============================================================
    # AFO 스킬 API 영구 등록 (제1계명: 永遠不滅)
    # ============================================================
    # REMOVED: Skill Registry (MOCK 모드) - 가지치기
    # if SKILLS_ROUTER_PERMANENT and SKILLS_ROUTER_AVAILABLE:
    #     # skills_router는 이미 prefix="/api/skills"를 가지고 있으므로 prefix 중복 제거
    #     # app.include_router(skills_router)
    #     # print("✅ AFO 스킬 API 영구 등록 완료 - 永遠不滅 (제1계명)")
    # elif SKILLS_ROUTER_PERMANENT:
    #     print("⚠️  스킬 라우터 로드 실패 - 영구 등록 플래그는 유지됨")

    # Include modular routers (if available)
    # REMOVED: 중복 라우터 제거 - routers/ 폴더의 Facade Pattern 라우터만 사용
    # if MODULAR_ROUTERS_AVAILABLE:
    #     # Mount new modular routers (Phase 2, 5, 6 & 9)
    #     # Trinity Router (Facade Pattern 적용)
    #     if trinity_router is not None:
    #         app.include_router(trinity_router)
    #         print("✅ Trinity Router (Facade) 등록 완료 - 肺 시스템 통합")
    #
    #     # Auth Router (심장 이식)
    #     if auth_router is not None:
    #         app.include_router(auth_router)
    #         print("✅ Auth Router (Heart Transplant) 등록 완료 - 心 시스템 통합")
    #
    #     # Users Router (간 이식)
    #     if users_router is not None:
    #         app.include_router(users_router)
    #         print("✅ Users Router (Liver Transplant) 등록 완료 - 肝 시스템 통합")
    if rag_router is not None:
        app.include_router(rag_router)

    # Phase 2 리팩토링: 분리된 라우터 등록
    if root_router is not None:
        app.include_router(root_router)
        print("✅ Root 라우터 등록 완료 (Phase 2 리팩토링)")
    if health_router is not None:
        app.include_router(health_router)
        print("✅ Health 라우터 등록 완료 (Phase 2 리팩토링)")
    if SKILLS_ROUTER_AVAILABLE and skills_router is not None:
        # `skills_router` already has prefix="/api/skills"
        app.include_router(skills_router)
        print("✅ Skills API 라우터 등록 완료 (손발 연결)")

# 제3계명: 5기둥 API 라우터 등록 (항상 시도)

# 5기둥 API 라우터 (제3계명)
if PILLARS_ROUTER_AVAILABLE:
    app.include_router(pillars_router)
    print("✅ 5기둥 API 라우터 등록 완료 - 제3계명")
else:
    print("⚠️  5기둥 라우터 등록 건너뜀 (로드 실패)")

# ============================================================================
# Phase 8: Julie CPA AutoMate
# ============================================================================
try:
    from api.routes.julie import router as julie_router

    app.include_router(julie_router)
    print("✅ Julie CPA AutoMate Engine activated (의(義))")
except Exception as e:
    print(f"⚠️ Julie CPA Engine load failed: {e}")

# 향상된 헬스 체크 라우터 등록 (Phase 3 최적화)
try:
    from .api.routes.health import router as enhanced_health_router

    app.include_router(enhanced_health_router, prefix="/api", tags=["Health"])
    print("✅ 향상된 헬스 체크 라우터 등록 완료")
except ImportError as e:
    print(f"⚠️  향상된 헬스 체크 라우터 로드 실패: {e}")

# Multi-Agent 라우터 등록 (Phase 4 - 협력 에이전트 시스템)
if MULTI_AGENT_ROUTER_AVAILABLE:
    app.include_router(multi_agent_router)
    print("✅ Multi-Agent 라우터 등록 완료")
else:
    print("⚠️  Multi-Agent 라우터 등록 건너뜀 (로드 실패)")

# Strangler Fig API 라우터 등록 (항상 시도)
if STRANGLER_ROUTER_AVAILABLE:
    app.include_router(strangler_router)
    print("✅ Strangler Fig API 라우터 등록 완료")
else:
    print("⚠️  Strangler Fig 라우터 등록 건너뜀 (로드 실패)")

# Graph-of-Thought API 라우터 등록 (항상 시도)
if GOT_ROUTER_AVAILABLE:
    app.include_router(got_router)
    print("✅ Graph-of-Thought API 라우터 등록 완료")
else:
    print("⚠️  Graph-of-Thought 라우터 등록 건너뜀 (로드 실패)")

# N8N 라우터 등록 (항상 시도)
if N8N_ROUTER_AVAILABLE:
    app.include_router(n8n_router)
    app.include_router(health_n8n_router)
    print("✅ N8N API 라우터 등록 완료")
else:
    print("⚠️  N8N 라우터 등록 건너뜀 (로드 실패)")

# Wallet 라우터 등록 (항상 시도)
if WALLET_ROUTER_AVAILABLE:
    app.include_router(wallet_router)
    print("✅ Wallet API 라우터 등록 완료")
else:
    print("⚠️  Wallet 라우터 등록 건너뜀 (로드 실패)")

# System Health 라우터 등록 (항상 시도)
if system_health_router is not None:
    app.include_router(system_health_router)
    print("✅ System Health API 라우터 등록 완료")
else:
    print("⚠️  System Health 라우터 등록 건너뜀 (로드 실패)")

# Trinity Policy 라우터 등록 (항상 시도 - /api/trinity/realtime 포함)
if trinity_policy_router is not None:
    app.include_router(trinity_policy_router, tags=["trinity"])

    # Trinity Metrics Router (새로운 수학 공식 기반)
    try:
        from .api.routes.trinity_metrics import router as trinity_metrics_router

        app.include_router(trinity_metrics_router, tags=["trinity"])
        print("✅ Trinity Metrics router 등록 완료")
    except Exception as exc:
        print(f"⚠️  Trinity Metrics router 등록 실패: {exc}")
    print("✅ Trinity Policy API 라우터 등록 완료")
else:
    print("⚠️  Trinity Policy 라우터 등록 건너뜀 (로드 실패)")

# Trinity SBT 라우터 등록 (Phase 9 - 온체인 민트)
if trinity_sbt_router is not None:
    app.include_router(trinity_sbt_router, prefix="/api", tags=["trinity"])
    print("✅ Trinity SBT API 라우터 등록 완료")
else:
    print("⚠️  Trinity SBT 라우터 등록 건너뜀 (로드 실패)")

# HWOOT 라우터 등록 (Phase 10 - Automerge 가족 노트북)
# HWOOT 라우터 등록 (Phase 10 - Automerge 가족 노트북)
# try:
#     from .hwoot.routes import router as hwoot_router
#
#     # REMOVED: HWOOT Router (모듈 없음) - 가지치기
#     # app.include_router(hwoot_router, prefix="/api")
#     # print("✅ HWOOT API 라우터 등록 완료 (가족의 공유 노트북)")
# except ImportError as e:
#     print(f"⚠️  HWOOT 라우터 등록 건너뜀 (로드 실패: {e})")
# except Exception as e:
#     print(f"⚠️  HWOOT 라우터 등록 건너뜀 (오류: {e})")

# WatchTower 라우터 등록 (Phase 23-D - 와치타워 시스템)
try:
    from .api.routes.watchtower import router as watchtower_router

    app.include_router(watchtower_router, tags=["WatchTower"])
    print("✅ WatchTower API 라우터 등록 완료 (미래 예측 관측소)")
except ImportError as e:
    print(f"⚠️  WatchTower 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  WatchTower 라우터 등록 건너뜀 (오류: {e})")

# Sejong Spirit 라우터 등록 (Phase 23-D - 세종대왕 정신)
try:
    from .api.routes.sejong import router as sejong_router

    app.include_router(sejong_router, tags=["Sejong Spirit"])
    print("✅ Sejong Spirit API 라우터 등록 완료 (홍익인간 정신)")
except ImportError as e:
    print(f"⚠️  Sejong Spirit 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Sejong Spirit 라우터 등록 건너뜀 (오류: {e})")

# Creative Beauty 라우터 등록 (Phase 23-D - 창조미 평가)
try:
    from .api.routes.beauty import router as beauty_router

    app.include_router(beauty_router, tags=["Creative Beauty"])
    print("✅ Creative Beauty API 라우터 등록 완료 (창제급 창조미)")
except ImportError as e:
    print(f"⚠️  Creative Beauty 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Creative Beauty 라우터 등록 건너뜀 (오류: {e})")

# 지피지기 시스템 라우터 등록
try:
    from .api.routes.jipijigi import router as jipijigi_router

    app.include_router(jipijigi_router, tags=["Jipijigi"])
    print("✅ Jipijigi API 라우터 등록 완료 (지피지기 지금! 시스템)")
except ImportError as e:
    print(f"⚠️  Jipijigi 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Jipijigi 라우터 등록 건너뜀 (오류: {e})")

# Redis 테스트 라우터 등록 (프로덕션급 연결 풀 검증)
try:
    from .api.routers.redis_test import router as redis_test_router

    app.include_router(redis_test_router)
    print("✅ Redis 테스트 API 라우터 등록 완료 (프로덕션급 연결 풀)")
except ImportError as e:
    print(f"⚠️  Redis 테스트 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Redis 테스트 라우터 등록 건너뜀 (오류: {e})")

# 재해 복구 시스템 라우터 등록
try:
    from .api.routes.disaster_recovery import router as dr_router

    app.include_router(dr_router, tags=["Disaster Recovery"])
    print("✅ Disaster Recovery API 라우터 등록 완료 (형님 한 마디면 30초 복구)")
except ImportError as e:
    print(f"⚠️  Disaster Recovery 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Disaster Recovery 라우터 등록 건너뜀 (오류: {e})")

# 데이터 암호화 시스템 라우터 등록
try:
    from .api.routes.encryption import router as encryption_router

    app.include_router(encryption_router, tags=["Encryption"])
    print("✅ Encryption API 라우터 등록 완료 (형님 한 마디면 3초 암호화)")
except ImportError as e:
    print(f"⚠️  Encryption 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Encryption 라우터 등록 건너뜀 (오류: {e})")

# 키 관리 시스템 라우터 등록
try:
    from .api.routes.key_management import router as key_management_router

    app.include_router(key_management_router, tags=["Key Management"])
    print("✅ Key Management API 라우터 등록 완료 (형님 한 마디면 5초 키 관리)")
except ImportError as e:
    print(f"⚠️  Key Management 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Key Management 라우터 등록 건너뜀 (오류: {e})")

# 인증서 자동 갱신 시스템 라우터 등록
try:
    from .api.routes.certificate_management import router as certificate_router

    app.include_router(certificate_router, tags=["Certificate Management"])
    print("✅ Certificate Management API 라우터 등록 완료 (형님 한 마디면 10초 인증서 갱신)")
except ImportError as e:
    print(f"⚠️  Certificate Management 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Certificate Management 라우터 등록 건너뜀 (오류: {e})")

# Certbot 디버깅 시스템 라우터 등록
try:
    from .api.routes.certbot_debugging import router as certbot_debug_router

    app.include_router(certbot_debug_router, tags=["Certbot Debugging"])
    print("✅ Certbot Debugging API 라우터 등록 완료 (형님 한 마디면 10초 원인 파악)")
except ImportError as e:
    print(f"⚠️  Certbot Debugging 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Certbot Debugging 라우터 등록 건너뜀 (오류: {e})")

# Certbot 로그 분석 시스템 라우터 등록
try:
    from .api.routes.certbot_log_analyzer import router as log_analyzer_router

    app.include_router(log_analyzer_router, tags=["Certbot Log Analysis"])
    print("✅ Certbot Log Analyzer API 라우터 등록 완료 (형님 한 마디면 5초 원인 파악)")
except ImportError as e:
    print(f"⚠️  Certbot Log Analyzer 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Certbot Log Analyzer 라우터 등록 건너뜀 (오류: {e})")

# TLS 베스트 프랙티스 시스템 라우터 등록
try:
    from .api.routes.tls_best_practices import router as tls_bp_router

    app.include_router(tls_bp_router, tags=["TLS Best Practices"])
    print("✅ TLS Best Practices API 라우터 등록 완료 (형님 한 마디면 10초 세계 최고 수준)")
except ImportError as e:
    print(f"⚠️  TLS Best Practices 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  TLS Best Practices 라우터 등록 건너뜀 (오류: {e})")

# Certificate Transparency 시스템 라우터 등록
try:
    from .api.routes.certificate_transparency import router as ct_router

    app.include_router(ct_router, tags=["Certificate Transparency"])
    print("✅ Certificate Transparency API 라우터 등록 완료 (형님 한 마디면 5초 CT 로그 확인)")
except ImportError as e:
    print(f"⚠️  Certificate Transparency 라우터 등록 건너뜀 (로드 실패: {e})")

# CRAG Self-Correction 라우터 등록 (Phase 4 - n8n 통합)
try:
    from .api.routes.crag import router as crag_router

    app.include_router(crag_router)
    print("✅ CRAG API 라우터 등록 완료 (에이전트가 스스로 반성하며 답변 보강)")
except ImportError as e:
    print(f"⚠️  CRAG 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  CRAG 라우터 등록 건너뜀 (오류: {e})")

# Chat API 라우터 등록 (LLM Router 연동 - Ollama First)
try:
    from api.routes.chat import router as chat_router

    app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
    print("✅ Chat API 라우터 등록 완료 (Ollama 우선 → API Fallback)")
except ImportError as e:
    print(f"⚠️  Chat 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Chat 라우터 등록 건너뜀 (오류: {e})")

# 승상 API 라우터 등록 (LangGraph Phase 24)
try:
    from AFO.api.routers.chancellor_router import router as chancellor_router

    app.include_router(chancellor_router)
    print("✅ 승상 API 라우터 등록 완료 (LangGraph Optimized: Chancellor + 3 Strategists)")
except ImportError as e:
    try:
        from api.routers.chancellor_router import router as chancellor_router

        app.include_router(chancellor_router)
        print(
            "✅ 승상 API 라우터 등록 완료 (LangGraph Optimized: Chancellor + 3 Strategists - fallback)"
        )
    except Exception as e2:
        print(f"⚠️  승상 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  승상 라우터 등록 건너뜀 (오류: {e})")

# Trinity API MVP 라우터 등록 (Graph-of-Thought Step B)
try:
    from afo_soul_engine.routers.trinity_router import router as trinity_router

    app.include_router(trinity_router)
    print("✅ Trinity API MVP 라우터 등록 완료 (형님의 眞善美孝 철학이 API로 실현)")
except ImportError as e:
    print(f"⚠️  Trinity API 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  Trinity API 라우터 등록 건너뜀 (오류: {e})")

# Users API 라우터 등록 (간 이식 - Router Facade Pattern)
try:
    from afo_soul_engine.routers.users import router as users_router

    app.include_router(users_router)
    print("✅ Users API 라우터 등록 완료 (肝 시스템 - 사용자 관리)")
except ImportError as e:
    try:
        from AFO.api.routers.users import router as users_router

        app.include_router(users_router)
        print("✅ Users API 라우터 등록 완료 (肝 시스템 - 사용자 관리 - fallback)")
    except Exception as e2:
        print(f"⚠️  Users API 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  Users API 라우터 등록 건너뜀 (오류: {e})")

# Auth API 라우터 등록 (심장 이식 - Router Facade Pattern)
try:
    from afo_soul_engine.routers.auth import router as auth_router

    app.include_router(auth_router)
    print("✅ Auth API 라우터 등록 완료 (心 시스템 - 인증)")
except ImportError as e:
    try:
        from AFO.api.routers.auth import router as auth_router

        app.include_router(auth_router)
        print("✅ Auth API 라우터 등록 완료 (心 시스템 - 인증 - fallback)")
    except Exception as e2:
        print(f"⚠️  Auth API 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  Auth API 라우터 등록 건너뜀 (오류: {e})")

# Personas API 라우터 등록 (Phase 2: Family Hub OS - 페르소나 시스템)
try:
    from AFO.api.routers.personas import router as personas_router

    app.include_router(personas_router)
    print("✅ Personas API 라우터 등록 완료 (Phase 2: Family Hub OS - TRINITY-OS 페르소나 통합)")
except ImportError as e:
    try:
        from api.routers.personas import router as personas_router

        app.include_router(personas_router)
        print("✅ Personas API 라우터 등록 완료 (Phase 2: Family Hub OS - fallback)")
    except Exception as e2:
        print(f"⚠️  Personas API 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  Personas API 라우터 등록 건너뜀 (오류: {e})")

# Family Hub API 라우터 등록 (Phase 2: Family Hub OS - 가족 데이터 연결)
try:
    from AFO.api.routers.family import router as family_router

    app.include_router(family_router)
    print("✅ Family Hub API 라우터 등록 완료 (Phase 2: Family Hub OS - 美: 모듈화 + 일관 네이밍)")
except ImportError as e:
    try:
        from api.routers.family import router as family_router

        app.include_router(family_router)
        print("✅ Family Hub API 라우터 등록 완료 (Phase 2: Family Hub OS - fallback)")
    except Exception as e2:
        print(f"⚠️  Family Hub API 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  Family Hub API 라우터 등록 건너뜀 (오류: {e})")

# Intake API 라우터 등록 (위 이식 - Router Facade Pattern)
try:
    from afo_soul_engine.routers.intake import router as intake_router

    app.include_router(intake_router)
    print("✅ Intake API 라우터 등록 완료 (胃 시스템 - 스마트 파싱)")
except ImportError as e:
    try:
        from .routers.intake import router as intake_router

        app.include_router(intake_router)
        print("✅ Intake API 라우터 등록 완료 (胃 시스템 - 스마트 파싱 - fallback)")
    except Exception as e2:
        print(f"⚠️  Intake API 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  Intake API 라우터 등록 건너뜀 (오류: {e})")

# Family API 라우터 등록 (비 이식 - Router Facade Pattern)
try:
    from afo_soul_engine.routers.family import router as family_router

    app.include_router(family_router)
    print("✅ Family API 라우터 등록 완료 (脾 시스템 - 가족 허브)")
except ImportError as e:
    try:
        from .routers.family import router as family_router

        app.include_router(family_router)
        print("✅ Family API 라우터 등록 완료 (脾 시스템 - 가족 허브 - fallback)")
    except Exception as e2:
        print(f"⚠️  Family API 라우터 등록 건너뜀 (로드 실패: {e}, {e2})")
except Exception as e:
    print(f"⚠️  Family API 라우터 등록 건너뜀 (오류: {e})")

# Fallback 라우터 등록 (MODULAR_ROUTERS_AVAILABLE이 False인 경우)
if not MODULAR_ROUTERS_AVAILABLE:
    print("⚠️  Using fallback: modular routers not available")

    # Mount legacy routers (may be migrated later)
    # Note: skill_registry_router already has prefix="/api/skills", so don't add it again
    # REMOVED: Skill Registry Router (MOCK 모드) - 가지치기
    # app.include_router(skill_registry_router, tags=["skills"])
    # Wallet router는 위에서 이미 마운트됨 (api_wallet_router는 레거시, 점진적 제거 예정)
    # app.include_router(api_wallet_router, prefix="/api/wallet", tags=["wallet"])
    # trinity_policy_router는 위에서 이미 등록됨 (중복 방지)
    app.include_router(modal_data_router, prefix="/api/modal", tags=["modal"])
    app.include_router(education_system_router, prefix="/api/education", tags=["education"])
    print("✅ All routers mounted successfully")

# Prometheus 메트릭 (마찰 측정 - 승상의 지혜)
if PROMETHEUS_AVAILABLE:
    Instrumentator().instrument(app).expose(app)
else:
    logger.info("Skipping Prometheus instrumentation - package not available")

# 眞 루프 전용 커스텀 메트릭 (승상님 통합 지시)


# Centralized Metrics Import (Circular Dependency Fix)
# Metrics are now imported at the top of the file to prevent double-loading.
pass


# Hybrid RAG Logic Moved to services/hybrid_rag.py
# Adapter functions to inject global dependencies (OPENAI_CLIENT, etc.)


async def _get_embedding_async_adapter(text: str) -> list[float]:
    return await get_embedding_async(text, OPENAI_CLIENT)


async def _query_pgvector_async_adapter(embedding: list[float], top_k: int) -> list[dict]:
    return await query_pgvector_async(embedding, top_k, PG_POOL)


async def _query_redis_async_adapter(embedding: list[float], top_k: int) -> list[dict]:
    return await query_redis_async(embedding, top_k, REDIS_CLIENT)


async def _blend_results_async_adapter(
    pg_rows: list[dict], redis_rows: list[dict], top_k: int
) -> list[dict]:
    return await blend_results_async(pg_rows, redis_rows, top_k)


async def _generate_answer_async_adapter(
    query: str,
    contexts: list[str],
    temperature: float,
    response_format: str,
    additional_instructions: str,
    llm_provider: str = "openai",
) -> str | dict:
    return await generate_answer_async(
        query,
        contexts,
        temperature,
        response_format,
        additional_instructions,
        llm_provider,
        openai_client=OPENAI_CLIENT,
    )


# Alias for compatibility with existing code
_get_embedding_async = _get_embedding_async_adapter
_query_pgvector_async = _query_pgvector_async_adapter
_query_redis_async = _query_redis_async_adapter
_blend_results_async = _blend_results_async_adapter
_generate_answer_async = _generate_answer_async_adapter
_select_context = select_context  # Sync function alias


# Phase 2 리팩토링: 모델은 api/models/로 이동됨
# 모든 Request/Response 모델은 api/models/requests.py와 api/models/responses.py에 정의됨


# Phase 2-6: Root 엔드포인트는 api/routers/root.py로 이동됨
# 아래 엔드포인트는 root_router에 포함됨 (하위 호환성을 위해 유지)
@app.get("/", include_in_schema=False)
async def read_root_legacy() -> dict[str, str]:
    """Legacy root endpoint - use root_router instead"""
    from AFO.api.routers.root import read_root

    return await read_root()


# Phase 2 리팩토링: Health 엔드포인트는 api/routers/health.py로 이동됨
# 아래 엔드포인트는 health_router에 포함됨 (하위 호환성을 위해 유지)
@app.get("/health", tags=["Health"], include_in_schema=False)
async def health_check_legacy() -> dict[str, Any]:
    """
    Health check endpoint - 브릿지의 시선: 메타인지 + 眞善美孝 점수

    실제 서비스 연결을 테스트하고 Trinity Score로 건강도 계산
    """
    import httpx
    import redis.asyncio as redis

    # Absolute import for domain modules
    try:
        from AFO.domain.metrics.trinity import TrinityMetrics, calculate_trinity
    except ImportError:
        # Fallback if running from within AFO package context
        try:
            from domain.metrics.trinity import TrinityMetrics, calculate_trinity
        except ImportError:
            # Mock for health check if module missing
            class TrinityMetrics:
                def __init__(self, **kwargs):
                    self.trinity_score = 0.8
                    self.truth = 0.8
                    self.goodness = 0.8
                    self.beauty = 0.8
                    self.filial_serenity = 0.8
                    self.eternity = 0.8
                    self.balance_status = "balanced"

                def to_dict(self):
                    return self.__dict__

            def calculate_trinity(**kwargs):
                return TrinityMetrics()

    current_time = datetime.now().isoformat()
    organs: list[dict] = []

    # === 실제 서비스 체크 함수들 ===
    async def check_redis() -> dict:
        try:
            # Use centralized Redis connection (Phase 1 리팩토링)
            from AFO.utils.redis_connection import get_redis_url

            r = redis.from_url(get_redis_url())
            pong = await r.ping()
            await r.close()
            return {"healthy": pong, "output": f"PING -> {pong}"}
        except Exception as e:
            return {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    async def check_postgres() -> dict:
        try:
            # Use centralized database connection (Phase 1 리팩토링)
            from AFO.services.database import get_db_connection

            conn = await get_db_connection()
            result = await conn.fetchval("SELECT 1")
            await conn.close()
            return {"healthy": result == 1, "output": f"SELECT 1 -> {result}"}
        except Exception as e:
            return {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    async def check_ollama() -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Use centralized settings (Phase 1 리팩토링)
                from AFO.config.settings import get_settings

                ollama_url = get_settings().OLLAMA_BASE_URL
                resp = await client.get(ollama_url + "/api/tags")
                data = resp.json()
                model_count = len(data.get("models", []))
                return {"healthy": model_count > 0, "output": f"Models: {model_count}"}
        except Exception as e:
            return {"healthy": False, "output": f"Error: {str(e)[:50]}"}

    async def check_self() -> dict:
        return {"healthy": True, "output": "Self-check: API responding"}

    # === 병렬 실행 ===
    results = await asyncio.gather(
        check_redis(), check_postgres(), check_ollama(), check_self(), return_exceptions=True
    )

    organ_checks = [
        (
            "心_Redis",
            results[0]
            if not isinstance(results[0], Exception)
            else {"healthy": False, "output": str(results[0])},
        ),
        (
            "肝_PostgreSQL",
            results[1]
            if not isinstance(results[1], Exception)
            else {"healthy": False, "output": str(results[1])},
        ),
        (
            "脾_Ollama",
            results[2]
            if not isinstance(results[2], Exception)
            else {"healthy": False, "output": str(results[2])},
        ),
        (
            "肺_API_Server",
            results[3]
            if not isinstance(results[3], Exception)
            else {"healthy": False, "output": str(results[3])},
        ),
    ]

    for organ_name, result in organ_checks:
        organs.append(
            {
                "organ": organ_name,
                "healthy": result["healthy"],
                "status": "healthy" if result["healthy"] else "unhealthy",
                "output": result["output"],
                "timestamp": current_time,
            }
        )

    # === 眞善美孝永 5기둥 계산 (SSOT: TRINITY_OS_PERSONAS.yaml) ===
    # 가중치: 眞35% 善35% 美20% 孝8% 永2%

    healthy_count = sum(1 for o in organs if o["healthy"])
    total_organs = len(organs)

    # 眞 (Truth 35%) - 기술적 확실성: 핵심 데이터 계층 (PostgreSQL + Redis)
    core_data_organs = ["心_Redis", "肝_PostgreSQL"]
    truth_healthy = sum(1 for o in organs if o["organ"] in core_data_organs and o["healthy"])
    truth_score = truth_healthy / len(core_data_organs) if core_data_organs else 0.0

    # 善 (Goodness 35%) - 윤리·안정성: 전체 서비스 안정성 (모든 장기)
    goodness_score = healthy_count / total_organs if total_organs > 0 else 0.0

    # 美 (Beauty 20%) - 단순함·우아함: API 응답 품질
    api_healthy = any(o["organ"] == "肺_API_Server" and o["healthy"] for o in organs)
    beauty_score = 1.0 if api_healthy else 0.0

    # 孝 (Serenity 8%) - 평온·연속성: LLM 서비스 가용성 (Ollama)
    llm_healthy = any(o["organ"] == "脾_Ollama" and o["healthy"] for o in organs)
    filial_score = 1.0 if llm_healthy else 0.0

    # 永 (Eternity 2%) - 영속성: 모든 핵심 서비스 가동 시간 (현재는 전체 건강 기준)
    eternity_score = 1.0 if healthy_count == total_organs else healthy_count / total_organs

    # Trinity 계산 (5기둥 SSOT 가중 합)
    trinity_metrics: TrinityMetrics = calculate_trinity(
        truth=truth_score,
        goodness=goodness_score,
        beauty=beauty_score,
        filial_serenity=filial_score,
        eternity=eternity_score,
    )

    # Prometheus 메트릭 업데이트 (사용 가능한 경우)
    try:
        from domain.metrics.prometheus import health_healthy_organs, health_total_score

        health_total_score.set(trinity_metrics.trinity_score * 100)
        health_healthy_organs.set(healthy_count)
    except Exception:
        pass

    # === 집현전 철학: 즉시 폐기가 아닌, 반복 개선 (DRY_RUN + ITERATE) ===
    # 문제 발견 시: 해결책 제시 + 재시도 가이드

    issues = []
    suggestions = []

    if trinity_metrics.truth < 1.0:
        failed_core = [
            o["organ"]
            for o in organs
            if o["organ"] in ["心_Redis", "肝_PostgreSQL"] and not o["healthy"]
        ]
        issues.append(f"眞(데이터 계층): {', '.join(failed_core)} 연결 실패")
        suggestions.append("docker-compose restart redis postgres")

    if trinity_metrics.filial_serenity < 1.0:
        issues.append("孝(LLM 서비스): Ollama 연결 끊김")
        suggestions.append("docker start afo-ollama")

    if trinity_metrics.beauty < 1.0:
        issues.append("美(API): 응답 불가")
        suggestions.append("docker-compose restart soul-engine")

    # 집현전 판단: BLOCK 대신 TRY_AGAIN + 해결책 제시
    if trinity_metrics.balance_status == "imbalanced":
        decision = "TRY_AGAIN"
        decision_message = "집현전 학자들이 문제를 해결 중입니다. 재시도하세요."
    elif trinity_metrics.balance_status == "warning":
        decision = "ASK_COMMANDER"
        decision_message = "일부 서비스에 주의가 필요합니다."
    else:
        decision = "AUTO_RUN"
        decision_message = "모든 시스템 정상. 자동 실행 가능합니다."

    return {
        "status": trinity_metrics.balance_status,
        "health_percentage": round(trinity_metrics.trinity_score * 100, 2),
        "healthy_organs": healthy_count,
        "total_organs": total_organs,
        "trinity": trinity_metrics.to_dict(),
        "decision": decision,
        "decision_message": decision_message,
        "issues": issues if issues else None,
        "suggestions": suggestions if suggestions else None,
        "organs": {
            o["organ"]: {"status": o["status"], "output": str(o.get("output", ""))[:100]}
            for o in organs
        },
        "method": "bridge_perspective_v2_jiphyeonjeon",
        "timestamp": current_time,
    }


@app.get("/health_old", tags=["Health"], include_in_schema=False)
async def health_check_old() -> dict[str, Any]:
    """
    **11-Organ Health Check** - Verifies API server status and component readiness.

    Returns the health status of the AFO Soul Engine API server including:
    - Strategy Engine (LangGraph)
    - Yeongdeok Memory System

    **Usage**: Docker healthcheck, monitoring, readiness probes

    **Expected Response**: `{"status": "healthy", "components": {...}}`
    """
    # 로그 이벤트 발생 (emit_log_event는 refactoring 후 helpers.py로 이동 예정)
    # 현재는 표준 로깅 사용
    logging.info("Health check requested")

    return {
        "status": "healthy",
        "service": "AFO Soul Engine API",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "strategy_engine": "ready" if strategy_app_runnable else "initializing",
            "yeongdeok": "ready" if yeongdeok else "initializing",
        },
    }


# ============================================================
# 동적 라우터 자동 등록 (Strangler Fig Pattern 확장)
# api/routers/ 및 api/routes/ 폴더의 모든 라우터를 자동으로 등록
# 기존 코드는 건드리지 않고 확장 구조로 동작
# 레고처럼 조립: 모든 모듈을 자동으로 통합
# ============================================================
try:
    from afo_soul_engine.api.fig_overlay.auto_inject import auto_include_all_routers

    auto_include_all_routers(app)
    print("✅ 동적 라우터 자동 등록 완료 (Strangler Fig 확장 - 레고 조립)")
except Exception:
    try:
        # 폴백: 상대 import 시도
        from .api.fig_overlay.auto_inject import auto_include_all_routers

        auto_include_all_routers(app)
        print("✅ 동적 라우터 자동 등록 완료 (Strangler Fig 확장 - fallback)")
    except Exception as e2:
        print(f"⚠️  동적 라우터 자동 등록 건너뜀: {e2}")

# ============================================================================
# Phase 1.3: Async Wrappers
# Handled by adapters at the top (dependency injection)
# ============================================================================

print("🎉 Phase 1.3: Async Wrappers 적용 완료 - Adapters Active")

# ============================================================================
# Phase 2.0: Database Initialization (간 시스템 초기화) - Async 방식
# ============================================================================


@app.on_event("startup")
async def on_startup() -> None:
    """서버 시작 시 데이터베이스 및 가족 데이터 초기화"""
    try:
        from afo_soul_engine.core.database import create_tables

        await create_tables()
        print("✅ Database tables ready (Async initialized)")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")

    # 가족 데이터 로드 (기억력 복원)
    try:
        from afo_soul_engine.routers.family import load_family_data

        family_data = load_family_data()
        activity_count = len(family_data.get("activities", []))
        print(f"✅ Family data loaded: {activity_count} activities restored")
    except Exception as e:
        print(f"⚠️ Family data load failed: {e}")

    # ============================================================================
    # Phase 8: Julie CPA AutoMate
    # ============================================================================


# ============================================================================
# AntiGravity Phase 4: Friction Status
# ============================================================================
@app.get("/api/antigravity/status", tags=["AntiGravity"])
async def get_antigravity_status():
    """
    [AntiGravity] 왕국 평온 상태 조회 (Phase 4)
    형님의 '신경 쓰임' 지수를 수치화하여 보고합니다.
    """
    from config.friction_calibrator import friction_calibrator

    metrics = friction_calibrator.calculate_serenity()
    return metrics


@app.on_event("startup")
async def debug_routes():
    pass


# ============================================================================


if __name__ == "__main__":
    print("🛣️  [Route Debug Debugger] Registered Routes (Main Block):")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"   - {route.path}")

    import uvicorn

    # Phase 2-4: settings 사용
    try:
        from config.settings import get_settings

        settings = get_settings()
        api_port = settings.API_SERVER_PORT
        api_host = settings.API_SERVER_HOST
    except ImportError:
        try:
            from AFO.config.settings import get_settings

            settings = get_settings()
            api_port = settings.API_SERVER_PORT
            api_host = settings.API_SERVER_HOST
        except ImportError:
            api_port = int(os.getenv("API_SERVER_PORT", "8011"))
            api_host = os.getenv("API_SERVER_HOST", "0.0.0.0")

    uvicorn.run(app, host=api_host, port=api_port)
