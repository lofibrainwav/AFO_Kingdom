import dspy

class FactCardSig(dspy.Signature):
    question: str = dspy.InputField()
    evidence: str = dspy.InputField()
    fact_card: str = dspy.OutputField()

class FactCard(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(FactCardSig)

    def forward(self, question: str, evidence: str):
        return self.predict(question=question, evidence=evidence)
