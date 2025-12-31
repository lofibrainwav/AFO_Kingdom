from __future__ import annotations

import glob
import hashlib
import math
import os
import re
from typing import List, Tuple

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,}|[가-힣]{2,}")


def _tokens(s: str) -> list[str]:
    out = []
    for m in _WORD.finditer(s or ""):
        t = m.group(0).lower()
        if t in {
            "the",
            "and",
            "for",
            "with",
            "from",
            "this",
            "that",
            "are",
            "was",
            "were",
            "http",
            "https",
        }:
            continue
        out.append(t)
    return out


def _hash_embed(text: str, dim: int = 384) -> list[float]:
    v = [0.0] * dim
    toks = _tokens(text)
    if not toks:
        return v
    freq = {}
    for t in toks:
        freq[t] = freq.get(t, 0) + 1
    for t, c in freq.items():
        h = int(hashlib.sha1(t.encode("utf-8", errors="ignore")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 1) & 1) == 1 else -1.0
        v[idx] += sign * (1.0 + math.log(1.0 + c))
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


def _score(q: str, text: str) -> float:
    qt = set(_tokens(q))
    if not qt:
        return 0.0
    tt = set(_tokens(text))
    inter = len(qt & tt)
    return inter / max(len(qt), 1)


def _excerpt(md: str, max_chars: int = 1200) -> str:
    s = (md or "").strip().replace("\r\n", "\n")
    return s if len(s) <= max_chars else s[:max_chars]


def _qdrant_search(question: str, top_k: int) -> list[str]:
    url = os.environ.get("AFO_QDRANT_URL", "http://localhost:6333").strip()
    collection = os.environ.get("AFO_OBSIDIAN_COLLECTION", "obsidian_vault").strip()
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(url=url)
        vec = _hash_embed(question)
        hits = client.search(
            collection_name=collection,
            query_vector=vec,
            limit=max(1, top_k),
            with_payload=True,
        )
        out = []
        for h in hits:
            p = getattr(h, "payload", None) or {}
            txt = p.get("text") if isinstance(p, dict) else None
            if isinstance(txt, str) and txt.strip():
                out.append(txt.strip())
        return out
    except Exception:
        return []


def retrieve_obsidian_docs(question: str, top_k: int = 5) -> list[str]:
    vault = os.environ.get("AFO_OBSIDIAN_VAULT", "").strip()
    if not vault:
        return []

    if os.environ.get("AFO_OBSIDIAN_QDRANT", "1").strip() == "1":
        docs = _qdrant_search(question, top_k=top_k)
        if docs:
            return docs

    use_llama = os.environ.get("AFO_LLAMAIDX_ON", "0").strip() == "1"
    if use_llama:
        try:
            from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

            docs = SimpleDirectoryReader(vault, recursive=True, required_exts=[".md"]).load_data()
            index = VectorStoreIndex.from_documents(docs)
            qe = index.as_query_engine(similarity_top_k=max(1, top_k))
            resp = qe.query(question)
            txt = str(resp) if resp is not None else ""
            if txt.strip():
                return [txt.strip()]
        except Exception:
            pass

    scored: list[tuple[float, str]] = []
    for fp in glob.glob(os.path.join(vault, "**/*.md"), recursive=True):
        try:
            with open(fp, encoding="utf-8") as f:
                md = f.read()
            sc = _score(question, md)
            if sc <= 0:
                continue
            scored.append((sc, _excerpt(md)))
        except Exception:
            continue

    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored[: max(1, top_k)]]
