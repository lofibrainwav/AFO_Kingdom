import dspy


class CommanderBriefingSig(dspy.Signature):
    command: str = dspy.InputField()
    context: str = dspy.InputField()
    briefing: str = dspy.OutputField()


class CommanderBriefing(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(CommanderBriefingSig)

    def forward(self, command: str, context: str):
        return self.predict(command=command, context=context)
