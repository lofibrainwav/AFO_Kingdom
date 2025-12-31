from __future__ import annotations

import glob
import hashlib
import json
import math
import os
import pathlib
import re
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http import models as M


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


def _chunk(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    s = (text or "").strip().replace("\r\n", "\n")
    if not s:
        return []
    out = []
    i = 0
    n = len(s)
    while i < n:
        j = min(n, i + size)
        out.append(s[i:j])
        if j == n:
            break
        i = max(0, j - overlap)
    return out


def main():
    vault = os.environ.get("AFO_OBSIDIAN_VAULT", "").strip()
    if not vault:
        raise SystemExit("Set AFO_OBSIDIAN_VAULT")

    url = os.environ.get("AFO_QDRANT_URL", "http://localhost:6333").strip()
    collection = os.environ.get("AFO_OBSIDIAN_COLLECTION", "obsidian_vault").strip()
    dim = int(os.environ.get("AFO_OBSIDIAN_DIM", "384"))
    size = int(os.environ.get("AFO_OBSIDIAN_CHUNK", "900"))
    overlap = int(os.environ.get("AFO_OBSIDIAN_OVERLAP", "120"))

    print(f"Connecting to Qdrant at {url}...")
    try:
        client = QdrantClient(url=url)
        # Simple check to verify connection
        client.get_collections()
    except Exception as e:
        print(f"WARNING: Qdrant unreachable ({e}). Skipping indexing.")
        return

    existing = [c.name for c in client.get_collections().collections]
    if collection not in existing:
        client.create_collection(
            collection_name=collection,
            vectors_config=M.VectorParams(size=dim, distance=M.Distance.COSINE),
            optimizers_config=M.OptimizersConfigDiff(indexing_threshold=20000),
        )

    points = []
    pid = 1
    for fp in glob.glob(os.path.join(vault, "**/*.md"), recursive=True):
        try:
            md = pathlib.Path(fp).read_text(encoding="utf-8")
        except Exception:
            continue

        chunks = _chunk(md, size=size, overlap=overlap)
        for ci, ch in enumerate(chunks):
            vec = _hash_embed(ch, dim=dim)
            payload = {
                "path": fp,
                "chunk": ci,
                "text": ch,
            }
            points.append(M.PointStruct(id=pid, vector=vec, payload=payload))
            pid += 1
            if len(points) >= 256:
                client.upsert(collection_name=collection, points=points)
                points = []

    if points:
        client.upsert(collection_name=collection, points=points)

    manifest = {
        "vault": vault,
        "qdrant_url": url,
        "collection": collection,
        "dim": dim,
        "chunk": size,
        "overlap": overlap,
    }
    os.makedirs("data/dspy", exist_ok=True)
    with open("data/dspy/obsidian_qdrant_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("OK: obsidian indexed to qdrant")
    print(f"- vault: {vault}")
    print(f"- collection: {collection}")
    print("- manifest: data/dspy/obsidian_qdrant_manifest.json")


if __name__ == "__main__":
    main()
