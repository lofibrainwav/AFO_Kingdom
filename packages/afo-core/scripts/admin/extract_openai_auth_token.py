#!/usr/bin/env python3
"""브라우저에서 OpenAI 인증 토큰 추출 및 API Wallet에 저장"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def extract_token_from_browser():
    """브라우저에서 토큰 추출 방법 안내"""
    print("=== OpenAI 인증 토큰 추출 방법 ===\n")

    print("1️⃣ 브라우저 개발자 도구 열기:")
    print("   - Chrome/Edge: F12 또는 Cmd+Option+I (Mac) / Ctrl+Shift+I (Windows)")
    print("   - Safari: Cmd+Option+I (개발자 메뉴 활성화 필요)\n")

    print("2️⃣ Application 탭 (Chrome) 또는 Storage 탭 (Firefox) 선택\n")

    print("3️⃣ Cookies 또는 Local Storage에서 토큰 찾기:")
    print("   - https://platform.openai.com")
    print("   - 또는 https://auth.openai.com\n")

    print("4️⃣ 찾을 토큰 이름:")
    print("   - 'session_token'")
    print("   - 'access_token'")
    print("   - 'auth_token'")
    print("   - 또는 Network 탭에서 API 요청 헤더 확인\n")

    print("5️⃣ 또는 Network 탭에서:")
    print("   - API 요청 클릭")
    print("   - Headers 탭")
    print("   - Authorization 헤더 또는 Cookie 헤더 확인\n")


def save_token_to_wallet(token: str):
    """토큰을 API Wallet에 저장"""
    if not token:
        print("❌ 토큰이 입력되지 않았습니다.")
        return False

    try:
        import psycopg2

        from api_wallet import APIWallet

        # PostgreSQL 연결
        conn = psycopg2.connect(
            host="localhost",
            port=15432,
            database="afo_memory",
            user="afo",
            password=os.getenv("AFO_DB_PASSWORD", "afo_db_password"),  # nosec
        )

        wallet = APIWallet(db_connection=conn)

        # 토큰 저장 (openai 이름으로)
        key_id = wallet.add(
            name="openai",
            api_key=token,
            service="openai",
            description="OpenAI 인증 토큰 (월구독제 브라우저에서 추출)",
        )

        print("\n✅ 인증 토큰이 성공적으로 저장되었습니다!")
        print(f"   키 ID: {key_id}")
        print("   이름: openai")
        print("   서비스: openai")

        # 확인
        saved_token = wallet.get("openai")
        if saved_token:
            print(f"   확인: ✅ 토큰 검증 성공 ({len(saved_token)} 문자)")
            print(f"   앞 10자: {saved_token[:10]}...")

        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    extract_token_from_browser()

    print("\n" + "=" * 50)
    print("토큰을 찾으셨나요? 아래에 붙여넣어주세요:\n")

    try:
        token = input("인증 토큰: ").strip()
    except EOFError:
        print("\n입력이 없어 종료합니다.")
        return

    if not token:
        print("\n❌ 토큰이 입력되지 않았습니다.")
        return

    save_token_to_wallet(token)


if __name__ == "__main__":
    main()
