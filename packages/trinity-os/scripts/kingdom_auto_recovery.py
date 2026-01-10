#!/usr/bin/env python3
"""AFO 왕국 자동 복구 메커니즘 (Auto Recovery)

眞善美孝 철학 기반 자동 복구 시스템
- 문제 해결 실패 시 자동 재시도 (최대 3회)
- 실패 원인 분석 및 대안 시도
- 복구 불가 시 상세 리포트 생성 및 알림
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, cast

# AFO 루트 디렉토리
AFO_ROOT = Path(__file__).resolve().parent.parent

# 최대 재시도 횟수
MAX_RETRIES = 3
# 재시도 간격 (초)
RETRY_DELAY = 5


class AutoRecovery:
    """자동 복구 메커니즘"""

    def __init__(self, max_retries: int = MAX_RETRIES, retry_delay: int = RETRY_DELAY):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.recovery_log: list[dict[str, Any]] = []

    def execute_with_recovery(
        self,
        command: list[str],
        description: str,
        alternative_commands: list[list[str]] | None = None,
    ) -> dict[str, Any]:
        """명령 실행 및 자동 복구"""
        result = {
            "description": description,
            "command": " ".join(command),
            "status": "unknown",
            "attempts": [],
            "final_result": None,
            "recovered": False,
        }

        # 기본 명령 재시도
        for attempt in range(1, self.max_retries + 1):
            try:
                proc_result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=AFO_ROOT,
                )

                attempt_result = {
                    "attempt": attempt,
                    "returncode": proc_result.returncode,
                    "stdout": proc_result.stdout[:500],
                    "stderr": proc_result.stderr[:500],
                    "success": proc_result.returncode == 0,
                }
                cast(list[Any], result["attempts"]).append(attempt_result)

                if proc_result.returncode == 0:
                    result["status"] = "success"
                    result["final_result"] = attempt_result
                    result["recovered"] = attempt > 1
                    return result

                # 실패 시 대기
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

            except subprocess.TimeoutExpired:
                attempt_result = {
                    "attempt": attempt,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": "Timeout expired",
                    "success": False,
                }
                cast(list[Any], result["attempts"]).append(attempt_result)

                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

            except Exception as e:
                attempt_result = {
                    "attempt": attempt,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": str(e),
                    "success": False,
                }
                cast(list[Any], result["attempts"]).append(attempt_result)

                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        # 기본 명령 실패 시 대안 명령 시도
        if alternative_commands:
            for alt_command in alternative_commands:
                try:
                    proc_result = subprocess.run(
                        alt_command,
                        capture_output=True,
                        text=True,
                        timeout=60,
                        cwd=AFO_ROOT,
                    )

                    if proc_result.returncode == 0:
                        result["status"] = "recovered_with_alternative"
                        result["final_result"] = {
                            "attempt": "alternative",
                            "returncode": proc_result.returncode,
                            "stdout": proc_result.stdout[:500],
                            "stderr": proc_result.stderr[:500],
                            "success": True,
                            "command": " ".join(alt_command),
                        }
                        result["recovered"] = True
                        return result

                except Exception:
                    continue

        # 모든 시도 실패
        result["status"] = "failed"
        result["final_result"] = result["attempts"][-1] if result["attempts"] else None
        return result

    def analyze_failure(self, result: dict[str, Any]) -> dict[str, Any]:
        """실패 원인 분석"""
        analysis: Any = {
            "failure_type": "unknown",
            "possible_causes": [],
            "recommendations": [],
        }

        if not result.get("attempts"):
            analysis["failure_type"] = "no_attempts"
            return analysis

        last_attempt = result["attempts"][-1]
        stderr = last_attempt.get("stderr", "").lower()

        # 타임아웃
        if "timeout" in stderr or last_attempt.get("returncode") == -1:
            analysis["failure_type"] = "timeout"
            analysis["possible_causes"] = [
                "서비스 응답 지연",
                "네트워크 문제",
                "리소스 부족",
            ]
            analysis["recommendations"] = [
                "서비스 상태 확인",
                "네트워크 연결 확인",
                "시스템 리소스 확인",
            ]

        # 연결 실패
        elif "connection" in stderr or "refused" in stderr:
            analysis["failure_type"] = "connection_failure"
            analysis["possible_causes"] = [
                "서비스 미실행",
                "포트 충돌",
                "방화벽 차단",
            ]
            analysis["recommendations"] = [
                "Docker 컨테이너 상태 확인",
                "포트 사용 확인",
                "서비스 재시작",
            ]

        # 권한 문제
        elif "permission" in stderr or "access denied" in stderr:
            analysis["failure_type"] = "permission_denied"
            analysis["possible_causes"] = [
                "파일 권한 부족",
                "디렉토리 접근 불가",
            ]
            analysis["recommendations"] = [
                "파일 권한 확인",
                "실행 권한 확인 (chmod +x)",
            ]

        # 모듈/파일 없음
        elif "no such file" in stderr or "module not found" in stderr:
            analysis["failure_type"] = "missing_dependency"
            analysis["possible_causes"] = [
                "파일/스크립트 없음",
                "Python 모듈 미설치",
            ]
            analysis["recommendations"] = [
                "필요 파일 확인",
                "의존성 설치 (pip install -r requirements.txt)",
            ]

        # 기타
        else:
            analysis["failure_type"] = "unknown_error"
            analysis["possible_causes"] = ["알 수 없는 오류"]
            analysis["recommendations"] = ["로그 확인 필요"]

        return analysis

    def recover_problem_solver(self, phase: int) -> dict[str, Any]:
        """문제 해결 스크립트 복구"""
        command = [
            "bash",
            str(AFO_ROOT / "scripts" / "kingdom_problem_solver.sh"),
            f"--phase={phase}",
        ]
        alternative = [
            ["bash", str(AFO_ROOT / "scripts" / "kingdom_auto_fix_all.sh")],
        ]

        return self.execute_with_recovery(
            command,
            f"문제 해결 Phase {phase}",
            alternative,
        )

    def recover_docker_service(self, service_name: str) -> dict[str, Any]:
        """Docker 서비스 복구"""
        command = [
            "docker-compose",
            "-f",
            str(AFO_ROOT / "docker_config" / "docker-compose.microservices.yml"),
            "restart",
            service_name,
        ]
        alternative = [
            [
                "docker-compose",
                "-f",
                str(AFO_ROOT / "docker_config" / "docker-compose.microservices.yml"),
                "up",
                "-d",
                service_name,
            ],
        ]

        return self.execute_with_recovery(
            command,
            f"Docker 서비스 {service_name} 재시작",
            alternative,
        )

    def generate_recovery_report(self) -> dict[str, Any]:
        """복구 리포트 생성"""
        successful = sum(
            1 for log in self.recovery_log if log.get("status") in ["success", "recovered_with_alternative"]
        )
        failed = sum(1 for log in self.recovery_log if log.get("status") == "failed")
        recovered = sum(1 for log in self.recovery_log if log.get("recovered", False))

        return {
            "timestamp": datetime.now().isoformat(),
            "total_operations": len(self.recovery_log),
            "successful": successful,
            "failed": failed,
            "recovered": recovered,
            "recovery_rate": (round(recovered / len(self.recovery_log) * 100, 2) if self.recovery_log else 0),
            "operations": self.recovery_log,
            "recommendation": self._get_recommendation(successful, failed),
        }

    def _get_recommendation(self, successful: int, failed: int) -> str:
        """권장사항 생성"""
        if failed == 0:
            return "✅ 모든 복구 성공"
        elif successful > failed:
            return "⚠️ 일부 복구 실패. 수동 확인 권장"
        else:
            return "🚨 복구 실패 다수. 즉시 수동 개입 필요"


def main():
    """메인 실행 (예시)"""
    recovery = AutoRecovery()

    # 예시: 문제 해결 Phase 1 복구
    result = recovery.recover_problem_solver(1)
    recovery.recovery_log.append(result)

    # 실패 시 원인 분석
    if result["status"] == "failed":
        analysis = recovery.analyze_failure(result)
        print(f"실패 원인: {analysis['failure_type']}")
        print(f"권장사항: {', '.join(analysis['recommendations'])}")

    # 리포트 생성
    report = recovery.generate_recovery_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # 종료 코드
    exit_code = 0 if report["failed"] == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
