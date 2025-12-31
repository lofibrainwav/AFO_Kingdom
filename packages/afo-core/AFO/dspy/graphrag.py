from __future__ import annotations

import re
from collections import deque
from typing import Dict, List, Optional, Set, Tuple

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,}|[가-힣]{2,}")

_STOP = {
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
    "you",
    "your",
    "http",
    "https",
    "www",
    "json",
    "true",
    "false",
    "null",
}
_DOMAIN_BOOST = {
    "soul",
    "engine",
    "dashboard",
    "wallet",
    "qdrant",
    "redis",
    "postgres",
    "postgresql",
    "docker",
    "compose",
    "container",
    "health",
    "warning",
    "metrics",
    "dspy",
    "mipro",
    "context7",
    "openai",
    "anthropic",
    "apikey",
    "api",
    "endpoint",
    "rag",
    "retrieval",
}


def _norm(tok: str) -> str:
    t = tok.strip().lower()
    t = t.strip("-_")
    return t


def extract_entities(text: str) -> list[str]:
    if not text:
        return []
    ents: list[str] = []
    for m in _WORD.finditer(text):
        t = _norm(m.group(0))
        if not t or t in _STOP:
            continue
        if len(t) < 3 and t not in _DOMAIN_BOOST:
            continue
        ents.append(t)
    # dedup preserve order
    seen = set()
    out = []
    for e in ents:
        if e not in seen:
            seen.add(e)
            out.append(e)
    return out


def build_graph(docs: list[str]) -> dict[str, set[str]]:
    g: dict[str, set[str]] = {}
    for d in docs:
        ents = extract_entities(d)
        if not ents:
            continue
        for e in ents:
            g.setdefault(e, set())
        # co-occurrence clique (safe, simple)
        for i in range(len(ents)):
            a = ents[i]
            for j in range(i + 1, len(ents)):
                b = ents[j]
                if a == b:
                    continue
                g[a].add(b)
                g[b].add(a)
    return g


def shortest_path(
    g: dict[str, set[str]], srcs: list[str], dsts: list[str]
) -> tuple[list[str] | None, int]:
    srcs_n = [s for s in srcs if s in g]
    dsts_set = {d for d in dsts if d in g}
    if not srcs_n or not dsts_set:
        return None, 10**9

    q = deque()
    prev: dict[str, str | None] = {}
    for s in srcs_n:
        q.append(s)
        prev[s] = None

    while q:
        cur = q.popleft()
        if cur in dsts_set:
            # reconstruct
            path = [cur]
            while prev[path[-1]] is not None:
                path.append(prev[path[-1]])
            path.reverse()
            return path, len(path) - 1
        for nxt in g.get(cur, ()):
            if nxt not in prev:
                prev[nxt] = cur
                q.append(nxt)
    return None, 10**9


def token_overlap_score(question: str, doc: str) -> float:
    q = set(extract_entities(question))
    d = set(extract_entities(doc))
    if not q or not d:
        return 0.0
    inter = len(q & d)
    return inter / max(len(q), 1)


def rerank(
    question: str, docs: list[str], top_k: int = 5
) -> tuple[list[tuple[float, str, list[str] | None]], dict]:
    q_ents = extract_entities(question)
    g = build_graph(docs)

    ranked: list[tuple[float, str, list[str] | None]] = []
    debug = {"q_entities": q_ents[:20], "graph_nodes": len(g)}
    for d in docs:
        d_ents = extract_entities(d)
        ov = token_overlap_score(question, d)

        path, dist = shortest_path(g, q_ents, d_ents)
        bridge = 0.0 if dist >= 10**9 else (1.0 / (1.0 + float(dist)))

        # domain boost: if doc contains domain entities, mild bump
        dom = 0.0
        de = set(d_ents)
        hit = len(de & _DOMAIN_BOOST)
        if hit:
            dom = min(hit * 0.03, 0.18)

        score = (0.45 * ov) + (0.45 * bridge) + (0.10 * dom)
        ranked.append((score, d, path))

    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked[: max(1, top_k)], debug


def format_evidence(question: str, ranked: list[tuple[float, str, list[str] | None]]) -> str:
    lines = []
    lines.append("Evidence:")
    for i, (s, d, _path) in enumerate(ranked, 1):
        head = (d or "").strip().replace("\r\n", "\n")
        lines.append(f"{i}) (score={s:.3f}) {head[:900]}")
    # reasoning
    lines.append("GraphReasoning:")
    best_path = None
    for _s, _d, p in ranked:
        if p and len(p) >= 2:
            best_path = p
            break
    if best_path:
        lines.append("- Path: " + " -> ".join(best_path[:18]))
    else:
        lines.append("- Path: (none)")

    lines.append("Sources:")
    lines.append("- (auto) graphrag_rerank")
    lines.append("- (auto) internal_rag_or_context7")
    return "\n".join(lines)
