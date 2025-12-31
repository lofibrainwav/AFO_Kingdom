import json
import os
import sys
from importlib import import_module

import dspy

from AFO.dspy.commander_briefing import CommanderBriefing
from AFO.dspy.metrics_v2 import calculate_trinity_objective


def load_gold(path: str):
    examples = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ex = dspy.Example(
                command=row["command"],
                context=row.get("context", ""),
                expected=row["expected"],
            ).with_inputs("command", "context")
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

    # TICKET-002: API Wallet Integration Logic (Adapter)
    if not api_key:
        try:
            from AFO.api_wallet import APIWallet

            print("🔐 Accessing API Wallet to fetch OpenAI key...")
            wallet = APIWallet()
            fetched_key = wallet.get("openai", decrypt=True) or wallet.get(
                "OPENAI_API_KEY", decrypt=True
            )

            if fetched_key:
                print("✅ Key retrieved from API Wallet.")
                api_key = fetched_key
                os.environ["OPENAI_API_KEY"] = api_key  # Inject to Env for subprocesses/litellm
            else:
                print("⚠️  Key 'openai' not found in API Wallet.")
        except Exception as e:
            print(f"⚠️  API Wallet access failed: {e}")

    if not lm_name:
        lm_name = "openai/gpt-4o-mini"  # Default fallback
        # raise SystemExit("Set AFO_DSPY_LM (e.g. openai/..., anthropic/...)") # Relaxing strictly for dev/default

    # Configure DSPy with explicit key if available
    lm_kwargs = {"model": lm_name}
    if api_key:
        lm_kwargs["api_key"] = api_key

    dspy.settings.configure(lm=dspy.LM(**lm_kwargs))

    gold_path = os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_commander_briefing.jsonl")
    if not os.path.exists(gold_path):
        print(f"Error: Gold data file not found at {gold_path}")
        return

    trainset = load_gold(gold_path)

    program = CommanderBriefing()

    Opt, opt_name = get_optimizer()
    compiled = None

    if Opt is not None:
        try:
            # MIPROv2/MIPRO usually require a metric and maybe other params like prompt_model/task_model
            # For simplicity using metric only as starter
            optimizer = Opt(metric=calculate_trinity_objective)
            # MIPROv2 compile signature might differ slightly but generally consistent
            compiled = optimizer.compile(program, trainset=trainset)
            print(f"OK: optimizer={opt_name}")
        except Exception as e:
            print(f"WARN: {opt_name} failed, fallback to BootstrapFewShot: {e}", file=sys.stderr)

    if compiled is None:
        optimizer = dspy.BootstrapFewShot(
            metric=calculate_trinity_objective, max_bootstrapped_demos=2, max_labeled_demos=2
        )
        compiled = optimizer.compile(program, trainset=trainset)
        print("OK: optimizer=BootstrapFewShot")

    out = compiled.dump_state()
    out_path = "data/dspy/compiled_commander_briefing.v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"OK: {out_path}")


if __name__ == "__main__":
    main()
