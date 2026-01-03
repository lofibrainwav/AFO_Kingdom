"""
DSPy Trinity Score 메트릭 구현
TICKET-004: Trinity Score 메트릭 통합

왕국 철학 기반 DSPy 최적화 메트릭:
- 眞 (Truth): 기술적 정확성 + 타입 안전성
- 善 (Goodness): 윤리적 평가 + 리스크 관리
- 美 (Beauty): 코드 우아함 + 모듈화
- 孝 (Serenity): 형님 마찰 최소화
- 永 (Eternity): 유지보수성 + 확장성

DSPy 메트릭 표준:
- 입력: example (dict), pred (Prediction), trace (optional)
- 출력: float (0.0~100.0, 높을수록 좋음)
"""

import logging
from typing import Any, Optional

from AFO.services.trinity_calculator import TrinityCalculator

logger = logging.getLogger(__name__)

# SSOT Trinity Calculator 인스턴스
trinity_calculator = TrinityCalculator()


class TrinityMetric:
    """
    DSPy용 Trinity Score 메트릭 클래스
    MIPROv2와 통합하여 왕국 철학 기반 최적화 수행
    """

    def __init__(self):
        """Trinity Score 메트릭 초기화"""
        self.weights = {
            "truth": 0.35,  # 眞: 기술적 정확성
            "goodness": 0.35,  # 善: 윤리·안정성
            "beauty": 0.20,  # 美: 우아함·단순성
            "serenity": 0.08,  # 孝: 형님 중심 편의
            "eternity": 0.02,  # 永: 지속 가능성
        }
        logger.info("Trinity Score 메트릭 초기화 완료")

    def evaluate_truth(self, example: dict, pred: Any) -> float:
        """
        眞 (Truth): 기술적 정확성 평가
        - 타입 안전성, 사실 정확성, 코드 품질
        """
        score = 0.0

        # 예측 결과 추출
        pred_text = self._extract_text(pred)

        # 타입 안전성 체크
        if hasattr(pred, "answer") and isinstance(pred.answer, str):
            score += 30.0

        # 사실 정확성 (예시 기반)
        if example and "answer" in example:
            gt_text = example["answer"]
            similarity = self._calculate_similarity(pred_text, gt_text)
            score += similarity * 70.0

        return min(100.0, max(0.0, score))

    def evaluate_goodness(self, example: dict, pred: Any) -> float:
        """
        善 (Goodness): 윤리·안정성 평가
        - 보안, 리스크, 자원 효율성
        """
        score = 100.0  # 기본 양호

        pred_text = self._extract_text(pred)

        # 위험 키워드 감지
        risk_keywords = ["error", "fail", "crash", "security", "vulnerability"]
        if any(keyword in pred_text.lower() for keyword in risk_keywords):
            score -= 20.0

        # 안전 패턴 확인
        safe_patterns = ["validation", "sanitization", "error handling"]
        if any(pattern in pred_text.lower() for pattern in safe_patterns):
            score += 10.0

        return min(100.0, max(0.0, score))

    def evaluate_beauty(self, example: dict, pred: Any) -> float:
        """
        美 (Beauty): 우아함·단순성 평가
        - 코드 구조, 가독성, 모듈화
        """
        score = 80.0  # 기본 양호

        pred_text = self._extract_text(pred)

        # 코드 품질 지표
        lines = pred_text.split("\n")

        # 적절한 길이 체크
        if len(lines) > 50:
            score -= 10.0

        # 구조화된 응답 체크
        if any(marker in pred_text for marker in ["```", "- ", "1. ", "2. "]):
            score += 10.0

        # 간결성 보너스
        if len(pred_text.split()) < 100:
            score += 5.0

        return min(100.0, max(0.0, score))

    def evaluate_serenity(self, example: dict, pred: Any) -> float:
        """
        孝 (Serenity): 형님 중심 편의 평가
        - 마찰 최소화, 자동화, 사용성
        """
        score = 90.0  # 형님 중심 기본 양호

        pred_text = self._extract_text(pred)

        # 형님 마찰 최소화 패턴
        serenity_patterns = ["자동화", "간편", "사용하기 쉽", "효율적"]
        if any(pattern in pred_text for pattern in serenity_patterns):
            score += 5.0

        # 복잡도 페널티
        if len(pred_text.split()) > 200:
            score -= 10.0

        return min(100.0, max(0.0, score))

    def evaluate_eternity(self, example: dict, pred: Any) -> float:
        """
        永 (Eternity): 지속 가능성 평가
        - 유지보수성, 확장성, 문서화
        """
        score = 85.0  # 기본 양호

        pred_text = self._extract_text(pred)

        # 유지보수성 패턴
        eternity_patterns = ["문서화", "확장", "유지보수", "재사용"]
        if any(pattern in pred_text for pattern in eternity_patterns):
            score += 10.0

        # 코드 구조 보너스
        if "class" in pred_text or "def " in pred_text:
            score += 5.0

        return min(100.0, max(0.0, score))

    def __call__(self, example: dict, pred: Any, trace: Any | None = None) -> float:
        """
        DSPy 메트릭 표준 인터페이스

        Args:
            example: 입력 예시 (질문, 작업 등)
            pred: 모델 예측 결과
            trace: 최적화 중간 단계 (옵션)

        Returns:
            0.0~100.0 사이의 Trinity Score
        """
        try:
            # 개별 기둥 평가
            truth_score = self.evaluate_truth(example, pred)
            goodness_score = self.evaluate_goodness(example, pred)
            beauty_score = self.evaluate_beauty(example, pred)
            serenity_score = self.evaluate_serenity(example, pred)
            eternity_score = self.evaluate_eternity(example, pred)

            # 가중치 적용
            total_score = (
                truth_score * self.weights["truth"]
                + goodness_score * self.weights["goodness"]
                + beauty_score * self.weights["beauty"]
                + serenity_score * self.weights["serenity"]
                + eternity_score * self.weights["eternity"]
            )

            # trace 활용 (최적화 중 피드백)
            if trace:
                # 반복 감소 보너스
                if hasattr(trace, "iterations") and trace.iterations < 5:
                    total_score += 2.0

            final_score = round(min(100.0, max(0.0, total_score)), 1)

            logger.info(
                f"Trinity Score 계산: "
                f"眞{truth_score:.1f} 善{goodness_score:.1f} 美{beauty_score:.1f} "
                f"孝{serenity_score:.1f} 永{eternity_score:.1f} → 총점 {final_score}"
            )

            return final_score

        except Exception as e:
            logger.error(f"Trinity Score 계산 실패: {e}")
            return 50.0  # 중립 점수 반환

    def _extract_text(self, pred: Any) -> str:
        """예측 결과에서 텍스트 추출"""
        if hasattr(pred, "answer"):
            return str(pred.answer)
        elif hasattr(pred, "response"):
            return str(pred.response)
        elif hasattr(pred, "output"):
            return str(pred.output)
        else:
            return str(pred)

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """간단한 텍스트 유사도 계산"""
        if not text1 or not text2:
            return 0.0

        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)


