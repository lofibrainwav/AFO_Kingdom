import os

import dspy


class CommanderBriefingSig(dspy.Signature):
    command: str = dspy.InputField()
    context: str = dspy.InputField()
    briefing: str = dspy.OutputField()


class CommanderBriefing(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(CommanderBriefingSig)

        # TICKET-025: Boot-Swap (Load Optimized State)
        optimized_path = "data/dspy/compiled_commander_briefing.v2.json"

        # Check absolute or relative path flexibility
        if not os.path.exists(optimized_path):
            # Try determining path relative to AFO root if CWD is different
            # However, assuming CWD is repo root for now as per start_kingdom.sh
            pass

        if os.path.exists(optimized_path):
            try:
                self.load(optimized_path)
                print(
                    f"🧠 [CommanderBriefing] HOT-SWAP: Loaded optimized intelligence from {optimized_path}"
                )
            except Exception as e:
                print(f"⚠️ [CommanderBriefing] Failed to load optimized state: {e}")
        else:
            print(
                f"ℹ️ [CommanderBriefing] No optimized state found at {optimized_path}. Using default."
            )

    def forward(self, command: str, context: str):
        return self.predict(command=command, context=context)
