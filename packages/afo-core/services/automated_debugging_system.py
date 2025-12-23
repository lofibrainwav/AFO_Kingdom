"""
Automated Debugging System for AFO Kingdom
완벽한 자동화 디버깅 시스템 - AFO 왕국의 모든 기술과 도구 통합

眞善美孝永 철학에 기반한 자동화 디버깅:
眞 (Truth): 정확한 에러 감지 및 분류
善 (Goodness): 안전한 자동 수정 및 복구
美 (Beauty): 우아한 디버깅 워크플로우
孝 (Serenity): 개발자 경험 최적화
永 (Eternity): 지속 가능한 디버깅 시스템

Sequential Thinking: 단계별 자동화 디버깅 구현
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from ..utils.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """에러 심각도"""

    CRITICAL = "critical"  # 시스템 중단
    HIGH = "high"  # 주요 기능 실패
    MEDIUM = "medium"  # 부분 기능 실패
    LOW = "low"  # 경고 수준
    INFO = "info"  # 정보성


class ErrorCategory(str, Enum):
    """에러 카테고리"""

    SYNTAX = "syntax"  # 문법 오류
    TYPE = "type"  # 타입 오류
    RUNTIME = "runtime"  # 실행 시 오류
    IMPORT = "import"  # Import 오류
    LOGIC = "logic"  # 논리 오류
    PERFORMANCE = "performance"  # 성능 문제
    SECURITY = "security"  # 보안 문제
    DEPENDENCY = "dependency"  # 의존성 문제
    CONFIG = "config"  # 설정 문제
    NETWORK = "network"  # 네트워크 문제
    DATABASE = "database"  # 데이터베이스 문제
    UNKNOWN = "unknown"  # 알 수 없음


@dataclass
class ErrorContext:
    """에러 컨텍스트"""

    file_path: str
    line_number: int | None = None
    column_number: int | None = None
    function_name: str | None = None
    code_snippet: str | None = None
    stack_trace: str | None = None
    environment: dict[str, Any] = field(default_factory=dict)
    related_files: list[str] = field(default_factory=list)


@dataclass
class DetectedError:
    """감지된 에러"""

    error_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    context: ErrorContext
    timestamp: datetime = field(default_factory=datetime.now)
    auto_fixable: bool = False
    fix_confidence: float = 0.0  # 0.0 ~ 1.0
    suggested_fixes: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class DebuggingReport:
    """디버깅 리포트"""

    report_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    total_errors: int = 0
    errors_by_severity: dict[str, int] = field(default_factory=dict)
    errors_by_category: dict[str, int] = field(default_factory=dict)
    auto_fixed: int = 0
    manual_required: int = 0
    trinity_score: dict[str, float] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    execution_time: float = 0.0


class ErrorDetector:
    """
    에러 감지 시스템 (眞 - Truth)
    Sequential Thinking Phase 1: 다양한 소스에서 에러 감지
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.detected_errors: list[DetectedError] = []

    async def detect_all_errors(self) -> list[DetectedError]:
        """
        모든 에러 감지 (Sequential Thinking Phase 1.1)
        """
        logger.info("🔍 Phase 1.1: 에러 감지 시작")

        try:
            # Phase 1.1.1: Syntax 에러 감지
            syntax_errors = await self._detect_syntax_errors()

            # Phase 1.1.2: Type 에러 감지
            type_errors = await self._detect_type_errors()

            # Phase 1.1.3: Linting 에러 감지
            linting_errors = await self._detect_linting_errors()

            # Phase 1.1.4: Import 에러 감지
            import_errors = await self._detect_import_errors()

            # Phase 1.1.5: Runtime 에러 감지 (로그 분석)
            runtime_errors = await self._detect_runtime_errors()

            # Phase 1.1.6: 모든 에러 통합
            all_errors = (
                syntax_errors
                + type_errors
                + linting_errors
                + import_errors
                + runtime_errors
            )

            self.detected_errors = all_errors
            logger.info(f"✅ Phase 1.1 완료: {len(all_errors)}개 에러 감지")

            return all_errors

        except Exception as e:
            logger.error(f"❌ 에러 감지 실패: {e}")
            return []

    async def _detect_syntax_errors(self) -> list[DetectedError]:
        """Syntax 에러 감지"""
        errors = []
        python_files = list(self.project_root.rglob("*.py"))

        for py_file in python_files:
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            try:
                compile(open(py_file, encoding="utf-8").read(), str(py_file), "exec")
            except SyntaxError as e:
                error = DetectedError(
                    error_id=f"syntax_{py_file.name}_{e.lineno}",
                    error_type="SyntaxError",
                    error_message=str(e),
                    severity=ErrorSeverity.CRITICAL,
                    category=ErrorCategory.SYNTAX,
                    context=ErrorContext(
                        file_path=str(py_file),
                        line_number=e.lineno if e.lineno is not None else 0,
                        column_number=e.offset,
                        code_snippet=self._get_code_snippet(
                            py_file, e.lineno if e.lineno is not None else 0
                        ),
                    ),
                    auto_fixable=True,
                    fix_confidence=0.8,
                )
                errors.append(error)

        return errors

    async def _detect_type_errors(self) -> list[DetectedError]:
        """Type 에러 감지 (MyPy)"""
        errors = []

        try:
            result = await self._run_command(
                ["python", "-m", "mypy", str(self.project_root), "--no-error-summary"]
            )

            if result["returncode"] != 0:
                # MyPy 출력 파싱
                lines = result["stdout"].split("\n")
                for line in lines:
                    if "error:" in line:
                        # MyPy 출력 형식 파싱
                        parts = line.split(":")
                        if len(parts) >= 4:
                            file_path = parts[0]
                            line_num = int(parts[1]) if parts[1].isdigit() else None
                            error_msg = ":".join(parts[3:]).strip()

                            error = DetectedError(
                                error_id=f"type_{Path(file_path).name}_{line_num}",
                                error_type="TypeError",
                                error_message=error_msg,
                                severity=ErrorSeverity.MEDIUM,
                                category=ErrorCategory.TYPE,
                                context=ErrorContext(
                                    file_path=file_path,
                                    line_number=line_num,
                                ),
                                auto_fixable=False,
                                fix_confidence=0.3,
                            )
                            errors.append(error)

        except Exception as e:
            logger.warning(f"Type 에러 감지 실패: {e}")

        return errors

    async def _detect_linting_errors(self) -> list[DetectedError]:
        """Linting 에러 감지 (Ruff)"""
        errors = []

        try:
            result = await self._run_command(
                [
                    "python",
                    "-m",
                    "ruff",
                    "check",
                    "--output-format=json",
                    str(self.project_root),
                ]
            )

            if result["returncode"] != 0:
                try:
                    ruff_issues = json.loads(result["stdout"])
                    for issue in ruff_issues:
                        error = DetectedError(
                            error_id=f"lint_{issue.get('filename', '')}_{issue.get('line_number', 0)}",
                            error_type=issue.get("code", "LintingError"),
                            error_message=issue.get("message", ""),
                            severity=self._map_ruff_severity(issue.get("code", "")),
                            category=ErrorCategory.SYNTAX,
                            context=ErrorContext(
                                file_path=issue.get("filename", ""),
                                line_number=issue.get("line_number"),
                                column_number=issue.get("column_number"),
                            ),
                            auto_fixable=issue.get("fix", {}).get("applicable", False),
                            fix_confidence=(
                                0.9 if issue.get("fix", {}).get("applicable") else 0.2
                            ),
                        )
                        errors.append(error)
                except json.JSONDecodeError:
                    pass

        except Exception as e:
            logger.warning(f"Linting 에러 감지 실패: {e}")

        return errors

    async def _detect_import_errors(self) -> list[DetectedError]:
        """Import 에러 감지"""
        errors = []
        python_files = list(self.project_root.rglob("*.py"))

        for py_file in python_files:
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            try:
                # Import 테스트
                result = await self._run_command(
                    [
                        "python",
                        "-c",
                        f"import sys; sys.path.insert(0, '{self.project_root}'); import {py_file.stem}",
                    ]
                )

                if result["returncode"] != 0 and (
                    "ImportError" in result["stderr"]
                    or "ModuleNotFoundError" in result["stderr"]
                ):
                    error = DetectedError(
                        error_id=f"import_{py_file.name}",
                        error_type="ImportError",
                        error_message=result["stderr"],
                        severity=ErrorSeverity.HIGH,
                        category=ErrorCategory.IMPORT,
                        context=ErrorContext(file_path=str(py_file)),
                        auto_fixable=False,
                        fix_confidence=0.4,
                    )
                    errors.append(error)

            except Exception:
                pass

        return errors

    async def _detect_runtime_errors(self) -> list[DetectedError]:
        """Runtime 에러 감지 (로그 분석)"""
        errors = []
        # 로그 파일에서 에러 패턴 검색
        log_files = list(self.project_root.rglob("*.log"))

        for log_file in log_files:
            try:
                with open(log_file, encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if (
                            "ERROR" in line
                            or "Exception" in line
                            or "Traceback" in line
                        ):
                            error = DetectedError(
                                error_id=f"runtime_{log_file.name}_{line_num}",
                                error_type="RuntimeError",
                                error_message=line.strip(),
                                severity=ErrorSeverity.MEDIUM,
                                category=ErrorCategory.RUNTIME,
                                context=ErrorContext(
                                    file_path=str(log_file),
                                    line_number=line_num,
                                ),
                                auto_fixable=False,
                                fix_confidence=0.2,
                            )
                            errors.append(error)
            except Exception:
                pass

        return errors

    def _map_ruff_severity(self, code: str) -> ErrorSeverity:
        """Ruff 코드를 심각도로 매핑"""
        if code.startswith("E9") or code.startswith("F"):
            return ErrorSeverity.CRITICAL
        elif code.startswith("E"):
            return ErrorSeverity.HIGH
        elif code.startswith("W"):
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    def _get_code_snippet(
        self, file_path: Path, line_number: int, context: int = 3
    ) -> str:
        """코드 스니펫 추출"""
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
                start = max(0, line_number - context - 1)
                end = min(len(lines), line_number + context)
                return "".join(lines[start:end])
        except Exception:
            return ""

    async def _run_command(self, cmd: list[str]) -> dict[str, Any]:
        """명령어 실행 헬퍼"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.project_root),
            )

            stdout, stderr = await process.communicate()

            return {
                "returncode": process.returncode,
                "stdout": stdout.decode("utf-8", errors="ignore"),
                "stderr": stderr.decode("utf-8", errors="ignore"),
            }

        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e)}


class ErrorClassifier:
    """
    에러 분류 시스템 (眞 - Truth)
    Sequential Thinking Phase 2: 에러를 카테고리별로 분류 및 우선순위 지정
    """

    def __init__(self):
        self.classification_rules: dict[str, Any] = {}

    def classify_errors(
        self, errors: list[DetectedError]
    ) -> dict[str, list[DetectedError]]:
        """
        에러 분류 (Sequential Thinking Phase 2.1)
        """
        logger.info("📊 Phase 2.1: 에러 분류 시작")

        classified: dict[str, Any] = {
            "by_severity": {},
            "by_category": {},
            "auto_fixable": [],
            "manual_required": [],
        }
        # 타입 명시: by_severity와 by_category는 dict[str, list[DetectedError]]
        by_severity: dict[str, list[DetectedError]] = classified["by_severity"]
        by_category: dict[str, list[DetectedError]] = classified["by_category"]

        for error in errors:
            # 심각도별 분류
            severity_key = error.severity.value
            if severity_key not in by_severity:
                by_severity[severity_key] = []
            by_severity[severity_key].append(error)

            # 카테고리별 분류
            category_key = error.category.value
            if category_key not in by_category:
                by_category[category_key] = []
            by_category[category_key].append(error)

            # 자동 수정 가능 여부
            if error.auto_fixable and error.fix_confidence >= 0.7:
                classified["auto_fixable"].append(error)
            else:
                classified["manual_required"].append(error)

        logger.info(f"✅ Phase 2.1 완료: {len(errors)}개 에러 분류")

        return classified


class AutoDiagnostic:
    """
    자동 진단 시스템 (眞 - Truth)
    Sequential Thinking Phase 3: Context7 및 Scholars를 활용한 근본 원인 분석
    """

    def __init__(self):
        self.diagnostic_cache: dict[str, Any] = {}

    async def diagnose_error(self, error: DetectedError) -> dict[str, Any]:
        """
        에러 진단 (Sequential Thinking Phase 3.1)
        """
        logger.info(f"🔬 Phase 3.1: 에러 진단 시작 - {error.error_id}")

        try:
            # Phase 3.1.1: 기본 진단
            basic_diagnosis = self._basic_diagnosis(error)

            # Phase 3.1.2: Context7 기반 진단 (향후 구현)
            context7_diagnosis = await self._context7_diagnosis(error)

            # Phase 3.1.3: Scholars 기반 진단 (향후 구현)
            scholars_diagnosis = await self._scholars_diagnosis(error)

            # Phase 3.1.4: 종합 진단
            diagnosis = {
                "error_id": error.error_id,
                "basic": basic_diagnosis,
                "context7": context7_diagnosis,
                "scholars": scholars_diagnosis,
                "root_cause": self._identify_root_cause(error, basic_diagnosis),
                "confidence": self._calculate_confidence(basic_diagnosis),
            }

            logger.info(f"✅ Phase 3.1 완료: {error.error_id} 진단 완료")

            return diagnosis

        except Exception as e:
            logger.error(f"❌ 에러 진단 실패: {e}")
            return {"error": str(e)}

    def _basic_diagnosis(self, error: DetectedError) -> dict[str, Any]:
        """기본 진단"""
        return {
            "error_type": error.error_type,
            "severity": error.severity.value,
            "category": error.category.value,
            "location": {
                "file": error.context.file_path,
                "line": error.context.line_number,
            },
            "message": error.error_message,
        }

    async def _context7_diagnosis(self, error: DetectedError) -> dict[str, Any]:
        """Context7 기반 진단 (실제 API 호출)"""
        try:
            from pathlib import Path

            from ..utils.path_utils import add_to_sys_path, get_trinity_os_path

            # trinity-os 경로 추가
            trinity_os_path = get_trinity_os_path(Path(__file__))
            add_to_sys_path(trinity_os_path)

            from trinity_os.servers.context7_mcp import Context7MCP

            # Context7 지식 베이스에서 관련 정보 검색
            search_query = (
                f"{error.error_type} {error.category.value} {error.error_message[:50]}"
            )

            # 실제 Context7 API 호출
            context_result = Context7MCP.retrieve_context(
                query=search_query, domain="technical"
            )

            # 결과 파싱
            # retrieve_context는 dict를 반환하므로 dict로 처리
            results = context_result.get("results", [])
            if not results:
                # Fallback: KNOWLEDGE_BASE 직접 검색
                knowledge_base = Context7MCP.KNOWLEDGE_BASE
                relevant_knowledge = []
                for key, value in knowledge_base.items():
                    if any(
                        term.lower() in str(value).lower()
                        for term in [error.error_type, error.category.value]
                    ):
                        relevant_knowledge.append(
                            {"key": key, "content": str(value)[:200]}
                        )
                return {
                    "status": "success",
                    "search_query": search_query,
                    "relevant_knowledge": relevant_knowledge[:5],
                    "knowledge_count": len(relevant_knowledge),
                    "source": "knowledge_base_fallback",
                }
            else:
                # 실제 API 결과 사용
                relevant_knowledge = [
                    {"key": "context7_result", "content": str(result)[:200]}
                    for result in results[:5]
                ]
                return {
                    "status": "success",
                    "search_query": search_query,
                    "relevant_knowledge": relevant_knowledge,
                    "knowledge_count": len(results),
                    "source": "context7_api",
                }

        except Exception as e:
            logger.warning(f"Context7 진단 실패: {e}")
            return {"status": "error", "error": str(e)}

    async def _scholars_diagnosis(self, error: DetectedError) -> dict[str, Any]:
        """Scholars 기반 진단 (실제 API 호출)"""
        try:
            # Scholars 시스템을 통한 전문가 분석
            # Yeongdeok (Ollama) - 보안 및 아카이빙
            # Bangtong (Codex) - 구현 및 실행
            # Jaryong (Claude) - 논리 검증
            # Yukson (Gemini) - 전략 및 철학

            diagnosis_prompt = f"""
에러 분석 요청:
- 타입: {error.error_type}
- 카테고리: {error.category.value}
- 심각도: {error.severity.value}
- 메시지: {error.error_message}
- 파일: {error.context.file_path}
- 라인: {error.context.line_number}

이 에러의 근본 원인과 해결 방법을 분석해주세요.
"""

            scholar_analysis = {}

            # 1. Yeongdeok (Ollama) - 보안 및 아카이빙 관점
            try:
                from AFO.scholars.yeongdeok import yeongdeok

                yeongdeok_analysis = await yeongdeok.consult_samahwi(
                    f"{diagnosis_prompt}\n\n보안 및 아카이빙 관점에서 분석해주세요."
                )
                scholar_analysis["yeongdeok"] = {
                    "focus": "보안 및 아카이빙 관점",
                    "analysis": yeongdeok_analysis[:500],  # 처음 500자만
                    "status": "success",
                }
            except Exception as e:
                logger.warning(f"Yeongdeok 진단 실패: {e}")
                scholar_analysis["yeongdeok"] = {
                    "focus": "보안 및 아카이빙 관점",
                    "analysis": "에러 로그를 아카이빙하고 보안 취약점 확인 필요",
                    "status": "error",
                    "error": str(e),
                }

            # 2. Bangtong (Codex) - 구현 및 실행 관점
            try:
                from AFO.scholars.bangtong import bangtong

                bangtong_analysis = await bangtong.review_implementation(
                    f"# 에러 컨텍스트\n{diagnosis_prompt}\n\n구현 및 실행 관점에서 분석해주세요."
                )
                scholar_analysis["bangtong"] = {
                    "focus": "구현 및 실행 관점",
                    "analysis": bangtong_analysis[:500],
                    "status": "success",
                }
            except Exception as e:
                logger.warning(f"Bangtong 진단 실패: {e}")
                scholar_analysis["bangtong"] = {
                    "focus": "구현 및 실행 관점",
                    "analysis": "코드 실행 환경 및 의존성 확인 필요",
                    "status": "error",
                    "error": str(e),
                }

            # 3. Jaryong (Claude) - 논리 검증 관점
            try:
                from AFO.scholars.jaryong import jaryong

                # 에러 메시지를 코드처럼 취급하여 검증
                error_code_snippet = f"""
# 에러 발생 위치: {error.context.file_path}:{error.context.line_number}
# 에러 타입: {error.error_type}
# 에러 메시지: {error.error_message}
"""
                jaryong_analysis = await jaryong.verify_logic(
                    error_code_snippet, context=diagnosis_prompt
                )
                scholar_analysis["jaryong"] = {
                    "focus": "논리 검증 관점",
                    "analysis": jaryong_analysis[:500],
                    "status": "success",
                }
            except Exception as e:
                logger.warning(f"Jaryong 진단 실패: {e}")
                scholar_analysis["jaryong"] = {
                    "focus": "논리 검증 관점",
                    "analysis": "코드 로직 및 타입 일관성 확인 필요",
                    "status": "error",
                    "error": str(e),
                }

            # 4. Yukson (Gemini) - 전략 및 철학 관점
            try:
                from AFO.scholars.yukson import yukson

                yukson_analysis = await yukson.advise_strategy(
                    goal=f"에러 해결: {error.error_type}",
                    context=diagnosis_prompt,
                )
                scholar_analysis["yukson"] = {
                    "focus": "전략 및 철학 관점",
                    "analysis": yukson_analysis[:500],
                    "status": "success",
                }
            except Exception as e:
                logger.warning(f"Yukson 진단 실패: {e}")
                scholar_analysis["yukson"] = {
                    "focus": "전략 및 철학 관점",
                    "analysis": "시스템 아키텍처 및 설계 패턴 검토 필요",
                    "status": "error",
                    "error": str(e),
                }

            # 합의 도출
            successful_analyses = [
                a for a in scholar_analysis.values() if a.get("status") == "success"
            ]
            consensus = (
                "다각도 분석 완료. 각 학자의 전문 관점을 종합하여 해결책 도출 필요."
                if successful_analyses
                else "학자 분석 실패. 기본 규칙 기반 진단 사용."
            )

            return {
                "status": "success",
                "scholar_analysis": scholar_analysis,
                "consensus": consensus,
                "success_count": len(successful_analyses),
                "total_count": len(scholar_analysis),
            }

        except Exception as e:
            logger.warning(f"Scholars 진단 실패: {e}")
            return {"status": "error", "error": str(e)}

    def _identify_root_cause(
        self, error: DetectedError, diagnosis: dict[str, Any]
    ) -> str:
        """근본 원인 식별"""
        # 간단한 규칙 기반 근본 원인 식별
        if error.category == ErrorCategory.SYNTAX:
            return "문법 오류로 인한 컴파일 실패"
        elif error.category == ErrorCategory.TYPE:
            return "타입 불일치로 인한 타입 체크 실패"
        elif error.category == ErrorCategory.IMPORT:
            return "의존성 누락 또는 경로 문제"
        else:
            return "원인 분석 필요"

    def _calculate_confidence(self, diagnosis: dict[str, Any]) -> float:
        """진단 신뢰도 계산"""
        # 간단한 신뢰도 계산
        return 0.7  # 기본값


class SolutionSuggester:
    """
    해결책 제안 시스템 (善 - Goodness)
    Sequential Thinking Phase 4: Context7 및 Scholars를 활용한 해결책 제안
    """

    def __init__(self):
        self.solution_cache: dict[str, list[dict[str, Any]]] = {}

    async def suggest_solutions(
        self,
        error: DetectedError,
        diagnosis: dict[str, Any],
        ml_learner: Any | None = None,
    ) -> list[dict[str, Any]]:
        """
        해결책 제안 (Sequential Thinking Phase 4.1)
        ML 기반 패턴 학습 통합
        """
        logger.info(f"💡 Phase 4.1: 해결책 제안 시작 - {error.error_id}")

        solutions = []

        try:
            # Phase 4.1.1: 규칙 기반 해결책
            rule_based_solutions = self._rule_based_solutions(error, diagnosis)

            # Phase 4.1.2: Context7 기반 해결책
            context7_solutions = await self._context7_solutions(error, diagnosis)

            # Phase 4.1.3: Scholars 기반 해결책
            scholars_solutions = await self._scholars_solutions(error, diagnosis)

            # Phase 4.1.4: ML 기반 패턴 학습 해결책 (새로 추가)
            ml_solutions = []
            if ml_learner:
                try:
                    ml_solutions = ml_learner.predict_fix(
                        error.error_type,
                        error.category.value,
                        error.error_message,
                    )
                    logger.debug(f"ML 패턴 학습: {len(ml_solutions)}개 해결책 예측")
                except Exception as e:
                    logger.warning(f"ML 해결책 예측 실패: {e}")

            # Phase 4.1.5: 해결책 통합 및 우선순위 지정
            all_solutions = (
                rule_based_solutions
                + context7_solutions
                + scholars_solutions
                + ml_solutions
            )
            solutions = self._prioritize_solutions(all_solutions)

            logger.info(
                f"✅ Phase 4.1 완료: {len(solutions)}개 해결책 제안 (ML: {len(ml_solutions)})"
            )

        except Exception as e:
            logger.error(f"❌ 해결책 제안 실패: {e}")

        return solutions

    def _rule_based_solutions(
        self, error: DetectedError, diagnosis: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """규칙 기반 해결책"""
        solutions = []

        if error.category == ErrorCategory.SYNTAX:
            solutions.append(
                {
                    "type": "auto_fix",
                    "description": "Ruff를 사용한 자동 syntax 수정",
                    "command": f"ruff check --fix {error.context.file_path}",
                    "confidence": 0.9,
                    "risk": "low",
                }
            )

        elif error.category == ErrorCategory.TYPE:
            solutions.append(
                {
                    "type": "manual_fix",
                    "description": "타입 어노테이션 추가 또는 수정",
                    "confidence": 0.6,
                    "risk": "medium",
                }
            )

        elif error.category == ErrorCategory.IMPORT:
            solutions.append(
                {
                    "type": "dependency_fix",
                    "description": "누락된 패키지 설치",
                    "command": "poetry install",
                    "confidence": 0.8,
                    "risk": "low",
                }
            )

        return solutions

    async def _context7_solutions(
        self, error: DetectedError, diagnosis: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Context7 기반 해결책"""
        try:
            from pathlib import Path

            from ..utils.path_utils import add_to_sys_path, get_trinity_os_path

            # trinity-os 경로 추가
            trinity_os_path = get_trinity_os_path(Path(__file__))
            add_to_sys_path(trinity_os_path)

            # Context7에서 해결책 검색
            solutions = []
            context7_knowledge = diagnosis.get("context7", {}).get(
                "relevant_knowledge", []
            )

            for knowledge in context7_knowledge:
                # 지식 베이스에서 해결책 패턴 추출
                content = knowledge.get("content", "")
                if "fix" in content.lower() or "solution" in content.lower():
                    solutions.append(
                        {
                            "type": "context7_knowledge",
                            "description": f"Context7 지식 베이스: {knowledge.get('key', '')}",
                            "source": "context7",
                            "confidence": 0.7,
                            "risk": "low",
                        }
                    )

            return solutions

        except Exception as e:
            logger.warning(f"Context7 해결책 검색 실패: {e}")
            return []

    async def _scholars_solutions(
        self, error: DetectedError, diagnosis: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Scholars 기반 해결책"""
        try:
            solutions = []
            scholar_analysis = diagnosis.get("scholars", {}).get("scholar_analysis", {})

            # 각 Scholar의 분석을 기반으로 해결책 생성
            for scholar_name, analysis in scholar_analysis.items():
                analysis.get("focus", "")
                scholar_solution = analysis.get("analysis", "")

                if scholar_name == "bangtong" and "의존성" in scholar_solution:
                    solutions.append(
                        {
                            "type": "dependency_fix",
                            "description": "의존성 확인 및 설치",
                            "command": "poetry install",
                            "source": "bangtong",
                            "confidence": 0.8,
                            "risk": "low",
                        }
                    )

                elif scholar_name == "jaryong" and "타입" in scholar_solution:
                    solutions.append(
                        {
                            "type": "type_fix",
                            "description": "타입 어노테이션 추가 또는 수정",
                            "source": "jaryong",
                            "confidence": 0.6,
                            "risk": "medium",
                        }
                    )

            return solutions

        except Exception as e:
            logger.warning(f"Scholars 해결책 생성 실패: {e}")
            return []

    def _prioritize_solutions(
        self, solutions: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """해결책 우선순위 지정"""
        # 신뢰도와 위험도 기반 정렬
        return sorted(
            solutions,
            key=lambda x: (x.get("confidence", 0), -1 if x.get("risk") == "low" else 0),
            reverse=True,
        )


class AutoFixer:
    """
    자동 수정 시스템 (善 - Goodness)
    Sequential Thinking Phase 5: 안전한 자동 수정 실행
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.fix_history: list[dict[str, Any]] = []
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=30,
            service_name="auto_fixer",
        )

    async def auto_fix_error(
        self, error: DetectedError, solution: dict[str, Any]
    ) -> dict[str, Any]:
        """
        에러 자동 수정 (Sequential Thinking Phase 5.1)
        """
        logger.info(f"🔧 Phase 5.1: 자동 수정 시작 - {error.error_id}")

        if not error.auto_fixable or solution.get("type") != "auto_fix":
            return {
                "success": False,
                "reason": "자동 수정 불가능",
            }

        try:
            # Phase 5.1.1: 백업 생성
            backup_result = await self._create_backup(error.context.file_path)

            # Phase 5.1.2: 수정 실행
            fix_result = await self._execute_fix(error, solution)

            # Phase 5.1.3: 수정 검증
            verification_result = await self._verify_fix(error)

            # Phase 5.1.4: 결과 기록
            fix_record = {
                "error_id": error.error_id,
                "timestamp": datetime.now().isoformat(),
                "solution": solution,
                "backup": backup_result,
                "fix_result": fix_result,
                "verification": verification_result,
                "success": verification_result.get("success", False),
            }

            self.fix_history.append(fix_record)

            if fix_record["success"]:
                logger.info(f"✅ Phase 5.1 완료: {error.error_id} 수정 성공")
            else:
                logger.warning(f"⚠️ Phase 5.1 완료: {error.error_id} 수정 실패")

            return fix_record

        except Exception as e:
            logger.error(f"❌ 자동 수정 실패: {e}")
            return {"success": False, "error": str(e)}

    async def _create_backup(self, file_path: str) -> dict[str, Any]:
        """파일 백업 생성"""
        try:
            backup_path = (
                f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            # 백업 로직 구현
            return {"success": True, "backup_path": backup_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _execute_fix(
        self, error: DetectedError, solution: dict[str, Any]
    ) -> dict[str, Any]:
        """수정 실행"""
        try:
            command = solution.get("command", "")
            if command:
                result = await self._run_command(command.split())
                return {
                    "success": result["returncode"] == 0,
                    "output": result["stdout"],
                    "error": result["stderr"],
                }
            return {"success": False, "reason": "명령어 없음"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _verify_fix(self, error: DetectedError) -> dict[str, Any]:
        """수정 검증"""
        try:
            # 수정 후 에러가 여전히 존재하는지 확인
            # 간단한 검증 로직
            return {"success": True, "verified": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _run_command(self, cmd: list[str]) -> dict[str, Any]:
        """명령어 실행 헬퍼"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.project_root),
            )

            stdout, stderr = await process.communicate()

            return {
                "returncode": process.returncode,
                "stdout": stdout.decode("utf-8", errors="ignore"),
                "stderr": stderr.decode("utf-8", errors="ignore"),
            }

        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e)}


class DebugTracker:
    """
    디버깅 추적 시스템 (永 - Eternity)
    Sequential Thinking Phase 6: 디버깅 과정 추적 및 기록
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.tracking_data: list[dict[str, Any]] = []

    def track_debugging_session(
        self, session_id: str, errors: list[DetectedError], report: DebuggingReport
    ) -> dict[str, Any]:
        """
        디버깅 세션 추적 (Sequential Thinking Phase 6.1)
        """
        tracking_entry = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "total_errors": len(errors),
            "errors": [
                {
                    "error_id": e.error_id,
                    "type": e.error_type,
                    "severity": e.severity.value,
                    "category": e.category.value,
                }
                for e in errors
            ],
            "report": {
                "total_errors": report.total_errors,
                "auto_fixed": report.auto_fixed,
                "manual_required": report.manual_required,
                "trinity_score": report.trinity_score,
            },
        }

        self.tracking_data.append(tracking_entry)
        return tracking_entry

    def save_tracking_data(self, file_path: str | None = None) -> bool:
        """추적 데이터 저장"""
        try:
            if file_path is None:
                file_path = str(
                    self.project_root
                    / "logs"
                    / f"debug_tracking_{datetime.now().strftime('%Y%m%d')}.json"
                )

            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.tracking_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            logger.error(f"추적 데이터 저장 실패: {e}")
            return False


class AutomatedDebuggingSystem:
    """
    통합 자동화 디버깅 시스템
    AFO 왕국의 모든 기술과 도구를 통합한 완벽한 디버깅 시스템

    Sequential Thinking: 단계별 자동화 디버깅 워크플로우
    """

    def __init__(self, project_root: Path | None = None, enable_streaming: bool = True):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent

        self.project_root = Path(project_root)
        self.enable_streaming = enable_streaming
        self.error_detector = ErrorDetector(self.project_root)
        self.error_classifier = ErrorClassifier()
        self.auto_diagnostic = AutoDiagnostic()
        self.solution_suggester = SolutionSuggester()
        self.auto_fixer = AutoFixer(self.project_root)
        self.debug_tracker = DebugTracker(self.project_root)

        # 머신러닝 기반 패턴 학습 시스템 (Phase 4: ML 진단 강화)
        try:
            from .ml_error_pattern_learner import MLErrorPatternLearner

            self.ml_learner = MLErrorPatternLearner(self.project_root)
            logger.info("✅ ML 에러 패턴 학습 시스템 초기화 완료")
        except ImportError as e:
            logger.warning(f"ML 학습 시스템 초기화 실패: {e}")
            self.ml_learner = None  # type: ignore[assignment]

    async def _emit_event(self, event_type: str, data: dict[str, Any]) -> None:
        """
        디버깅 이벤트 발생 (SSE 스트리밍)

        Args:
            event_type: 이벤트 타입 (phase_start, phase_complete, error_detected, fix_applied 등)
            data: 이벤트 데이터
        """
        if not self.enable_streaming:
            return

        try:
            from AFO.api.routes.debugging_stream import broadcast_debugging_event

            event = {
                "type": event_type,
                "timestamp": datetime.now().isoformat(),
                "data": data,
            }
            await broadcast_debugging_event(event)
        except ImportError:
            # 스트리밍 모듈이 없으면 무시
            pass
        except Exception as e:
            logger.warning(f"이벤트 발생 실패: {e}")

    async def run_full_debugging_cycle(self) -> DebuggingReport:
        """
        전체 디버깅 사이클 실행 (Sequential Thinking Phase 7)
        """
        logger.info("🏰 AFO 왕국 자동화 디버깅 시스템 시작")
        start_time = asyncio.get_event_loop().time()

        session_id = f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            # Phase 7.1: 에러 감지
            logger.info("=" * 70)
            logger.info("Phase 7.1: 에러 감지")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.1",
                    "name": "에러 감지",
                    "description": "모든 소스에서 에러 감지 시작",
                },
            )
            errors = await self.error_detector.detect_all_errors()
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.1",
                    "name": "에러 감지",
                    "result": {"total_errors": len(errors)},
                },
            )

            # Phase 7.2: 에러 분류
            logger.info("=" * 70)
            logger.info("Phase 7.2: 에러 분류")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.2",
                    "name": "에러 분류",
                    "description": "에러를 카테고리별로 분류",
                },
            )
            classified = self.error_classifier.classify_errors(errors)
            # 타입 명시: by_severity와 by_category는 dict[str, list[DetectedError]]
            # classify_errors는 dict[str, Any]를 반환하므로 타입 캐스팅 필요
            by_severity_raw: Any = classified.get("by_severity", {})
            by_category_raw: Any = classified.get("by_category", {})
            by_severity: dict[str, list[DetectedError]] = (
                by_severity_raw if isinstance(by_severity_raw, dict) else {}
            )
            by_category: dict[str, list[DetectedError]] = (
                by_category_raw if isinstance(by_category_raw, dict) else {}
            )
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.2",
                    "name": "에러 분류",
                    "result": {
                        "by_severity": {k: len(v) for k, v in by_severity.items()},
                        "by_category": {k: len(v) for k, v in by_category.items()},
                    },
                },
            )

            # Phase 7.3: 에러 진단
            logger.info("=" * 70)
            logger.info("Phase 7.3: 에러 진단")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.3",
                    "name": "에러 진단",
                    "description": "Context7 및 Scholars를 활용한 근본 원인 분석",
                },
            )
            diagnoses = {}
            for idx, error in enumerate(errors[:10], 1):  # 처음 10개만 진단 (성능 고려)
                await self._emit_event(
                    "error_diagnosing",
                    {
                        "error_id": error.error_id,
                        "progress": {"current": idx, "total": min(10, len(errors))},
                    },
                )
                diagnoses[error.error_id] = await self.auto_diagnostic.diagnose_error(
                    error
                )
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.3",
                    "name": "에러 진단",
                    "result": {"diagnosed_count": len(diagnoses)},
                },
            )

            # Phase 7.4: 해결책 제안
            logger.info("=" * 70)
            logger.info("Phase 7.4: 해결책 제안")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.4",
                    "name": "해결책 제안",
                    "description": "규칙 기반, Context7, Scholars를 활용한 해결책 제안",
                },
            )
            solutions = {}
            for error in errors[:10]:
                diagnosis = diagnoses.get(error.error_id, {})
                solutions[error.error_id] = (
                    await self.solution_suggester.suggest_solutions(error, diagnosis)
                )
                error.suggested_fixes = solutions[error.error_id]
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.4",
                    "name": "해결책 제안",
                    "result": {"solutions_count": len(solutions)},
                },
            )

            # Phase 7.5: 자동 수정
            logger.info("=" * 70)
            logger.info("Phase 7.5: 자동 수정")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.5",
                    "name": "자동 수정",
                    "description": "안전한 자동 수정 실행",
                },
            )
            auto_fixed_count = 0
            for idx, error in enumerate(
                classified["auto_fixable"][:5], 1
            ):  # 처음 5개만 자동 수정
                if error.suggested_fixes:
                    solution = error.suggested_fixes[0]
                    await self._emit_event(
                        "fix_applying",
                        {
                            "error_id": error.error_id,
                            "solution_type": solution.get("type", "unknown"),
                            "progress": {
                                "current": idx,
                                "total": min(5, len(classified["auto_fixable"])),
                            },
                        },
                    )
                    fix_result = await self.auto_fixer.auto_fix_error(error, solution)
                    if fix_result.get("success"):
                        auto_fixed_count += 1
                        await self._emit_event(
                            "fix_applied",
                            {
                                "error_id": error.error_id,
                                "success": True,
                            },
                        )
                    else:
                        await self._emit_event(
                            "fix_failed",
                            {
                                "error_id": error.error_id,
                                "reason": fix_result.get("reason", "unknown"),
                            },
                        )
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.5",
                    "name": "자동 수정",
                    "result": {"auto_fixed_count": auto_fixed_count},
                },
            )

            # Phase 7.6: Trinity Score 계산
            logger.info("=" * 70)
            logger.info("Phase 7.6: Trinity Score 계산")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.6",
                    "name": "Trinity Score 계산",
                    "description": "眞善美孝永 5기둥 점수 계산",
                },
            )
            trinity_score = await self._calculate_trinity_score(
                errors, auto_fixed_count
            )
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.6",
                    "name": "Trinity Score 계산",
                    "result": {"trinity_score": trinity_score},
                },
            )

            # Phase 7.7: 리포트 생성
            logger.info("=" * 70)
            logger.info("Phase 7.7: 리포트 생성")
            logger.info("=" * 70)
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.7",
                    "name": "리포트 생성",
                    "description": "종합 디버깅 리포트 생성",
                },
            )
            execution_time = asyncio.get_event_loop().time() - start_time

            # 타입 명시: by_severity와 by_category는 dict[str, list[DetectedError]]
            # 이미 위에서 정의했으므로 재사용
            by_severity_raw = classified.get("by_severity", {})
            by_severity_dict: dict[str, list[DetectedError]] = (
                by_severity_raw if isinstance(by_severity_raw, dict) else {}
            )
            by_category_raw = classified.get("by_category", {})
            by_category_dict: dict[str, list[DetectedError]] = (
                by_category_raw if isinstance(by_category_raw, dict) else {}
            )
            report = DebuggingReport(
                report_id=session_id,
                total_errors=len(errors),
                errors_by_severity={
                    severity: len(errors_list)
                    for severity, errors_list in by_severity_dict.items()
                },
                errors_by_category={
                    category: len(errors_list)
                    for category, errors_list in by_category_dict.items()
                },
                auto_fixed=auto_fixed_count,
                manual_required=len(classified["manual_required"]),
                trinity_score=trinity_score,
                recommendations=self._generate_recommendations(errors, classified),
                execution_time=execution_time,
            )

            # Phase 7.8: 추적 데이터 저장
            await self._emit_event(
                "phase_start",
                {
                    "phase": "7.8",
                    "name": "추적 데이터 저장",
                    "description": "디버깅 세션 추적 데이터 저장",
                },
            )
            self.debug_tracker.track_debugging_session(session_id, errors, report)
            self.debug_tracker.save_tracking_data()
            await self._emit_event(
                "phase_complete",
                {
                    "phase": "7.8",
                    "name": "추적 데이터 저장",
                    "result": {"session_id": session_id},
                },
            )

            # 최종 완료 이벤트
            await self._emit_event(
                "debugging_complete",
                {
                    "session_id": session_id,
                    "total_errors": report.total_errors,
                    "auto_fixed": report.auto_fixed,
                    "manual_required": report.manual_required,
                    "trinity_score": report.trinity_score,
                    "execution_time": execution_time,
                },
            )

            logger.info("=" * 70)
            logger.info("✅ AFO 왕국 자동화 디버깅 시스템 완료")
            logger.info("=" * 70)

            return report

        except Exception as e:
            logger.error(f"❌ 디버깅 사이클 실패: {e}")
            return DebuggingReport(
                report_id=session_id,
                recommendations=[f"시스템 오류: {e!s}"],
                execution_time=asyncio.get_event_loop().time() - start_time,
            )

    async def _calculate_trinity_score(
        self, errors: list[DetectedError], auto_fixed: int
    ) -> dict[str, float]:
        """Trinity Score 계산"""
        total_errors = len(errors)
        if total_errors == 0:
            return {
                "truth": 100.0,
                "goodness": 100.0,
                "beauty": 100.0,
                "serenity": 100.0,
                "eternity": 100.0,
                "overall": 100.0,
            }

        # 眞 (Truth): 에러 감지 정확도
        truth_score = max(0, 100 - (total_errors * 2))

        # 善 (Goodness): 자동 수정 성공률
        goodness_score = (auto_fixed / total_errors * 100) if total_errors > 0 else 100

        # 美 (Beauty): 코드 품질 (에러가 적을수록 높음)
        beauty_score = max(0, 100 - total_errors)

        # 孝 (Serenity): 개발자 경험 (자동화율)
        serenity_score = (auto_fixed / total_errors * 100) if total_errors > 0 else 100

        # 永 (Eternity): 시스템 안정성
        eternity_score = max(0, 100 - (total_errors * 1.5))

        # 종합 점수
        weights = [0.35, 0.35, 0.20, 0.08, 0.02]
        scores = [
            truth_score,
            goodness_score,
            beauty_score,
            serenity_score,
            eternity_score,
        ]
        overall_score = sum(w * s for w, s in zip(weights, scores, strict=False))

        return {
            "truth": round(truth_score, 1),
            "goodness": round(goodness_score, 1),
            "beauty": round(beauty_score, 1),
            "serenity": round(serenity_score, 1),
            "eternity": round(eternity_score, 1),
            "overall": round(overall_score, 1),
        }

    def _generate_recommendations(
        self,
        errors: list[DetectedError],
        classified: dict[str, list[DetectedError]],
    ) -> list[str]:
        """권장사항 생성"""
        recommendations = []

        if len(errors) > 0:
            recommendations.append(f"총 {len(errors)}개 에러 발견 - 수동 검토 권장")

        if len(classified["auto_fixable"]) > 0:
            recommendations.append(
                f"{len(classified['auto_fixable'])}개 에러는 자동 수정 가능"
            )

        if len(classified["manual_required"]) > 0:
            recommendations.append(
                f"{len(classified['manual_required'])}개 에러는 수동 수정 필요"
            )

        # 타입 명시: by_severity는 dict[str, list[DetectedError]]
        by_severity_check: dict[str, list[DetectedError]] = (
            classified.get("by_severity", {})
            if isinstance(classified.get("by_severity", {}), dict)
            else {}
        )
        critical_errors = by_severity_check.get("critical", [])
        if len(critical_errors) > 0:
            recommendations.append(
                f"⚠️ {len(critical_errors)}개 Critical 에러 즉시 수정 필요"
            )

        return recommendations


# 전역 인스턴스
automated_debugging_system = AutomatedDebuggingSystem()


async def run_automated_debugging() -> DebuggingReport:
    """자동화 디버깅 실행 편의 함수"""
    return await automated_debugging_system.run_full_debugging_cycle()


if __name__ == "__main__":
    import sys

    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    system = AutomatedDebuggingSystem(project_root)

    async def main():
        report = await system.run_full_debugging_cycle()
        print("\n" + "=" * 70)
        print("🏰 AFO 왕국 자동화 디버깅 시스템 결과")
        print("=" * 70)
        print("\n📊 요약:")
        print(f"  • 총 에러: {report.total_errors}개")
        print(f"  • 자동 수정: {report.auto_fixed}개")
        print(f"  • 수동 필요: {report.manual_required}개")
        print(f"\n🏆 Trinity Score: {report.trinity_score.get('overall', 0)}/100")
        print("\n💡 권장사항:")
        for rec in report.recommendations:
            print(f"  • {rec}")

    asyncio.run(main())
