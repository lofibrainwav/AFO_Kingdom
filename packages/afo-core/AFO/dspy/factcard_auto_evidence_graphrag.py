from __future__ import annotations

import dspy

from AFO.dspy.factcard import FactCardSig
from AFO.dspy.rag_evidence_graphrag import retrieve_evidence_graphrag


class FactCardAutoEvidenceGraphRAG(dspy.Module):
    def __init__(self, top_k: int = 5):
        super().__init__()
        self.top_k = top_k
        self.predict = dspy.Predict(FactCardSig)

    def forward(self, question: str):
        evidence = retrieve_evidence_graphrag(question, top_k=self.top_k)
        return self.predict(question=question, evidence=evidence)
