#!/usr/bin/env python3
"""
DSPy 격리 venv 러너 - 메인 시스템에서 안전하게 격리 venv 호출

TICKET-001: 격리 venv MIPROv2 실행 러너
DSPY_ENABLED 환경 변수에 따라 격리 venv의 DSPy 기능을 호출

사용법:
    # 안전 모드 (기본값)
    DSPY_ENABLED=false python scripts/dspy_isolated_runner.py

    # 격리 실행 모드
    DSPY_ENABLED=true python scripts/dspy_isolated_runner.py

출력:
    - DSPY_ENABLED=false: 안전하게 스킵
    - DSPY_ENABLED=true: 격리 venv에서 MIPROv2 실행
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


def is_dspy_enabled() -> bool:
    """DSPY 기능 활성화 여부 확인"""
    return os.getenv("DSPY_ENABLED", "false").lower() in ("true", "1", "yes")


def run_dspy_isolated() -> dict[str, Any]:
    """
    격리 venv에서 DSPy MIPROv2 실행

    Returns:
        실행 결과
    """
    result = {
        "dspy_enabled": True,
        "venv_path": ".venv-dspy/bin/python",
        "command": None,
        "return_code": None,
        "stdout": None,
        "stderr": None,
        "success": False,
        "error": None,
    }

    try:
        # 격리 venv Python 경로 확인
        venv_python = Path(".venv-dspy/bin/python")
        if not venv_python.exists():
            result["error"] = f"격리 venv가 존재하지 않음: {venv_python}"
            return result

        # 격리 venv에서 직접 실행되는 코드 경로
        test_script = Path(".venv-dspy/lib/python3.12/site-packages/afo/dspy/test_mipro_example.py")
        if not test_script.exists():
            # 격리 venv에 코드가 없으면 메인 시스템 코드 사용
            test_script = Path("packages/afo-core/afo/dspy/test_mipro_example.py")

        cmd = [str(venv_python), str(test_script)]

        result["command"] = " ".join(cmd)

        # 명령 실행 (타임아웃 300초 = 5분)
        process = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=300, cwd=Path.cwd()
        )

        result["return_code"] = process.returncode
        result["stdout"] = process.stdout
        result["stderr"] = process.stderr
        result["success"] = process.returncode == 0

        if process.returncode != 0:
            result["error"] = f"격리 venv 실행 실패 (코드: {process.returncode})"

    except subprocess.TimeoutExpired:
        result["error"] = "격리 venv 실행 타임아웃 (5분 초과)"
    except Exception as e:
        result["error"] = f"격리 venv 실행 중 예외 발생: {e}"

    return result


def safe_skip_message() -> dict[str, Any]:
    """안전 스킵 메시지"""
    return {
        "dspy_enabled": False,
        "message": "DSPY_ENABLED=false - 안전하게 스킵합니다",
        "safe_mode": True,
        "success": True,
        "error": None,
    }


async def main():
    """메인 함수"""
    print("🧠 AFO 왕국 DSPy 격리 러너")
    print("=" * 50)

    # DSPY 활성화 상태 확인
    dspy_enabled = is_dspy_enabled()
    print(f"DSPY_ENABLED: {dspy_enabled}")

    if not dspy_enabled:
        # 안전 모드: 스킵
        result = safe_skip_message()
        print("✅ 안전 모드: DSPy 기능 비활성화됨")
        print("💡 DSPY_ENABLED=true로 설정하면 격리 venv에서 MIPROv2가 실행됩니다")
    else:
        # 격리 실행 모드
        print("🚀 격리 실행 모드: DSPy MIPROv2 시작...")
        result = run_dspy_isolated()

        if result["success"]:
            print("✅ 격리 venv MIPROv2 실행 성공")
            print(f"📊 실행 결과: {len(result.get('stdout', ''))} 문자 출력")
        else:
            print("❌ 격리 venv MIPROv2 실행 실패")
            if result.get("error"):
                print(f"🔍 에러: {result['error']}")
            if result.get("stderr"):
                print(f"📝 stderr: {result['stderr'][:500]}...")

    # JSON 결과 출력 (머신 파싱용)
    print("\n" + "=" * 50)
    print("📋 JSON 결과:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 종료 코드
    return 0 if result.get("success", False) else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
