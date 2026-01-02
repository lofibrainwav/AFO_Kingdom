<<<<<<< HEAD
"""
AFO Core AFO Subpackage
MD→티켓 자동화 관련 모듈들
"""

# MD→티켓 자동화 모듈들 노출
from .md_parser import MDParser
from .matching_engine import MatchingEngine
from .ticket_generator import TicketGenerator
from .skeleton_index import SkeletonIndexer, SkeletonIndex, ModuleInfo
=======
# Trinity Score: 90.0 (Established by Chancellor)
"""AFO 패키지 - 루트 모듈 re-export
테스트 호환성을 위해 afo-core 루트 모듈들을 AFO 네임스페이스로 노출
"""

import importlib
import sys
from pathlib import Path

# 부모 디렉토리(afo-core 루트)를 path에 추가
_parent = Path(__file__).parent.parent
if str(_parent) not in sys.path:
    sys.path.insert(0, str(_parent))


# 모듈 re-export (lazy import 방식으로 에러 방지)
def __getattr__(name):
    """Lazy import for AFO submodules"""
    if name == "api_wallet":
        import api_wallet

        return api_wallet
    elif name == "llm_router":
        import llm_router

        return llm_router
    elif name == "input_server":
        import input_server

        return input_server
    elif name == "afo_skills_registry":
        import afo_skills_registry

        return afo_skills_registry
    elif name == "api_server":
        import api_server

        return api_server
    elif name == "chancellor_graph":
        import importlib

        return importlib.import_module("AFO.chancellor_graph")
    elif name == "kms":
        import kms

        return kms
    elif name == "scholars":
        import scholars

        return scholars
    elif name == "services":
        import services

        return services
    elif name == "utils":
        import utils

        return utils

    elif name == "llms":
        import llms

        return llms
    elif name == "domain":
        import domain

        return domain
    raise AttributeError(f"module 'AFO' has no attribute '{name}'")

>>>>>>> wip/ph20-01-post-work

__all__ = [
    "MDParser",
    "MatchingEngine", 
    "TicketGenerator",
    "SkeletonIndexer",
    "SkeletonIndex",
    "ModuleInfo"
]
