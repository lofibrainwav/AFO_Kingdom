from __future__ import annotations

import glob
import hashlib
import json
import math
import os
import pathlib
import re
import time
from typing import Any, Dict, List


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
    freq: dict[str, int] = {}
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


def _sha1_file(fp: str) -> str:
    h = hashlib.sha1()
    with open(fp, "rb") as f:
        for b in iter(lambda: f.read(1024 * 256), b""):
            h.update(b)
    return h.hexdigest()


def _load_json(path: str, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save_json(path: str, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    vault = os.environ.get("AFO_OBSIDIAN_VAULT", "").strip()
    if not vault:
        raise SystemExit("Set AFO_OBSIDIAN_VAULT")

    url = os.environ.get("AFO_QDRANT_URL", "http://localhost:6333").strip()
    collection = os.environ.get("AFO_OBSIDIAN_COLLECTION", "obsidian_vault").strip()
    dim = int(os.environ.get("AFO_OBSIDIAN_DIM", "384"))
    size = int(os.environ.get("AFO_OBSIDIAN_CHUNK", "900"))
    overlap = int(os.environ.get("AFO_OBSIDIAN_OVERLAP", "120"))
    state_path = os.environ.get("AFO_OBSIDIAN_STATE", "data/dspy/obsidian_qdrant_state.json")

    state = _load_json(state_path, {"files": {}, "last_run": None})
    files_state: dict[str, Any] = (
        state.get("files", {}) if isinstance(state.get("files"), dict) else {}
    )

    md_files = sorted(glob.glob(os.path.join(vault, "**/*.md"), recursive=True))
    current = set(md_files)
    previous = set(files_state.keys())

    removed = sorted(list(previous - current))

    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models as M

        client = QdrantClient(url=url)

        existing = [c.name for c in client.get_collections().collections]
        if collection not in existing:
            client.create_collection(
                collection_name=collection,
                vectors_config=M.VectorParams(size=dim, distance=M.Distance.COSINE),
                optimizers_config=M.OptimizersConfigDiff(indexing_threshold=20000),
            )

        # 삭제 반영(파일 단위) — Qdrant 다운/권한 문제면 전체 스킵
        if removed:
            for fp in removed:
                try:
                    client.delete(
                        collection_name=collection,
                        points_selector=M.Filter(
                            must=[M.FieldCondition(key="path", match=M.MatchValue(value=fp))]
                        ),
                    )
                except Exception:
                    pass
                files_state.pop(fp, None)

        # 변경된 파일만 업서트
        changed = 0
        upserted_points = 0
        batch: list[M.PointStruct] = []

        for fp in md_files:
            try:
                mtime = os.path.getmtime(fp)
            except Exception:
                continue

            prev = files_state.get(fp) or {}
            prev_mtime = float(prev.get("mtime", 0.0) or 0.0)

            if prev and abs(mtime - prev_mtime) < 1e-6:
                continue

            # mtime이 바뀐 파일만 sha1 계산
            try:
                sha = _sha1_file(fp)
                prev_sha = str(prev.get("sha1") or "")
                if prev_sha == sha and prev:
                    files_state[fp] = {"mtime": mtime, "sha1": sha}
                    continue
            except Exception:
                continue

            try:
                md = pathlib.Path(fp).read_text(encoding="utf-8")
            except Exception:
                continue

            chunks = _chunk(md, size=size, overlap=overlap)
            for ci, ch in enumerate(chunks):
                vec = _hash_embed(ch, dim=dim)
                pid = hashlib.sha1(f"{fp}::{ci}".encode("utf-8", errors="ignore")).hexdigest()
                payload = {"path": fp, "chunk": ci, "text": ch, "sha1": sha}
                batch.append(M.PointStruct(id=pid, vector=vec, payload=payload))
                if len(batch) >= 256:
                    client.upsert(collection_name=collection, points=batch)
                    upserted_points += len(batch)
                    batch = []

            if chunks:
                changed += 1
            files_state[fp] = {"mtime": mtime, "sha1": sha}

        if batch:
            client.upsert(collection_name=collection, points=batch)
            upserted_points += len(batch)

        state["files"] = files_state
        state["last_run"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        _save_json(state_path, state)

        os.makedirs("data/dspy", exist_ok=True)
        with open("data/dspy/obsidian_refresh_report.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "asof": state["last_run"],
                    "vault": vault,
                    "qdrant_url": url,
                    "collection": collection,
                    "changed_files": changed,
                    "removed_files": len(removed),
                    "upserted_points": upserted_points,
                    "state": state_path,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print("OK: obsidian incremental refresh")
        print(f"- changed_files: {changed}")
        print(f"- removed_files: {len(removed)}")
        print(f"- upserted_points: {upserted_points}")
        print("- report: data/dspy/obsidian_refresh_report.json")

    except Exception as e:
        # Qdrant 다운이어도 운영 루프는 죽지 않게: state/summary는 다음 단계에서 계속
        os.makedirs("data/dspy", exist_ok=True)
        with open("data/dspy/obsidian_refresh_report.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "asof": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "vault": vault,
                    "qdrant_url": url,
                    "collection": collection,
                    "status": "skipped",
                    "reason": str(e)[:500],
                    "state": state_path,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print("WARN: qdrant unreachable or error -> skipped indexing")
        print("- report: data/dspy/obsidian_refresh_report.json")


if __name__ == "__main__":
    main()
