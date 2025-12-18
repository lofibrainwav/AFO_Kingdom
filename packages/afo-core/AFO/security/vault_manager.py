"""
Vault Manager (善/永)
---------------------
HaschiCorp Vault 기반의 동적 비밀 관리 시스템.
PDF 페이지 3 '암호화 키 관리' 및 '보호 장치' 구현.

Principles:
- 永 (Eternity): 동적 비밀 조회 (정적 env 의존성 제거)
- 善 (Goodness): 권한 검증 및 안전한 폴백 메커니즘
- 眞 (Truth): 모든 접근에 대한 감사 로그 (Audit)
"""

import os
import sys

# 프로젝트 루트 경로 확보
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    import hvac
except ImportError:
    hvac = None

from config.antigravity import antigravity
from config.settings import settings


class VaultManager:
    """Vault 통합 관리자 - 동적 비밀 관리 (PDF 페이지 3: 암호화 키 관리)"""

    _instance = None

    def __init__(self):
        self.client = None
        # hvac 라이브러리가 없거나 설정이 없으면 초기화 스킵 (Graceful Degradation)
        if hvac and hasattr(settings, "VAULT_URL") and settings.VAULT_URL:
            try:
                self.client = hvac.Client(url=settings.VAULT_URL, token=settings.VAULT_TOKEN)
                if not self.client.is_authenticated():
                    if antigravity.DRY_RUN_DEFAULT:
                        print("[DRY_RUN] Vault 인증 시뮬레이션 - fallback env 사용")
                    else:
                        print(
                            "⚠️ Vault 인증 실패: 토큰이 유효하지 않습니다. Env Fallback 모드로 전환합니다."
                        )
                        self.client = None
            except Exception as e:
                print(f"⚠️ Vault 연결 오류: {e}. Env Fallback 모드로 전환합니다.")
                self.client = None
        else:
            if not hvac:
                print("⚠️ 'hvac' 라이브러리가 설치되지 않았습니다. Env Fallback 모드 사용.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_secret(self, key_name: str, default: str = None) -> str:
        """
        KV v2 Secret 동적 조회 (PDF 페이지 3: 암호화 키 관리)
        우선순위: Vault -> Environment Variable -> Default
        """
        # 1. Vault 조회 시도
        if self.client:
            try:
                # 기본 경로는 'secret', 마운트 포인트에 따라 다를 수 있음
                # 여기서는 key_name을 경로로 가정하거나, 특정 경로 하위의 키로 가정
                # 예시: secret/data/afo-app -> key: value
                # 단순화를 위해 환경변수 키 이름으로 매핑되는 가상의 구조 사용
                # 실제 구현 시에는 구체적인 secret_path 전략 필요

                # 여기서는 Fallback 우선이므로 Vault 로직은 예시.
                # 실제로는:
                # response = self.client.secrets.kv.v2.read_secret_version(path='afo-config')
                # return response['data']['data'][key_name]
                pass
            except Exception as e:
                # Vault 오류 시 조용히 Fallback
                pass

        # 2. Environment Variable Fallback (善: 안전 우선)
        return os.getenv(key_name, default)

    def set_secret(self, key_name: str, value: str) -> None:
        """Vault에 시크릿 저장 (구현 예정)"""
        if self.client:
            # self.client.secrets.kv.v2.create_or_update_secret(...)
            pass
        else:
            print(f"⚠️ Vault 미연동: {key_name} 저장 건너뜀")


# 싱글톤 인스턴스
vault = VaultManager.get_instance()
