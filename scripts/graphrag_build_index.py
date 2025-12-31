import argparse

from AFO.dspy.graphrag_index import build_index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/dspy/graphrag_index.json")
    ap.add_argument(
        "--inputs",
        nargs="*",
        default=[
            "data/dspy/rag_shadow*.jsonl",
            "data/dspy/factcard_autoevidence_runs.jsonl",
            "data/dspy/*.jsonl",
        ],
    )
    args = ap.parse_args()

    payload = build_index(args.inputs, args.out)
    print("OK: GraphRAG index built")
    print(f"- out: {args.out}")
    print(f"- docs: {payload['doc_count']}")
    print(f"- nodes: {payload['node_count']}")


if __name__ == "__main__":
    main()
