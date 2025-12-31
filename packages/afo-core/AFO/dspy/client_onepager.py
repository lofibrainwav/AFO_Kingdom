import dspy

class ClientOnePagerSig(dspy.Signature):
    client_context: str = dspy.InputField()
    topic: str = dspy.InputField()
    evidence: str = dspy.InputField()
    one_pager: str = dspy.OutputField()

class ClientOnePager(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ClientOnePagerSig)

    def forward(self, client_context: str, topic: str, evidence: str):
        return self.predict(client_context=client_context, topic=topic, evidence=evidence)
