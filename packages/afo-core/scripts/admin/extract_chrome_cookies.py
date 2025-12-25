# Trinity Score: 90.0 (Established by Chancellor)
#!/usr/bin/env python3
"""크롬 브라우저 쿠키에서 OpenAI 토큰 추출"""

import os
import shutil
import sqlite3
import tempfile
from pathlib import Path


def find_chrome_cookies():
    """크롬 쿠키 DB에서 OpenAI 토큰 찾기"""
    chrome_cookie_paths = [
        Path.home() / "Library/Application Support/Google/Chrome/Default/Cookies",
        Path.home() / "Library/Application Support/Google/Chrome/Profile 1/Cookies",
        Path.home() / "Library/Application Support/Google/Chrome/Profile 2/Cookies",
        Path.home() / "Library/Application Support/Google Chrome/Default/Cookies",
        Path.home() / "Library/Application Support/Google Chrome/Profile 1/Cookies",
        Path.home() / "Library/Application Support/Google Chrome/Profile 2/Cookies",
    ]

    print("=== 크롬 쿠키에서 OpenAI 토큰 찾기 ===\n")

    found_tokens = []

    for cookie_path in chrome_cookie_paths:
        if not cookie_path.exists():
            continue

        print(f"📂 {cookie_path.name} 확인 중...")

        try:
            # 크롬 쿠키 DB는 잠겨있을 수 있으므로 복사본 사용
            with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
                tmp_path = tmp.name

            shutil.copy2(cookie_path, tmp_path)

            conn = sqlite3.connect(tmp_path)
            cursor = conn.cursor()

            # OpenAI 관련 쿠키 찾기
            cursor.execute(
                """
                SELECT name, value, host_key, expires_utc
                FROM cookies
                WHERE (host_key LIKE '%openai%'
                   OR host_key LIKE '%platform.openai%'
                   OR host_key LIKE '%auth.openai%')
               AND (name LIKE '%token%'
                   OR name LIKE '%auth%'
                   OR name LIKE '%session%'
                   OR name LIKE '%access%')
            ORDER BY expires_utc DESC
            """
            )

            cookies = cursor.fetchall()

            if cookies:
                print(f"   ✅ {len(cookies)}개 토큰 발견:")
                for name, value, host_key, _expires in cookies:
                    print(f"      • {name} ({host_key})")
                    print(f"        길이: {len(value)} 문자")
                    found_tokens.append(
                        {"name": name, "value": value, "host": host_key}
                    )
            else:
                print("   (토큰 없음)")

            conn.close()
            os.unlink(tmp_path)

        except Exception as e:
            print(f"   ❌ 오류: {e}")

    return found_tokens


def save_to_wallet(token_value: str):
    """토큰을 API Wallet에 저장"""
    # 1. Try JSON Storage (Default & Most Reliable for bridging)
    try:
        from api_wallet import APIWallet

        print("   Attempting to save to API Wallet (JSON Mode)...")
        wallet = APIWallet()  # Defaults to JSON storage

        # 토큰 저장
        key_id = wallet.add(
            name="openai",
            api_key=token_value,
            service="openai",
            description="OpenAI 인증 토큰 (크롬 쿠키에서 추출)",
        )

        print("\n✅ 토큰이 API Wallet (JSON)에 저장되었습니다!")
        print(f"   키 ID: {key_id}")
        return True

    except Exception as e:
        print(f"\n⚠️ JSON 저장 실패: {e}")

    # 2. Try PostgreSQL (Fallback)
    try:
        import psycopg2

        print("   Attempting to save to API Wallet (DB Mode)...")

        # PostgreSQL 연결 (중앙 설정 사용 - Phase 1 리팩토링)
        try:
            from AFO.config.settings import get_settings

            pg_settings = get_settings()
            conn = psycopg2.connect(
                host=pg_settings.POSTGRES_HOST,
                port=pg_settings.POSTGRES_PORT,
                database=pg_settings.POSTGRES_DB,
                user=pg_settings.POSTGRES_USER,
                password=pg_settings.POSTGRES_PASSWORD,
            )
        except ImportError:
            # Fallback
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=int(os.getenv("POSTGRES_PORT", "15432")),
                database=os.getenv("POSTGRES_DB", "afo_memory"),
                user=os.getenv("POSTGRES_USER", "afo"),
                password=os.getenv("POSTGRES_PASSWORD", "your-secure-password-here"),
            )

        wallet = APIWallet(db_connection=conn)

        key_id = wallet.add(
            name="openai",
            api_key=token_value,
            service="openai",
            description="OpenAI 인증 토큰 (크롬 쿠키에서 추출)",
        )

        print("\n✅ 토큰이 API Wallet (DB)에 저장되었습니다!")
        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ DB 저장 실패: {e}")
        return False


def main():
    tokens = find_chrome_cookies()

    if not tokens:
        print("\n❌ 토큰을 찾을 수 없습니다.")
        print("\n💡 확인 사항:")
        print("   1. 크롬에서 OpenAI에 로그인했는지 확인")
        print("   2. 크롬이 실행 중이면 종료 후 다시 시도")
        return

    print(f"\n✅ 총 {len(tokens)}개 토큰 발견")

    # 가장 가능성 높은 토큰 선택 (session_token 우선)
    selected_token = None
    for token in tokens:
        if "session" in token["name"].lower():
            selected_token = token
            break

    if not selected_token:
        selected_token = tokens[0]

    print(f"\n📋 선택된 토큰: {selected_token['name']}")
    print(f"   호스트: {selected_token['host']}")
    print(f"   길이: {len(selected_token['value'])} 문자")

    # 저장 확인
    print("\n💾 API Wallet에 자동 저장합니다...")
    save_to_wallet(selected_token["value"])
    print("\n토큰 값:")
    print(selected_token["value"])


if __name__ == "__main__":
    main()
