#!/usr/bin/env python3
"""
RAG 시스템 설정 파일
리포지토리 구조에 맞게 경로 자동 감지
API Wallet 통합: API 키 자동 로드
"""

from __future__ import annotations

import contextlib
import os
import sys
from pathlib import Path

# API Wallet 통합
try:
    # 리포지토리 루트에서 api_wallet 모듈 로드
    current_file = Path(__file__).resolve()
    repo_root = current_file.parent.parent.parent
    sys.path.insert(0, str(repo_root))
    from api_wallet import APIWallet

    _wallet = APIWallet()
    API_WALLET_AVAILABLE = True
except Exception:
    API_WALLET_AVAILABLE = False
    _wallet = None


def get_repo_root() -> Path:
    """리포지토리 루트 경로 자동 감지"""
    # 현재 스크립트 위치에서 시작
    current_file = Path(__file__).resolve()

    # scripts/rag/config.py -> 리포지토리 루트
    repo_root = current_file.parent.parent.parent

    # .git 또는 특정 파일로 확인
    if (repo_root / ".git").exists() or (repo_root / "docs").exists():
        return repo_root

    # 환경 변수 확인
    repo_path = os.getenv("AFO_REPO_ROOT")
    if repo_path:
        return Path(repo_path)

    # 기본값: 현재 파일 기준 상대 경로
    return repo_root


def get_obsidian_vault_path() -> Path:
    """옵시디언 vault 경로 자동 감지"""
    repo_root = get_repo_root()
    vault_path = repo_root / "docs"

    # 환경 변수로 오버라이드 가능
    env_vault = os.getenv("OBSIDIAN_VAULT_PATH")
    if env_vault:
        return Path(env_vault)

    return vault_path


def get_sync_state_file() -> Path:
    """동기화 상태 파일 경로"""
    repo_root = get_repo_root()
    return repo_root / ".obsidian_sync_state.json"


def get_openai_api_key() -> str | None:
    """OpenAI API 키 가져오기 (환경 변수 → API Wallet PostgreSQL → JSON 순서)"""
    # 1. 환경 변수에서 먼저 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 2. API Wallet에서 가져오기 시도 (PostgreSQL 우선)
    if API_WALLET_AVAILABLE and _wallet:
        # PostgreSQL 연결 시도
        try:
            import psycopg2

            # PostgreSQL 연결 (여러 설정 시도)
            pg_conn = None
            # Phase 2-4: settings 사용
            try:
                from AFO.config.settings import get_settings

                settings = get_settings()
                pg_settings = settings.get_postgres_connection_params()

                connection_configs = [
                    {
                        "host": pg_settings.get("host", "localhost"),
                        "port": pg_settings.get("port", 15432),
                        "database": pg_settings.get("database", "afo_memory"),
                        "user": pg_settings.get("user", "afo"),
                        "password": pg_settings.get("password", "your-secure-password-here"),
                    },
                    # fallback: 기본 postgres 설정
                    {
                        "host": pg_settings.get("host", "localhost"),
                        "port": pg_settings.get("port", 15432),
                        "database": "postgres",
                        "user": "postgres",
                        "password": "postgres",
                    },
                ]
            except Exception:
                # Fallback: os.getenv 사용
                connection_configs = [
                    {
                        "host": os.getenv("POSTGRES_HOST", "localhost"),
                        "port": int(os.getenv("POSTGRES_PORT", "15432")),
                        "database": os.getenv("POSTGRES_DB", "afo_memory"),
                        "user": os.getenv("POSTGRES_USER", "afo"),
                        "password": os.getenv("POSTGRES_PASSWORD", "your-secure-password-here"),
                    },
                    # fallback: 기본 postgres 설정
                    {
                        "host": os.getenv("POSTGRES_HOST", "localhost"),
                        "port": int(os.getenv("POSTGRES_PORT", "15432")),
                        "database": "postgres",
                        "user": "postgres",
                        "password": "postgres",
                    },
                ]

            # DATABASE_URL 환경 변수 확인
            database_url = os.getenv("DATABASE_URL")
            if database_url:
                with contextlib.suppress(Exception):
                    pg_conn = psycopg2.connect(database_url)

            # 기본 설정으로 시도
            if not pg_conn:
                for config in connection_configs:
                    try:
                        pg_conn = psycopg2.connect(**config)
                        break
                    except Exception:
                        continue

            if pg_conn:
                try:
                    # PostgreSQL 연결된 Wallet 생성
                    from api_wallet import APIWallet

                    pg_wallet = APIWallet(db_connection=pg_conn)

                    # 키 목록에서 OpenAI 검색
                    keys = pg_wallet.list_keys()
                    for key_info in keys:
                        service = key_info.get("service", "").lower()
                        name = key_info.get("name", "").lower()
                        if "openai" in service or "gpt" in service or "openai" in name:
                            key = pg_wallet.get(key_info["name"])
                            if key:
                                pg_conn.close()
                                return key

                    pg_conn.close()
                except Exception:
                    if pg_conn:
                        with contextlib.suppress(Exception):
                            pg_conn.close()
        except ImportError:
            pass  # psycopg2 없으면 JSON 저장소만 사용
        except Exception:
            pass  # PostgreSQL 연결 실패 시 JSON 저장소로 fallback

        # JSON 저장소에서 검색 (fallback)
        # 여러 가능한 이름으로 시도
        possible_names = ["openai", "OPENAI", "OpenAI", "gpt", "GPT"]
        for name in possible_names:
            key = _wallet.get(name)
            if key:
                return key

        # service 필드로 검색
        keys = _wallet.list_keys()
        for key_info in keys:
            service = key_info.get("service", "").lower()
            if "openai" in service or "gpt" in service:
                key = _wallet.get(key_info["name"])
                if key:
                    return key

    return None


# 설정 값
REPO_ROOT = get_repo_root()
OBSIDIAN_VAULT_PATH = get_obsidian_vault_path()
SYNC_STATE_FILE = get_sync_state_file()
# 중앙 설정 사용 (Phase 1 리팩토링)
try:
    import sys
    from pathlib import Path

    # AFO 모듈 경로 추가
    repo_root = Path(__file__).parent.parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from AFO.config.settings import get_settings

    QDRANT_URL = get_settings().QDRANT_URL
except (ImportError, AttributeError):
    # Fallback
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION_NAME = "obsidian_vault"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SYNC_INTERVAL = 60  # 초

# OpenAI API 키 (환경 변수 또는 API Wallet에서 자동 로드)
OPENAI_API_KEY = get_openai_api_key()

# 환경 변수로 설정 (다른 모듈에서 사용 가능하도록)
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def print_config():
    """설정 정보 출력"""
    print("📋 RAG 시스템 설정:")
    print(f"  리포지토리 루트: {REPO_ROOT}")
    print(f"  옵시디언 vault: {OBSIDIAN_VAULT_PATH}")
    print(f"  동기화 상태 파일: {SYNC_STATE_FILE}")
    print(f"  Qdrant URL: {QDRANT_URL}")
    print(f"  컬렉션 이름: {QDRANT_COLLECTION_NAME}")
    print(f"  API Wallet: {'✅ 사용 가능' if API_WALLET_AVAILABLE else '❌ 사용 불가'}")
    if OPENAI_API_KEY:
        print(f"  OpenAI API Key: ✅ 설정됨 ({len(OPENAI_API_KEY)} 문자)")
    else:
        print("  OpenAI API Key: ❌ 설정되지 않음")


if __name__ == "__main__":
    print_config()
