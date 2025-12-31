import argparse
import json
import os
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def http_get(url: str, timeout: float = 3.0):
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="replace")
        return r.status, body


def http_post(url: str, payload: dict, timeout: float = 8.0):
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url, data=data, headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    with urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", errors="replace")
        return r.status, body


def try_openapi(base: str):
    for p in ("/openapi.json", "/api/openapi.json"):
        url = base.rstrip("/") + p
        try:
            st, body = http_get(url, timeout=3.0)
            if st == 200:
                return url, json.loads(body)
        except Exception:
            pass
    return None, None


def discover(base_urls):
    for b in base_urls:
        url, spec = try_openapi(b)
        if spec:
            return b, url, spec
    return None, None, None


def find_paths(spec: dict):
    paths = list((spec.get("paths") or {}).keys())
    key = re.compile(r"(rag|retriev|search|query|context|docs|document|qdrant)", re.IGNORECASE)
    cand = [p for p in paths if key.search(p)]
    return sorted(cand)


def tokenize(s: str):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9가-힣\s]", " ", s)
    toks = [t for t in s.split() if len(t) >= 2]
    return toks


def overlap_score(q: str, d: str) -> float:
    qt = set(tokenize(q))
    dt = set(tokenize(d))
    if not qt or not dt:
        return 0.0
    inter = len(qt & dt)
    return inter / max(len(qt), 1)


def extract_docs(resp):
    if isinstance(resp, dict):
        for k in ("documents", "docs", "contexts", "context", "sources", "results", "hits"):
            v = resp.get(k)
            if isinstance(v, list) and v:
                out = []
                for item in v:
                    if isinstance(item, str):
                        out.append(item)
                    elif isinstance(item, dict):
                        for kk in (
                            "text",
                            "content",
                            "chunk",
                            "page_content",
                            "snippet",
                            "document",
                            "doc",
                        ):
                            if kk in item and isinstance(item[kk], str):
                                out.append(item[kk])
                                break
                        else:
                            out.append(json.dumps(item, ensure_ascii=False))
                return out
        for k in ("text", "content", "answer", "response", "message", "detail", "error"):
            v = resp.get(k)
            if isinstance(v, str) and v.strip():
                return [v]
    if isinstance(resp, str) and resp.strip():
        return [resp]
    return []


def resp_text(resp):
    if isinstance(resp, dict):
        for k in ("message", "detail", "error", "response", "text"):
            v = resp.get(k)
            if isinstance(v, str) and v.strip():
                return v
        return json.dumps(resp, ensure_ascii=False)[:500]
    return str(resp)[:500]


def call_post_then_get(base: str, path: str, question: str):
    url = base.rstrip("/") + path
    payloads = [
        {"query": question},
        {"question": question},
        {"text": question},
        {"prompt": question},
        {"input": question},
        {"q": question},
    ]
    last_err = None
    for pl in payloads:
        try:
            st, body = http_post(url, pl, timeout=10.0)
            if st in (200, 201):
                try:
                    return {"url": url, "method": "POST", "payload": pl, "resp": json.loads(body)}
                except Exception:
                    return {"url": url, "method": "POST", "payload": pl, "resp": body}
        except HTTPError as e:
            last_err = f"HTTPError {e.code}"
        except URLError as e:
            last_err = f"URLError {e}"
        except Exception as e:
            last_err = str(e)

    # GET fallback: try q= / query=
    for key in ("q", "query"):
        try:
            qs = urlencode({key: question})
            get_url = url + ("&" if "?" in url else "?") + qs
            st, body = http_get(get_url, timeout=6.0)
            if st == 200:
                try:
                    return {
                        "url": get_url,
                        "method": "GET",
                        "payload": {key: question},
                        "resp": json.loads(body),
                    }
                except Exception:
                    return {
                        "url": get_url,
                        "method": "GET",
                        "payload": {key: question},
                        "resp": body,
                    }
        except Exception as e:
            last_err = str(e)

    raise RuntimeError(f"Failed calling {url}. last_err={last_err}")


def heuristic_rewrite(q: str) -> str:
    q0 = q.strip()
    if not q0:
        return q0
    # 핵심 키워드 강화 (짧게, 엔티티 강조)
    extra = " evidence snippets root cause check failing warning health_percentage"
    # 너무 길면 줄이기
    words = (q0 + extra).split()
    if len(words) > 28:
        words = words[:28]
    return " ".join(words)


def append_jsonl(out_path: str, row: dict):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def score_docs(question: str, docs):
    scored = [{"score": overlap_score(question, d), "text": (d or "")[:1500]} for d in docs]
    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[0]["score"] if scored else 0.0
    return scored, top


def should_retry(
    doc_count: int, top_score: float, resp_msg: str, min_docs: int, min_score: float
) -> bool:
    msg = (resp_msg or "").lower()
    if "no llm client" in msg:
        return True
    if doc_count < min_docs:
        return True
    if top_score < min_score:
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["discover", "run"])
    ap.add_argument("--base", default="http://localhost:8010")
    ap.add_argument("--path", default="")
    ap.add_argument("--question", default="")
    ap.add_argument("--out", default="data/dspy/rag_shadow.jsonl")
    ap.add_argument("--topk", type=int, default=5)

    ap.add_argument("--self_correct", action="store_true")
    ap.add_argument("--max_rounds", type=int, default=2)
    ap.add_argument("--min_docs", type=int, default=1)
    ap.add_argument("--min_score", type=float, default=0.12)

    args = ap.parse_args()

    if args.cmd == "discover":
        base, openapi_url, spec = discover([args.base])
        if not spec:
            print("OPENAPI_NOT_FOUND")
            sys.exit(2)
        cand = find_paths(spec)
        print(f"BASE={base}")
        print(f"OPENAPI={openapi_url}")
        print("CANDIDATE_PATHS:")
        for p in cand[:60]:
            print(p)
        sys.exit(0)

    if not args.path or not args.question:
        print("Need --path and --question")
        sys.exit(2)

    attempts = []
    q = args.question

    rounds = max(1, args.max_rounds if args.self_correct else 1)
    for r in range(rounds):
        t0 = time.time()
        result = call_post_then_get(args.base, args.path, q)
        resp = result["resp"]
        docs = extract_docs(resp)
        scored, top = score_docs(q, docs)
        msg = resp_text(resp)

        attempts.append({
            "round": r + 1,
            "question": q,
            "method": result["method"],
            "url": result["url"],
            "payload": result["payload"],
            "doc_count": len(docs),
            "top_score": round(top, 4),
            "top_docs": scored[: max(args.topk, 1)],
            "raw_type": "json" if isinstance(resp, dict) else "text",
            "resp_head": msg[:200],
            "elapsed_s": round(time.time() - t0, 3),
        })

        if not args.self_correct:
            break

        if r + 1 >= rounds:
            break

        if should_retry(len(docs), top, msg, args.min_docs, args.min_score):
            q = heuristic_rewrite(args.question)
            continue
        break

    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "base": args.base,
        "path": args.path,
        "original_question": args.question,
        "self_correct": bool(args.self_correct),
        "attempts": attempts,
    }
    append_jsonl(args.out, row)

    last = attempts[-1]
    print("OK: shadow logged")
    print(f"- out: {args.out}")
    print(f"- rounds: {len(attempts)}")
    print(f"- last: docs={last['doc_count']} top_score={last['top_score']} method={last['method']}")
    for i, it in enumerate(last["top_docs"][: max(args.topk, 1)], 1):
        head = it["text"][:120].replace("\n", " ")
        print(f"  [{i}] score={it['score']:.3f} head={head}")


if __name__ == "__main__":
    main()
