import argparse
import json
import os
import time

from AFO.dspy.obsidian_shadow import retrieve_obsidian_docs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--topk", type=int, default=3)
    ap.add_argument("--out", default="data/dspy/obsidian_shadow.jsonl")
    args = ap.parse_args()

    docs = retrieve_obsidian_docs(args.question, top_k=args.topk)
    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "question": args.question,
        "top_docs": [{"text": d[:1400]} for d in docs],
        "vault": os.environ.get("AFO_OBSIDIAN_VAULT", ""),
        "llamaidx_on": os.environ.get("AFO_LLAMAIDX_ON", "0"),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("OK: obsidian shadow probe")
    print(f"- out: {args.out}")
    print(f"- docs: {len(docs)}")


if __name__ == "__main__":
    main()
