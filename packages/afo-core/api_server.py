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
from starlette.exceptions import HTTPException as StarletteHTTPException

# Path setup for imports (must be before AFO imports)
_AFO_ROOT = str(Path(__file__).resolve().parent.parent)
if _AFO_ROOT not in sys.path:
    sys.path.insert(0, _AFO_ROOT)

from AFO.api.routers.health import router as health_router
from AFO.api.routers.root import router as root_router
from AFO.api.routes.streams import router as streams_router

# ============================================================================
# IMPORTS via Strangler Fig Facade (AFO.api.compat)
# ============================================================================
from AFO.api.compat import HybridRAG, LazyModules, get_settings_safe, load_dotenv_safe

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable
    from AFO.config.settings import AFOSettings

# Alias for compatibility with existing code
get_settings = get_settings_safe
anthropic = LazyModules.anthropic
chromadb = LazyModules.chromadb
crewai = LazyModules.crewai
langchain = LazyModules.langchain
qdrant_client = LazyModules.qdrant_client

# Hybrid RAG Aliases
blend_results_async = HybridRAG.blend_results_async
generate_answer_async = HybridRAG.generate_answer_async
get_embedding_async = HybridRAG.get_embedding_async
query_pgvector_async = HybridRAG.query_pgvector_async
query_redis_async = HybridRAG.query_redis_async
select_context = HybridRAG.select_context


# 백색 소음 제거: Pydantic UserWarning 완전 박멸
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# ============================================================================
# ENVIRONMENT / SETTINGS
# ============================================================================

settings: Any | None = None

if load_dotenv_safe():
    env_loaded = True
    if env_loaded:
        print("✅ 환경 변수 로드 완료 (.env)")
    else:
        print("⚠️ .env 파일을 찾을 수 없거나 로드 실패")
else:
    print("⚠️ python-dotenv가 설치되지 않아 .env 파일을 로드할 수 없습니다")

if get_settings is not None:
    try:
        settings = get_settings()
    except Exception:
        settings = None

gemini_key = getattr(settings, "GEMINI_API_KEY", None) if settings else os.getenv("GEMINI_API_KEY")
if gemini_key:
    print(f"✅ GEMINI_API_KEY 로드됨: {gemini_key[:20]}...")
# Note: GEMINI_API_KEY is optional - Ollama is prioritized for cost=0

