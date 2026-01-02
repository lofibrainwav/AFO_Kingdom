from __future__ import annotations

import argparse
import inspect
import json
import os
from pathlib import Path
from typing import Any

try:
    import dspy
except ImportError:
    dspy = None  # type: ignore[assignment]

from AFO.config.antigravity import antigravity
from AFO.dspy_optimizer import compile_mipro


def _pick_field(d: dict[str, Any], keys: list[str]) -> str:
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _load_jsonl(path: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def _ensure_parent(p: str) -> None:
    Path(p).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def _maybe_configure_lm() -> None:
    if dspy is None:
        raise RuntimeError("DSPy is not installed.")

    # 이미 앱 런타임에서 설정되어 있으면 그대로 사용
    if getattr(dspy.settings, "lm", None):
        return

    # OpenAI 키가 있으면 최소 설정
    if os.getenv("OPENAI_API_KEY"):
        model = os.getenv("DSPY_OPENAI_MODEL", "gpt-4o-mini")
        lm = dspy.OpenAI(model=model)
        dspy.settings.configure(lm=lm)
        return

    raise RuntimeError(
        "DSPy LM is not configured. Set OPENAI_API_KEY (and optionally DSPY_OPENAI_MODEL), "
        "or configure dspy.settings.configure(lm=...) in your runtime."
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True, help="Path to JSONL train set.")
    ap.add_argument("--auto", default="light", choices=["light", "medium", "heavy"])
    ap.add_argument("--out", default="artifacts/dspy/RAG_OPTIMIZED.json", help="Output save path.")
    ap.add_argument("--val-size", type=int, default=20)
    ap.add_argument(
        "--strict", action="store_true", help="Fail fast (if compile_mipro supports strict)."
    )
    args = ap.parse_args()

    if dspy is None:
        raise RuntimeError("DSPy is not installed.")

    _maybe_configure_lm()
    _ensure_parent(args.out)

    rows = _load_jsonl(args.train)

    # Build DSPy Examples
    examples = []
    for r in rows:
        q = _pick_field(r, ["question", "query", "input", "prompt"])
        gt = _pick_field(r, ["ground_truth", "answer", "output", "expected"])
        if not q or not gt:
            continue
        ex = dspy.Example(question=q, ground_truth=gt).with_inputs("question")
        examples.append(ex)

    if not examples:
        raise RuntimeError("No usable examples found in train set.")

    # Lazy import to avoid heavy side effects unless actually running CLI
    from AFO.rag.dspy_module import AfoRagProgram

    # We import get_multimodal_engine from the core module directly as it seems to be in the root of the package source
    # Adjusted import based on inspected file structure: multimodal_rag_engine.py is in packages/afo-core/
    # If the package 'AFO' maps to 'packages/afo-core', then 'AFO.multimodal_rag_engine' works.
    # However, 'multimodal_rag_engine.py' is NOT inside 'AFO/' directory in 'packages/afo-core/'.
    # It is a sibling of 'AFO/'. This suggests 'afo-core' might be a flat layout.
    # BUT 'packages/afo-core/AFO/' exists.
    # If 'multimodal_rag_engine.py' is in root of 'packages/afo-core', and 'pyproject.toml' makes 'packages/afo-core' the package source?
    # Wait, 'packages/afo-core/afo_soul_engine/' is also there. This looks like a diverse collection.
    # The file 'packages/afo-core/multimodal_rag_engine.py' is likely importable as 'multimodal_rag_engine' if 'packages/afo-core' is in PYTHONPATH.
    # BUT 'AFO' package usually implies 'packages/afo-core/AFO'.
    # Let's try importing from 'AFO' first if possible, assuming some path magic, OR assume 'multimodal_rag_engine' is a top level module.
    # Given the previous context, let's look at how other modules import it.
    # The user instruction used: `from AFO.rag.multimodal_rag_engine import get_multimodal_engine` in the sample CLI code.
    # BUT the user also asked to put `dspy_module.py` in `packages/afo-core/AFO/rag/`.
    # And `multimodal_rag_engine.py` is in `packages/afo-core/`.
    # If `packages/afo-core` is added to python path, then `import multimodal_rag_engine` works.
    # If `packages/afo-core` is the root of the installable package `afo-core`, then `multimodal_rag_engine` is a top level module.
    # But `AFO` is also a directory there.
    # Let's assume for now `multimodal_rag_engine` is available at top level or we might need to adjust.
    # Actually, the user's sample code had `from AFO.rag.multimodal_rag_engine`.
    # This implies the user intends to MOVE it? No, user didn't say move.
    # User said "create TICKET-003 files".
    # I will stick to what seems safe: Import relatively or using what I see.
    # If `multimodal_rag_engine.py` is in `packages/afo-core`, and `AFO` is in `packages/afo-core`, they are siblings.
    # If running as `python -m AFO.rag.optimizer_cli`, `sys.path` usually includes the root.
    # If `packages/afo-core` is in python path, then `import multimodal_rag_engine` is correct.
    # I'll use `from multimodal_rag_engine import get_multimodal_engine` inside the CLI, handling the likelihood it's top-level in this dev environment.
    try:
        from multimodal_rag_engine import get_multimodal_engine
    except ImportError:
        try:
            # Fallback if it's somehow under AFO (though not seen there) or if AFO is the package root
            from AFO.rag.multimodal_rag_engine import get_multimodal_engine
        except ImportError:
            # Last resort, maybe it's just 'multimodal_rag_engine' but path issue?
            raise ImportError(
                "Could not import get_multimodal_engine from multimodal_rag_engine or AFO.rag.multimodal_rag_engine"
            )

    program = AfoRagProgram(engine=get_multimodal_engine(), top_k=5)

    # Simple val split (tail)
    valset = None
    if len(examples) > args.val_size:
        valset = examples[-args.val_size :]
        trainset = examples[: -args.val_size]
    else:
        trainset = examples

    # Call compile_mipro with signature-aware kwargs
    sig = inspect.signature(compile_mipro)
    kwargs: dict[str, Any] = {
        "program": program,
        "trainset": trainset,
        "valset": valset,
        "auto": args.auto,
        "save_path": args.out,
    }
    if "strict" in sig.parameters:
        kwargs["strict"] = args.strict

    if antigravity.DRY_RUN:
        # compile_mipro 내부에서 DRY_RUN 처리되지만, CLI에서도 한 번 더 명시
        print("[DRY_RUN] optimizer_cli executing in DRY_RUN mode.")

    compile_mipro(**kwargs)
    print(f"[OK] Saved optimized program to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
