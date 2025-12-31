# Language: ko-KR (AFO SSOT)
import argparse
import glob
import hashlib
import json
import os
import subprocess
import time

import dspy

from AFO.dspy.factcard_auto_evidence_graphrag import FactCardAutoEvidenceGraphRAG


def _read_jsonl(path: str):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    out.append(obj)
            except Exception:
                continue
    return out


def _append_jsonl(path: str, row: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def _pick_question(row: dict) -> str:
    for k in ("question", "query", "q", "text", "input", "prompt"):
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _collect_questions(input_globs: list[str], limit: int) -> list[str]:
    qs = []
    seen = set()
    for pat in input_globs:
        for fp in glob.glob(pat):
            for row in _read_jsonl(fp):
                q = _pick_question(row)
                if not q:
                    continue
                h = _sha1(q)
                if h in seen:
                    continue
                seen.add(h)
                qs.append(q)
                if len(qs) >= limit:
                    return qs
    return qs


def _already_done_hashes(paths: list[str]) -> set[str]:
    done = set()
    for p in paths:
        for row in _read_jsonl(p):
            q = row.get("question")
            fc = row.get("fact_card")
            if isinstance(row.get("id"), str):
                done.add(row["id"])
            if isinstance(q, str) and isinstance(fc, str):
                done.add(_sha1(q + "\n" + fc))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--inputs",
        nargs="*",
        default=[
            "data/dspy/rag_shadow*.jsonl",
            "data/dspy/factcard_autoevidence_runs.jsonl",
            "data/dspy/*.jsonl",
        ],
    )
    ap.add_argument("--runs_out", default="data/dspy/factcard_graphrag_runs.jsonl")
    ap.add_argument("--gold_out", default="data/dspy/gold_factcard_graphrag.jsonl")
    ap.add_argument("--candidates_out", default="data/dspy/gold_candidates_graphrag.jsonl")
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--min_score", type=float, default=0.90)
    ap.add_argument("--candidate_min", type=float, default=0.75)
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--mock", action="store_true", help="Use DummyLM for verification")
    args = ap.parse_args()

    lm_name = os.environ.get("AFO_DSPY_LM", "").strip()

    # Mock Support for Verification
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
                '{"fact_card": "[GraphRAG Harvest] Harvested Evidence... [MOCK VERIFIED]"}'
            ])
        )
    else:
        if not lm_name:
            raise SystemExit("Set AFO_DSPY_LM (e.g., openai/gpt-4.1-mini)")
        dspy.settings.configure(lm=dspy.LM(lm_name))

    base_url = os.environ.get("AFO_BASE_URL", "http://localhost:8010")
    rag_path = os.environ.get("AFO_RAG_PATH", "/api/query")
    ctx_path = os.environ.get("AFO_CONTEXT7_PATH", "/api/context7/search")
    idx_path = os.environ.get("AFO_GRAPHRAG_INDEX", "data/dspy/graphrag_index.json")

    # Build Index Step
    print("Building GraphRAG Index...")
    subprocess.run(
        ["poetry", "run", "python", "scripts/graphrag_build_index.py", "--out", idx_path],
        check=True,
    )

    questions = _collect_questions(args.inputs, args.limit)
    if not questions:
        print("OK: no new questions found to harvest")
        return  # Not an error, just empty

    prog = FactCardAutoEvidenceGraphRAG(top_k=args.topk)

    done = _already_done_hashes([args.runs_out, args.gold_out, args.candidates_out])

    executed = 0
    print(f"Harvesting {len(questions)} questions...")
    for q in questions:
        t0 = time.time()
        # Mock logic injection for Evidence retrieval if mock
        if args.mock:
            # Just skip real retrieval if mock, FactCardAutoEvidenceGraphRAG might fail connection if used
            pass

        try:
            pred = prog(question=q)
            fc = getattr(pred, "fact_card", "")
        except Exception as e:
            print(f"Error processing question '{q[:30]}...': {e}")
            continue

        if not isinstance(fc, str):
            fc = str(fc)
        rid = _sha1(q + "\n" + fc)
        if rid in done:
            continue
        row = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "question": q,
            "fact_card": fc,
            "elapsed_s": round(time.time() - t0, 3),
            "base_url": base_url,
            "rag_path": rag_path,
            "context7_path": ctx_path,
            "graphrag_index": idx_path,
        }
        _append_jsonl(args.runs_out, row)
        done.add(rid)
        executed += 1
        print(f"Harvested: {q[:40]}...")

    print(f"OK: graphrag factcards appended: {executed}")
    if executed == 0:
        return

    # Promote Step
    promote_cmd = [
        "poetry",
        "run",
        "python",
        "scripts/dspy_promote_graphrag_gold.py",
        "--infile",
        args.runs_out,
        "--gold_out",
        args.gold_out,
        "--candidates_out",
        args.candidates_out,
        "--min_score",
        str(args.min_score),
        "--candidate_min",
        str(args.candidate_min),
    ]
    if args.commit:
        promote_cmd.append("--commit")

    print("Running Promotion Gate...")
    subprocess.run(promote_cmd, check=True)


if __name__ == "__main__":
    main()