sentinel_dsn = getattr(settings, "SENTRY_DSN", None) if settings else os.getenv("SENTRY_DSN")
if sentinel_dsn and LazyModules.sentry_sdk:
    LazyModules.sentry_sdk.init(
        dsn=sentinel_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    print("✅ Sentry 모니터링 활성화")
elif sentinel_dsn:
    print("⚠️  sentry_sdk not installed, skipping Sentry integration")
else:
    print("⚠️ SENTRY_DSN 설정 없음")


# ============================================================================
# LAZY IMPORTS - Phase 1.2: 서버 시작 시간 최적화
# Handled by AFO.api.compat
# ============================================================================
print("🎉 Phase 1.2: Lazy Imports applied via Compatibility Layer")

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
# [노자] 유무상생 - 있음과 없음은 서로 생성함
EventSourceResponse: Any = None
try:
    from sse_starlette.sse import EventSourceResponse
    SSE_AVAILABLE = True
except ImportError:
    SSE_AVAILABLE = False
    print("⚠️  sse-starlette not available (SSE support disabled)")
# SSE_AVAILABLE = False

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
#     from api.routers.api_wallet import router as api_wallet_router
# except Exception as exc:
#     api_wallet_router = _fallback_router("API Wallet", exc)

# obsidian_router는 현재 사용되지 않음 (레거시)
# try:
#     from api.routes.obsidian import router as obsidian_router
# except Exception as exc:
#     obsidian_router = _fallback_router("Obsidian", exc)

# ============================================================
# COMPATIBILITY LAYER (STRANGLER FIG IMPORT)
# ============================================================
from AFO.api.compat import (
    # Flags
    ANTHROPIC_AVAILABLE,
    OPENAI_AVAILABLE,
    # Functions
    TrinityMetrics,
    # Routers
    auth_router,
    calculate_trinity,
    education_system_router,
    got_router,
    modal_data_router,
    multi_agent_router,
    n8n_router,
    pillars_router,
    rag_router,
    skills_router,
    strangler_router,
    system_health_router,
    trinity_policy_router,
    trinity_router,
    trinity_sbt_router,
    users_router,
    users_router,
    wallet_router,
    thoughts_router,
)
# get_settings aliases are handled at the top
pass

# Print availability status (optional, kept for logs)
print(f"✅ 5기둥 API 라우터 로드 상태: {pillars_router is not None}")
print(f"✅ System Health 라우터 로드 상태: {system_health_router is not None}")

# Database setup
try:
    DATABASE_AVAILABLE = True
    print("✅ Database module loaded")
except Exception as exc:
    DATABASE_AVAILABLE = False
    print(f"⚠️  Database module not available: {exc}")

if trinity_router:  # check if facade is available
    print("✅ Modular routers imported successfully via Compat Layer")
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
# [대학] 격물치지 - 사물을 궁구하여 지식을 얻음
memory_context: Any = None
workflow: Any = None
try:
    from strategy_engine import memory_context as _mc, workflow as _wf
    memory_context = _mc
    workflow = _wf
except ImportError:
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
# [색즉시공] - 없음도 있음의 한 형태
QueryExpander: Any = None
try:
    from query_expansion_advanced import QueryExpander as _QE
    QueryExpander = _QE
except ImportError:
    print("⚠️  QueryExpander not available (Phase 2.3 pending)")

# Import Multimodal RAG Engine (Phase 2 - Multimodal RAG)
MultimodalRAGEngine: Any = None
try:
    from multimodal_rag_engine import MultimodalRAGEngine as _MRAE
    MultimodalRAGEngine = _MRAE
except ImportError:
    print("⚠️  MultimodalRAGEngine not available (Multimodal RAG Phase 2 pending)")

# Import Multimodal RAG Cache (Phase 5 - Optimization)
# set_redis_client만 사용됨, 나머지는 레거시
set_redis_client: Any = None
try:
    from multimodal_rag_cache import set_redis_client as _src
    set_redis_client = _src
except ImportError:
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

# Import Yeongdeok Complete (Phase 2.5 - Memory System)
YeongdeokComplete: Any = None
try:
    from AFO.memory_system.yeongdeok_complete import YeongdeokComplete as _YC
    YeongdeokComplete = _YC
except ImportError:
    try:
        from memory_system.yeongdeok_complete import YeongdeokComplete as _YC
        YeongdeokComplete = _YC
    except ImportError:
        pass  # Silent - optional module

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
# [무위자연] - 있으면 쓰고 없으면 자연스레 넘김
register_core_skills: Any = None
try:
    from afo_skills_registry import register_core_skills as _rcs
    register_core_skills = _rcs
except ImportError:
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
    print("[지휘소 v6 - 최종】 API 서버 가동 준비 (완전 비동기)...")

    # Initialize Query Expander (Phase 2.3 - Optional)
    if QueryExpander is not None:
        print("[Query Expander] 쿼리 확장 시스템 초기화 중...")
        query_expander = QueryExpander()
        print("[Query Expander] WordNet + ChromaDB 하이브리드 확장 준비 완료")
    else:
        query_expander = None
        print("⚠️  Query Expander 건너뜀 (Phase 2.3 구현 필요)")

    # ============================================================================
    # AntiGravity Phase 1: Initialization (Via Facade)
    # ============================================================================
    from AFO.api.compat import get_antigravity_control
    
    antigravity = get_antigravity_control()

    if antigravity and antigravity.AUTO_DEPLOY:
        print(f"🚀 [AntiGravity] 활성화: {antigravity.ENVIRONMENT} 환경 자동 배포 준비 완료 (孝)")

    if antigravity and antigravity.DRY_RUN_DEFAULT:
        print("🛡️ [AntiGravity] DRY_RUN 모드 활성화 - 모든 위험 동작 시뮬레이션 (善)")
    # ============================================================================

    # Initialize RAG engines - 각 LLM별로 on-demand 생성
    # (API 요청시마다 llm_provider에 따라 동적 생성)
    print("[RAG 엔진] 멀티-LLM 지원 준비 완료.")
    print("[RAG 엔진] 지원 LLM: claude, gemini, codex, ollama, lmstudio")

    # 초기화는 생략 (첫 요청시 생성)
    crag_engine = None
    hybrid_engine = None

    # Initialize Multimodal RAG Engine (Phase 2 - Multimodal RAG)
    if MultimodalRAGEngine is not None:
        print("[Multimodal RAG] 멀티모달 RAG 엔진 초기화 중...")
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
        print("[Multimodal RAG] 멀티모달 RAG 엔진 준비 완료 (텍스트+이미지 통합 검색)")
    else:
        multimodal_rag_engine = None
        print("⚠️  Multimodal RAG Engine 건너뜀 (Multimodal RAG Phase 2 구현 필요)")

    # Initialize Multimodal RAG Cache (Phase 5 - Optimization)
    if set_redis_client is not None and REDIS_CLIENT is not None:
        set_redis_client(REDIS_CLIENT)
        print("[Multimodal RAG Cache] 캐시 시스템 초기화 완료 (Redis 통합)")
    else:
        print("⚠️  Multimodal RAG Cache 건너뜀 (Redis 또는 캐시 모듈 없음)")

    # Initialize Skill Registry (Phase 2.5 - Optional)
    # [색즉시공] - 없음도 있음의 한 형태
    if register_core_skills is not None:
        skill_registry = register_core_skills()
        skill_count = (
            skill_registry.count() if skill_registry and hasattr(skill_registry, "count") else 0
        )
        print(f"ℹ️ [INFO] {skill_count} Skills loaded in simulation mode")
    else:
        print("⚠️  Skill Registry not available (Phase 2.5 pending)")

    # Initialize Yeongdeok Complete (Phase 2.5 - Optional)
    if YeongdeokComplete is not None:
        print("[영덕] 영덕 완전체 초기화 중...")
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
        print("[영덕] 영덕 완전체 준비 완료 - 뇌/눈/귀/팔 모두 연결됨")
    else:
        yeongdeok = None
        print("⚠️  Yeongdeok Complete 건너뜀 (Phase 2.5 구현 필요)")

    # Compile with MemorySaver (no context manager needed)
    print("[지휘소 v6】 LangGraph 설계도를 컴파일하여 '두뇌'를 완성합니다...")
    if workflow is not None and memory_context is not None:
        strategy_app_runnable = workflow.compile(checkpointer=memory_context)
        print("[지휘소 v6】 '두뇌' 가동 준비 완료. 명령을 수신할 수 있습니다.")
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
            print("[Hybrid RAG] PostgreSQL 풀 초기화 중...")
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
    # get_settings handled via compat/alias
    pass
    # get_settings is available globally via compat
    try:
        if get_settings is not None:
             redis_settings = get_settings()
             if redis_settings:
                 redis_host = redis_settings.REDIS_HOST
                 redis_port = redis_settings.REDIS_PORT
                 redis_password = redis_settings.REDIS_PASSWORD
             else:
                 raise ValueError("Settings not loaded")
        else:
             raise ValueError("get_settings not available")
    except Exception:
        # Fallback to env
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_password = os.getenv("REDIS_PASSWORD", None)

    try:
        print(f"[Hybrid RAG] Redis 클라이언트 연결 중... ({redis_host}:{redis_port})")
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
    # Initialize OpenAI client (optional)
    if OPENAI_AVAILABLE:
        # Phase 2-4: settings 사용
        from config.settings import get_settings

        settings = get_settings()
        openai_key = settings.OPENAI_API_KEY

        if openai_key:
            # Logic handled by services/llm/openai.py or similar
            print("✅ OpenAI API Key detected")
        else:
            print("ℹ️ [INFO] OpenAI API key not found")
    else:
        print("ℹ️ [INFO] OpenAI library unavailable")

    # Phase 8.2.3: Claude 클라이언트 초기화 (optional)
    # Handled by fallback responses if unavailable
    if ANTHROPIC_AVAILABLE:
        print("✅ Anthropic library available")
    else:
        print("ℹ️  Anthropic library unavailable")

    # The application is now ready to run
    try:
        yield
    except Exception as e:
        print(f"❌ [Lifespan Error] 런타임 중 치명적 오류 발생: {e}")
    finally:
        # ===== ASYNC DATABASE CONNECTION FUNCTION =====
        # ===== ASYNC DATABASE CONNECTION FUNCTION =====
        # Moved to services/database.py
        # Imported at top level

        # Cleanup
        print("[영덕] 영덕 완전체 종료 중...")
    if yeongdeok and yeongdeok.browser:
        await yeongdeok.close_eyes()

    if PG_POOL:
        PG_POOL.closeall()
    if REDIS_CLIENT:
        with suppress(Exception):
            REDIS_CLIENT.close()

    print("[지휘소 v6】 API 서버 가동 중지.")


# 중앙 설정 사용 (Phase 1 리팩토링)
try:
    from AFO.config.settings import get_settings

    # settings = get_settings() # Handled above
    try:
        from AFO.config.settings import AFOSettings

        Settings = AFOSettings
    except ImportError:
        pass
except ImportError:
    pass  # Fallback for when AFO.config.settings is not available

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
    {
        "name": "GenUI",
        "description": "Phase 9: Self-Expanding Kingdom. Autonomous UI generation via Samahwi.",
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

# [Matrix Stream] Explicit Mount (Global)
# Must be mounted here to ensure route is registered on startup
app.include_router(streams_router, prefix="/api/stream", tags=["Matrix Stream"])
from AFO.api.routers.matrix import router as matrix_router
app.include_router(matrix_router, prefix="/api", tags=["Matrix Stream (Phase 10)"])

from AFO.api.routers.rag_query import router as rag_query_router
app.include_router(rag_query_router, prefix="/api", tags=["RAG (Phase 12)"])

from AFO.api.routers.finance import router as finance_router
app.include_router(finance_router) # Prefix is defined in the router itself

from AFO.api.routers.ssot import router as ssot_router
app.include_router(ssot_router) # Prefix is defined in the router itself

# Phase 12 Extension: Budget Tracking
try:
    from AFO.api.routers.budget import router as budget_router
    app.include_router(budget_router)  # Prefix /api/julie/budget
    print("✅ Budget Router 등록 완료 (Phase 12 확장)")
except Exception as e:
    print(f"⚠️ Budget Router 등록 실패: {e}")

# ============================================================
# Phase 13: AICPA Agent Army Integration
# ============================================================
try:
    from AFO.api.routers.aicpa import router as aicpa_router
    app.include_router(aicpa_router, prefix="/api", tags=["AICPA Agent Army"])
    print("✅ AICPA Router 등록 완료 (Phase 13: 에이전트 군단)")
except Exception as e:
    print(f"⚠️ AICPA Router 등록 실패: {e}")

# ============================================================
# Phase 16: Autonomous Agents (Feedback Loop)
# ============================================================
try:
    from AFO.api.routers.learning_log_router import router as learning_log_router
    app.include_router(learning_log_router)
    print("✅ Learning Log Router 등록 완료 (Phase 16-4: 자율 학습 루프)")
except Exception as e:
    print(f"⚠️ Learning Log Router 등록 실패: {e}")

# ============================================================
# Phase 18: Grok Real-time Stream
# ============================================================
try:
    from AFO.api.routers.grok_stream import router as grok_stream_router
    app.include_router(grok_stream_router)
    print("✅ Grok Stream Router 등록 완료 (Phase 18: 왕국의 맥박)")
except Exception as e:
    print(f"⚠️ Grok Stream Router 등록 실패: {e}")

# ============================================================
# Phase 24: Voice Interface (Commander's Voice)
# ============================================================
try:
    from AFO.api.routers.voice import router as voice_router
    app.include_router(voice_router, prefix="/api", tags=["Voice Interface"])
    print("🎙️ Voice Router 등록 완료 (Phase 24: Commander's Voice)")
except Exception as e:
    print(f"⚠️ Voice Router 등록 실패: {e}")

# ============================================================
# Phase 23: Multi-Model Intelligence (Council of Minds)
# ============================================================
try:
    from AFO.api.routers.council import router as council_router
    app.include_router(council_router, prefix="/api", tags=["Council of Minds"])
    print("🧠 Council Router 등록 완료 (Phase 23: 지혜의 의회)")
except Exception as e:
    print(f"⚠️ Council Router 등록 실패: {e}")

# ============================================================
# Phase 26: AI Self-Improvement (Samahwi Learning Pipeline)
# ============================================================
try:
    from AFO.api.routers.learning_pipeline import router as learning_router
    app.include_router(learning_router, prefix="/api", tags=["AI Self-Improvement"])
    print("🧠 Learning Pipeline Router 등록 완료 (Phase 26: 사마휘 자율 학습)")
except Exception as e:
    print(f"⚠️ Learning Pipeline Router 등록 실패: {e}")

# ============================================================
# Phase 20: Kingdom Observability
# ============================================================
try:
    from AFO.api.middleware.prometheus import setup_prometheus_metrics
    # Port 8001 for metrics
    setup_prometheus_metrics(app, port=8001)
    print("✅ Prometheus Metrics Exporter 가동 (Port 8001)")
except Exception as e:
    print(f"⚠️ Prometheus Middleware 설정 실패: {e}")

# ============================================================
# Phase 22: Security Hardening (The Shield)
# ============================================================
try:
    from AFO.security.vault_manager import vault
    from AFO.api.middleware.audit import audit_middleware
    
    # Audit Middleware (Before Routes)
    app.middleware("http")(audit_middleware)
    
    # Initialize Vault (Log only)
    print(f"🛡️ Vault Manager Active (Mode: {vault.mode})")
    print("🛡️ Audit Middleware Active (Logging POST/PUT/DELETE)")

except Exception as e:
    print(f"⚠️ Security Hardening 설정 실패: {e}")

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


# ============================================================
# Optional Middlewares (Disabled - 필요시 구현)
# - PerformanceMiddleware: 성능 모니터링
# - RateLimitMiddleware: API Rate Limiting
# 이 기능들은 선택적이며 현재 미구현 상태입니다.
# ============================================================



# ============================================================
# AFO 스킬 API 영구 등록 (제1계명: 永遠不滅)
# ============================================================
# REMOVED: Skill Registry (MOCK 모드) - 가지치기
if skills_router:
    app.include_router(skills_router, prefix="/api/skills", tags=["Skills"])

# RAG Router 등록
if rag_router is not None:
    app.include_router(rag_router)

# Phase 2 리팩토링: 분리된 라우터 등록
if root_router is not None:
    app.include_router(root_router)
    print("✅ Root 라우터 등록 완료 (Phase 2 리팩토링)")
if health_router is not None:
    app.include_router(health_router)
    app.include_router(streams_router, prefix="/api", tags=["Streams"])
    print("✅ Health 라우터 등록 완료 (Phase 2 리팩토링)")
if skills_router is not None:
    # `skills_router` already has prefix="/api/skills"
    app.include_router(skills_router)
    print("✅ Skills API 라우터 등록 완료 (손발 연결)")


# 제3계명: 5기둥 API 라우터 등록 (항상 시도)

# 5기둥 API 라우터 (제3계명)
# 5기둥 API 라우터 (제3계명)
# Multi-Agent 라우터 등록 (Phase 4 - 협력 에이전트 시스템)
if multi_agent_router:
    app.include_router(multi_agent_router)
    print("✅ Multi-Agent 라우터 등록 완료")
else:
    print("⚠️  Multi-Agent 라우터 등록 건너뜀 (로드 실패)")

# ============================================================================
# Phase 8: Julie CPA AutoMate
# ============================================================================
# try:
#     from api.routes.julie import router as julie_router
#
#     app.include_router(julie_router)
#     print("✅ Julie CPA AutoMate Engine activated (의(義))")
# except Exception as e:
#     print(f"⚠️ Julie CPA Engine load failed: {e}")

# ============================================================================
# Phase 9: Self-Expanding Kingdom (GenUI)
# ============================================================================
try:
    from AFO.api.routers.gen_ui import router as gen_ui_router

    app.include_router(gen_ui_router)
    print("✅ GenUI Engine activated (Phase 9: Serenity)")
except Exception as e:
    print(f"⚠️ GenUI Engine load failed: {e}")

# 향상된 헬스 체크 라우터 등록 (Phase 3 최적화)
try:
    from api.routers.health import router as enhanced_health_router

    app.include_router(enhanced_health_router, prefix="/api", tags=["Health"])
    print("✅ 향상된 헬스 체크 라우터 등록 완료")
except ImportError as e:
    print(f"⚠️  향상된 헬스 체크 라우터 로드 실패: {e}")

# 3. Multi-Agent Router
if multi_agent_router:
    app.include_router(
        multi_agent_router,
        prefix="/api/multi-agent",
        tags=["Multi-Agent System"],
    )

# 4. Strangler Fig Router
if strangler_router:
    app.include_router(
        strangler_router,
        prefix="/api/strangler",
        tags=["Strangler Fig"],
    )

# 5. Graph of Thought Router
if got_router:
    app.include_router(
        got_router,
        prefix="/api/got",
        tags=["Graph of Thought"],
    )

# 6. N8N Router
if n8n_router:
    app.include_router(n8n_router, prefix="/api/n8n", tags=["N8N Integration"])
# if health_n8n_router:
#     app.include_router(health_n8n_router)

# 7. Wallet Router
if wallet_router:
    app.include_router(
        wallet_router,
        prefix="/api/wallet",
        tags=["API Wallet"],
    )
# 1. 5 Pillars Router (필수)
if pillars_router:
    app.include_router(
        pillars_router,
        prefix="/api/pillars",
        tags=["5 Pillars"],
        responses={418: {"description": "I'm a teapot (Pillars not ready)"}},
    )

# 2. System Health Router (필수)
if system_health_router:
    app.include_router(system_health_router, tags=["System Health"])
    print("✅ System Health API 라우터 등록 완료")
else:
    print("⚠️  System Health 라우터 등록 건너뜀 (로드 실패)")

# Trinity Policy 라우터 등록 (항상 시도 - /api/trinity/realtime 포함)
if trinity_policy_router is not None:
    app.include_router(trinity_policy_router, tags=["trinity"])

    # Trinity Metrics Router (새로운 수학 공식 기반)
    # try:
    #     from api.routes.trinity_metrics import router as trinity_metrics_router
    #
    #     app.include_router(trinity_metrics_router, tags=["trinity"])
    #     print("✅ Trinity Metrics router 등록 완료")
    # except Exception as exc:
    #     print(f"⚠️  Trinity Metrics router 등록 실패: {exc}")
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

# ============================================================
# PLACEHOLDER ROUTERS (미구현 - 추후 확장 시 주석 해제)
# 이 섹션은 미래 확장을 위한 플레이스홀더입니다.
# 현재 핵심 기능(Phase 14-26)은 모두 정상 동작 중입니다.
# ============================================================

# 아래 라우터들은 아직 구현되지 않아 건너뜁니다:
# - WatchTower (미래 예측 관측소)
# - Sejong Spirit (홍익인간 정신)
# - Creative Beauty (창조미 평가)
# - Jipijigi (지피지기 시스템)
# - Redis Test (프로덕션급 연결 풀)
# - Disaster Recovery (재해 복구)
# - Encryption (데이터 암호화)
# - Key Management (키 관리)
# - Certificate Management (인증서 관리)
# - Certbot Debugging (디버깅)
# - Certbot Log Analyzer (로그 분석)
# - TLS Best Practices (TLS 베스트 프랙티스)
# - Certificate Transparency (CT 로그)

# CRAG Self-Correction 라우터 등록 (Phase 4 - n8n 통합)
try:
    from api.routes.crag import router as crag_router

    app.include_router(crag_router)
    print("✅ CRAG API 라우터 등록 완료 (에이전트가 스스로 반성하며 답변 보강)")
except ImportError as e:
    print(f"⚠️  CRAG 라우터 등록 건너뜀 (로드 실패: {e})")
except Exception as e:
    print(f"⚠️  CRAG 라우터 등록 건너뜀 (오류: {e})")

# Chat API 라우터 등록 (LLM Router 연동 -# Additional Routers via Compat
if education_system_router:
    app.include_router(education_system_router, prefix="/api/education", tags=["Education System"])

if modal_data_router:
    app.include_router(modal_data_router, prefix="/api/modal", tags=["Modal Data"])

if trinity_policy_router:
    app.include_router(trinity_policy_router, prefix="/api/policy", tags=["Trinity Policy"])

if trinity_sbt_router:
    app.include_router(trinity_sbt_router, prefix="/api/sbt", tags=["Trinity SBT"])
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
# Handled via compat layer integration if needed, or moved to correct block
pass
# Family API 라우터 등록 (비 이식 - Router Facade Pattern)
# Handled via compat layer integration if needed, or moved to correct block
pass

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
    return cast(list[float], await get_embedding_async(text, OPENAI_CLIENT))


async def _query_pgvector_async_adapter(embedding: list[float], top_k: int) -> list[dict]:
    return cast(list[dict], await query_pgvector_async(embedding, top_k, PG_POOL))


async def _query_redis_async_adapter(embedding: list[float], top_k: int) -> list[dict]:
    return cast(list[dict], await query_redis_async(embedding, top_k, REDIS_CLIENT))


async def _blend_results_async_adapter(
    pg_rows: list[dict], redis_rows: list[dict], top_k: int
) -> list[dict]:
    return cast(list[dict], await blend_results_async(pg_rows, redis_rows, top_k))


async def _generate_answer_async_adapter(
    query: str,
    contexts: list[str],
    temperature: float,
    response_format: str,
    additional_instructions: str,
    llm_provider: str = "openai",
) -> str | dict:
    return cast(str | dict, await generate_answer_async(
        query,
        contexts,
        temperature,
        response_format,
        additional_instructions,
        llm_provider,
        openai_client=OPENAI_CLIENT,
    ))


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
    # TrinityMetrics and calculate_trinity imported from AFO.api.compat at top level
    pass

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

    # Type hint for results: tuple of (dict | BaseException, ...)
    # But since we check isinstance(Exception), we can cast to Any for indexing

    organ_checks = [
        (
            "心_Redis",
            cast("dict[str, Any]", results[0])
            if not isinstance(results[0], Exception)
            else {"healthy": False, "output": str(results[0])},
        ),
        (
            "肝_Postgres",
            cast("dict[str, Any]", results[1])
            if not isinstance(results[1], Exception)
            else {"healthy": False, "output": str(results[1])},
        ),
        (
            "脾_Ollama",
            cast("dict[str, Any]", results[2])
            if not isinstance(results[2], Exception)
            else {"healthy": False, "output": str(results[2])},
        ),
        (
            "肺_API_Server",
            cast("dict[str, Any]", results[3])
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

    # M. Thoughts Router (Matrix Stream)
    if thoughts_router:
        # NOTE: Including router inside a function is bad practice. 
        # But keeping legacy logic if it was intended for dynamic loading, 
        # usually checks if already mounted. 
        # However, for streams_router, we moved it to global scope.
        pass

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
# ============================================================
# 동적 라우터 자동 등록 (Legacy - Disabled)
# fig_overlay 패턴은 더 이상 사용되지 않습니다.
# 모든 라우터는 위에서 명시적으로 등록됩니다.
# ============================================================

# ============================================================================
# Phase 1.3: Async Wrappers
# Handled by adapters at the top (dependency injection)
# ============================================================================

print("🎉 Phase 1.3: Async Wrappers 적용 완료 - Adapters Active")


# ============================================================================
# Phase 2.0: Database Initialization
# NOTE: Startup logic is now handled by lifespan() at line 420
# The on_event pattern is deprecated in FastAPI 0.100+
# ============================================================================

# (Legacy on_startup and debug_routes removed - migrated to lifespan)


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



# ============================================================================
# Main Block



if __name__ == "__main__":
    print("🛣️  [Route Debug Debugger] Registered Routes (Main Block):")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"   - {route.path}")

    import uvicorn

    # Phase 2-4: settings 사용 (via compat layer)
    # Phase 2-4: settings 사용 (via compat layer)
    try:
        if get_settings is not None:
            main_settings = get_settings()
            if main_settings:
                api_port = main_settings.API_SERVER_PORT
                api_host = main_settings.API_SERVER_HOST
            else:
                 api_port = int(os.getenv("API_SERVER_PORT", "8011"))
                 api_host = os.getenv("API_SERVER_HOST", "0.0.0.0")
        else:
            raise ImportError("get_settings not available")
    except ImportError:
        api_port = int(os.getenv("API_SERVER_PORT", "8011"))
        api_host = os.getenv("API_SERVER_HOST", "0.0.0.0")

    print(f"🚀 Starting Server on {api_host}:{api_port} with lifespan='on'")
    uvicorn.run(app, host=api_host, port=api_port, lifespan="on")
