#!/usr/bin/env python3
"""
AFO 왕국 Critical 문제 지속 파악 시스템 (Problem Detector)

眞善美孝 철학 기반 문제 감지 엔진
- 성능 문제: Python 캐시, Node.js 모듈, 디스크 사용량
- 연결 문제: Redis, PostgreSQL, API 서버
- 보안 문제: 쿠키 파일, 디버그 파일, 하드코딩된 시크릿
- check_11_organs.py와 연동하여 오장육부 건강도와 연계
- JSON 출력으로 문제점 목록 및 우선순위 제공
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# AFO 루트 디렉토리 (TRINITY-OS의 부모 디렉토리)
TRINITY_OS_ROOT = Path(__file__).resolve().parent.parent
AFO_ROOT = TRINITY_OS_ROOT.parent  # TRINITY-OS의 부모 = AFO 루트


class ProblemDetector:
    """Critical 문제 감지 엔진"""

    def __init__(self):
        self.problems: list[dict[str, Any]] = []
        self.health_report: dict[str, Any] = {}

    def detect_performance_issues(self) -> list[dict[str, Any]]:
        """성능 문제 감지"""
        issues = []

        # 1. Python 캐시
        try:
            result = subprocess.run(
                'find . -type d -name "__pycache__" 2>/dev/null | wc -l',
                shell=True,
                capture_output=True,
                text=True,
                cwd=AFO_ROOT,
                timeout=10,
            )
            cache_count = int(result.stdout.strip() or "0")
            if cache_count > 100:  # 100개 이상이면 문제
                issues.append(
                    {
                        "category": "performance",
                        "type": "python_cache",
                        "severity": "critical" if cache_count > 1000 else "high",
                        "priority": 1 if cache_count > 1000 else 2,
                        "description": f"Python 캐시 디렉토리 {cache_count}개 발견",
                        "count": cache_count,
                        "threshold": 100,
                        "solution": "find . -type d -name '__pycache__' -prune -exec rm -rf {} +",
                    }
                )
        except Exception as e:
            issues.append(
                {
                    "category": "performance",
                    "type": "python_cache_check_failed",
                    "severity": "medium",
                    "priority": 3,
                    "description": f"Python 캐시 체크 실패: {e!s}",
                }
            )

        # 2. Node.js 모듈 (불필요한 것)
        try:
            result = subprocess.run(
                'find . -name "node_modules" -type d -not -path "*/afo-frontend/*" -not -path "*/trinity-dashboard/*" 2>/dev/null | wc -l',
                shell=True,
                capture_output=True,
                text=True,
                cwd=AFO_ROOT,
                timeout=10,
            )
            node_count = int(result.stdout.strip() or "0")
            if node_count > 0:
                issues.append(
                    {
                        "category": "performance",
                        "type": "unnecessary_node_modules",
                        "severity": "high",
                        "priority": 2,
                        "description": f"불필요한 node_modules 디렉토리 {node_count}개 발견",
                        "count": node_count,
                        "solution": "find . -name 'node_modules' -type d -not -path '*/afo-frontend/*' -not -path '*/trinity-dashboard/*' -prune -exec rm -rf {} +",
                    }
                )
        except Exception as e:
            issues.append(
                {
                    "category": "performance",
                    "type": "node_modules_check_failed",
                    "severity": "medium",
                    "priority": 3,
                    "description": f"Node.js 모듈 체크 실패: {e!s}",
                }
            )

        # 3. 디스크 사용량
        try:
            result = subprocess.run(
                "df -h . | tail -1 | awk '{print $5}' | sed 's/%//'",
                shell=True,
                capture_output=True,
                text=True,
                cwd=AFO_ROOT,
                timeout=5,
            )
            disk_usage = int(result.stdout.strip() or "0")
            if disk_usage > 80:
                issues.append(
                    {
                        "category": "performance",
                        "type": "disk_usage",
                        "severity": "critical" if disk_usage > 90 else "high",
                        "priority": 1 if disk_usage > 90 else 2,
                        "description": f"디스크 사용률 {disk_usage}% (임계값: 80%)",
                        "usage_percent": disk_usage,
                        "threshold": 80,
                        "solution": "디스크 정리 필요 (백업, 캐시, 로그 파일 정리)",
                    }
                )
        except Exception as e:
            issues.append(
                {
                    "category": "performance",
                    "type": "disk_usage_check_failed",
                    "severity": "medium",
                    "priority": 3,
                    "description": f"디스크 사용량 체크 실패: {e!s}",
                }
            )

        return issues

    def detect_connection_issues(self) -> list[dict[str, Any]]:
        """연결 문제 감지"""
        issues = []

        # 1. Redis 연결
        try:
            # Docker 컨테이너 찾기
            result = subprocess.run(
                "docker ps --format '{{.Names}}' | grep -i redis | head -1",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            redis_container = result.stdout.strip() or "docker_config-redis-1"

            # Redis ping 테스트
            result = subprocess.run(
                f"docker exec {redis_container} redis-cli PING 2>/dev/null",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if "PONG" not in result.stdout:
                issues.append(
                    {
                        "category": "connection",
                        "type": "redis_connection",
                        "severity": "critical",
                        "priority": 1,
                        "description": "Redis 연결 실패",
                        "container": redis_container,
                        "output": result.stdout.strip()[:100],
                        "solution": f"docker exec {redis_container} redis-cli PING 확인 또는 컨테이너 재시작",
                    }
                )
        except Exception as e:
            issues.append(
                {
                    "category": "connection",
                    "type": "redis_check_failed",
                    "severity": "high",
                    "priority": 2,
                    "description": f"Redis 체크 실패: {e!s}",
                }
            )

        # 2. PostgreSQL 연결
        try:
            result = subprocess.run(
                "docker ps --format '{{.Names}}' | grep -i postgres | head -1",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            postgres_container = result.stdout.strip() or "docker_config-postgres-1"

            result = subprocess.run(
                f"docker exec {postgres_container} pg_isready -U afo 2>/dev/null",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if "accepting" not in result.stdout:
                issues.append(
                    {
                        "category": "connection",
                        "type": "postgresql_connection",
                        "severity": "critical",
                        "priority": 1,
                        "description": "PostgreSQL 연결 실패",
                        "container": postgres_container,
                        "output": result.stdout.strip()[:100],
                        "solution": f"docker exec {postgres_container} pg_isready 확인 또는 컨테이너 재시작",
                    }
                )
        except Exception as e:
            issues.append(
                {
                    "category": "connection",
                    "type": "postgresql_check_failed",
                    "severity": "high",
                    "priority": 2,
                    "description": f"PostgreSQL 체크 실패: {e!s}",
                }
            )

        # 3. API 서버 연결
        try:
            result = subprocess.run(
                "curl -sf http://localhost:8000/health 2>/dev/null | jq -r '.status' 2>/dev/null || echo 'down'",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            status = result.stdout.strip()
            if status != "healthy":
                issues.append(
                    {
                        "category": "connection",
                        "type": "api_server_connection",
                        "severity": "critical" if status == "down" else "high",
                        "priority": 1 if status == "down" else 2,
                        "description": f"API 서버 상태: {status}",
                        "status": status,
                        "solution": "API 서버 재시작 또는 포트 8000 확인",
                    }
                )
        except Exception as e:
            issues.append(
                {
                    "category": "connection",
                    "type": "api_server_check_failed",
                    "severity": "medium",
                    "priority": 3,
                    "description": f"API 서버 체크 실패: {e!s}",
                }
            )

        return issues

    def detect_security_issues(self) -> list[dict[str, Any]]:
        """보안 문제 감지"""
        issues = []

        # 1. 쿠키 파일
        cookie_patterns = [
            "suno_cookies*.json",
            "*.cookies.json",
            ".cookie_temp",
            ".suno_cookie_temp",
        ]
        for pattern in cookie_patterns:
            try:
                result = subprocess.run(
                    f"find . -name '{pattern}' -type f 2>/dev/null | wc -l",
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=AFO_ROOT,
                    timeout=10,
                )
                count = int(result.stdout.strip() or "0")
                if count > 0:
                    # .gitignore 확인
                    gitignore_path = AFO_ROOT / ".gitignore"
                    gitignore_content = ""
                    if gitignore_path.exists():
                        gitignore_content = gitignore_path.read_text(encoding="utf-8", errors="ignore")

                    if pattern.replace("*", ".*") not in gitignore_content:
                        issues.append(
                            {
                                "category": "security",
                                "type": "cookie_file_exposed",
                                "severity": "critical",
                                "priority": 1,
                                "description": f"쿠키 파일 {count}개 발견 및 .gitignore에 없음",
                                "pattern": pattern,
                                "count": count,
                                "solution": f".gitignore에 '{pattern}' 패턴 추가",
                            }
                        )
            except Exception as e:
                issues.append(
                    {
                        "category": "security",
                        "type": "cookie_check_failed",
                        "severity": "medium",
                        "priority": 3,
                        "description": f"쿠키 파일 체크 실패 ({pattern}): {e!s}",
                    }
                )

        # 2. 디버그 파일
        debug_patterns = [
            "debug_*.png",
            "debug_*.html",
            "debug_*.jpg",
            "debug_*.jpeg",
        ]
        for pattern in debug_patterns:
            try:
                result = subprocess.run(
                    f"find . -maxdepth 1 -name '{pattern}' -type f 2>/dev/null | wc -l",
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=AFO_ROOT,
                    timeout=10,
                )
                count = int(result.stdout.strip() or "0")
                if count > 0:
                    issues.append(
                        {
                            "category": "security",
                            "type": "debug_files_in_root",
                            "severity": "high",
                            "priority": 2,
                            "description": f"루트 디렉토리에 디버그 파일 {count}개 발견",
                            "pattern": pattern,
                            "count": count,
                            "solution": "디버그 파일을 debug_logs/ 디렉토리로 이동",
                        }
                    )
            except Exception:
                pass  # 디버그 파일 체크 실패는 무시

        # 3. 하드코딩된 시크릿 (간단한 체크)
        try:
            # Python 파일만 체크 (venv 제외)
            result = subprocess.run(
                "grep -rn 'password=' --include='*.py' . 2>/dev/null | grep -v venv | grep -v '.env' | wc -l",  # nosec
                shell=True,
                capture_output=True,
                text=True,
                cwd=AFO_ROOT,
                timeout=30,
            )
            count = int(result.stdout.strip() or "0")
            if count > 0:
                issues.append(
                    {
                        "category": "security",
                        "type": "hardcoded_secrets",
                        "severity": "high",
                        "priority": 2,
                        "description": f"하드코딩된 비밀번호 패턴 {count}개 발견",
                        "count": count,
                        "solution": "환경 변수로 변경 필요 (os.getenv 사용)",
                    }
                )
        except Exception:
            pass  # 시크릿 체크 실패는 무시 (너무 느릴 수 있음)

        return issues

    def load_health_report(self) -> dict[str, Any]:
        """check_11_organs.py 결과 로드"""
        try:
            result = subprocess.run(
                ["python3", str(AFO_ROOT / ".claude" / "scripts" / "check_11_organs.py")],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=AFO_ROOT,
            )
            if result.returncode == 0:
                health_data = json.loads(result.stdout)
                return health_data
            else:
                return {"error": "Health check failed", "output": result.stderr[:200]}
        except Exception as e:
            return {"error": f"Health check exception: {e!s}"}

    def calculate_priority(self, problem: dict[str, Any]) -> int:
        """문제 우선순위 계산"""
        severity_weights = {
            "critical": 10,
            "high": 5,
            "medium": 2,
            "low": 1,
        }
        base_priority = severity_weights.get(problem.get("severity", "medium"), 2)

        # Trinity Score 기반 조정
        if "health_percentage" in self.health_report:
            health = self.health_report.get("health_percentage", 100)
            if health < 70:  # 건강도가 낮으면 Critical 문제 우선순위 상향
                if problem.get("severity") == "critical":
                    base_priority += 5

        return base_priority

    def calculate_real_trinity_score(self) -> dict[str, Any]:
        """실제 건강도 기반 Trinity Score 계산"""
        if "error" in self.health_report:
            return {
                "truth": 0.0,
                "goodness": 0.0,
                "beauty": 0.0,
                "filial_serenity": 0.0,
                "trinity_score": 0.0,
                "balance_delta": 0.0,
                "status": "error",
                "message": "건강도 체크 실패 - Trinity Score 계산 불가",
            }

        # 오장육부별 Trinity 분류
        trinity_map = {"眞": [], "善": [], "美": []}
        organs = self.health_report.get("organs", [])

        for organ in organs:
            trinity_type = organ.get("trinity", "")
            is_healthy = organ.get("healthy", False)
            if trinity_type in trinity_map:
                trinity_map[trinity_type].append(1.0 if is_healthy else 0.0)

        # 각 Trinity별 평균 계산
        truth_score = sum(trinity_map["眞"]) / len(trinity_map["眞"]) if trinity_map["眞"] else 0.0
        goodness_score = sum(trinity_map["善"]) / len(trinity_map["善"]) if trinity_map["善"] else 0.0
        beauty_score = sum(trinity_map["美"]) / len(trinity_map["美"]) if trinity_map["美"] else 0.0

        # 전체 건강도 = Filial Serenity (孝)
        health_percentage = self.health_report.get("health_percentage", 0.0)
        filial_serenity = health_percentage / 100.0

        # Trinity Score = (眞 + 善 + 美 + 孝) / 4
        trinity_score = (truth_score + goodness_score + beauty_score + filial_serenity) / 4.0

        # Balance Delta = Max - Min
        values = [truth_score, goodness_score, beauty_score, filial_serenity]
        balance_delta = max(values) - min(values) if values else 0.0

        # Balance 상태 판정
        if balance_delta < 0.3:
            balance_status = "balanced"
        elif balance_delta < 0.5:
            balance_status = "warning"
        else:
            balance_status = "imbalanced"

        # 불균형 문제 자동 감지
        balance_issues = []
        if truth_score < 0.7:
            balance_issues.append(
                {
                    "type": "truth_low",
                    "severity": "high",
                    "description": f"眞(Truth) 점수가 낮습니다: {truth_score:.2%} (목표: 70%+)",
                    "affected_organs": [
                        org.get("organ", "")
                        for org in organs
                        if org.get("trinity") == "眞" and not org.get("healthy", False)
                    ],
                }
            )
        if goodness_score < 0.7:
            balance_issues.append(
                {
                    "type": "goodness_low",
                    "severity": "high",
                    "description": f"善(Goodness) 점수가 낮습니다: {goodness_score:.2%} (목표: 70%+)",
                    "affected_organs": [
                        org.get("organ", "")
                        for org in organs
                        if org.get("trinity") == "善" and not org.get("healthy", False)
                    ],
                }
            )
        if beauty_score < 0.7:
            balance_issues.append(
                {
                    "type": "beauty_low",
                    "severity": "high",
                    "description": f"美(Beauty) 점수가 낮습니다: {beauty_score:.2%} (목표: 70%+)",
                    "affected_organs": [
                        org.get("organ", "")
                        for org in organs
                        if org.get("trinity") == "美" and not org.get("healthy", False)
                    ],
                }
            )
        if balance_delta > 0.3:
            balance_issues.append(
                {
                    "type": "balance_imbalanced",
                    "severity": "high" if balance_delta > 0.5 else "medium",
                    "description": f"Trinity Balance 불균형: Δ={balance_delta:.2%} (목표: <30%)",
                    "max_pillar": max(
                        [("眞", truth_score), ("善", goodness_score), ("美", beauty_score), ("孝", filial_serenity)],
                        key=lambda x: x[1],
                    )[0],
                    "min_pillar": min(
                        [("眞", truth_score), ("善", goodness_score), ("美", beauty_score), ("孝", filial_serenity)],
                        key=lambda x: x[1],
                    )[0],
                }
            )

        return {
            "truth": truth_score,
            "goodness": goodness_score,
            "beauty": beauty_score,
            "filial_serenity": filial_serenity,
            "trinity_score": trinity_score,
            "balance_delta": balance_delta,
            "balance_status": balance_status,
            "status": "calculated",
            "health_percentage": health_percentage,
            "balance_issues": balance_issues,
        }

    def detect_all(self) -> dict[str, Any]:
        """모든 문제 감지"""
        # 오장육부 건강도 로드
        self.health_report = self.load_health_report()

        # 문제 감지
        performance_issues = self.detect_performance_issues()
        connection_issues = self.detect_connection_issues()
        security_issues = self.detect_security_issues()

        all_issues = performance_issues + connection_issues + security_issues

        # 실제 Trinity Score 계산
        trinity_metrics = self.calculate_real_trinity_score()

        # Trinity Balance 불균형 문제를 이슈 목록에 추가
        if trinity_metrics.get("status") == "calculated":
            for balance_issue in trinity_metrics.get("balance_issues", []):
                all_issues.append(
                    {
                        "category": "trinity_balance",
                        "type": balance_issue["type"],
                        "severity": balance_issue["severity"],
                        "priority": 8 if balance_issue["severity"] == "high" else 4,
                        "description": balance_issue["description"],
                        "affected_organs": balance_issue.get("affected_organs", []),
                        "solution": "해당 장기 서비스 복구 필요",
                    }
                )

        # 우선순위 계산 및 정렬
        for issue in all_issues:
            issue["priority"] = self.calculate_priority(issue)

        # 우선순위 순으로 정렬 (높은 것부터)
        all_issues.sort(key=lambda x: x["priority"], reverse=True)

        # 결과 요약
        summary = {
            "critical": sum(1 for i in all_issues if i["severity"] == "critical"),
            "high": sum(1 for i in all_issues if i["severity"] == "high"),
            "medium": sum(1 for i in all_issues if i["severity"] == "medium"),
            "low": sum(1 for i in all_issues if i["severity"] == "low"),
        }

        return {
            "timestamp": datetime.now().isoformat(),
            "health_report": self.health_report,
            "trinity_metrics": trinity_metrics,
            "summary": summary,
            "total_problems": len(all_issues),
            "problems": all_issues,
            "recommendation": self._get_recommendation(summary, all_issues),
        }

    def _get_recommendation(self, summary: dict[str, Any], problems: list[dict[str, Any]]) -> str:
        """권장사항 생성"""
        if summary["critical"] > 0:
            return f"🚨 긴급: Critical 문제 {summary['critical']}개 즉시 해결 필요"
        elif summary["high"] > 0:
            return f"⚠️ 중요: High 문제 {summary['high']}개 빠른 시일 내 해결 권장"
        elif summary["medium"] > 0:
            return f"💡 개선: Medium 문제 {summary['medium']}개 중기 개선 권장"
        else:
            return "✅ 문제 없음: 모든 시스템 정상"


def main():
    """메인 실행"""
    detector = ProblemDetector()
    report = detector.detect_all()

    # JSON 출력
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # 종료 코드 (Critical 문제가 있으면 1 반환)
    exit_code = 0 if report["summary"]["critical"] == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
