# Trinity Score: 90.0 (Established by Chancellor)
"""AFO 패키지 - 루트 모듈 re-export
테스트 호환성을 위해 afo-core 루트 모듈들을 AFO 네임스페이스로 노출
MD→티켓 자동화 관련 모듈들도 포함
"""

from __future__ import annotations

import sys
from pathlib import Path

# 부모 디렉토리(afo-core 루트)를 path에 추가
_parent = Path(__file__).parent.parent
if str(_parent) not in sys.path:
    sys.path.insert(0, str(_parent))

# MD→티켓 자동화 모듈들 노출 (optional - may not exist)
try:
    from .matching_engine import MatchingEngine
    from .md_parser import MDParser
    from .skeleton_index import ModuleInfo, SkeletonIndex, SkeletonIndexer
    from .ticket_generator import TicketGenerator

    _MD_MODULES_AVAILABLE = True
except ImportError:
    MDParser = None  # type: ignore[misc,assignment]
    MatchingEngine = None  # type: ignore[misc,assignment]
    TicketGenerator = None  # type: ignore[misc,assignment]
    SkeletonIndexer = None  # type: ignore[misc,assignment]
    SkeletonIndex = None  # type: ignore[misc,assignment]
    ModuleInfo = None  # type: ignore[misc,assignment]
    _MD_MODULES_AVAILABLE = False


# 모듈 re-export (lazy import 방식으로 에러 방지)
def __getattr__(name: str):
    """Lazy import for AFO submodules"""
    if name == "api_wallet":
        import api_wallet

        return api_wallet
    if name == "llm_router":
        import llm_router

        return llm_router
    if name == "input_server":
        import input_server

        return input_server
    if name == "afo_skills_registry":
        import afo_skills_registry

        return afo_skills_registry
    if name == "api_server":
        import api_server

        return api_server
    if name == "chancellor_graph":
        import importlib

        return importlib.import_module("AFO.chancellor_graph")
    if name == "kms":
        import kms

        return kms
    if name == "scholars":
        import scholars

        return scholars
    if name == "services":
        import services

        return services
    if name == "utils":
        import utils

        return utils
    if name == "llms":
        import llms

        return llms
    if name == "domain":
        import domain

        return domain
    raise AttributeError(f"module 'AFO' has no attribute '{name}'")


__all__ = [
    "MDParser",
    "MatchingEngine",
    "ModuleInfo",
    "SkeletonIndex",
    "SkeletonIndexer",
    "TicketGenerator",
]
