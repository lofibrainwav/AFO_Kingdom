#!/usr/bin/env python3
"""Sequential Thinking MCP Module
단계별 사고 및 추론을 위한 MCP 도구 모듈

이 모듈은 AFO 왕국의 Sequential Thinking 방법론을 구현하여,
단계별 사고 과정을 체계적으로 관리하고 Trinity Score 기반으로
진실성과 평온성을 평가합니다.

주요 기능:
- 단계별 사고 기록 및 관리
- Trinity Score (眞善美孝永) 기반 사고 품질 평가
- 세션 기반 사고 추적
- 사고 과정 요약 및 분석
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# 상수 정의
DEFAULT_TRUTH_BASE_SCORE = 0.1
DEFAULT_SERENITY_BASE_SCORE = 0.1
TRUTH_KEYWORD_WEIGHT = 0.1
SERENITY_KEYWORD_WEIGHT = 0.08
MAX_IMPACT_SCORE = 1.0


class SequentialThinkingMCP:
    """Sequential Thinking MCP - 단계별 사고 지원

    AFO 왕국의 단계별 사고 방법론을 구현하여 체계적인 문제 해결과
    Trinity 철학 기반 사고 품질 평가를 제공합니다.

    Attributes:
        thought_history: 사고 기록 리스트
        current_session: 현재 세션 ID

    """

    def __init__(self):
        """Sequential Thinking MCP 초기화

        사고 기록을 초기화하고 로깅을 설정합니다.
        """
        self.thought_history: list[dict[str, Any]] = []
        self.current_session: str | None = None
        logger.info("SequentialThinkingMCP initialized")

    def process_thought(
        self, thought: str, thought_number: int, total_thoughts: int, next_thought_needed: bool
    ) -> dict[str, Any]:
        """단계별 사고 처리

        Args:
            thought: 현재 사고 내용
            thought_number: 현재 단계 번호
            total_thoughts: 전체 단계 수
            next_thought_needed: 다음 단계 필요 여부

        Returns:
            처리 결과 딕셔너리

        """
        try:
            if not thought or not isinstance(thought, str):
                raise ValueError("Invalid thought input")

            if thought_number < 1 or total_thoughts < 1:
                raise ValueError("Invalid step numbers")

            if thought_number > total_thoughts:
                raise ValueError("Current step exceeds total steps")

            # 사고 기록 저장
            thought_entry = {
                "thought": thought,
                "thought_number": thought_number,
                "total_thoughts": total_thoughts,
                "next_thought_needed": next_thought_needed,
                "timestamp": self._get_timestamp(),
                "truth_impact": self._evaluate_truth_impact(thought),
                "serenity_impact": self._evaluate_serenity_impact(thought),
            }

            self.thought_history.append(thought_entry)
            logger.debug(f"Thought processed: step {thought_number}/{total_thoughts}")

            # 결과 생성
            result = {
                "thought_processed": thought,
                "step": f"{thought_number}/{total_thoughts}",
                "progress": thought_number / total_thoughts,
                "completed": thought_number >= total_thoughts,
                "next_needed": next_thought_needed,
                "metadata": {
                    "truth_impact": thought_entry["truth_impact"],
                    "serenity_impact": thought_entry["serenity_impact"],
                    "session_id": self.current_session or "default",
                },
            }

            if thought_number >= total_thoughts:
                result["summary"] = self._generate_summary()

            return result

        except Exception as e:
            logger.error(f"Error processing thought: {e}")
            raise

    def _evaluate_truth_impact(self, thought: str) -> float:
        """사고 내용의 진실성(truth) 영향 평가

        Trinity Score의 眞(Truth) 기둥을 평가하여 사고의 논리적 타당성과
        증거 기반 정도를 측정합니다.

        Args:
            thought: 평가할 사고 내용

        Returns:
            0.0~1.0 사이의 진실성 점수

        """
        try:
            if not thought or not isinstance(thought, str):
                logger.warning(f"Invalid thought input: {type(thought)}")
                return DEFAULT_TRUTH_BASE_SCORE

            # 진실성 지표 키워드들
            truth_indicators = [
                # 영어 키워드
                "fact",
                "evidence",
                "data",
                "logic",
                "reason",
                "verify",
                "validate",
                "proof",
                "logic",
                "verify",
                "validate",
                "analysis",
                "research",
                "measurement",
                "observation",
                "experiment",
                "hypothesis",
                "theory",
                # 한글 키워드
                "사실",
                "증거",
                "데이터",
                "논리",
                "이유",
                "검증",
                "확인",
                "증명",
                "논리",
                "검증",
                "확인",
                "분석",
                "연구",
                "측정",
                "관찰",
                "실험",
                "가설",
                "이론",
            ]

            score = DEFAULT_TRUTH_BASE_SCORE
            thought_lower = thought.lower()

            # 키워드 매칭으로 점수 계산
            for indicator in truth_indicators:
                if indicator in thought_lower:
                    score += TRUTH_KEYWORD_WEIGHT

            # 길이 기반 보너스 (너무 짧은 사고는 진실성이 낮음)
            word_count = len(thought.split())
            if word_count > 10:
                score += 0.1
            elif word_count < 3:
                score -= 0.1

            # 특수 문자나 코드 포함 보너스
            if any(char in thought for char in ["=", "==", "!=", "<", ">", "and", "or"]):
                score += 0.1

            final_score = min(max(score, 0.0), MAX_IMPACT_SCORE)
            logger.debug(f"Truth impact calculated: {final_score:.2f} for thought: {thought[:50]}...")
            return final_score

        except Exception as e:
            logger.error(f"Error evaluating truth impact: {e}")
            return DEFAULT_TRUTH_BASE_SCORE

    def _evaluate_serenity_impact(self, thought: str) -> float:
        """사고 내용의 평온성(serenity) 영향 평가

        Trinity Score의 孝(Serenity) 기둥을 평가하여 사고의 안정성과
        인지 부하 수준을 측정합니다.

        Args:
            thought: 평가할 사고 내용

        Returns:
            0.0~1.0 사이의 평온성 점수

        """
        try:
            if not thought or not isinstance(thought, str):
                logger.warning(f"Invalid thought input: {type(thought)}")
                return DEFAULT_SERENITY_BASE_SCORE

            # 평온성 지표 키워드들
            serenity_indicators = [
                # 영어 키워드
                "calm",
                "stable",
                "balanced",
                "harmony",
                "clear",
                "simple",
                "serenity",
                "balance",
                "harmony",
                "calm",
                "clear",
                "simple",
                "consistent",
                "reliable",
                "predictable",
                "organized",
                "structured",
                # 한글 키워드
                "평온",
                "안정",
                "균형",
                "조화",
                "명확",
                "단순",
                "일관",
                "신뢰",
                "예측",
                "조직",
                "구조",
            ]

            score = DEFAULT_SERENITY_BASE_SCORE
            thought_lower = thought.lower()

            # 키워드 매칭으로 점수 계산
            for indicator in serenity_indicators:
                if indicator in thought_lower:
                    score += SERENITY_KEYWORD_WEIGHT

            # 문장 구조 분석 (간단한 문장이 더 평온함)
            sentences = thought.split(".")
            if len(sentences) > 5:
                score -= 0.1  # 너무 복잡한 사고는 평온성 낮음
            elif len(sentences) <= 2:
                score += 0.1  # 간단한 사고는 평온성 높음

            # 감정 표현 감소 보너스 (감정적인 표현이 적을수록 평온)
            emotional_words = ["!", "?", "urgent", "critical", "error", "fail"]
            emotional_count = sum(1 for word in emotional_words if word in thought_lower)
            score -= emotional_count * 0.05

            final_score = min(max(score, 0.0), MAX_IMPACT_SCORE)
            logger.debug(f"Serenity impact calculated: {final_score:.2f} for thought: {thought[:50]}...")
            return final_score

        except Exception as e:
            logger.error(f"Error evaluating serenity impact: {e}")
            return DEFAULT_SERENITY_BASE_SCORE

    def _get_timestamp(self) -> str:
        """현재 타임스탬프 반환"""
        return datetime.now().isoformat()

    def _generate_summary(self) -> str:
        """단계별 사고 요약 생성"""
        if not self.thought_history:
            return "No thought process recorded."

        total_steps = len(self.thought_history)
        avg_truth = sum(t.get("truth_impact", 0) for t in self.thought_history) / total_steps
        avg_serenity = sum(t.get("serenity_impact", 0) for t in self.thought_history) / total_steps

        return (
            f"Total {total_steps} steps completed. Average truth: {avg_truth:.2f}, Average serenity: {avg_serenity:.2f}"
        )

    def get_thought_history(self) -> list[dict[str, Any]]:
        """사고 기록 반환"""
        return self.thought_history.copy()

    def clear_history(self) -> None:
        """사고 기록 초기화"""
        self.thought_history.clear()
        logger.info("Thought history cleared")

    def start_session(self, session_id: str) -> None:
        """새로운 사고 세션 시작"""
        if not session_id or not isinstance(session_id, str):
            raise ValueError("Invalid session ID")

        self.current_session = session_id
        self.clear_history()
        logger.info(f"Started new thinking session: {session_id}")

    def end_session(self) -> dict[str, Any]:
        """현재 세션 종료 및 요약 반환"""
        summary = {
            "session_id": self.current_session,
            "total_thoughts": len(self.thought_history),
            "completed_at": self._get_timestamp(),
            "final_summary": self._generate_summary(),
        }

        self.current_session = None
        logger.info(f"Ended thinking session with {summary['total_thoughts']} thoughts")
        return summary
