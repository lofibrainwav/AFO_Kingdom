# Trinity Score: 90.0 (Established by Chancellor)
"""
AFO Kingdom System Initialization

Handles system component initialization during FastAPI lifespan startup.
"""

import asyncio
import logging
from typing import Any, cast

logger = logging.getLogger(__name__)

# Global state variables (will be moved to proper state management later)
strategy_app_runnable = None
crag_engine = None
hybrid_engine = None
yeongdeok = None
query_expander = None
skill_registry = None
multimodal_rag_engine = None

# Database connections
PG_POOL = None
REDIS_CLIENT = None
OPENAI_CLIENT = None
CLAUDE_CLIENT = None

# Neural event queue
neural_event_queue: asyncio.Queue[Any] = asyncio.Queue()


async def initialize_system() -> None:
    """Initialize all AFO Kingdom system components."""
    print("[지휘소 v6 - 최종】 API 서버 가동 준비 (완전 비동기)...")

    try:
        # Initialize Query Expander
        await _initialize_query_expander()

        # Initialize AntiGravity controls
        await _initialize_antigravity()

        # Initialize Database Connections (Redis needed for RAG cache)
        await _initialize_databases()

        # Initialize RAG engines
        await _initialize_rag_engines()

        # Initialize Multimodal RAG
        await _initialize_multimodal_rag()

        # Initialize Skills Registry
        await _initialize_skills_registry()

        # Initialize Yeongdeok Memory System
        await _initialize_yeongdeok()

        # Initialize Strategy Engine
        await _initialize_strategy_engine()

        # Initialize LLM Clients
        await _initialize_llm_clients()

        print("[지휘소 v6】 '진정한 두뇌' (Chancellor Graph) 가동 준비 완료. (True Intelligence)")

    except Exception as e:
        logger.error(f"System initialization failed: {e}")
        raise


async def _initialize_query_expander() -> None:
    """Initialize Query Expander system."""
    global query_expander

    try:
        from query_expansion_advanced import QueryExpander as _QE

        query_expander = _QE()
        print("[Query Expander] WordNet + ChromaDB 하이브리드 확장 준비 완료")
    except ImportError:
        query_expander = None
        print("⚠️ Query Expander 건너뜀 (Phase 2.3 구현 필요)")


async def _initialize_antigravity() -> None:
    """Initialize AntiGravity system controls."""
    try:
        from AFO.api.compat import get_antigravity_control

        antigravity = get_antigravity_control()

        if antigravity and antigravity.AUTO_DEPLOY:
            print(
                f"🚀 [AntiGravity] 활성화: {antigravity.ENVIRONMENT} 환경 자동 배포 준비 완료 (孝)"
            )

        if antigravity and antigravity.DRY_RUN_DEFAULT:
            print("🛡️ [AntiGravity] DRY_RUN 모드 활성화 - 모든 위험 동작 시뮬레이션 (善)")
    except Exception as e:
        print(f"⚠️ AntiGravity 초기화 실패: {e}")


async def _initialize_rag_engines() -> None:
    """Initialize RAG engine components."""
    global crag_engine, hybrid_engine

    print("[RAG 엔진] 멀티-LLM 지원 준비 완료.")
    print("[RAG 엔진] 지원 LLM: claude, gemini, codex, ollama, lmstudio")

    # Initialize as None - will be created on-demand
    crag_engine = None
    hybrid_engine = None


async def _initialize_multimodal_rag() -> None:
    """Initialize Multimodal RAG engine."""
    global multimodal_rag_engine

    try:
        from AFO.api.compat import get_settings_safe
        from multimodal_rag_engine import MultimodalRAGEngine as _MRAE

        settings = get_settings_safe()
        mock_mode = getattr(settings, "MOCK_MODE", True) if settings else True

        multimodal_rag_engine = _MRAE(
            vectorstore=None,  # 벡터 DB는 나중에 통합 가능
            llm_provider="openai",  # 기본값: OpenAI GPT-4V
            use_reranking=False,  # Phase 3에서 활성화
            mock_mode=mock_mode,
        )
        print("[Multimodal RAG] 멀티모달 RAG 엔진 준비 완료 (텍스트+이미지 통합 검색)")
    except ImportError:
        multimodal_rag_engine = None
        print("⚠️ Multimodal RAG Engine 건너뜀 (Multimodal RAG Phase 2 구현 필요)")

    # Initialize Multimodal RAG Cache
    try:
        print(f"🔍 Multimodal RAG Cache 초기화 시도... REDIS_CLIENT: {REDIS_CLIENT is not None}")
        from multimodal_rag_cache import set_redis_client as _src

        print("✅ Multimodal RAG Cache 모듈 import 성공")

        if REDIS_CLIENT:
            _src(REDIS_CLIENT)  # type: ignore[unreachable]
            print("✅ [Multimodal RAG Cache] 캐시 시스템 초기화 완료 (Redis 통합)")
        else:
            print("⚠️ Multimodal RAG Cache 건너뜀 (Redis 클라이언트 없음)")
    except ImportError as e:
        print(f"⚠️ Multimodal RAG Cache 건너뜀 (모듈 import 실패: {e})")
    except Exception as e:
        print(f"⚠️ Multimodal RAG Cache 건너뜀 (초기화 실패: {e})")


