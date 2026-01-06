"""
AFO Unified Sovereignty Gate
Codifies the Triple Condition for AUTO_RUN.
"""

from typing import Any, Dict, Optional


class UnifiedSovereigntyGate:
    """
    The Absolute Gate of the Kingdom.
    TRINITY >= 0.90 AND RISK <= 0.10 AND ICCLS_GAP < 0.30
    """

    def __init__(self, min_trinity: float = 90.0, max_risk: float = 10.0, max_gap: float = 0.30):
        self.min_trinity = min_trinity
        self.max_risk = max_risk
        self.max_gap = max_gap

    def check_sovereignty(self, trinity: float, risk: float, gap: float) -> dict[str, Any]:
        """
        Verify if the current state allows autonomous execution.
        """
        trinity_pass = trinity >= self.min_trinity
        risk_pass = risk <= self.max_risk
        gap_pass = gap < self.max_gap

        all_pass = trinity_pass and risk_pass and gap_pass

        return {
            "all_pass": all_pass,
            "conditions": {
                "trinity": {"value": trinity, "pass": trinity_pass, "threshold": self.min_trinity},
                "risk": {"value": risk, "pass": risk_pass, "threshold": self.max_risk},
                "iccls_gap": {"value": gap, "pass": gap_pass, "threshold": self.max_gap},
            },
            "verdict": "🏰 AUTO_RUN APPROVED" if all_pass else "🛡️ HUMAN_GATE REQUIRED",
        }

    def __repr__(self):
        return (
            f"UnifiedSovereigntyGate(T>={self.min_trinity}, R<={self.max_risk}, G<{self.max_gap})"
        )
