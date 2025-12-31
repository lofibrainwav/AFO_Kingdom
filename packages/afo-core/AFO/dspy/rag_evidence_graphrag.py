from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from AFO.dspy.graphrag import format_evidence, rerank
from AFO.dspy.obsidian_shadow import retrieve_obsidian_docs


def _http_post_json(url: str, payload: dict, timeout: float = 10.0):
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url, data=data, headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    with urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="replace")
        return r.status, body


def _http_get(url: str, timeout: float = 8.0):
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="replace")
        return r.status, body


def _extract_chunks(resp):
    if isinstance(resp, dict):
        for k in ("documents", "docs", "contexts", "context", "sources", "results", "hits"):
            v = resp.get(k)
            if isinstance(v, list) and v:
                out = []
                for it in v:
                    if isinstance(it, str):
                        out.append(it)
                    elif isinstance(it, dict):
                        for kk in (
                            "text",
                            "content",
                            "snippet",
                            "chunk",
                            "page_content",
                            "document",
                            "doc",
                        ):
                            if kk in it and isinstance(it[kk], str) and it[kk].strip():
                                out.append(it[kk])
                                break
                return out
        for k in ("answer", "response", "text", "content", "message", "detail", "error"):
            v = resp.get(k)
            if isinstance(v, str) and v.strip():
                return [v]
        return [json.dumps(resp, ensure_ascii=False)]
    if isinstance(resp, str) and resp.strip():
        return [resp]
    return []


def _try_inprocess(question: str, top_k: int):
    try:
        import AFO.dspy.rag_integration as ri
    except Exception:
        return None

    for name in (
        "retrieve",
        "search",
        "query",
        "rag_query",
        "run_query",
        "get_context",
        "get_docs",
    ):
        fn = getattr(ri, name, None)
        if callable(fn):
            try:
                out = fn(question, top_k=top_k)
                return out
            except TypeError:
                try:
                    return fn(question)
                except Exception:
                    pass
            except Exception:
                pass
    return None


def _normalize_to_docs(obj):
    if obj is None:
        return []
    if isinstance(obj, list):
        return [str(x) for x in obj if str(x).strip()]
    if isinstance(obj, dict):
        return _extract_chunks(obj)
    return [str(obj)]


def _load_index_docs() -> list[str]:
    path = os.environ.get("AFO_GRAPHRAG_INDEX", "data/dspy/graphrag_index.json")
    try:
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        docs = payload.get("docs") or []
        return [d for d in docs if isinstance(d, str) and d.strip()]
    except Exception:
        return []


def fetch_candidate_docs(question: str, top_k: int = 8) -> list[str]:
    merged: list[str] = []

    # 0) Obsidian Shadow (optional, no impact if env missing)
    try:
        obs = retrieve_obsidian_docs(question, top_k=max(1, min(5, top_k)))
        if obs:
            merged.extend(obs)
    except Exception:
        pass

    # 1) in-process RAG
    out = _try_inprocess(question, top_k=top_k)
    docs = _normalize_to_docs(out)
    if docs:
        merged.extend(docs)

    base = os.environ.get("AFO_BASE_URL", "http://localhost:8010").rstrip("/")
    rag_path = os.environ.get("AFO_RAG_PATH", "/api/query")
    url = base + rag_path

    payloads = [
        {"query": question},
        {"question": question},
        {"q": question},
        {"text": question},
        {"input": question},
        {"prompt": question},
    ]
    for pl in payloads:
        try:
            st, body = _http_post_json(url, pl, timeout=12.0)
            if st in (200, 201):
                try:
                    resp = json.loads(body)
                except Exception:
                    resp = body
                docs = _extract_chunks(resp)
                if docs:
                    merged.extend(docs)
                    break
                if isinstance(resp, str) and resp.strip():
                    merged.append(resp)
                    break
        except (HTTPError, URLError, Exception):
            continue

    # 2) Context7 GET fallback
    ctx_path = os.environ.get("AFO_CONTEXT7_PATH", "/api/context7/search")
    ctx_url = base + ctx_path
    for key in ("q", "query"):
        try:
            qs = urlencode({key: question})
            st, body = _http_get(ctx_url + ("&" if "?" in ctx_url else "?") + qs, timeout=10.0)
            if st == 200:
                try:
                    resp = json.loads(body)
                except Exception:
                    resp = body
                docs = _extract_chunks(resp)
                if docs:
                    merged.extend(docs)
                    break
        except Exception:
            continue

    # dedup + trim
    out_docs = []
    seen = set()
    for d in merged:
        s = str(d).strip()
        if not s:
            continue
        h = hash(s[:200])
        if h in seen:
            continue
        seen.add(h)
        out_docs.append(s)
        if len(out_docs) >= max(8, top_k * 2):
            break
    return out_docs


def retrieve_evidence_graphrag(question: str, top_k: int = 5) -> str:
    live_docs = fetch_candidate_docs(question, top_k=max(8, top_k * 2))
    index_docs = _load_index_docs()

    merged = list(live_docs)
    if index_docs:
        merged.extend(index_docs[:200])

    if not merged:
        return "Evidence:\n1) (no_docs)\nGraphReasoning:\n- Path: (none)\nSources:\n- (auto) graphrag_rerank\n- (auto) none"

    ranked, _debug = rerank(question, merged, top_k=top_k)
    return format_evidence(question, ranked)
