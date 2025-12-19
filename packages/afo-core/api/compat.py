"""
AFO API Compatibility Layer (Strangler Fig Support)
--------------------------------------------------
Centralizes all complex import logic, fallbacks, and optional dependencies
to keep api_server.py clean and type-safe.

Part of the 'Zero Defect' initiative (Kingdom Architect).
"""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter

logger = logging.getLogger(__name__)

# --- Type Stubs ---
if TYPE_CHECKING:
    from AFO.config.settings import AFOSettings
    from AFO.domain.metrics.trinity import TrinityMetrics as TrinityMetricsType

    # Define exact types for things we import
    SettingsType = AFOSettings
else:
    SettingsType = Any
    TrinityMetricsType = Any

# --- Helper Functions ---


def _fallback_router(name: str, exc: Exception, essential: bool = False) -> APIRouter:
    """Return an empty router when optional imports fail."""
    print(f"⚠️  {name} router not available: {exc}")
    # In compat layer, we just return empty router and maybe log
    return APIRouter()


# --- Lazy Import Flags ---

OPENAI_AVAILABLE = False
CREWAI_AVAILABLE = False
LANGCHAIN_AVAILABLE = False
ANTHROPIC_AVAILABLE = False
CHROMADB_AVAILABLE = False
QDRANT_AVAILABLE = False
PGVECTOR_AVAILABLE = False
PSYCOPG2_AVAILABLE = False
SSE_AVAILABLE = False

try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    pass

try:
    import crewai

    CREWAI_AVAILABLE = True
except ImportError:
    pass

try:
    import langchain

    LANGCHAIN_AVAILABLE = True
except ImportError:
    pass

try:
    import anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

# --- Router Imports (Single Assignment Pattern) ---

# 1. 5 Pillars Router
pillars_router: APIRouter | None = None
try:
    from AFO.api.routes.five_pillars import router as _pillars_1

    pillars_router = _pillars_1
except ImportError:
    try:
        from api.routes.five_pillars import router as _pillars_2

        pillars_router = _pillars_2
    except ImportError:
        pillars_router = _fallback_router("5 Pillars", ImportError("Not found"))

# 2. System Health Router
system_health_router: APIRouter | None = None
try:
    from afo_soul_engine.api.routes.system_health import router as _sys_health_1

    system_health_router = _sys_health_1
except ImportError:
    try:
        from AFO.api.routes.system_health import router as _sys_health_2

        system_health_router = _sys_health_2
    except ImportError:
        try:
            from api.routes.system_health import router as _sys_health_3

            system_health_router = _sys_health_3
        except ImportError:
            system_health_router = _fallback_router("System Health", ImportError("Not found"))

# 3. Strangler Fig Router
strangler_router: APIRouter | None = None
try:
    from afo_soul_engine.api.routes.strangler import router as _strangler_1

    strangler_router = _strangler_1
except ImportError:
    try:
        from AFO.api.routes.strangler import router as _strangler_2

        strangler_router = _strangler_2
    except ImportError:
        strangler_router = _fallback_router("Strangler Fig", ImportError("Not found"))

# 4. Graph of Thought Router
got_router: APIRouter | None = None
try:
    from afo_soul_engine.api.routes.got import router as _got_1

    got_router = _got_1
except ImportError:
    try:
        from AFO.api.routes.got import router as _got_2

        got_router = _got_2
    except ImportError:
        got_router = _fallback_router("Graph-of-Thought", ImportError("Not found"))

# 5. N8N Router
n8n_router: APIRouter | None = None
health_n8n_router: APIRouter | None = None
try:
    from afo_soul_engine.api.routes.n8n import health_n8n_router as _n8n_health_1
    from afo_soul_engine.api.routes.n8n import n8n_router as _n8n_1

    health_n8n_router = _n8n_health_1
    n8n_router = _n8n_1
except ImportError:
    try:
        from AFO.api.routes.n8n import health_n8n_router as _n8n_health_2
        from AFO.api.routes.n8n import n8n_router as _n8n_2

        health_n8n_router = _n8n_health_2
        n8n_router = _n8n_2
    except ImportError:
        n8n_router = _fallback_router("N8N", ImportError("Not found"))
        health_n8n_router = _fallback_router("N8N Health", ImportError("Not found"))

# 6. Wallet Router
wallet_router: APIRouter | None = None
try:
    from afo_soul_engine.api.routes.wallet import wallet_router as _wallet_1

    wallet_router = _wallet_1
except ImportError:
    try:
        from AFO.api.routes.wallet import wallet_router as _wallet_2

        wallet_router = _wallet_2
    except ImportError:
        wallet_router = _fallback_router("Wallet", ImportError("Not found"))

# 7. Ragas Router
ragas_router: APIRouter | None = None
try:
    from AFO.api.routes.ragas import ragas_router as _ragas_1

    ragas_router = _ragas_1
except ImportError:
    ragas_router = _fallback_router("Ragas", ImportError("Not found"))

# 8. RAG Router
rag_router: APIRouter | None = None
try:
    from AFO.api.routes.rag import rag_router as _rag_1

    rag_router = _rag_1
except ImportError:
    rag_router = _fallback_router("RAG", ImportError("Not found"))

