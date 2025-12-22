"""
AFO 왕국 중앙 설정 모듈
모든 환경 변수와 기본값을 한 곳에서 관리
"""

from .antigravity import antigravity
from .settings import AFOSettings, get_settings

__all__ = ["AFOSettings", "antigravity", "get_settings"]
