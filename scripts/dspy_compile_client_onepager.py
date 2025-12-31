import json
import os
import dspy

from AFO.dspy.client_onepager import ClientOnePager
from AFO.dspy.metrics_ticket006 import objective_onepager

def load_gold(path: str):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ex = dspy.Example(
                client_context=row["client_context"],
                topic=row["topic"],
                evidence=row.get("evidence", ""),
                expected=row.get("expected", ""),
            ).with_inputs("client_context", "topic", "evidence")
            examples.append(ex)
    return examples

def main():
    lm_name = os.environ.get("AFO_DSPY_LM", "")
    if not lm_name:
        raise SystemExit("Set AFO_DSPY_LM")
    dspy.settings.configure(lm=dspy.LM(lm_name))

    trainset = load_gold(os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_client_onepager.jsonl"))
    program = ClientOnePager()

    optimizer = dspy.BootstrapFewShot(metric=objective_onepager)
    compiled = optimizer.compile(program, trainset=trainset)

    with open("data/dspy/compiled_client_onepager.json", "w", encoding="utf-8") as f:
        json.dump(compiled.dump_state(), f, ensure_ascii=False, indent=2)

    print("OK: data/dspy/compiled_client_onepager.json")

if __name__ == "__main__":
    main()
