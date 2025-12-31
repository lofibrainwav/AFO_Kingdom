from __future__ import annotations

import glob
import hashlib
import json
import os
from typing import Any, Dict, List

from AFO.dspy.graphrag import build_graph


def _safe_json_loads(line: str):
    try:
        return json.loads(line)
    except Exception:
        return None


def _collect_texts_from_row(row: dict[str, Any]) -> list[str]:
    texts: list[str] = []

    # rag_shadow_mode v2 format: attempts[].top_docs[].text
    if isinstance(row.get("attempts"), list):
        for att in row["attempts"]:
            for td in att.get("top_docs") or []:
                t = td.get("text") if isinstance(td, dict) else None
                if isinstance(t, str) and t.strip():
                    texts.append(t)

    # older: top_docs
    for td in row.get("top_docs") or []:
        t = td.get("text") if isinstance(td, dict) else None
        if isinstance(t, str) and t.strip():
            texts.append(t)

    # factcard runs / onepager runs
    for k in ("fact_card", "one_pager", "evidence", "expected"):
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            texts.append(v)

    # raw response heads sometimes
    v = row.get("resp_head")
    if isinstance(v, str) and v.strip():
        texts.append(v)

    return texts


def build_index(input_globs: list[str], out_path: str) -> dict[str, Any]:
    docs: list[str] = []
    seen = set()

    for pat in input_globs:
        for fp in glob.glob(pat):
            try:
                with open(fp, encoding="utf-8") as f:
                    for line in f:
                        row = _safe_json_loads(line)
                        if not isinstance(row, dict):
                            continue
                        for t in _collect_texts_from_row(row):
                            h = hashlib.sha1(t.encode("utf-8", errors="ignore")).hexdigest()
                            if h in seen:
                                continue
                            seen.add(h)
                            docs.append(t)
            except Exception:
                continue

    g = build_graph(docs)
    payload = {
        "version": 1,
        "doc_count": len(docs),
        "node_count": len(g),
        "docs": docs,
        "graph": {k: sorted(list(v)) for k, v in g.items()},
    }

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return payload
