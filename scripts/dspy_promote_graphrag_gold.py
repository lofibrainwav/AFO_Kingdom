# Language: ko-KR (AFO SSOT)
import argparse
import hashlib
import json
import os
import re
import time


SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{10,}")
MOCK_RE = re.compile(r"\bMOCK\b|mock verified|mock_execution|mock execution", re.IGNORECASE)


def read_jsonl(path: str):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    rows.append(obj)
            except Exception:
                continue
    return rows


def append_jsonl(path: str, row: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def count_evidence_items(text: str) -> int:
    # Evidence 섹션의 "1) ...", "2) ..." 패턴 카운트
    return len(re.findall(r"(?m)^\s*\d+\)\s+\S", text or ""))


def count_sources(text: str) -> int:
    # Sources 섹션의 "- ..." 패턴 카운트
    return len(re.findall(r"(?m)^\s*-\s+\S", text or ""))


def has_heading(text: str, heading: str) -> bool:
    return bool(re.search(rf"(?m)^\s*{re.escape(heading)}\s*:\s*$", text or ""))


def has_graph_path(text: str) -> bool:
    if not text:
        return False
    m = re.search(r"(?m)^\s*-\s*Path:\s*(.+)$", text)
    if not m:
        return False
    p = m.group(1).strip().lower()
    if "(none)" in p or p == "none":
        return False
    return True


def compute_trinity_gate(fact_card: str) -> dict:
    """
    0..1 점수. 목표는 "진짜 A급만" 통과시키는 Gate.
    - Mock/secret/fetch_failed는 즉시 Fail
    """
    fc = fact_card or ""

    # hard fail conditions
    if SECRET_RE.search(fc):
        return {
            "score": 0.0,
            "truth": 0.0,
            "goodness": 0.0,
            "beauty": 0.0,
            "reason": "secret_detected",
        }
    if MOCK_RE.search(fc):
        return {"score": 0.0, "truth": 0.0, "goodness": 0.0, "beauty": 0.0, "reason": "mock_output"}
    if "evidence_fetch_failed" in fc or "(no_docs)" in fc:
        return {"score": 0.0, "truth": 0.0, "goodness": 0.0, "beauty": 0.0, "reason": "no_evidence"}

    # Structure
    h_e = has_heading(fc, "Evidence")
    h_g = has_heading(fc, "GraphReasoning")
    h_s = has_heading(fc, "Sources")

    ev_n = count_evidence_items(fc)
    src_n = count_sources(fc)
    gpath = has_graph_path(fc)

    # Truth (Evidence 중심)
    truth = 0.0
    truth += 0.25 if h_e else 0.0
    truth += 0.45 if ev_n >= 2 else (0.25 if ev_n == 1 else 0.0)
    truth += 0.20 if gpath else 0.0
    truth += 0.10 if "action" in fc.lower() or "next" in fc.lower() else 0.0
    truth = min(1.0, truth)

    # Goodness (출처/안전)
    goodness = 0.0
    goodness += 0.25 if h_s else 0.0
    goodness += 0.60 if src_n >= 2 else (0.30 if src_n == 1 else 0.0)
    goodness += 0.15 if ("risk" in fc.lower() or "caution" in fc.lower() or "주의" in fc) else 0.0
    goodness = min(1.0, goodness)

    # Beauty (형식/가독성)
    beauty = 0.0
    beauty += 0.20 if (h_e and h_s) else 0.0
    beauty += 0.20 if h_g else 0.0
    # 너무 긴 출력은 감점(가독성)
    length = len(fc)
    if length <= 2200:
        beauty += 0.40
    elif length <= 3200:
        beauty += 0.25
    else:
        beauty += 0.10
    # 최소 구조(섹션 3개) 보너스
    beauty += 0.20 if (h_e and h_g and h_s) else 0.0
    beauty = min(1.0, beauty)

    # Weighted Trinity (Truth 0.45 / Goodness 0.35 / Beauty 0.20)
    score = (0.45 * truth) + (0.35 * goodness) + (0.20 * beauty)
    score = max(0.0, min(1.0, score))

    reason = "ok"
    if not (h_e and h_s):
        reason = "missing_sections"
    elif ev_n < 2:
        reason = "insufficient_evidence"
    elif src_n < 2:
        reason = "insufficient_sources"
    elif not gpath:
        reason = "no_graph_path"

    return {
        "score": round(score, 4),
        "truth": round(truth, 4),
        "goodness": round(goodness, 4),
        "beauty": round(beauty, 4),
        "evidence_items": ev_n,
        "sources_items": src_n,
        "has_graph_path": bool(gpath),
        "reason": reason,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", default="data/dspy/factcard_graphrag_runs.jsonl")
    ap.add_argument("--gold_out", default="data/dspy/gold_factcard_graphrag.jsonl")
    ap.add_argument("--candidates_out", default="data/dspy/gold_candidates_graphrag.jsonl")
    ap.add_argument("--report_out", default="data/dspy/graphrag_promotion_report.json")
    ap.add_argument("--min_score", type=float, default=0.90)
    ap.add_argument("--candidate_min", type=float, default=0.75)
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    rows = read_jsonl(args.infile)
    existing_gold = read_jsonl(args.gold_out)
    existing_hashes = {r.get("id") for r in existing_gold if isinstance(r.get("id"), str)}

    promoted = 0
    candidates = 0
    rejected = 0

    samples = {"promoted": [], "candidates": [], "rejected": []}

    for r in rows:
        q = r.get("question") or ""
        fc = r.get("fact_card") or ""
        if not q or not fc:
            continue

        rid = sha1(q + "\n" + fc)
        if rid in existing_hashes:
            continue

        gate = compute_trinity_gate(fc)
        score = gate["score"]

        entry = {
            "id": rid,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "question": q,
            "fact_card": fc,
            "gate": gate,
            "meta": {
                "source": os.path.basename(args.infile),
                "graphrag_index": r.get("graphrag_index"),
                "base_url": r.get("base_url"),
                "rag_path": r.get("rag_path"),
            },
        }

        if score >= args.min_score:
            promoted += 1
            samples["promoted"].append({"id": rid, "score": score, "reason": gate["reason"]})
            if args.commit:
                append_jsonl(args.gold_out, entry)
        elif score >= args.candidate_min:
            candidates += 1
            samples["candidates"].append({"id": rid, "score": score, "reason": gate["reason"]})
            if args.commit:
                append_jsonl(args.candidates_out, entry)
        else:
            rejected += 1
            if len(samples["rejected"]) < 10:
                samples["rejected"].append({"id": rid, "score": score, "reason": gate["reason"]})

    report = {
        "asof": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "infile": args.infile,
        "gold_out": args.gold_out,
        "candidates_out": args.candidates_out,
        "min_score": args.min_score,
        "candidate_min": args.candidate_min,
        "commit": bool(args.commit),
        "counts": {"promoted": promoted, "candidates": candidates, "rejected": rejected},
        "samples": samples,
    }

    os.makedirs(os.path.dirname(args.report_out), exist_ok=True)
    with open(args.report_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("OK: GraphRAG Gold Promotion Gate")
    print(f"- infile: {args.infile}")
    print(f"- commit: {args.commit}")
    print(f"- promoted: {promoted}  candidates: {candidates}  rejected: {rejected}")
    print(f"- report: {args.report_out}")


if __name__ == "__main__":
    main()
