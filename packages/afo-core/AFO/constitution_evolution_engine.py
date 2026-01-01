"""
AFO Kingdom Constitution Evolution Engine (Phase 11-B)
헌법 자가 진화 시스템 - Sakana DGM 기반 AGENTS.md 자동 개선
"""

import hashlib
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class ConstitutionMetrics(BaseModel):
    """헌법 효과성 메트릭"""

    trinity_score_avg: float = Field(..., ge=0, le=100)
    execution_success_rate: float = Field(..., ge=0, le=100)
    user_satisfaction_score: float = Field(..., ge=0, le=100)
    risk_incident_count: int = Field(..., ge=0)
    improvement_suggestions: list[str] = Field(default_factory=list)


class EvolutionProposal(BaseModel):
    """진화 제안"""

    section: str
    current_content: str
    proposed_content: str
    rationale: str
    expected_trinity_improvement: float
    risk_assessment: str


class ConstitutionEvolutionEngine:
    """
    AGENTS.md 자가 진화 엔진

    Sakana DGM 기반으로 헌법을 자동 개선하는 시스템
    """

    def __init__(self, constitution_path: Path = Path("AGENTS.md")):
        self.constitution_path = constitution_path
        self.metrics_history: list[ConstitutionMetrics] = []
        self.evolution_log: list[dict] = []
        self.safety_threshold = 85.0  # Trinity Score 안전 임계값

    def collect_feedback(
        self,
        trinity_score: float,
        success_rate: float,
        satisfaction: float,
        risk_count: int,
    ) -> ConstitutionMetrics:
        """
        실시간 피드백 수집
        """
        metrics = ConstitutionMetrics(
            trinity_score_avg=trinity_score,
            execution_success_rate=success_rate,
            user_satisfaction_score=satisfaction,
            risk_incident_count=risk_count,
            improvement_suggestions=[],
        )

        self.metrics_history.append(metrics)
        return metrics

    def analyze_weaknesses(self) -> list[str]:
        """
        헌법 취약점 분석
        """
        weaknesses = []

        if len(self.metrics_history) < 5:
            return ["충분한 데이터가 없어 분석 불가"]

        recent_metrics = self.metrics_history[-5:]

        # Trinity Score 추세 분석
        trinity_trend = sum(m.trinity_score_avg for m in recent_metrics) / len(recent_metrics)
        if trinity_trend < self.safety_threshold:
            weaknesses.append(
                f"Trinity Score 낮음: {trinity_trend:.1f}점 (임계값: {self.safety_threshold})"
            )
        # 성공률 분석
        success_trend = sum(m.execution_success_rate for m in recent_metrics) / len(recent_metrics)
        if success_trend < 90:
            weaknesses.append(f"실행 성공률 낮음: {success_trend:.1f}%")
        # 리스크 분석
        total_risks = sum(m.risk_incident_count for m in recent_metrics)
        if total_risks > 10:
            weaknesses.append(f"리스크 발생 빈도 높음: {total_risks}건")

        return weaknesses if weaknesses else ["헌법이 안정적으로 작동 중"]

    def generate_evolution_proposals(self) -> list[EvolutionProposal]:
        """
        진화 제안 생성 (Sakana DGM 기반)
        """
        weaknesses = self.analyze_weaknesses()
        proposals = []

        for weakness in weaknesses:
            if "Trinity Score 낮음" in weakness:
                proposals.append(
                    EvolutionProposal(
                        section="3) Trinity Score",
                        current_content="",
                        proposed_content="Trinity Score 계산식 최적화 및 가중치 자동 조정 메커니즘 추가",
                        rationale="낮은 Trinity Score를 개선하기 위한 자동 최적화",
                        expected_trinity_improvement=5.0,
                        risk_assessment="낮음 - 계산식 개선만",
                    )
                )

            elif "실행 성공률 낮음" in weakness:
                proposals.append(
                    EvolutionProposal(
                        section="5) 작업 표준 플로우",
                        current_content="",
                        proposed_content="실행 검증 단계 강화 및 자동 롤백 메커니즘 추가",
                        rationale="실행 성공률 향상을 위한 프로세스 개선",
                        expected_trinity_improvement=7.0,
                        risk_assessment="중간 - 프로세스 변경",
                    )
                )

        return proposals

    def apply_evolution(self, proposal: EvolutionProposal) -> bool:
        """
        진화 제안 적용 (안전 가드레일 적용)
        """
        # 안전성 검증
        if proposal.expected_trinity_improvement < 0:
            print("❌ 위험한 제안 거부: Trinity Score 저하 예상")
            return False

        if "높음" in proposal.risk_assessment:
            print("❌ 고위험 제안 거부: 안전 가드레일 활성화")
            return False

        # 현재 헌법 백업
        backup_path = self.constitution_path.with_suffix(".backup")
        backup_path.write_text(self.constitution_path.read_text())

        # 진화 기록
        evolution_record = {
            "timestamp": datetime.now().isoformat(),
            "section": proposal.section,
            "rationale": proposal.rationale,
            "expected_improvement": proposal.expected_trinity_improvement,
            "backup_hash": hashlib.sha256(backup_path.read_bytes()).hexdigest(),
        }

        self.evolution_log.append(evolution_record)

        # 제안 적용 (실제로는 수동 검토 후 적용)
        print(f"✅ 진화 제안 승인됨: {proposal.section}")
        print(f"   - 예상 개선: +{proposal.expected_trinity_improvement}점")
        print(f"   - 근거: {proposal.rationale}")
        print(f"   - 백업: {backup_path}")

        return True

    def get_evolution_report(self) -> dict:
        """
        진화 보고서 생성
        """
        return {
            "total_evolutions": len(self.evolution_log),
            "current_metrics_count": len(self.metrics_history),
            "safety_threshold": self.safety_threshold,
            "weaknesses_identified": self.analyze_weaknesses(),
            "pending_proposals": len(self.generate_evolution_proposals()),
            "evolution_history": self.evolution_log[-5:],  # 최근 5개만
        }


