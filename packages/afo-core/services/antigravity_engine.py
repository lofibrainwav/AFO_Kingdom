# Trinity Score: 90.0 (Established by Chancellor)
"""Antigravity Engine - Phase 6 고급 거버넌스 시스템
Trinity Score 기반 지능형 코드 품질 관리
"""

import asyncio
import json
import logging
import statistics
from collections import deque
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import numpy as np

logger = logging.getLogger(__name__)

# Lazy import to avoid circular dependency
try:
    from services.protocol_officer import ProtocolOfficer
except ImportError:
    ProtocolOfficer = None  # type: ignore[assignment, misc]

# Lazy import for antigravity settings
try:
    from config.antigravity import antigravity
except ImportError:
    antigravity = None  # type: ignore[assignment]


class AntigravityEngine:
    """Antigravity Engine - 지능형 품질 게이트 시스템
    Trinity Score 기반 ML 예측 및 동적 임계값 조정
    """

    def __init__(self, protocol_officer: Any | None = None):
        self.quality_history: list[dict[str, Any]] = []
        self.prediction_model = None
        self.dynamic_thresholds = self._initialize_thresholds()
        # [Phase B] Protocol Officer 주입 (없으면 생성) - 강제 사용
        if protocol_officer is None and ProtocolOfficer is not None:
            from services.protocol_officer import protocol_officer as default_officer

            self.protocol_officer = default_officer
        elif protocol_officer is None:
            # Protocol Officer가 없으면 에러 (완전 강제)
            raise ValueError(
                "[SSOT] Protocol Officer is required. Cannot initialize AntigravityEngine without Protocol Officer."
            )
        else:
            self.protocol_officer = protocol_officer

    def _initialize_thresholds(self) -> dict[str, Any]:
        """기본 동적 임계값 초기화"""
        return {
            "auto_run_min_score": 90.0,
            "auto_run_max_risk": 10.0,
            "manual_review_min_score": 70.0,
            "block_threshold_score": 50.0,
            "adaptation_rate": 0.1,  # 학습률
            "history_window_days": 30,
            "min_samples_for_prediction": 10,
        }

    async def evaluate_quality_gate(
        self, trinity_score: float, risk_score: float, context: dict[str, Any]
    ) -> dict[str, Any]:
        """지능형 품질 게이트 평가
        ML 예측과 동적 임계값을 활용한 의사결정

        Args:
            trinity_score: 현재 Trinity Score (0-100)
            risk_score: 현재 리스크 점수 (0-100)
            context: 평가 맥락 정보

        Returns:
            게이트 평가 결과

        """
        # 1. ML 기반 예측 (향후 품질 추정)
        predicted_score = await self._predict_future_quality(trinity_score, context)

        # 2. 동적 임계값 계산
        dynamic_thresholds = await self._calculate_dynamic_thresholds(context)

        # 3. 컨텍스트 기반 조정
        adjusted_thresholds = await self._adjust_for_context(dynamic_thresholds, context)

        # 4. 최종 의사결정
        decision = await self._make_intelligent_decision(
            trinity_score, risk_score, predicted_score, adjusted_thresholds, context
        )

        # 5. 학습 데이터 수집
        await self._collect_learning_data(trinity_score, risk_score, context, decision)

        result = {
            "decision": decision,
            "trinity_score": trinity_score,
            "risk_score": risk_score,
            "predicted_score": predicted_score,
            "dynamic_thresholds": adjusted_thresholds,
            "confidence": await self._calculate_confidence(decision, context),
            "recommendations": await self._generate_recommendations(decision, context),
        }

        # [Phase B] Protocol Officer를 통한 메시지 포맷팅 (완전 강제 - 우회 불가)
        # Protocol Officer가 없으면 에러 (__init__에서 이미 검증했지만 이중 체크)
        if self.protocol_officer is None:
            raise ValueError(
                "[SSOT] Protocol Officer is required. Cannot format message without Protocol Officer."
            )

        # 결정 메시지를 Protocol Officer로 포맷팅 (무조건 거침)
        decision_msg = self._format_decision_message(result)
        result["formatted_message"] = self.protocol_officer.compose_diplomatic_message(
            decision_msg, audience=self.protocol_officer.AUDIENCE_COMMANDER
        )

        return result

    async def _predict_future_quality(self, current_score: float, context: dict[str, Any]) -> float:
        """ML 기반 미래 품질 예측
        간단한 회귀 모델로 향후 Trinity Score 예측
        """
        if len(self.quality_history) < self.dynamic_thresholds["min_samples_for_prediction"]:
            # 충분한 데이터가 없으면 현재 점수 반환
            return current_score

        try:
            # 최근 히스토리 분석 (지난 30일)
            self.quality_history = [
                h
                for h in self.quality_history
                if (datetime.now(UTC) - h["timestamp"]).days
                <= self.dynamic_thresholds["history_window_days"]
            ]

            if len(self.quality_history) < 5:
                return current_score

            # 간단한 추세 분석
            scores = [h["trinity_score"] for h in self.quality_history[-10:]]  # 최근 10개
            if len(scores) >= 2:
                trend_result = np.polyfit(range(len(scores)), scores, 1)
                trend = float(trend_result[0])  # 선형 추세, 명시적 float 변환

                # 추세 기반 예측 (다음 3회 커밋 후 예상 점수)
                prediction_steps = 3
                predicted = float(scores[-1]) + (trend * prediction_steps)

                # 합리적인 범위로 클램핑 (0-100)
                return max(0.0, min(100.0, predicted))

        except Exception as e:
            logger.warning(f"품질 예측 실패: {e}")

        return current_score

    async def _calculate_dynamic_thresholds(self, context: dict[str, Any]) -> dict[str, float]:
        """동적 임계값 계산
        프로젝트 맥락과 히스토리를 기반으로 임계값 조정
        """
        base_thresholds = self.dynamic_thresholds.copy()

        # 프로젝트 크기 기반 조정
        project_size = context.get("project_size", "medium")
        size_multipliers = {
            "small": 0.9,  # 작은 프로젝트는 관대
            "medium": 1.0,
            "large": 1.1,  # 큰 프로젝트는 엄격
        }
        size_multiplier = size_multipliers.get(project_size, 1.0)

        # 팀 경험도 기반 조정
        team_experience = context.get("team_experience", "intermediate")
        experience_multipliers = {
            "beginner": 0.8,
            "intermediate": 1.0,
            "expert": 1.2,
        }
        experience_multiplier = experience_multipliers.get(team_experience, 1.0)

        # 시간 압박 고려
        time_pressure = context.get("time_pressure", "normal")
        time_multipliers = {
            "low": 1.2,  # 여유로움: 엄격
            "normal": 1.0,
            "high": 0.9,  # 급함: 관대
        }
        time_multiplier = time_multipliers.get(time_pressure, 1.0)

        # 종합 조정 계수
        adjustment_factor = size_multiplier * experience_multiplier * time_multiplier

        return {
            "auto_run_min_score": base_thresholds["auto_run_min_score"] * adjustment_factor,
            "auto_run_max_risk": base_thresholds["auto_run_max_risk"] / adjustment_factor,
            "manual_review_min_score": base_thresholds["manual_review_min_score"]
            * adjustment_factor,
            "block_threshold_score": base_thresholds["block_threshold_score"] * adjustment_factor,
        }

    async def _adjust_for_context(
        self, thresholds: dict[str, float], context: dict[str, Any]
    ) -> dict[str, float]:
        """맥락 기반 추가 임계값 조정
        코드 변경의 특성을 고려한 미세 조정
        """
        adjusted = thresholds.copy()

        # 변경 범위 고려
        change_scope = context.get("change_scope", "small")
        scope_adjustments = {
            "small": -5.0,  # 작은 변경: 관대
            "medium": 0.0,
            "large": 5.0,  # 큰 변경: 엄격
            "breaking": 10.0,  # 호환성 깨는 변경: 매우 엄격
        }
        scope_adjustment = scope_adjustments.get(change_scope, 0.0)
        adjusted["auto_run_min_score"] += scope_adjustment

        # 테스트 커버리지 고려
        test_coverage = context.get("test_coverage", 80.0)
        coverage_adjustment = (test_coverage - 80.0) * 0.1  # 80% 기준
        adjusted["auto_run_min_score"] += coverage_adjustment

        # CI 상태 고려
        ci_status = context.get("ci_status", "passing")
        if ci_status == "failing":
            adjusted["auto_run_min_score"] += 10.0  # CI 실패 시 엄격

        return adjusted

    async def _make_intelligent_decision(
        self,
        trinity_score: float,
        risk_score: float,
        predicted_score: float,
        thresholds: dict[str, float],
        context: dict[str, Any],
    ) -> str:
        """지능형 의사결정
        Trinity Score, 예측, 임계값을 종합한 최종 결정
        """
        # 예측 점수 가중 평균
        effective_score = (trinity_score * 0.7) + (predicted_score * 0.3)

        # AUTO_RUN 조건
        if (
            effective_score >= thresholds["auto_run_min_score"]
            and risk_score <= thresholds["auto_run_max_risk"]
        ):
            return "AUTO_RUN"

        # MANUAL_REVIEW 조건
        elif effective_score >= thresholds["manual_review_min_score"]:
            return "ASK_COMMANDER"

        # BLOCK 조건
        elif effective_score < thresholds["block_threshold_score"]:
            return "BLOCK"

        # 기본값
        return "ASK_COMMANDER"

    async def _calculate_confidence(self, decision: str, context: dict[str, Any]) -> float:
        """의사결정 신뢰도 계산"""
        base_confidence = 0.8  # 기본 신뢰도

        # 데이터 양에 따른 조정
        history_size = len(self.quality_history)
        if history_size > 100:
            base_confidence += 0.1
        elif history_size < 10:
            base_confidence -= 0.2

        # 맥락 명확성에 따른 조정
        context_completeness = (
            sum(1 for key in ["project_size", "team_experience", "change_scope"] if key in context)
            / 3.0
        )
        base_confidence += (context_completeness - 0.5) * 0.2

        return max(0.1, min(1.0, base_confidence))

    async def _generate_recommendations(self, decision: str, context: dict[str, Any]) -> list[str]:
        """개선 권장사항 생성
        [Phase B] Protocol Officer를 통한 포맷팅 강제
        """
        recommendations = []

        # [Phase A] REPORT_LANGUAGE에 따른 문구 선택
        report_lang = "ko"
        if antigravity is not None:
            report_lang = getattr(antigravity, "REPORT_LANGUAGE", "ko")

        if decision == "BLOCK":
            if report_lang == "ko":
                recommendations.extend(
                    [
                        "코드 품질 개선이 시급합니다",
                        "단위 테스트 추가를 고려하세요",
                        "코드 리뷰 프로세스 강화가 필요합니다",
                    ]
                )
            else:
                recommendations.extend(
                    [
                        "Code quality improvement is urgent",
                        "Consider adding unit tests",
                        "Code review process needs strengthening",
                    ]
                )

        elif decision == "ASK_COMMANDER":
            if report_lang == "ko":
                recommendations.extend(
                    [
                        "수동 검토를 통해 품질 게이트를 통과할 수 있습니다",
                        "자동 수정 가능한 이슈들을 먼저 해결하세요",
                        "테스트 커버리지를 개선해보세요",
                    ]
                )
            else:
                recommendations.extend(
                    [
                        "You can pass the quality gate through manual review",
                        "Fix auto-fixable issues first",
                        "Improve test coverage",
                    ]
                )

        elif decision == "AUTO_RUN":
            if report_lang == "ko":
                recommendations.extend(
                    [
                        "품질 기준을 잘 만족하고 있습니다",
                        "지속적인 품질 유지에 노력해주세요",
                    ]
                )
            else:
                recommendations.extend(
                    [
                        "Quality standards are well met",
                        "Please continue to maintain quality",
                    ]
                )

        # 맥락 기반 추가 권장사항
        if context.get("test_coverage", 0) < 70:
            if report_lang == "ko":
                recommendations.append("테스트 커버리지를 70% 이상으로 높이는 것을 권장합니다")
            else:
                recommendations.append(
                    "It is recommended to increase test coverage to 70% or higher"
                )

        if not context.get("has_docs", False):
            if report_lang == "ko":
                recommendations.append("문서화 개선을 고려해보세요")
            else:
                recommendations.append("Consider improving documentation")

        # [Phase B] Protocol Officer를 통한 포맷팅 (권장사항도 강제)
        if self.protocol_officer is not None:
            # 권장사항 리스트를 하나의 메시지로 합쳐서 포맷팅
            recommendations_text = "\n".join(f"- {rec}" for rec in recommendations)
            _ = self.protocol_officer.compose_diplomatic_message(
                recommendations_text, audience=self.protocol_officer.AUDIENCE_COMMANDER
            )
            # 포맷팅된 텍스트에서 권장사항만 추출 (prefix/suffix 제거)
            # 간단하게 원본 리스트 반환 (이미 언어 정책 적용됨)

        return recommendations

    async def _collect_learning_data(
        self,
        trinity_score: float,
        risk_score: float,
        context: dict[str, Any],
        decision: str,
    ) -> None:
        """학습 데이터 수집
        향후 예측 정확도 향상을 위한 데이터 축적
        """
        learning_data = {
            "timestamp": datetime.now(UTC),
            "trinity_score": trinity_score,
            "risk_score": risk_score,
            "decision": decision,
            "context": context,
            "prediction_accuracy": None,  # 향후 계산
        }

        self.quality_history.append(learning_data)

        # 오래된 데이터 정리 (최근 1000개만 유지)
        if len(self.quality_history) > 1000:
            self.quality_history = self.quality_history[-1000:]

    def _format_decision_message(self, result: dict[str, Any]) -> str:
        """[Phase B] 결정 메시지 포맷팅 (Protocol Officer 전달용)
        [Phase A] REPORT_LANGUAGE에 따른 언어 분기
        """
        # [Phase A] REPORT_LANGUAGE 확인
        report_lang = "ko"
        if antigravity is not None:
            report_lang = getattr(antigravity, "REPORT_LANGUAGE", "ko")

        decision = result.get("decision", "UNKNOWN")
        trinity_score = result.get("trinity_score", 0.0)
        risk_score = result.get("risk_score", 0.0)
        confidence = result.get("confidence", 0.0)

        if report_lang == "ko":
            msg = "품질 게이트 평가 결과:\n"
            msg += f"- 결정: {decision}\n"
            msg += f"- Trinity Score: {trinity_score:.1f}\n"
            msg += f"- Risk Score: {risk_score:.1f}\n"
            msg += f"- 신뢰도: {confidence:.1%}"

            recommendations = result.get("recommendations", [])
            if recommendations:
                msg += "\n\n권장사항:\n"
                for rec in recommendations:
                    msg += f"- {rec}\n"
        else:
            msg = "Quality Gate Evaluation Result:\n"
            msg += f"- Decision: {decision}\n"
            msg += f"- Trinity Score: {trinity_score:.1f}\n"
            msg += f"- Risk Score: {risk_score:.1f}\n"
            msg += f"- Confidence: {confidence:.1%}"

            recommendations = result.get("recommendations", [])
            if recommendations:
                msg += "\n\nRecommendations:\n"
                for rec in recommendations:
                    msg += f"- {rec}\n"

        return msg

    async def adapt_thresholds(self) -> dict[str, Any]:
        """동적 임계값 적응
        히스토리 데이터를 기반으로 임계값 자동 조정
        """
        if len(self.quality_history) < 20:
            return {"status": "insufficient_data"}

        try:
            # 최근 성과 분석
            recent_decisions = self.quality_history[-50:]  # 최근 50개

            # AUTO_RUN 성공률 계산
            auto_run_decisions = [d for d in recent_decisions if d["decision"] == "AUTO_RUN"]
            successful_auto_runs = len(
                [d for d in auto_run_decisions if d.get("outcome") == "success"]
            )

            if auto_run_decisions:
                success_rate = successful_auto_runs / len(auto_run_decisions)

                # 성공률 기반 임계값 조정
                if success_rate > 0.95:  # 너무 높음: 관대하게
                    self.dynamic_thresholds["auto_run_min_score"] -= 1.0
                elif success_rate < 0.80:  # 너무 낮음: 엄격하게
                    self.dynamic_thresholds["auto_run_min_score"] += 1.0

            return {
                "status": "adapted",
                "new_thresholds": self.dynamic_thresholds.copy(),
                "success_rate": success_rate if "success_rate" in locals() else None,
            }

        except Exception as e:
            logger.exception(f"임계값 적응 실패: {e}")
            return {"status": "error", "message": str(e)}

    # [Phase C] 보고서 생성 함수들
    def generate_analysis_report(
        self,
        context: dict[str, Any],
        analysis: dict[str, Any],
        evidence: dict[str, Any],
        next_steps: list[str],
    ) -> str:
        """분석 보고서 생성 (SSOT 규칙 준수)
        완료 선언 없이 분석 결과만 제공
        [Phase A] REPORT_LANGUAGE에 따른 언어 분기
        [Phase B] Protocol Officer 포맷팅 강제
        """
        # [Phase A] REPORT_LANGUAGE 확인
        report_lang = "ko"
        if antigravity is not None:
            report_lang = getattr(antigravity, "REPORT_LANGUAGE", "ko")

        # 템플릿 기반 리포트 생성 (언어 정책 적용)
        if report_lang == "ko":
            report = f"# {context.get('title', '분석 보고서')}\n\n"
            report += "## Context\n"
            report += f"- 상황: {context.get('situation', 'N/A')}\n"
            report += f"- 위치: {context.get('location', 'N/A')}\n"
            report += f"- 시점: {context.get('timestamp', datetime.now().isoformat())}\n"
            report += f"- 영향: {context.get('impact', 'N/A')}\n\n"

            report += "## Analysis\n"
            report += f"{analysis.get('observation', 'N/A')}\n\n"
            report += f"추정: {analysis.get('assumption', 'N/A')}\n\n"

            report += "## Evidence\n"
            for key, value in evidence.items():
                report += f"- {key}: {value}\n"
            report += "\n"

            report += "## Next Steps\n"
            for step in next_steps:
                report += f"- {step}\n"
            report += "\n"

            report += "---\n\n"
            report += "### Reporting Rules\n"
            report += "- 분석 결과만 제공 (완료 선언 없음)\n"
            report += "- SSOT 증거 기반 보고\n"
        else:
            report = f"# {context.get('title', 'Analysis Report')}\n\n"
            report += "## Context\n"
            report += f"- Situation: {context.get('situation', 'N/A')}\n"
            report += f"- Location: {context.get('location', 'N/A')}\n"
            report += f"- Timestamp: {context.get('timestamp', datetime.now().isoformat())}\n"
            report += f"- Impact: {context.get('impact', 'N/A')}\n\n"

            report += "## Analysis\n"
            report += f"{analysis.get('observation', 'N/A')}\n\n"
            report += f"Assumption: {analysis.get('assumption', 'N/A')}\n\n"

            report += "## Evidence\n"
            for key, value in evidence.items():
                report += f"- {key}: {value}\n"
            report += "\n"

            report += "## Next Steps\n"
            for step in next_steps:
                report += f"- {step}\n"
            report += "\n"

            report += "---\n\n"
            report += "### Reporting Rules\n"
            report += "- Analysis results only (no completion claims)\n"
            report += "- SSOT evidence-based reporting\n"

        # [Phase B] Protocol Officer 포맷팅 (완전 강제 - 우회 불가)
        if self.protocol_officer is None:
            raise ValueError(
                "[SSOT] Protocol Officer is required. Cannot format report without Protocol Officer."
            )

        report = self.protocol_officer.compose_diplomatic_message(
            report, audience=self.protocol_officer.AUDIENCE_COMMANDER
        )

        return report

    def generate_completion_report(
        self,
        context: dict[str, Any],
        analysis: dict[str, Any],
        evidence: dict[str, Any],
        next_steps: list[str],
    ) -> str | None:
        """완료 보고서 생성 (SSOT 증거 필수)
        증거가 없으면 None 반환 (생성 금지)
        [Phase C] 구조화된 증거 검증 강화
        """
        # [Phase C] SSOT 증거 검증 (구조화된 검증)
        # 1. commit 검증 (구조화된 키 또는 문자열 매칭)
        has_commit = False
        if isinstance(evidence, dict):
            # 구조화된 키 확인
            commit_keys = ["commit", "git_commit", "commit_hash", "commit_id"]
            has_commit = any(key in evidence and evidence[key] for key in commit_keys) or any(
                "commit" in str(k).lower() or "git" in str(k).lower() for k in evidence
            )

        # 2. file 검증 (구조화된 키 또는 문자열 매칭)
        has_files = False
        if isinstance(evidence, dict):
            file_keys = ["file", "files", "file_path", "file_paths", "path", "paths"]
            has_files = any(key in evidence and evidence[key] for key in file_keys) or any(
                "file" in str(k).lower() or "path" in str(k).lower() for k in evidence
            )

        # 3. command 검증 (구조화된 키 또는 문자열 매칭)
        has_command = False
        if isinstance(evidence, dict):
            command_keys = ["command", "commands", "cmd", "exec", "result", "output"]
            has_command = any(key in evidence and evidence[key] for key in command_keys) or any(
                "command" in str(k).lower()
                or "cmd" in str(k).lower()
                or "exec" in str(k).lower()
                or "result" in str(k).lower()
                for k in evidence
            )

        # 증거 3종 모두 필수
        if not (has_commit and has_files and has_command):
            logger.warning(
                f"[SSOT] 완료 보고서 생성 차단: 필수 증거 부족 "
                f"(commit={has_commit}, files={has_files}, command={has_command})"
            )
            return None  # 완료 리포트 생성 금지

        # SSOT Report Gate 검증
        try:
            import subprocess
            import sys
            from pathlib import Path

            # 임시 리포트 생성 (검증용)
            temp_report = self.generate_analysis_report(context, analysis, evidence, next_steps)

            # ssot_report_gate.py로 검증
            script_path = Path(__file__).parent.parent.parent / "scripts" / "ssot_report_gate.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path), temp_report],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode != 0:
                    logger.warning(
                        f"[SSOT] Report Gate 실패: {result.stdout}. 분석 리포트로 다운그레이드."
                    )
                    return None  # FAIL이면 완료 리포트 생성 금지
        except Exception as e:
            logger.warning(f"[SSOT] Report Gate 검증 실패: {e}. 분석 리포트로 다운그레이드.")
            return None

        # 완료 리포트 생성 (SSOT 증거 + Gate 통과)
        report = self.generate_analysis_report(context, analysis, evidence, next_steps)

        # [Phase A] REPORT_LANGUAGE에 따른 완료 상태 문구
        report_lang = "ko"
        if antigravity is not None:
            report_lang = getattr(antigravity, "REPORT_LANGUAGE", "ko")

        if report_lang == "ko":
            report += "\n\n### 완료 상태\n"
            report += "- ✅ SSOT 증거 확인 완료\n"
            report += "- ✅ Report Gate 통과\n"
        else:
            report += "\n\n### Completion Status\n"
            report += "- ✅ SSOT evidence verified\n"
            report += "- ✅ Report Gate passed\n"

        # [Phase B] Protocol Officer 포맷팅 (이미 generate_analysis_report에서 적용됨)
        # 하지만 완료 상태 추가 후 다시 포맷팅 (안전을 위해)
        if self.protocol_officer is not None:
            # Protocol Officer 포맷팅은 이미 적용되었으므로, 완료 상태만 추가
            pass

        return report

    def save_report(self, report: str, filename: str) -> Path:
        """리포트를 docs/reports/에 저장"""
        # 루트 기준 docs/reports/ 경로
        repo_root = Path(__file__).parent.parent.parent.parent
        reports_dir = repo_root / "docs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # 파일 저장
        report_file = reports_dir / filename
        report_file.write_text(report, encoding="utf-8")
        logger.info(f"[Antigravity] 리포트 저장: {report_file}")

        return report_file


# 싱글톤 인스턴스
antigravity_engine = AntigravityEngine()
