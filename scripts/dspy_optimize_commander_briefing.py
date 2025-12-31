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

    # Configure DSPy with explicit key if available
    lm_kwargs = {"model": lm_name}
    if api_key:
        lm_kwargs["api_key"] = api_key

    dspy.settings.configure(lm=dspy.LM(**lm_kwargs))

    # Teacher Model for MIPROv2 (Stronger model for proposing instructions)
    # Using the same key/provider for simplicity, but forcing a stronger model if possible
    teacher_lm_name = "openai/gpt-4o"
    teacher_kwargs = {"model": teacher_lm_name}
    if api_key:
        teacher_kwargs["api_key"] = api_key
    teacher_lm = dspy.LM(**teacher_kwargs)

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
            print(f"🚀 Initializing {opt_name} Optimizer...")
            # MIPROv2/MIPRO configuration
            # - metric: The optimization objective (Trinity)
            # - prompt_model: The teacher model improving the prompt (GPT-4o)
            # - task_model: The student model (GPT-4o-mini) - implicitly dspy.settings.lm

            optimizer_kwargs = {
                "metric": calculate_trinity_objective,
                "prompt_model": teacher_lm,
                "teacher_settings": {"lm": teacher_lm},
            }

            # Handle different versions/signatures of MIPRO instantiation
            # Some versions use prompt_model, others use teacher_settings. passing both is safer if kwargs handled.
            # But strictly speaking, standard dspy MIPROv2 takes `metric`, `prompt_model`, `task_model`.

            try:
                optimizer = Opt(metric=calculate_trinity_objective, prompt_model=teacher_lm)
            except TypeError:
                # Fallback for older/newer signatures
                optimizer = Opt(metric=calculate_trinity_objective)

            print(f"🔥 Compiling with {opt_name} (Candidates=7, InitTemp=0.5)...")
            # Compile with specific robust hyperparameters
            compiled = optimizer.compile(
                program,
                trainset=trainset,
                num_candidates=7,
                init_temperature=0.5,
                max_bootstrapped_demos=2,
                max_labeled_demos=2,
                requires_permission_to_run=False,  # Don't ask for console input
            )
            print(f"✅ Optimization successful with {opt_name}")
        except Exception as e:
            print(f"⚠️  {opt_name} failed, fallback to BootstrapFewShot: {e}", file=sys.stderr)
            compiled = None  # Trigger fallback

    if compiled is None:
        print("💡 Falling back to standard BootstrapFewShot...")
        optimizer = dspy.BootstrapFewShot(
            metric=calculate_trinity_objective, max_bootstrapped_demos=2, max_labeled_demos=2
        )
        compiled = optimizer.compile(program, trainset=trainset)
        print("✅ Optimization successful with BootstrapFewShot")

    out = compiled.dump_state()
    out_path = "data/dspy/compiled_commander_briefing.v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"💾 Optimized program saved to: {out_path}")


if __name__ == "__main__":
    main()
