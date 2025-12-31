from __future__ import annotations

import dspy

from AFO.dspy.factcard import FactCardSig
from AFO.dspy.rag_helpers import retrieve_evidence


class FactCardAutoEvidence(dspy.Module):
    def __init__(self, top_k: int = 5):
        super().__init__()
        self.top_k = top_k
        self.predict = dspy.Predict(FactCardSig)

    def forward(self, question: str):
        evidence = retrieve_evidence(question, top_k=self.top_k)
        return self.predict(question=question, evidence=evidence)