async def _initialize_skills_registry() -> None:
    """Initialize Skills Registry system."""
    global skill_registry

    try:
        from afo_skills_registry import register_core_skills as _rcs

        skill_registry = _rcs()
        skill_count = (
            skill_registry.count() if skill_registry and hasattr(skill_registry, "count") else 0
        )
        print(f"ℹ️ [INFO] {skill_count} Skills loaded in simulation mode")
    except ImportError:
        print("⚠️ Skill Registry not available (Phase 2.5 pending)")


async def _initialize_yeongdeok() -> None:
    """Initialize Yeongdeok Complete memory system."""
    global yeongdeok

    try:
        from AFO.api.compat import get_settings_safe
        from AFO.memory_system.yeongdeok_complete import YeongdeokComplete as _YC

        settings = get_settings_safe()
        n8n_url = getattr(settings, "N8N_URL", "") if settings else ""
        n8n_key = getattr(settings, "API_YUNGDEOK", "") if settings else ""

        yeongdeok = _YC(
            n8n_url=n8n_url,
            n8n_api_key=n8n_key,
            enable_llm_brain=False,  # LLM 없어도 작동 (RAG Memory만 사용)
            neural_event_queue=neural_event_queue,  # 신경 흐름 이벤트 큐 연결
        )
        print("[영덕] 영덕 완전체 준비 완료 - 뇌/눈/귀/팔 모두 연결됨")
    except ImportError:
        try:
            from memory_system.yeongdeok_complete import YeongdeokComplete as _YC_FB

            yeongdeok = _YC_FB(
                n8n_url="",
                n8n_api_key="",
                enable_llm_brain=False,
                neural_event_queue=neural_event_queue,
            )
            print("[영덕] 영덕 완전체 준비 완료 (fallback) - 뇌/눈/귀/팔 모두 연결됨")
        except ImportError:
            yeongdeok = None
            print("⚠️ Yeongdeok Complete 건너뜀 (Phase 2.5 구현 필요)")


async def _initialize_strategy_engine() -> None:
    """Initialize Strategy Engine and LangGraph."""
    global strategy_app_runnable

    print("[지휘소 v6】 LangGraph 설계도를 컴파일하여 '두뇌'를 완성합니다...")

    try:
        # Try Real Brain (Chancellor Graph)
        # Use SSOT: AFO/chancellor_graph.py
        try:
            from AFO.chancellor_graph import chancellor_graph
        except ImportError:
            # Fallback to legacy path for backward compatibility
            import sys
            from pathlib import Path

            _CORE_ROOT = Path(__file__).resolve().parent.parent
            if str(_CORE_ROOT) not in sys.path:
                sys.path.insert(0, str(_CORE_ROOT))
            from chancellor_graph import chancellor_graph

        strategy_app_runnable = chancellor_graph
        print("[지휘소 v6】 '진정한 두뇌' (Chancellor Graph) 가동 준비 완료. (True Intelligence)")
    except ImportError:
        # Fallback to Workflow Mock Compilation
        try:
            from strategy_engine import memory_context as _mc
            from strategy_engine import workflow as _wf

            if _wf and _mc:
                strategy_app_runnable = cast("Any", _wf).compile(checkpointer=_mc)
                print("[지휘소 v6】 '두뇌' (Mock) 가동 준비 완료.")
            else:
                strategy_app_runnable = None
                print("⚠️ Strategy workflow 또는 memory_context 없음 - LangGraph 컴파일 건너뜀")
        except (ImportError, AttributeError):
            strategy_app_runnable = None
            print("⚠️ LangGraph compilation failed - running in degraded mode")


async def _initialize_databases() -> None:
    """Initialize database connections."""
    global PG_POOL, REDIS_CLIENT

    from AFO.api.compat import get_settings_safe

    settings = get_settings_safe()
    if not settings:
        print("⚠️ Settings not available - database initialization skipped")
        return

    # PostgreSQL connection
    try:
        from psycopg2.pool import SimpleConnectionPool

        pg_host = getattr(settings, "POSTGRES_HOST", "localhost")
        pg_port = getattr(settings, "POSTGRES_PORT", 15432)
        pg_db = getattr(settings, "POSTGRES_DB", "afo_memory")
        pg_user = getattr(settings, "POSTGRES_USER", "afo")
        pg_password = getattr(settings, "POSTGRES_PASSWORD", "afo_secret_change_me")

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
        print(f"⚠️ PostgreSQL 연결 실패: {e}")

    # Redis connection
    try:
        import redis

        redis_host = getattr(settings, "REDIS_HOST", "localhost")
        redis_port = getattr(settings, "REDIS_PORT", 6379)
        redis_password = getattr(settings, "REDIS_PASSWORD", None)

        REDIS_CLIENT = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=2,
        )
        REDIS_CLIENT.ping()
        print(f"✅ Redis 연결 성공 ({redis_host}:{redis_port})")
    except Exception as e:
        REDIS_CLIENT = None
        print(f"⚠️ Redis 연결 실패: {e}")


async def _initialize_llm_clients() -> None:
    """Initialize LLM client connections."""
    global OPENAI_CLIENT, CLAUDE_CLIENT

    from AFO.api.compat import ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE, get_settings_safe

    settings = get_settings_safe()

    # OpenAI client
    if OPENAI_AVAILABLE and settings:
        openai_key = getattr(settings, "OPENAI_API_KEY", None)
        if openai_key:
            print("✅ OpenAI API Key detected")
        else:
            print("ℹ️ [INFO] OpenAI API key not found")

    # Anthropic client
    if ANTHROPIC_AVAILABLE:
        print("✅ Anthropic library available")
    else:
        print("ℹ️ Anthropic library unavailable")
