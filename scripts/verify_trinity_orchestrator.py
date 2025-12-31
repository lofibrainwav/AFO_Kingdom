# Language: ko-KR (AFO SSOT)
import asyncio
import os

import dspy

from AFO.dspy.trinity_orchestrator import TrinityOrchestrator


async def verify_trinity():
    print("🧪 Verifying Trinity Orchestrator (Multi-Agent Committee)...")

    # Standard DSPy mock configuration for architectural tests
    import dspy.predict

    # We create a dummy LM that returns predefined outputs based on fields requested in the prompt
    class MockStrategistLM(dspy.LM):
        def __init__(self):
            super().__init__("mock-model")

        def __call__(self, prompt=None, messages=None, **kwargs):
            text = prompt or (messages[-1]["content"] if messages else "")
            text = text.lower()

            # 1. Detection: Which signature are we serving?
            if "selected_strategist" in text:
                # StrategistSelection
                if "architecture" in text:
                    val, rat = "ZGL", "Architecture/Logic request."
                elif "safe" in text or "delete" in text:
                    val, rat = "SMY", "Security/Risk assessment."
                elif "beautiful" in text:
                    val, rat = "ZYU", "UX/Aesthetics request."
                else:
                    val, rat = "COMMITTEE", "General query."

                response_dict = {"strategy_rationale": rat, "selected_strategist": val}
            else:
                # ActiveRagSignature (thought_process, answer)
                response_dict = {
                    "reasoning": "Standard System 2 Reasoning applied.",
                    "thought_process": "1. Search Obsidian\n2. Analyze GraphRAG Entities\n3. Synthesize Answer",
                    "answer": "This is a logically verified mock answer based on the strategist's expertise.",
                }

            import json

            return [json.dumps(response_dict)]

    # Configure the global settings
    dspy.settings.configure(lm=MockStrategistLM())

    orchestrator = TrinityOrchestrator()

    questions = [
        "What is the system architecture of AFO Kingdom?",
        "Is it safe to delete the logs directory?",
        "How can we make the dashboard more beautiful?",
    ]

    for q in questions:
        print(f"\n--- Testing Query: {q} ---")
        try:
            # CALL the module directly, not .forward()
            prediction = orchestrator(question=q)
            print(f"✅ Strategist Selected: {getattr(prediction, 'strategist', 'Unknown')}")
            print(f"📖 Answer: {getattr(prediction, 'answer', 'N/A')[:100]}...")
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(verify_trinity())
