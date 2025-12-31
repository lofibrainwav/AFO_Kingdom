import argparse
import json
import os
import time

import dspy

from AFO.dspy.factcard_auto_evidence import FactCardAutoEvidence


def append_jsonl(path: str, row: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--out", default="data/dspy/factcard_autoevidence_runs.jsonl")
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--mock", action="store_true", help="Use DummyLM for verification")
    args = ap.parse_args()

    if args.mock:
        # Inline DummyLM for DSPy 3.x compatibility
        class DummyLM(dspy.LM):
            def __init__(self, answers):
                super().__init__("dummy")
                self.answers = answers

            def __call__(self, prompt=None, **kwargs):
                return self.answers

            def basic_request(self, prompt, **kwargs):
                # Return format expected by DSPy Predict/ChainOfThought
                # usually list of strings or dicts
                return {"completions": [{"text": a} for a in self.answers]}

        dspy.settings.configure(
            lm=DummyLM(['{"fact_card": "[FactCard] Evidence based on sources... [MOCK VERIFIED]"}'])
        )
    else:
        lm_name = os.environ.get("AFO_DSPY_LM", "")
        if not lm_name:
            raise SystemExit("Set AFO_DSPY_LM (e.g., openai/gpt-4o-mini)")

        # Try to load API Key from APIWallet if not in Env
        if not os.environ.get("OPENAI_API_KEY"):
            try:
                from AFO.api_wallet import APIWallet

                wallet = APIWallet()
                key = wallet.get("openai") or wallet.get("OPENAI_API_KEY")
                if key:
                    os.environ["OPENAI_API_KEY"] = key
                    print(f"Loaded OPENAI_API_KEY from Wallet: {key[:5]}...")
            except ImportError:
                pass  # APIWallet might not be available or setup
            except Exception as e:
                print(f"Warning: Failed to load key from Wallet: {e}")

        dspy.settings.configure(lm=dspy.LM(lm_name))

    t0 = time.time()

    # Explicitly calculate evidence for logging/verification
    if args.mock:
        from AFO.dspy.rag_helpers import retrieve_evidence

        ev = retrieve_evidence(args.question, top_k=args.topk)
        print(f"DEBUG: Retrieved Evidence:\n{ev}\n")

    prog = FactCardAutoEvidence(top_k=args.topk)
    pred = prog(question=args.question)
    fact_card = getattr(pred, "fact_card", "")

    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "question": args.question,
        "fact_card": fact_card,
        "elapsed_s": round(time.time() - t0, 3),
        "base_url": os.environ.get("AFO_BASE_URL", "http://localhost:8010"),
        "rag_path": os.environ.get("AFO_RAG_PATH", "/api/query"),
    }
    append_jsonl(args.out, row)

    print("OK: FactCardAutoEvidence")
    print(f"- out: {args.out}")
    print(fact_card[:1200])


if __name__ == "__main__":
    main()