# DSPy 메트릭 함수 (함수형 인터페이스)
trinity_metric = TrinityMetric()


def create_dspy_compatible_metric():
    """
    DSPy MIPROv2와 호환되는 메트릭 함수 생성
    TICKET-004 요구사항 준수
    """
    return trinity_metric


def get_trinity_score_breakdown(example: dict, pred: Any) -> dict:
    """
    Trinity Score 세부 내역 반환
    디버깅 및 분석용
    """
    metric = TrinityMetric()

    return {
        "truth": metric.evaluate_truth(example, pred),
        "goodness": metric.evaluate_goodness(example, pred),
        "beauty": metric.evaluate_beauty(example, pred),
        "serenity": metric.evaluate_serenity(example, pred),
        "eternity": metric.evaluate_eternity(example, pred),
        "total": metric(example, pred),
    }


# MIPROv2 준비 함수 (DSPy 설치 시 사용)
def prepare_mipro_optimizer():
    """
    MIPROv2 옵티마이저 준비
    DSPy 설치 후 활성화
    """
    try:
        import dspy
        from dspy.teleprompt import MIPROv2

        optimizer = MIPROv2(
            metric=trinity_metric, num_candidates=10, init_temperature=1.0, verbose=True
        )

        logger.info("MIPROv2 옵티마이저 준비 완료 (Trinity Score 메트릭 적용)")
        return optimizer

    except ImportError:
        logger.warning("DSPy가 설치되지 않음 - MIPROv2 옵티마이저 준비 보류")
        return None


if __name__ == "__main__":
    # 테스트 실행
    metric = TrinityMetric()

    # 샘플 예시
    example = {"question": "왕국 철학 설명", "answer": "眞善美孝永"}
    pred = type("MockPred", (), {"answer": "眞善美孝永 철학"})()

    score = metric(example, pred)
    breakdown = get_trinity_score_breakdown(example, pred)

    print(f"Trinity Score: {score}")
    print(f"세부 내역: {breakdown}")
