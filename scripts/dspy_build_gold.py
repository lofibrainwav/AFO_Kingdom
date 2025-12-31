import argparse
import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def iter_json_objects(path: Path) -> Iterable[dict[str, Any]]:
    try:
        raw = path.read_text(encoding="utf-8").strip()
    except Exception:
        return

    if not raw:
        return
    if raw.startswith("["):
        try:
            arr = json.loads(raw)
            if isinstance(arr, list):
                for x in arr:
                    if isinstance(x, dict):
                        yield x
            return
        except Exception:
            pass

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                yield obj
        except Exception:
            continue


def pick_first(d: dict[str, Any], keys: list[str]) -> Any | None:
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None


def to_float(x: Any) -> float | None:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None


def extract_score(obj: dict[str, Any]) -> float | None:
    candidates = [
        pick_first(obj, ["trinity", "trinity_score", "score"]),
        (obj.get("metrics") or {}).get("trinity") if isinstance(obj.get("metrics"), dict) else None,
        (obj.get("trinity_score") or {}).get("total")
        if isinstance(obj.get("trinity_score"), dict)
        else None,
        (obj.get("trinity") or {}).get("total") if isinstance(obj.get("trinity"), dict) else None,
    ]
    for c in candidates:
        v = to_float(c)
        if v is not None:
            return v
    return None


def extract_triplet(obj: dict[str, Any]) -> tuple[float | None, float | None, float | None]:
    def get_nested(d: dict[str, Any], root_keys: list[str], leaf: str) -> float | None:
        for rk in root_keys:
            val = d.get(rk)
            if isinstance(val, dict) and leaf in val:
                f = to_float(val.get(leaf))
                if f is not None:
                    return f
        return None

    truth = to_float(pick_first(obj, ["truth", "truth_score"])) or get_nested(
        obj, ["trinity", "trinity_score", "metrics"], "truth"
    )
    goodness = to_float(pick_first(obj, ["goodness", "goodness_score", "risk"])) or get_nested(
        obj, ["trinity", "trinity_score", "metrics"], "goodness"
    )
    beauty = to_float(pick_first(obj, ["beauty", "beauty_score"])) or get_nested(
        obj, ["trinity", "trinity_score", "metrics"], "beauty"
    )
    return truth, goodness, beauty


def normalize_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x.strip()
    if isinstance(x, (list, tuple)):
        return "\n".join([normalize_text(i) for i in x]).strip()
    if isinstance(x, dict):
        return json.dumps(x, ensure_ascii=False)
    return str(x).strip()


def map_to_commander_gold(obj: dict[str, Any]) -> dict[str, str] | None:
    command = normalize_text(
        pick_first(
            obj, ["command", "user_command", "instruction", "task", "query", "prompt", "input"]
        )
    )
    expected = normalize_text(
        pick_first(obj, ["expected", "answer", "output", "response", "completion"])
    )
    context = normalize_text(
        pick_first(obj, ["context", "system", "system_prompt", "meta", "notes", "background"])
    )
    if not command or not expected:
        return None
    if not context:
        context = ""
    return {"command": command, "context": context, "expected": expected}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inputs", action="append", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min_score", type=float, default=0.0)
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    selected: list[dict[str, Any]] = []

    # Process inputs (files or directories)
    input_paths = []
    for raw_path in args.inputs:
        p = Path(raw_path)
        if p.is_dir():
            input_paths.extend(sorted(p.rglob("*.json*")))
        else:
            input_paths.append(p)

    for fp in input_paths:
        if not fp.exists():
            continue

        for obj in iter_json_objects(fp):
            score = extract_score(obj)
            if score is not None and score < args.min_score:
                continue
            gold = map_to_commander_gold(obj)
            if not gold:
                continue
            truth, goodness, beauty = extract_triplet(obj)
            gold_meta = {
                "_src": str(fp),
                "_score": score,
                "_truth": truth,
                "_goodness": goodness,
                "_beauty": beauty,
            }
            selected.append({**gold, **gold_meta})

            if len(selected) >= args.limit:
                break
        if len(selected) >= args.limit:
            break

    selected = selected[: args.limit]

    with out_path.open("w", encoding="utf-8") as f:
        for row in selected:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"OK: wrote {len(selected)} rows -> {out_path}")


if __name__ == "__main__":
    main()
