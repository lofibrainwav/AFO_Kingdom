# Language: ko-KR (AFO SSOT)
from typing import Literal

import dspy


class StrategistSelection(dspy.Signature):
    """
    Select the most appropriate strategist for the given context.
    - Zhuge Liang (ZGL): Technical architecture, logic, RAG optimization (眞)
    - Sima Yi (SMY): Security, risk, ethics, guardrails (善)
    - Zhou Yu (ZYU): UX, aesthetics, narrative, emotional resonance (美)
    """

    question = dspy.InputField()
    context = dspy.InputField(optional=True)

    strategy_rationale = dspy.OutputField(desc="Why this strategist was selected")
    selected_strategist = dspy.OutputField(desc="One of: ZGL, SMY, ZYU, or COMMITTEE")


class TrinityOrchestrator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.selector = dspy.Predict(StrategistSelection)
        # In a real scenario, these would be separate specialist modules
        # For now, we use our Active RAG agent as the engine for all
        from AFO.dspy.rag_active_agent import RagActiveAgent

        self.specialists = {
            "ZGL": RagActiveAgent(),
            "SMY": RagActiveAgent(),
            "ZYU": RagActiveAgent(),
            "COMMITTEE": RagActiveAgent(),
        }

    def forward(self, question: str, context: str = ""):
        # 1. Selection Phase
        selection = self.selector(question=question, context=context)
        strategist = selection.selected_strategist

        # Fallback for LLM non-compliance
        if strategist not in self.specialists:
            strategist = "COMMITTEE"

        # 2. Execution Phase (Delegation)
        # Calling the module directly instead of .forward()
        result = self.specialists[strategist](question=question, context=context)

        # 3. Enrichment Phase
        result.strategist = strategist
        result.rationale = selection.strategy_rationale

        return result