# 9. Multi-Agent Router
multi_agent_router: APIRouter | None = None
try:
    from AFO.api.routes.multi_agent import router as _multi_agent_1

    multi_agent_router = _multi_agent_1
except ImportError:
    multi_agent_router = _fallback_router("Multi-Agent", ImportError("Not found"))

# 10. Skills Router
skills_router: APIRouter | None = None
try:
    from AFO.api.routes.skills import router as _skills_1

    skills_router = _skills_1
except ImportError:
    try:
        from afo_soul_engine.api.routes.skills import router as _skills_2

        skills_router = _skills_2
    except ImportError:
        skills_router = _fallback_router("Skills", ImportError("Not found"))

# 11. Legacy/Optional Routers (Direct Imports if available, else fallback)
# These usually have simpler paths or are less critical
try:
    from AFO.api.routes.deployment import router as deployment_router
except ImportError as exc:
    deployment_router = _fallback_router("Deployment", exc)

try:
    from AFO.api.routes.langgraph_router import router as twin_dragon_router
except ImportError as exc:
    twin_dragon_router = _fallback_router("Twin Dragon", exc)

try:
    from AFO.api.routes.langgraph_tutor import router as langgraph_tutor_router
except ImportError as exc:
    langgraph_tutor_router = _fallback_router("LangGraph Tutor", exc)  # type: ignore[assignment]

try:
    from AFO.api.routes.crewai import router as crewai_router
except ImportError as exc:
    crewai_router = _fallback_router("CrewAI", exc)  # type: ignore[assignment]

try:
    from AFO.api.routes.llm_router import router as llm_router_api
except ImportError as exc:
    llm_router_api = _fallback_router("LLM Router", exc)  # type: ignore[assignment]

try:
    from AFO.api.routers.users import router as users_router
except ImportError as exc:
    users_router = _fallback_router("Users", exc)

try:
    from AFO.api.routers.auth import router as auth_router
except ImportError as exc:
    auth_router = _fallback_router("Auth", exc)

try:
    from AFO.api.routers.trinity_router import router as trinity_router
except ImportError as exc:
    trinity_router = _fallback_router("Trinity Facade", exc)

try:
    from AFO.api.routes.rag_advanced import router as rag_advanced_router
except ImportError as exc:
    rag_advanced_router = _fallback_router("Advanced RAG", exc)

try:
    from AFO.api.routers.education_system import router as education_system_router
except ImportError as exc:
    education_system_router = _fallback_router("Education System", exc)

try:
    from AFO.api.routers.modal_data import router as modal_data_router
except ImportError as exc:
    modal_data_router = _fallback_router("Modal Data", exc)

try:
    from AFO.api.routers.skill_registry import router as skill_registry_router
except ImportError as exc:
    skill_registry_router = _fallback_router("Skill Registry", exc)

try:
    from AFO.api.routers.trinity_policy import router as trinity_policy_router
except ImportError as exc:
    trinity_policy_router = _fallback_router("Trinity Policy", exc)

try:
    from AFO.api.routes.trinity_sbt import router as trinity_sbt_router
except ImportError as exc:
    trinity_sbt_router = _fallback_router("Trinity SBT", exc)


# --- Trinity Metrics (Mock vs Real) ---
TrinityMetrics: Any = None
calculate_trinity: Any = None

try:
    from AFO.domain.metrics.trinity import TrinityMetrics as _RealTrinityMetrics
    from AFO.domain.metrics.trinity import calculate_trinity as _real_calculate_trinity

    TrinityMetrics = _RealTrinityMetrics
    calculate_trinity = _real_calculate_trinity
except ImportError:
    try:
        from domain.metrics.trinity import (  # type: ignore[import]
            TrinityMetrics as _RealTrinityMetrics_2,
        )
        from domain.metrics.trinity import calculate_trinity as _real_calculate_trinity_2

        TrinityMetrics = _RealTrinityMetrics_2
        calculate_trinity = _real_calculate_trinity_2
    except ImportError:
        # Runtime Mock
        class MockTrinityMetrics:
            def __init__(self, **kwargs: Any) -> None:
                self.trinity_score = 0.8
                self.truth = 0.8
                self.goodness = 0.8
                self.beauty = 0.8
                self.filial_serenity = 0.8
                self.eternity = 0.8
                self.balance_status = "balanced"

            def to_dict(self) -> dict[str, Any]:
                return self.__dict__

        TrinityMetrics = MockTrinityMetrics  # type: ignore[assignment]

        def mock_calculate_trinity(
            truth: float = 0.0,
            goodness: float = 0.0,
            beauty: float = 0.0,
            filial_serenity: float = 0.0,
            eternity: float = 0.0,
            from_100_scale: bool = True,
            **kwargs: Any,
        ) -> Any:
            return MockTrinityMetrics()

        calculate_trinity = mock_calculate_trinity

# --- Settings ---

get_settings: Callable[[], SettingsType] | None = None

try:
    from AFO.config.settings import get_settings as _real_get_settings

    get_settings = _real_get_settings
except ImportError:
    try:
        from config.settings import get_settings as _fallback_get_settings  # type: ignore[import]

        get_settings = _fallback_get_settings
    except ImportError:
        get_settings = None
