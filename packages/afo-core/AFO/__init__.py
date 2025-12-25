"""
AFO 패키지 - 루트 모듈 re-export
테스트 호환성을 위해 afo-core 루트 모듈들을 AFO 네임스페이스로 노출
"""

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


__all__ = [
    "afo_skills_registry",
    "api_server",
    "api_wallet",
    "chancellor_graph",
    "domain",
    "input_server",
    "kms",
    "llm_router",
    "llms",
    "scholars",
    "services",
    "utils",
]
