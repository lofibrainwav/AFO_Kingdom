#!/usr/bin/env python3
"""
AFO 왕국 통합 건강 리포트 생성기 (Unified Health Report)

眞善美孝 철학 기반 모든 모니터링 결과 통합
- check_11_organs.py: 오장육부 건강 체크
- monitoring_dashboard.py: 실시간 모니터링
- verify_kingdom_status.py: 왕국 상태 검증
- kingdom_problem_detector.py: 문제 감지
- Trinity Score 자동 계산 및 추적
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# AFO 루트 디렉토리
AFO_ROOT = Path(__file__).resolve().parent.parent


class HealthReportGenerator:
    """통합 건강 리포트 생성기"""

    def __init__(self):
        self.reports: dict[str, Any] = {}
        self.timestamp = datetime.now().isoformat()

    def run_check_11_organs(self) -> dict[str, Any]:
        """오장육부 건강 체크 실행"""
        try:
            result = subprocess.run(
                [
                    "python3",
                    str(AFO_ROOT / ".claude" / "scripts" / "check_11_organs.py"),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=AFO_ROOT,
            )
            if result.returncode == 0:
                return {
                    "status": "success",
                    "data": json.loads(result.stdout),
                    "error": None,
                }
            return {
                "status": "failed",
                "data": None,
                "error": result.stderr[:200],
            }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": str(e),
            }

    def run_problem_detector(self) -> dict[str, Any]:
        """문제 감지 실행"""
        try:
            result = subprocess.run(
                ["python3", str(AFO_ROOT / "scripts" / "kingdom_problem_detector.py")],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=AFO_ROOT,
            )
            if result.returncode == 0:
                return {
                    "status": "success",
                    "data": json.loads(result.stdout),
                    "error": None,
                }
            # 문제가 있어도 리포트는 생성 (exit code 1은 문제 발견 의미)
            try:
                return {
                    "status": "problems_found",
                    "data": json.loads(result.stdout),
                    "error": None,
                }
            except json.JSONDecodeError:
                return {
                    "status": "failed",
                    "data": None,
                    "error": result.stderr[:200],
                }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": str(e),
            }

    def run_verify_kingdom_status(self) -> dict[str, Any]:
        """왕국 상태 검증 실행"""
        try:
            result = subprocess.run(
                [
                    "python3",
                    str(
                        AFO_ROOT
                        / "scripts"
                        / "verification"
                        / "verify_kingdom_status.py"
                    ),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=AFO_ROOT,
            )
            # verify_kingdom_status.py는 JSON 출력이 아닐 수 있음
            # 출력에서 "All Green" 또는 에러 메시지 확인
            output = result.stdout + result.stderr
            if "All Green" in output or result.returncode == 0:
                return {
                    "status": "success",
                    "data": {"message": "All Green", "output": output[:500]},
                    "error": None,
                }
            return {
                "status": "failed",
                "data": {"output": output[:500]},
                "error": None,
            }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": str(e),
            }

    def calculate_trinity_score(self) -> dict[str, float]:
        """Trinity Score 계산"""
        trinity = {
            "truth": 0.0,
            "goodness": 0.0,
            "beauty": 0.0,
            "serenity": 0.0,
            "eternity": 0.0,
        }

        # 1. Truth (眞): 문제 감지 정확도, 시스템 무결성
        if "problem_detector" in self.reports:
            problem_data = self.reports["problem_detector"].get("data", {})
            if problem_data:
                total_problems = problem_data.get("total_problems", 0)
                # 문제가 적을수록 Truth 높음
                trinity["truth"] = max(0.0, 1.0 - (total_problems * 0.1))
            else:
                trinity["truth"] = 0.5  # 데이터 없음

        # 2. Goodness (善): 안정성, 오장육부 건강도
        if "check_11_organs" in self.reports:
            health_data = self.reports["check_11_organs"].get("data", {})
            if health_data:
                health_pct = health_data.get("health_percentage", 0) / 100.0
                trinity["goodness"] = health_pct
            else:
                trinity["goodness"] = 0.5

        # 3. Beauty (美): 코드 품질, 구조 우아함
        if "verify_kingdom_status" in self.reports:
            verify_data = self.reports["verify_kingdom_status"]
            if verify_data.get("status") == "success":
                trinity["beauty"] = 0.9  # All Green이면 높음
            else:
                trinity["beauty"] = 0.7  # 실패하면 낮음

        # 4. Serenity (孝): 형님의 평온, 마찰 제거
        # 문제가 없고 건강도가 높으면 Serenity 높음
        total_problems = 0
        if "problem_detector" in self.reports:
            problem_data = self.reports["problem_detector"].get("data", {})
            if problem_data:
                total_problems = problem_data.get("total_problems", 0)

        health_pct = 0.0
        if "check_11_organs" in self.reports:
            health_data = self.reports["check_11_organs"].get("data", {})
            if health_data:
                health_pct = health_data.get("health_percentage", 0) / 100.0

        # 문제 없고 건강하면 Serenity 높음
        if total_problems == 0 and health_pct >= 0.8:
            trinity["serenity"] = 1.0
        elif total_problems == 0:
            trinity["serenity"] = 0.9
        else:
            trinity["serenity"] = max(0.5, 1.0 - (total_problems * 0.1))

        # 5. Eternity (永): 지속 가능성, 레거시 계승
        # 모든 시스템이 정상이면 Eternity 높음
        all_success = all(
            report.get("status") in ["success", "problems_found"]
            for report in self.reports.values()
        )
        trinity["eternity"] = 0.95 if all_success else 0.7

        # 소수점 2자리로 반올림
        return {k: round(v, 2) for k, v in trinity.items()}

    def calculate_overall_score(self, trinity: dict[str, float]) -> float:
        """전체 점수 계산 (Trinity Score 공식)"""
        # Trinity Score = 0.35×眞 + 0.35×善 + 0.20×美 + 0.08×孝 + 0.02×永
        score = (
            0.35 * trinity["truth"]
            + 0.35 * trinity["goodness"]
            + 0.20 * trinity["beauty"]
            + 0.08 * trinity["serenity"]
            + 0.02 * trinity["eternity"]
        )
        return round(score, 4)

    def generate_report(self) -> dict[str, Any]:
        """통합 리포트 생성"""
        # 각 모니터링 시스템 실행
        self.reports["check_11_organs"] = self.run_check_11_organs()
        self.reports["problem_detector"] = self.run_problem_detector()
        self.reports["verify_kingdom_status"] = self.run_verify_kingdom_status()

        # Trinity Score 계산
        trinity = self.calculate_trinity_score()
        overall_score = self.calculate_overall_score(trinity)

        # Balance Gap 계산
        scores = [
            trinity["truth"],
            trinity["goodness"],
            trinity["beauty"],
            trinity["serenity"],
            trinity["eternity"],
        ]
        balance_gap = max(scores) - min(scores)
        balanced = balance_gap < 0.3

        # 권장사항 생성
        recommendation = self._get_recommendation(trinity, overall_score, balance_gap)

        return {
            "timestamp": self.timestamp,
            "overall_score": overall_score,
            "trinity_scores": trinity,
            "balance_gap": round(balance_gap, 4),
            "balanced": balanced,
            "reports": self.reports,
            "recommendation": recommendation,
            "summary": self._generate_summary(),
        }

    def _get_recommendation(
        self, trinity: dict[str, float], overall_score: float, balance_gap: float
    ) -> str:
        """권장사항 생성"""
        if overall_score >= 0.9 and balance_gap < 0.3:
            return "🎉 완벽한 상태! 모든 시스템 정상 작동 중"
        if overall_score >= 0.8:
            return "✅ 양호한 상태. 일부 개선 권장"
        if overall_score >= 0.7:
            return "⚠️ 주의 필요. 문제 해결 권장"
        return "🚨 긴급 상황! 즉시 시스템 점검 필요"

    def _generate_summary(self) -> dict[str, Any]:
        """요약 생성"""
        summary = {
            "health_status": "unknown",
            "problem_count": 0,
            "critical_issues": 0,
            "systems_healthy": 0,
            "systems_total": 0,
        }

        # 오장육부 건강도
        if "check_11_organs" in self.reports:
            health_data = self.reports["check_11_organs"].get("data", {})
            if health_data:
                health_pct = health_data.get("health_percentage", 0)
                summary["systems_healthy"] = health_data.get("healthy_organs", 0)
                summary["systems_total"] = health_data.get("total_organs", 0)

                if health_pct >= 80:
                    summary["health_status"] = "healthy"
                elif health_pct >= 60:
                    summary["health_status"] = "warning"
                else:
                    summary["health_status"] = "critical"

        # 문제 개수
        if "problem_detector" in self.reports:
            problem_data = self.reports["problem_detector"].get("data", {})
            if problem_data:
                summary["problem_count"] = problem_data.get("total_problems", 0)
                summary["critical_issues"] = problem_data.get("summary", {}).get(
                    "critical", 0
                )

        return summary


def main():
    """메인 실행"""
    generator = HealthReportGenerator()
    report = generator.generate_report()

    # JSON 출력
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # 종료 코드 (전체 점수 < 0.7이면 1 반환)
    exit_code = 0 if report["overall_score"] >= 0.7 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
