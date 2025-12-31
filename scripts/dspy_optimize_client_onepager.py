import json
import os
import sys
from importlib import import_module

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

def get_optimizer():
    candidates = [
        ("dspy.teleprompt", "MIPROv2"),
        ("dspy.teleprompt", "MIPRO"),
        ("dspy.teleprompt.mipro", "MIPROv2"),
        ("dspy.teleprompt.mipro", "MIPRO"),
    ]
    for mod, cls in candidates:
        try:
            m = import_module(mod)
            if hasattr(m, cls):
                return getattr(m, cls), cls
        except Exception:
            continue
    return None, None

def main():
    lm_name = os.environ.get("AFO_DSPY_LM", "")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        try:
            from AFO.api_wallet import APIWallet
            wallet = APIWallet()
            fetched_key = wallet.get("openai", decrypt=True) or wallet.get("OPENAI_API_KEY", decrypt=True)
            if fetched_key:
                os.environ["OPENAI_API_KEY"] = fetched_key
                api_key = fetched_key
        except Exception:
            pass

    lm_kwargs = {"model": lm_name if lm_name else "openai/gpt-4o-mini"}
    if api_key:
        lm_kwargs["api_key"] = api_key
    dspy.settings.configure(lm=dspy.LM(**lm_kwargs))

    gold_path = os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_client_onepager.jsonl")
    trainset = load_gold(gold_path)

    program = ClientOnePager()
    Opt, opt_name = get_optimizer()
    compiled = None

    if Opt is not None:
        try:
            optimizer = Opt(metric=objective_onepager)
            compiled = optimizer.compile(program, trainset=trainset)
            print(f"OK: optimizer={opt_name}")
        except Exception as e:
            print(f"WARN: {opt_name} failed, fallback to BootstrapFewShot: {e}", file=sys.stderr)

    if compiled is None:
        optimizer = dspy.BootstrapFewShot(metric=objective_onepager)
        compiled = optimizer.compile(program, trainset=trainset)
        print("OK: optimizer=BootstrapFewShot")

    out_path = "data/dspy/compiled_client_onepager.v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(compiled.dump_state(), f, ensure_ascii=False, indent=2)
    print(f"OK: {out_path}")

if __name__ == "__main__":
    main()
