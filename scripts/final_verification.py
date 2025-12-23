"""
Final Verification Script
최종 검증 스크립트 - 서버 재시작 후 모든 엔드포인트 확인
"""

# #region agent log
import json
from datetime import datetime
from pathlib import Path

import requests

LOG_PATH = Path("/Users/brnestrm/AFO_Kingdom/.cursor/debug.log")


def log_debug(
    location: str, message: str, data: dict | None = None, hypothesis_id: str = "A"
) -> None:
    """Debug logging to NDJSON file"""
    try:
        log_entry = {
            "id": f"log_{int(datetime.now().timestamp() * 1000)}",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "location": location,
            "message": message,
            "data": data or {},
            "sessionId": "final-verification",
            "runId": "final",
            "hypothesisId": hypothesis_id,
        }
        with Path(LOG_PATH).open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Logging failed: {e}")


# #endregion agent log

BASE_URL = "http://localhost:8010"


def check_all_endpoints():
    """모든 엔드포인트 확인"""
    # #region agent log
    log_debug(
        "final_verification.py:check_all_endpoints", "Starting endpoint check", {}, "A"
    )
    # #endregion agent log

    endpoints = [
        ("Comprehensive Health", "/api/health/comprehensive"),
        ("Intake Health", "/api/intake/health"),
        ("Family Health (API)", "/api/family/health"),
        ("Family Health (Legacy)", "/family/health"),
    ]

    results = {}
    print("\n📋 엔드포인트 상태 확인:\n")

    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            # #region agent log
            log_debug(
                f"final_verification.py:check_all_endpoints:{name}",
                "Endpoint response received",
                {"status_code": response.status_code, "endpoint": endpoint},
                "A",
            )
            # #endregion agent log
            is_ok = response.status_code == 200
            results[name] = is_ok
            status = "✅" if is_ok else "❌"
            print(f"{status} {name}: {endpoint} - {response.status_code}")
            if is_ok and response.content:
                try:
                    data = response.json()
                    print(f"   Response: {str(data)[:100]}...")
                except:
                    pass
        except Exception as e:
            # #region agent log
            log_debug(
                f"final_verification.py:check_all_endpoints:{name}",
                "Endpoint check failed",
                {"error": str(e), "endpoint": endpoint},
                "A",
            )
            # #endregion agent log
            results[name] = False
            print(f"❌ {name}: {endpoint} - Error: {e}")

    return results


def main():
    print("\n🏰 최종 검증\n")
    print("=" * 60)

    # 서버가 실행 중인지 확인
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ API 서버가 실행 중입니다\n")
        else:
            print(f"⚠️  API 서버가 응답하지 않습니다 (Status: {response.status_code})\n")
    except Exception as e:
        print(f"❌ API 서버에 연결할 수 없습니다: {e}\n")
        print(
            "💡 서버를 시작하세요: cd AFO && python -m uvicorn api_server:app --reload --port 8010\n"
        )
        return

    # 모든 엔드포인트 확인
    results = check_all_endpoints()

    # 요약
    print("\n" + "=" * 60)
    print("📊 최종 결과")
    print("=" * 60)

    working = [name for name, ok in results.items() if ok]
    not_working = [name for name, ok in results.items() if not ok]

    if working:
        print(f"\n✅ 작동하는 엔드포인트: {len(working)}개")
        for name in working:
            print(f"   - {name}")

    if not_working:
        print(f"\n❌ 작동하지 않는 엔드포인트: {len(not_working)}개")
        for name in not_working:
            print(f"   - {name}")

    # 최종 판단
    critical_endpoints = ["Comprehensive Health", "Intake Health"]
    critical_working = all(results.get(name, False) for name in critical_endpoints)

    if critical_working:
        print("\n🎉 핵심 엔드포인트가 모두 작동합니다!")
    else:
        print("\n⚠️  일부 핵심 엔드포인트가 작동하지 않습니다.")
        print("   서버를 재시작했는지 확인하세요.")
        print("   서버 시작 로그에서 다음 메시지를 확인하세요:")
        print("   - '✅ Comprehensive Health Check 라우터 등록 완료 (조기 등록)'")
        print("   - '✅ Intake API 라우터 등록 완료 (조기 등록)'")

    # #region agent log
    log_debug(
        "final_verification.py:main",
        "Final verification completed",
        {
            "results": results,
            "working": working,
            "not_working": not_working,
            "critical_working": critical_working,
        },
        "MAIN",
    )
    # #endregion agent log


if __name__ == "__main__":
    main()
