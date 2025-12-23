"""
Antigravity Engine - Phase 6 고급 거버넌스 시스템
Trinity Score 기반 지능형 코드 품질 관리
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class AntigravityEngine:
    """
    Antigravity Engine - 지능형 품질 게이트 시스템
    Trinity Score 기반 ML 예측 및 동적 임계값 조정
    """

    def __init__(self):
        self.quality_history: list[dict[str, Any]] = []
        self.prediction_model = None
        self.dynamic_thresholds = self._initialize_thresholds()

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
        """
        지능형 품질 게이트 평가
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
        adjusted_thresholds = await self._adjust_for_context(
            dynamic_thresholds, context
        )

        # 4. 최종 의사결정
        decision = await self._make_intelligent_decision(
            trinity_score, risk_score, predicted_score, adjusted_thresholds, context
        )

        # 5. 학습 데이터 수집
        await self._collect_learning_data(trinity_score, risk_score, context, decision)

        return {
            "decision": decision,
            "trinity_score": trinity_score,
            "risk_score": risk_score,
            "predicted_score": predicted_score,
            "dynamic_thresholds": adjusted_thresholds,
            "confidence": await self._calculate_confidence(decision, context),
            "recommendations": await self._generate_recommendations(decision, context),
        }

    async def _predict_future_quality(
        self, current_score: float, context: dict[str, Any]
    ) -> float:
        """
        ML 기반 미래 품질 예측
        간단한 회귀 모델로 향후 Trinity Score 예측
        """
        if (
            len(self.quality_history)
            < self.dynamic_thresholds["min_samples_for_prediction"]
        ):
            # 충분한 데이터가 없으면 현재 점수 반환
            return current_score

        try:
            # 최근 히스토리 분석 (지난 30일)
            recent_history = [
                h
                for h in self.quality_history
                if (datetime.now() - h["timestamp"]).days
                <= self.dynamic_thresholds["history_window_days"]
            ]

            if len(recent_history) < 5:
                return current_score

            # 간단한 추세 분석
            scores = [h["trinity_score"] for h in recent_history[-10:]]  # 최근 10개
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

    async def _calculate_dynamic_thresholds(
        self, context: dict[str, Any]
    ) -> dict[str, float]:
        """
        동적 임계값 계산
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
            "auto_run_min_score": base_thresholds["auto_run_min_score"]
            * adjustment_factor,
            "auto_run_max_risk": base_thresholds["auto_run_max_risk"]
            / adjustment_factor,
            "manual_review_min_score": base_thresholds["manual_review_min_score"]
            * adjustment_factor,
            "block_threshold_score": base_thresholds["block_threshold_score"]
            * adjustment_factor,
        }

    async def _adjust_for_context(
        self, thresholds: dict[str, float], context: dict[str, Any]
    ) -> dict[str, float]:
        """
        맥락 기반 추가 임계값 조정
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
        """
        지능형 의사결정
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

    async def _calculate_confidence(
        self, decision: str, context: dict[str, Any]
    ) -> float:
        """
        의사결정 신뢰도 계산
        """
        base_confidence = 0.8  # 기본 신뢰도

        # 데이터 양에 따른 조정
        history_size = len(self.quality_history)
        if history_size > 100:
            base_confidence += 0.1
        elif history_size < 10:
            base_confidence -= 0.2

        # 맥락 명확성에 따른 조정
        context_completeness = (
            sum(
                1
                for key in ["project_size", "team_experience", "change_scope"]
                if key in context
            )
            / 3.0
        )
        base_confidence += (context_completeness - 0.5) * 0.2

        return max(0.1, min(1.0, base_confidence))

    async def _generate_recommendations(
        self, decision: str, context: dict[str, Any]
    ) -> list[str]:
        """
        개선 권장사항 생성
        """
        recommendations = []

        if decision == "BLOCK":
            recommendations.extend(
                [
                    "코드 품질 개선이 시급합니다",
                    "단위 테스트 추가를 고려하세요",
                    "코드 리뷰 프로세스 강화가 필요합니다",
                ]
            )

        elif decision == "ASK_COMMANDER":
            recommendations.extend(
                [
                    "수동 검토를 통해 품질 게이트를 통과할 수 있습니다",
                    "자동 수정 가능한 이슈들을 먼저 해결하세요",
                    "테스트 커버리지를 개선해보세요",
                ]
            )

        elif decision == "AUTO_RUN":
            recommendations.extend(
                [
                    "품질 기준을 잘 만족하고 있습니다",
                    "지속적인 품질 유지에 노력해주세요",
                ]
            )

        # 맥락 기반 추가 권장사항
        if context.get("test_coverage", 0) < 70:
            recommendations.append(
                "테스트 커버리지를 70% 이상으로 높이는 것을 권장합니다"
            )

        if not context.get("has_docs", False):
            recommendations.append("문서화 개선을 고려해보세요")

        return recommendations

    async def _collect_learning_data(
        self,
        trinity_score: float,
        risk_score: float,
        context: dict[str, Any],
        decision: str,
    ) -> None:
        """
        학습 데이터 수집
        향후 예측 정확도 향상을 위한 데이터 축적
        """
        learning_data = {
            "timestamp": datetime.now(),
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

    async def adapt_thresholds(self) -> dict[str, Any]:
        """
        동적 임계값 적응
        히스토리 데이터를 기반으로 임계값 자동 조정
        """
        if len(self.quality_history) < 20:
            return {"status": "insufficient_data"}

        try:
            # 최근 성과 분석
            recent_decisions = self.quality_history[-50:]  # 최근 50개

            # AUTO_RUN 성공률 계산
            auto_run_decisions = [
                d for d in recent_decisions if d["decision"] == "AUTO_RUN"
            ]
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


# 싱글톤 인스턴스
antigravity_engine = AntigravityEngine()
