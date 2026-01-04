from __future__ import annotations

import json
import os
import time
import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import dspy
from dspy.teleprompt import MIPROv2

from AFO.domain.metrics.trinity_runtime_v1 import trinity_metric, get_last_eval


@dataclass(frozen=True)
class QA:
    question: str
    answer: str
    user_id: str = "u0"


def _load_jsonl(path: str) -> list[QA]:
    out: list[QA] = []
    p = Path(path)
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        out.append(QA(question=o["question"], answer=str(o["answer"]).strip().lower(), user_id=str(o.get("user_id", "u0"))))
    return out


def _load_entrypoint(ep: str) -> Callable[..., Any]:
    mod, fn = ep.split(":")
    m = importlib.import_module(mod)
    f = getattr(m, fn)
    if not callable(f):
        raise TypeError(f"entrypoint not callable: {ep}")
    return f


def _norm(s: str) -> str:
    return (s or "").strip().lower()


class KingdomRAG(dspy.Module):
    def __init__(self, retrieve_fn: Callable[..., Any], k: int = 5):
        super().__init__()
        self._retrieve_fn = retrieve_fn
        self._k = k
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question: str, user_id: str = "u0"):
        ctx = self._retrieve_fn(question=question, user_id=user_id, k=self._k)
        if isinstance(ctx, list):
            context = "\n\n".join(str(x) for x in ctx)
        else:
            context = str(ctx)
        pred = self.generate(context=context, question=question)
        ans = getattr(pred, "answer", None)
        if ans is None:
            ans = str(pred)
        return dspy.Prediction(answer=_norm(str(ans)))


def _append_jsonl(path: str, obj: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main() -> None:
    auto = os.environ.get("AFO_MIPRO_AUTO", "medium")
    num_trials = int(os.environ.get("AFO_MIPRO_NUM_TRIALS", "60"))
    k = int(os.environ.get("AFO_RAG_TOPK", "5"))

    train_path = os.environ.get("AFO_MIPRO_TRAINSET", "artifacts/mipro_datasets/rag_train.jsonl")
    dev_path = os.environ.get("AFO_MIPRO_DEVSET", "artifacts/mipro_datasets/rag_dev.jsonl")

    retrieve_ep = os.environ.get("AFO_RAG_RETRIEVE_ENTRYPOINT", "").strip()
    if not retrieve_ep:
        raise SystemExit("Missing AFO_RAG_RETRIEVE_ENTRYPOINT (e.g. AFO.rag.some_module:retrieve)")

    retrieve_fn = _load_entrypoint(retrieve_ep)

    train = _load_jsonl(train_path)
    dev = _load_jsonl(dev_path)

    rag = KingdomRAG(retrieve_fn=retrieve_fn, k=k)

    tp = MIPROv2(metric=trinity_metric, auto=auto, num_trials=num_trials)

    raw = f"artifacts/mipro_runs/mipro_rag_{auto}_{int(time.time())}.jsonl"
    _append_jsonl(raw, {"ts": time.time(), "status": "runner_created", "auto": auto, "num_trials": num_trials, "train": len(train), "dev": len(dev)})

    def _to_example(x: QA):
        return dspy.Example(question=x.question, answer=x.answer, user_id=x.user_id).with_inputs("question", "user_id")

    trainset = [_to_example(x) for x in train]
    devset = [_to_example(x) for x in dev]

    optimized = tp.compile(rag, trainset=trainset)

    scores: list[float] = []
    for ex in devset:
        pred = optimized(question=ex.question, user_id=getattr(ex, "user_id", "u0"))
        s = trinity_metric(ex, pred)
        scores.append(float(s))

    avg = sum(scores) / max(1, len(scores))
    last = get_last_eval() or {}

    _append_jsonl(raw, {
        "ts": time.time(),
        "status": "run_result",
        "auto": auto,
        "num_trials": num_trials,
        "score_total": float(avg),
        "score_breakdown": last.get("score_breakdown"),
        "best_id": getattr(tp, "best_id", None) or getattr(tp, "best_trial_idx", None),
    })

    print(f"RAW={raw}")
    print({"avg_score_total": avg, "dev_n": len(scores)})


if __name__ == "__main__":
    main()
