"""
Verify Server Restart
서버가 실제로 재시작되었는지 확인하는 스크립트
"""

# #region agent log
import json
from datetime import datetime
from pathlib import Path

import requests


LOG_PATH = Path("/Users/brnestrm/AFO_Kingdom/.cursor/debug.log")


def log_debug(location: str, message: str, data: dict | None = None, hypothesis_id: str = "A") -> None:
    """Debug logging to NDJSON file"""
    try:
        log_entry = {
            "id": f"log_{int(datetime.now().timestamp() * 1000)}",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "location": location,
            "message": message,
            "data": data or {},
            "sessionId": "verify-server-restart",
            "runId": "verify",
            "hypothesisId": hypothesis_id,
        }
        with Path(LOG_PATH).open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Logging failed: {e}")


# #endregion agent log

BASE_URL = "http://localhost:8010"


def check_endpoints():
    """엔드포인트 확인"""
    # #region agent log
    log_debug(
        "verify_server_restart.py:check_endpoints",
        "Checking endpoints",
        {},
        "A",
    )
    # #endregion agent log

    endpoints = [
        "/api/health/comprehensive",
        "/api/intake/health",
        "/api/family/health",
        "/family/health",  # Fallback
    ]

    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            # #region agent log
            log_debug(
                f"verify_server_restart.py:check_endpoints:{endpoint}",
                "Endpoint response received",
                {"status_code": response.status_code, "endpoint": endpoint},
                "A",
            )
            # #endregion agent log
            results[endpoint] = response.status_code == 200
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint}: {response.status_code}")
        except Exception as e:
            # #region agent log
            log_debug(
                f"verify_server_restart.py:check_endpoints:{endpoint}",
                "Endpoint check failed",
                {"error": str(e), "endpoint": endpoint},
                "A",
            )
            # #endregion agent log
            results[endpoint] = False
            print(f"❌ {endpoint}: {e}")

    return results


def main():
    print("\n🏰 서버 재시작 확인\n")
    print("=" * 60)

    print("\n📋 엔드포인트 상태:")
    results = check_endpoints()

    print("\n" + "=" * 60)
    print("📊 요약")
    print("=" * 60)

    working = [k for k, v in results.items() if v]
    not_working = [k for k, v in results.items() if not v]

    if working:
        print(f"✅ 작동하는 엔드포인트: {len(working)}개")
        for endpoint in working:
            print(f"   - {endpoint}")

    if not_working:
        print(f"\n❌ 작동하지 않는 엔드포인트: {len(not_working)}개")
        for endpoint in not_working:
            print(f"   - {endpoint}")

    if "/api/health/comprehensive" in not_working:
        print("\n⚠️  Comprehensive Health 엔드포인트가 작동하지 않습니다.")
        print("   서버를 재시작했는지 확인하세요.")
        print("   서버 시작 로그에서 '✅ Comprehensive Health Check 라우터 등록 완료' 메시지를 확인하세요.")

    if "/api/intake/health" in not_working:
        print("\n⚠️  Intake 엔드포인트가 작동하지 않습니다.")
        print("   서버를 재시작했는지 확인하세요.")
        print("   서버 시작 로그에서 '✅ Intake API 라우터 등록 완료' 메시지를 확인하세요.")

    if "/api/family/health" in not_working and "/family/health" in working:
        print("\n⚠️  Family 엔드포인트는 /family/health로 작동하지만 /api/family/health는 작동하지 않습니다.")
        print("   이는 정상일 수 있습니다 (Family 라우터가 /family prefix로 등록됨).")

    # #region agent log
    log_debug(
        "verify_server_restart.py:main",
        "Server restart verification completed",
        {"results": results, "working": working, "not_working": not_working},
        "MAIN",
    )
    # #endregion agent log


if __name__ == "__main__":
    main()
