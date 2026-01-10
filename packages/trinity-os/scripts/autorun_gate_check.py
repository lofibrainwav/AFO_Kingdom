#!/usr/bin/env python3
from typing import Any, Mapping, cast
"""
TRINITY-OS Autorun Gate Check (Light/Deep)

목적:
- 오토런(Serenity Gate) 준비 상태를 "지피지기" 방식으로 빠르게 확인.
- 기본 모드는 가벼운 검사(Health/Trinity)만 수행.
- --deep 옵션에서만 헌법/프론트/DB까지 포함한 Deep Gate를 실행.

원칙:
- DRY_RUN 안전 우선: 기본 모드는 변경 없는 읽기성 검사만 호출.
- Writer ≠ Judge: 이 스크립트는 점수/상태를 새로 계산/선언하지 않고
  기존 전용 스크립트의 **원문 출력/Exit Code**만 수집해 제공합니다.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def find_afo_root(trinity_root: Path) -> tuple[Path, str]:
    """TRINITY-OS가 단독 레포로 실행되는 경우와
    AFO 루트 하위에 통합되어 실행되는 경우를 모두 지원한다.
    """
    # Standalone TRINITY-OS 내부에 AFO 코어가 같이 있는 경우
    if (trinity_root / "afo_soul_engine").exists() and (trinity_root / ".claude").exists():
        return trinity_root, "standalone"

    # 통합 리포(AFO 루트/ TRINITY-OS 하위)인 경우
    parent = trinity_root.parent
    if (parent / "afo_soul_engine").exists() and (parent / ".claude").exists():
        return parent, "integrated"

    # 부분 통합(하나만 있는 경우)
    if (parent / "afo_soul_engine").exists():
        return parent, "integrated_partial"
    if (trinity_root / "afo_soul_engine").exists():
        return trinity_root, "standalone_partial"

    return trinity_root, "unknown"


def run_command(
    cmd: list[str],
    cwd: Path,
    timeout: int,
) -> dict:
    """서브 스크립트 실행 유틸 (stdout/stderr/exit code 수집)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check: Any = False,
        )
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "cmd": " ".join(cmd),
        }
    except subprocess.TimeoutExpired as e:
        return {
            "status": "timeout",
            "exit_code": None,
            "stdout": (e.stdout or "").strip(),
            "stderr": (e.stderr or "").strip(),
            "cmd": " ".join(cmd),
        }
    except (OSError, subprocess.SubprocessError) as e:
        return {
            "status": "error",
            "exit_code": None,
            "stdout": "",
            "stderr": str(e),
            "cmd": " ".join(cmd),
        }


def try_parse_json(text: str) -> dict | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def latest_trinity_log(afo_root: Path) -> str | None:
    logs_dir = afo_root / "logs"
    if not logs_dir.exists():
        return None
    candidates = list(logs_dir.glob("trinity_health_*.json"))
    if not candidates:
        return None
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    return str(latest)


def main() -> None:
    parser = argparse.ArgumentParser(description="TRINITY-OS Autorun Gate Check")
    parser.add_argument(
        "--deep",
        action="store_true",
        help="헌법/프론트/DB까지 포함한 Deep Gate를 실행합니다(시간/의존성 비용 큼).",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="JSON을 사람이 보기 좋게 출력합니다.",
    )
    args = parser.parse_args()

    trinity_root = Path(__file__).resolve().parent.parent
    afo_root, mode = find_afo_root(trinity_root)
    python_exe = sys.executable or "python3"

    report: dict = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "deep": args.deep,
        "afo_root": str(afo_root),
        "checks": {},
        "notes": [],
    }

    # 1) 11-Organ Health (Light)
    health_script = afo_root / ".claude" / "scripts" / "check_11_organs.py"
    if health_script.exists():
        res = run_command([python_exe, str(health_script)], cwd=afo_root, timeout=60)
        parsed = try_parse_json(cast(Mapping[str, Any], res).get("stdout", ""))
        res["parsed"] = parsed
        report["checks"]["check_11_organs"] = res
    else:
        report["checks"]["check_11_organs"] = {
            "status": "skipped",
            "reason": f"not found: {health_script}",
        }
        report["notes"].append("check_11_organs.py 경로를 찾지 못했습니다.")

    # 2) Trinity Health Check (Light)
    trinity_script = afo_root / "afo_soul_engine" / "health" / "trinity_health_check.py"
    if trinity_script.exists():
        res = run_command([python_exe, str(trinity_script)], cwd=afo_root, timeout=120)
        res["latest_log"] = latest_trinity_log(afo_root)
        report["checks"]["trinity_health_check"] = res
    else:
        report["checks"]["trinity_health_check"] = {
            "status": "skipped",
            "reason": f"not found: {trinity_script}",
        }
        report["notes"].append("trinity_health_check.py 경로를 찾지 못했습니다.")

    # 3) Constitutional Deep Gate (Optional)
    if args.deep:
        deep_script = afo_root / "scripts" / "verify_kingdom_status.py"
        if deep_script.exists():
            # Deep Gate는 npm/type/build 등을 포함할 수 있으니 timeout 길게.
            res = run_command([python_exe, str(deep_script)], cwd=afo_root, timeout=600)
            report["checks"]["verify_kingdom_status"] = res
        else:
            report["checks"]["verify_kingdom_status"] = {
                "status": "skipped",
                "reason": f"not found: {deep_script}",
            }
            report["notes"].append("verify_kingdom_status.py 경로를 찾지 못했습니다.")

    # Final output
    if args.pretty:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
