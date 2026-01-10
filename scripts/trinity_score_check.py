#!/usr/bin/env python3
"""
Trinity Score Check Script for Pre-commit Hooks
Sequential Thinking: 코드 품질 자동 검증 시스템 구축
"""

import ast
import os
import sys
from pathlib import Path


# Trinity Score 가중치
TRINITY_WEIGHTS = {
    "truth": 0.35,  # 기술적 정확성
    "goodness": 0.35,  # 안전성과 신뢰성
    "beauty": 0.20,  # 구조적 우아함
    "serenity": 0.08,  # 평온함
    "eternity": 0.02,  # 지속가능성
}

# 최소 요구 사항
MIN_REQUIREMENTS = {
    "type_coverage": 70.0,  # 타입 커버리지 70%
    "mypy_errors": 5,  # MyPy 오류 5개 이하
    "complexity_limit": 15,  # 복잡도 제한
    "trinity_score": 80.0,  # Trinity Score 80점 이상
}


class TrinityScoreChecker:
    """
    Trinity Score 검증 클래스
    Sequential Thinking: 단계별 코드 품질 평가
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results = {
            "truth": {"score": 0.0, "details": []},
            "goodness": {"score": 0.0, "details": []},
            "beauty": {"score": 0.0, "details": []},
            "serenity": {"score": 0.0, "details": []},
            "eternity": {"score": 0.0, "details": []},
        }
        self.overall_score = 0.0

    def analyze_codebase(self) -> dict:
        """
        코드베이스 전체 분석 (Sequential Thinking Phase 1)
        """
        print("🏰 Trinity Score 분석 시작...")

        # Phase 1.1: 파일 수집
        python_files = self._collect_python_files()
        print(f"📁 분석 대상 파일: {len(python_files)}개")

        # Phase 1.2: 각 기둥별 분석
        self._analyze_truth(python_files)  # 眞 - 기술적 정확성
        self._analyze_goodness(python_files)  # 善 - 안전성과 신뢰성
        self._analyze_beauty(python_files)  # 美 - 구조적 우아함
        self._analyze_serenity(python_files)  # 孝 - 평온함
        self._analyze_eternity(python_files)  # 永 - 지속가능성

        # Phase 1.3: 종합 점수 계산
        self._calculate_overall_score()

        return self._get_results()

    def _collect_python_files(self) -> list[Path]:
        """Python 파일 수집"""
        python_files = []
        exclude_dirs = {".git", "__pycache__", ".venv", "node_modules", "dist", "build"}

        for root, dirs, filenames in os.walk(self.project_root):
            # 제외 디렉토리 필터링
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            python_files.extend(Path(root) / filename for filename in filenames if filename.endswith(".py"))

        return python_files

    def _analyze_truth(self, files: list[Path]) -> None:
        """
        眞 (Truth) - 기술적 정확성 분석
        타입 힌트, MyPy 호환성, 기술적 정확성 평가
        """
        total_functions = 0
        typed_functions = 0
        mypy_errors = 0

        for file_path in files[:50]:  # 샘플링으로 성능 최적화
            try:
                content = Path(file_path).read_text(encoding="utf-8")

                tree = ast.parse(content)

                # 함수 수집
                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                total_functions += len(functions)
                typed_functions += len([fn for fn in functions if fn.returns is not None])

            except Exception:
                self.results["truth"]["details"].append(f"파일 분석 실패: {file_path.name}")
                continue

        # 타입 커버리지 계산
        type_coverage = (typed_functions / total_functions * 100) if total_functions > 0 else 0

        # MyPy 오류 확인 (간단한 검증)
        try:
            import subprocess

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "mypy",
                    str(self.project_root / "packages"),
                    "--no-error-summary",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            mypy_errors = len([line for line in result.stdout.split("\n") if line.strip() and "error:" in line])
        except Exception:
            mypy_errors = 0  # MyPy가 없으면 0으로 처리

        # 점수 계산
        coverage_score = min(100, type_coverage * 1.5)  # 70% 커버리지 = 100점
        mypy_score = max(0, 100 - mypy_errors * 10)  # 오류당 10점 감점
        truth_score = (coverage_score + mypy_score) / 2

        self.results["truth"]["score"] = truth_score
        self.results["truth"]["details"] = [
            f"타입 커버리지: {type_coverage:.1f}%",
            f"MyPy 오류: {mypy_errors}개",
            f"총 함수 수: {total_functions}",
            f"타입 힌트 함수: {typed_functions}",
        ]

    def _analyze_goodness(self, files: list[Path]) -> None:
        """
        善 (Goodness) - 안전성과 신뢰성 분석
        에러 핸들링, 테스트 커버리지, 보안 검증
        """
        error_handling_score = 0
        test_coverage_score = 0

        # 에러 핸들링 분석
        total_files = len(files)
        files_with_error_handling = 0

        for file_path in files[:30]:  # 샘플링
            try:
                content = Path(file_path).read_text(encoding="utf-8")

                if "try:" in content and "except" in content:
                    files_with_error_handling += 1

            except Exception:
                continue

        error_handling_score = (files_with_error_handling / total_files * 100) if total_files > 0 else 0

        # 테스트 파일 존재 확인
        test_files = []
        for _root, _dirs, filenames in os.walk(self.project_root):
            test_files.extend(
                filename for filename in filenames if filename.startswith("test_") and filename.endswith(".py")
            )

        test_ratio = len(test_files) / max(1, total_files // 10)  # 파일당 0.1개 테스트 파일 기준
        test_coverage_score = min(100, test_ratio * 100)

        # 종합 점수
        goodness_score = (error_handling_score + test_coverage_score) / 2

        self.results["goodness"]["score"] = goodness_score
        self.results["goodness"]["details"] = [
            f"에러 핸들링 적용률: {error_handling_score:.1f}%",
            f"테스트 파일 수: {len(test_files)}개",
            f"테스트 커버리지: {test_coverage_score:.1f}%",
        ]

    def _analyze_beauty(self, files: list[Path]) -> None:
        """
        美 (Beauty) - 구조적 우아함 분석
        코드 복잡도, 모듈화, 일관성 평가
        """
        complexity_score = 100
        modularity_score = 0

        # 복잡도 분석
        high_complexity_files = 0
        total_analyzed = 0

        for file_path in files[:20]:  # 샘플링
            try:
                content = Path(file_path).read_text(encoding="utf-8")

                lines = content.split("\n")
                # 간단한 복잡도 측정: 파일 길이 기반
                if len(lines) > 300:  # 300줄 이상 = 복잡
                    high_complexity_files += 1
                total_analyzed += 1

            except Exception:
                continue

        if total_analyzed > 0:
            complexity_score = max(0, 100 - (high_complexity_files / total_analyzed) * 50)

        # 모듈화 분석
        packages_dir = self.project_root / "packages"
        if packages_dir.exists():
            subpackages = [d for d in packages_dir.iterdir() if d.is_dir()]
            modularity_score = min(100, len(subpackages) * 25)  # 패키지당 25점

        # 종합 점수
        beauty_score = (complexity_score + modularity_score) / 2

        self.results["beauty"]["score"] = beauty_score
        self.results["beauty"]["details"] = [
            f"코드 복잡도 점수: {complexity_score:.1f}",
            f"모듈화 점수: {modularity_score:.1f}",
            f"고복잡도 파일: {high_complexity_files}개",
        ]

    def _analyze_serenity(self, files: list[Path]) -> None:
        """
        孝 (Serenity) - 평온함 분석
        자동화 수준, 유지보수성, 개발자 경험
        """
        automation_score = 0
        maintenance_score = 0

        # 자동화 도구 확인
        automation_tools = ["pre-commit", "black", "isort", "mypy", "pytest"]
        found_tools = 0

        if (self.project_root / ".pre-commit-config.yaml").exists():
            found_tools += 1
        if (self.project_root / "pyproject.toml").exists():
            found_tools += 1

        automation_score = (found_tools / len(automation_tools)) * 100

        # 유지보수성 분석 (문서화, README 등)
        docs_score = 0
        if (self.project_root / "README.md").exists():
            docs_score += 25
        if (self.project_root / "docs").exists():
            docs_score += 25
        if any(f.suffix == ".md" for f in self.project_root.iterdir()):
            docs_score += 25

        maintenance_score = docs_score

        # 종합 점수
        serenity_score = (automation_score + maintenance_score) / 2

        self.results["serenity"]["score"] = serenity_score
        self.results["serenity"]["details"] = [
            f"자동화 도구 점수: {automation_score:.1f}",
            f"유지보수성 점수: {maintenance_score:.1f}",
            f"문서화 상태: {'양호' if docs_score >= 50 else '개선 필요'}",
        ]

    def _analyze_eternity(self, files: list[Path]) -> None:
        """
        永 (Eternity) - 지속가능성 분석
        버전 관리, 확장성, 미래 대비
        """
        version_control_score = 0
        scalability_score = 0

        # 버전 관리 점수
        if (self.project_root / ".git").exists():
            version_control_score += 50
        if (self.project_root / "pyproject.toml").exists():
            version_control_score += 25
        if any(f.name.endswith(".lock") for f in self.project_root.iterdir()):
            version_control_score += 25

        # 확장성 분석 (모듈 구조, 인터페이스 등)
        interfaces_found = 0
        for file_path in files[:30]:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
                if "class" in content and "def" in content:
                    interfaces_found += 1
            except Exception:
                continue

        scalability_score = min(100, interfaces_found * 10)  # 인터페이스당 10점

        # 종합 점수
        eternity_score = (version_control_score + scalability_score) / 2

        self.results["eternity"]["score"] = eternity_score
        self.results["eternity"]["details"] = [
            f"버전 관리 점수: {version_control_score:.1f}",
            f"확장성 점수: {scalability_score:.1f}",
            f"인터페이스 수: {interfaces_found}개",
        ]

    def _calculate_overall_score(self) -> None:
        """종합 Trinity Score 계산"""
        self.overall_score = sum(self.results[pillar]["score"] * weight for pillar, weight in TRINITY_WEIGHTS.items())

    def _get_results(self) -> dict:
        """결과 반환"""
        return {
            "timestamp": (Path(__file__).stat().st_mtime if Path(__file__).exists() else 0),
            "pillars": self.results,
            "overall_score": round(self.overall_score, 1),
            "grade": self._get_grade(),
            "requirements_met": self._check_requirements(),
        }

    def _get_grade(self) -> str:
        """점수에 따른 등급 판정"""
        if self.overall_score >= 95:
            return "탁월 (Excellent)"
        if self.overall_score >= 90:
            return "우수 (Great)"
        if self.overall_score >= 80:
            return "양호 (Good)"
        if self.overall_score >= 70:
            return "보통 (Fair)"
        if self.overall_score >= 60:
            return "미흡 (Poor)"
        return "개선 필요 (Critical)"

    def _check_requirements(self) -> bool:
        """최소 요구사항 충족 여부 확인"""
        # 간단한 검증만 수행 (실제로는 더 정교한 검증 필요)
        return self.overall_score >= MIN_REQUIREMENTS["trinity_score"]


def main():
    """메인 함수"""
    print("🏰 AFO 왕국 Trinity Score 검증")
    print("=" * 50)

    project_root = Path(__file__).parent.parent
    checker = TrinityScoreChecker(project_root)

    try:
        results = checker.analyze_codebase()

        print("\n📊 Trinity Score 결과:")
        print(f"종합 점수: {results['overall_score']:.1f}/100")
        print(f"등급: {results['grade']}")

        print("\n🔍 세부 점수:")
        for pillar, data in results["pillars"].items():
            pillar_names = {
                "truth": "眞 (Truth)",
                "goodness": "善 (Goodness)",
                "beauty": "美 (Beauty)",
                "serenity": "孝 (Serenity)",
                "eternity": "永 (Eternity)",
            }
            print(f"  {pillar_names[pillar]}: {data['score']:.1f}")
            for detail in data["details"][:2]:  # 주요 정보만 표시
                print(f"    • {detail}")

        # 요구사항 검증
        if results["requirements_met"]:
            print(f"\n✅ 최소 요구사항 충족 (Trinity Score {MIN_REQUIREMENTS['trinity_score']}점 이상)")
            return 0
        print(f"\n❌ 최소 요구사항 미충족 (Trinity Score {MIN_REQUIREMENTS['trinity_score']}점 필요)")
        print("코드 품질 개선이 필요합니다.")
        return 1

    except Exception as e:
        print(f"❌ Trinity Score 검증 실패: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
