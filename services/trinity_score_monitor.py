# Trinity Score 추이 분석 모니터링 서비스
"""
Trinity Score의 시간별 추이 분석 및 이상 감지
Prometheus 메트릭 기반 모니터링
"""

import logging
import time
from collections import deque
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class TrinityScoreSample:
    """Trinity Score 샘플 데이터"""
    timestamp: float
    trinity_score: float
    truth: float
    goodness: float
    beauty: float
    filial_serenity: float
    eternity: float
    balance_status: str


class TrinityScoreMonitor:
    """
    Trinity Score 추이 분석 모니터링

    기능:
    - 시간별 Trinity Score 기록
    - 추이 분석 (상승/하락 추세)
    - 이상 감지 (갑작스러운 변화)
    - Prometheus 메트릭 노출
    """

    def __init__(self, max_samples: int = 1000, anomaly_threshold: float = 0.2):
        """
        Args:
            max_samples: 보관할 최대 샘플 수
            anomaly_threshold: 이상 감지 임계값 (변화량)
        """
        self.max_samples = max_samples
        self.anomaly_threshold = anomaly_threshold
        self.samples: deque[TrinityScoreSample] = deque(maxlen=max_samples)

        # Prometheus 메트릭 초기화 (선택적)
        self._init_prometheus_metrics()

    def _init_prometheus_metrics(self):
        """Prometheus 메트릭 초기화"""
        try:
            from prometheus_client import Gauge, Histogram

            self.trinity_score_gauge = Gauge(
                "afo_trinity_score",
                "Current Trinity Score (0.0-1.0)",
                ["pillar"]
            )

            self.trinity_score_histogram = Histogram(
                "afo_trinity_score_change",
                "Trinity Score change rate",
                buckets=[-1.0, -0.5, -0.2, -0.1, 0.0, 0.1, 0.2, 0.5, 1.0]
            )

        except ImportError:
            logger.warning("Prometheus not available, skipping metrics initialization")
            self.trinity_score_gauge = None
            self.trinity_score_histogram = None

    def record_sample(self, sample: TrinityScoreSample):
        """샘플 기록"""
        self.samples.append(sample)

        # Prometheus 메트릭 기록
        if self.trinity_score_gauge:
            self.trinity_score_gauge.labels("overall").set(sample.trinity_score)
            self.trinity_score_gauge.labels("truth").set(sample.truth)
            self.trinity_score_gauge.labels("goodness").set(sample.goodness)
            self.trinity_score_gauge.labels("beauty").set(sample.beauty)
            self.trinity_score_gauge.labels("serenity").set(sample.filial_serenity)
            self.trinity_score_gauge.labels("eternity").set(sample.eternity)

    def record_current_score(self, trinity_metrics):
        """현재 Trinity Score 기록"""
        sample = TrinityScoreSample(
            timestamp=time.time(),
            trinity_score=trinity_metrics.trinity_score,
            truth=trinity_metrics.truth,
            goodness=trinity_metrics.goodness,
            beauty=trinity_metrics.beauty,
            filial_serenity=trinity_metrics.filial_serenity,
            eternity=trinity_metrics.eternity,
            balance_status=trinity_metrics.balance_status
        )

        self.record_sample(sample)

        # 변화량 분석 및 기록
        if len(self.samples) >= 2:
            prev_sample = self.samples[-2]
            change = sample.trinity_score - prev_sample.trinity_score

            if self.trinity_score_histogram:
                self.trinity_score_histogram.observe(change)

            # 이상 감지
            if abs(change) > self.anomaly_threshold:
                self._log_anomaly(sample, prev_sample, change)

    def _log_anomaly(self, current: TrinityScoreSample, previous: TrinityScoreSample, change: float):
        """이상 상황 로깅"""
        logger.warning(
            f"Trinity Score anomaly detected: {change:.3f} change "
            f"({previous.trinity_score:.3f} → {current.trinity_score:.3f})"
        )

        # 상세 분석
        pillar_changes = {
            "truth": current.truth - previous.truth,
            "goodness": current.goodness - previous.goodness,
            "beauty": current.beauty - previous.beauty,
            "serenity": current.filial_serenity - previous.filial_serenity,
            "eternity": current.eternity - previous.eternity,
        }

        significant_changes = [
            f"{pillar}: {change:.3f}"
            for pillar, change in pillar_changes.items()
            if abs(change) > 0.1  # 10% 이상 변화
        ]

        if significant_changes:
            logger.info(f"Significant pillar changes: {', '.join(significant_changes)}")

    def get_trend_analysis(self, window_minutes: int = 60) -> dict:
        """추이 분석"""
        if len(self.samples) < 2:
            return {"error": "Insufficient data for trend analysis"}

        # 최근 윈도우 데이터 필터링
        cutoff_time = time.time() - (window_minutes * 60)
        window_samples = [s for s in self.samples if s.timestamp >= cutoff_time]

        if len(window_samples) < 2:
            return {"error": f"Insufficient data in {window_minutes}min window"}

        # 추세 계산
        first_score = window_samples[0].trinity_score
        last_score = window_samples[-1].trinity_score
        total_change = last_score - first_score

        # 각 기둥별 추세
        pillar_trends = {}
        pillars = ["truth", "goodness", "beauty", "filial_serenity", "eternity"]

        for pillar in pillars:
            first_val = getattr(window_samples[0], pillar)
            last_val = getattr(window_samples[-1], pillar)
            pillar_trends[pillar] = last_val - first_val

        return {
            "window_minutes": window_minutes,
            "sample_count": len(window_samples),
            "overall_trend": total_change,
            "trend_direction": "improving" if total_change > 0.05 else "declining" if total_change < -0.05 else "stable",
            "pillar_trends": pillar_trends,
            "balance_status_distribution": self._get_balance_distribution(window_samples)
        }

    def _get_balance_distribution(self, samples: list[TrinityScoreSample]) -> dict:
        """균형 상태 분포 분석"""
        status_counts = {}
        for sample in samples:
            status = sample.balance_status
            status_counts[status] = status_counts.get(status, 0) + 1

        return status_counts

    def get_statistics(self) -> dict:
        """통계 정보"""
        if not self.samples:
            return {"error": "No samples available"}

        scores = [s.trinity_score for s in self.samples]

        return {
            "total_samples": len(self.samples),
            "current_score": scores[-1],
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "score_volatility": self._calculate_volatility(scores),
            "balance_status_summary": self._get_balance_distribution(list(self.samples))
        }

    def _calculate_volatility(self, scores: list[float]) -> float:
        """점수 변동성 계산"""
        if len(scores) < 2:
            return 0.0

        changes = [abs(scores[i] - scores[i - 1]) for i in range(1, len(scores))]
        return sum(changes) / len(changes)

    def get_recent_samples(self, limit: int = 10) -> list[dict]:
        """최근 샘플 조회"""
        recent = list(self.samples)[-limit:]
        return [
            {
                "timestamp": s.timestamp,
                "trinity_score": s.trinity_score,
                "balance_status": s.balance_status,
                "pillars": {
                    "truth": s.truth,
                    "goodness": s.goodness,
                    "beauty": s.beauty,
                    "serenity": s.filial_serenity,
                    "eternity": s.eternity,
                }
            }
            for s in recent
        ]


# 전역 모니터 인스턴스
trinity_score_monitor = TrinityScoreMonitor()


def record_trinity_score_metrics(trinity_metrics):
    """편의 함수: Trinity Score 메트릭 기록"""
    trinity_score_monitor.record_current_score(trinity_metrics)