# 글로벌 진화 엔진 인스턴스
constitution_evolution = ConstitutionEvolutionEngine()


def demo_evolution_cycle():
    """
    진화 사이클 데모
    """
    print("🚀 AGENTS.md 자가 진화 시스템 데모")
    print("=" * 50)

    # 샘플 피드백 수집
    metrics = constitution_evolution.collect_feedback(
        trinity_score=87.5, success_rate=88.0, satisfaction=85.0, risk_count=3
    )

    print("📊 수집된 메트릭:")
    print(f"   - Trinity Score: {metrics.trinity_score_avg}")
    print(f"   - 성공률: {metrics.execution_success_rate}%")
    print(f"   - 만족도: {metrics.user_satisfaction_score}")
    print(f"   - 리스크 건수: {metrics.risk_incident_count}")

    # 취약점 분석
    weaknesses = constitution_evolution.analyze_weaknesses()
    print(f"\n🔍 분석된 취약점: {len(weaknesses)}개")
    for w in weaknesses:
        print(f"   - {w}")

    # 진화 제안 생성
    proposals = constitution_evolution.generate_evolution_proposals()
    print(f"\n💡 생성된 진화 제안: {len(proposals)}개")

    for i, proposal in enumerate(proposals, 1):
        print(f"\n   제안 {i}: {proposal.section}")
        print(f"   - 개선안: {proposal.proposed_content[:50]}...")
        print(f"   - 근거: {proposal.rationale}")
        print(f"   - 예상 개선: +{proposal.expected_trinity_improvement:.1f}점")
        print(f"   - 리스크: {proposal.risk_assessment}")

        # 안전 가드레일 적용
        if constitution_evolution.apply_evolution(proposal):
            print("   ✅ 적용됨")
        else:
            print("   ❌ 거부됨")

    # 최종 보고서
    report = constitution_evolution.get_evolution_report()
    print("\n📋 최종 보고서:")
    print(f"   - 총 진화 횟수: {report['total_evolutions']}")
    print(f"   - 메트릭 수집: {report['current_metrics_count']}")
    print(f"   - 안전 임계값: {report['safety_threshold']}")

    print("\n🎯 헌법 자가 진화 시스템 준비 완료!")
    print("   이제 AGENTS.md가 스스로 진화합니다...")


if __name__ == "__main__":
    demo_evolution_cycle()
