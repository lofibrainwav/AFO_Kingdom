"""
Type stubs for AFO Kingdom modules
This file provides minimal type stubs to resolve Pyright import issues
"""


# Stub modules that may not exist but are referenced
class AFO:
    @staticmethod
    def config():
        return None

    @staticmethod
    def antigravity():
        return None

    @staticmethod
    def api_wallet():
        return None

    @staticmethod
    def llm_router():
        return None

    @staticmethod
    def input_server():
        return None

    @staticmethod
    def afo_skills_registry():
        return None

    @staticmethod
    def api_server():
        return None

    @staticmethod
    def chancellor_graph():
        return None

    @staticmethod
    def kms():
        return None

    @staticmethod
    def scholars():
        return None

    @staticmethod
    def services():
        return None

    @staticmethod
    def utils():
        return None

    @staticmethod
    def llms():
        return None

    @staticmethod
    def domain():
        return None


# Stub for optional dependencies
try:
    import crewai
except ImportError:
    crewai = None

try:
    import autogen
except ImportError:
    autogen = None

try:
    import docx
except ImportError:
    docx = None
