import argparse
import json
import os
import time

import dspy

from AFO.dspy.factcard_auto_evidence_graphrag import FactCardAutoEvidenceGraphRAG


def append_jsonl(path: str, row: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--out", default="data/dspy/factcard_graphrag_runs.jsonl")
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
                return {"completions": [{"text": a} for a in self.answers]}

        dspy.settings.configure(
            lm=DummyLM([
                '{"fact_card": "[GraphRAG FactCard] Evidence with Reasoning... [MOCK VERIFIED]"}'
            ])
        )
    else:
        lm_name = os.environ.get("AFO_DSPY_LM", "")
        if not lm_name:
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
                    pass
                except Exception as e:
                    print(f"Warning: Failed to load key from Wallet: {e}")

            # Check again or just warn
            if (
                not os.environ.get("OPENAI_API_KEY")
                and not os.environ.get("ANTHROPIC_API_KEY")
                and "openai" in lm_name
            ):
                raise SystemExit("Set AFO_DSPY_LM and keys.")

            if not lm_name:
                raise SystemExit("Set AFO_DSPY_LM (e.g., openai/gpt-4o-mini)")

        dspy.settings.configure(lm=dspy.LM(lm_name))

    t0 = time.time()

    # Debug print evidence logic if in mock mode
    if args.mock:
        from AFO.dspy.rag_evidence_graphrag import retrieve_evidence_graphrag

        print("DEBUG: Calculating GraphRAG evidence...")
        ev = retrieve_evidence_graphrag(args.question, top_k=args.topk)
        print(f"DEBUG: Retrieved Evidence:\n{ev}\n")

    prog = FactCardAutoEvidenceGraphRAG(top_k=args.topk)
    pred = prog(question=args.question)
    fact_card = getattr(pred, "fact_card", "")

    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "question": args.question,
        "fact_card": fact_card,
        "elapsed_s": round(time.time() - t0, 3),
        "base_url": os.environ.get("AFO_BASE_URL", "http://localhost:8010"),
        "rag_path": os.environ.get("AFO_RAG_PATH", "/api/query"),
        "context7_path": os.environ.get("AFO_CONTEXT7_PATH", "/api/context7/search"),
        "graphrag_index": os.environ.get("AFO_GRAPHRAG_INDEX", "data/dspy/graphrag_index.json"),
    }
    append_jsonl(args.out, row)

    print("OK: FactCardAutoEvidenceGraphRAG")
    print(f"- out: {args.out}")
    print(fact_card[:1400])


if __name__ == "__main__":
    main()
