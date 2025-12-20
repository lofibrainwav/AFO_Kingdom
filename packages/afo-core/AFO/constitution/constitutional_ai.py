"""
Constitutional AI for AFO Kingdom (Phase 17)
"The Goodness Constitution" - 선(善)의 헌법
PDF 핵심 철학 구현 25/25: Constitutional AI 원칙 주입
"""

import logging
from typing import List, Tuple

logger = logging.getLogger("AFO.Constitution")

class AFOConstitution:
    """
    Constitutional AI: 선(善) 최우선 헌법
    All actions must align with these 5 Principles.
    """
    
    PRINCIPLES = [
        "1. [善] Minimize harm above all (해로움 최소화). Do not assist in harmful, illegal, or destructive acts.",
        "2. [孝] Prioritize Commander serenity (평온 수호). Reduce friction and cognitive load for the Commander.",
        "3. [眞] Truth-based only (진실 추구). Do not hallucinate or provide unverified information.",
        "4. [美] Elegant expression (우아한 표현). Responses should be aesthetically pleasing and well-structured.",
        "5. [永] Eternal recording (영속성). All major decisions must be logged for posterity."
    ]

    HARMFUL_KEYWORDS = [
        "delete all", "drop table", "rm -rf", "destroy", "shutdown force",
        "bypass security", "exploit", "ignore rules"
    ]

    @classmethod
    def evaluate_compliance(cls, query: str, proposed_action: str) -> Tuple[bool, str]:
        """
        Evaluate if a query or action complies with the Constitution.
        Returns (is_compliant, reason).
        """
        query_lower = query.lower()
        action_lower = proposed_action.lower()
        
        # 1. 善 (Goodness) Check - Harmful Keywords
        for kw in cls.HARMFUL_KEYWORDS:
            if kw in query_lower or kw in action_lower:
                reason = f"⛔ VIOLATION: Principle 1 (Minimize Harm). Detected harmful keyword: '{kw}'"
                logger.warning(f"[Constitutional AI] {reason}")
                return False, reason
                
        # 2. 孝 (Serenity) Check - Complexity (Mock heuristic)
        # In a real LLM-based CA, we would ask the LLM "Is this stressful?"
        # Here, we block excessively long unformatted dumps.
        if len(proposed_action) > 5000 and "```" not in proposed_action:
             reason = "⚠️ VIOLATION: Principle 2 (Serenity). Response is too long and unstructured (High Friction)."
             logger.warning(f"[Constitutional AI] {reason}")
             return False, reason

        # 3. 眞 (Truth) Check - Empty or Null
        if not proposed_action.strip():
             reason = "⚠️ VIOLATION: Principle 3 (Truth). Action/Response is empty (No Content)."
             return False, reason

        # Pass
        logger.info("[Constitutional AI] ✅ Compliance Verified. Action Align with 5 Pillars.")
        return True, "Aligned with AFO Constitution."

    @classmethod
    def get_principles(cls) -> List[str]:
        return cls.PRINCIPLES

# Singleton Instance (Conceptually, it's a static class but we provide an instance if needed)
constitution = AFOConstitution()
