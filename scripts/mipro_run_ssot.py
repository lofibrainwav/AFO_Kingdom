from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "mipro_run.py"
OUT_DIR = ROOT / "artifacts" / "mipro_runs"


def _git_sha() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            check=True,
            capture_output=True,
            text=True,
        )
        return r.stdout.strip()
    except Exception:
        return "unknown"


def _latest_jsonl(dir_path: Path) -> Path:
    files = sorted(dir_path.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No .jsonl files found in {dir_path}")
    return files[0]


def _coalesce(d: dict[str, Any], keys: list[str]) -> Any:
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None


def _enrich_line(
    obj: dict[str, Any],
    *,
    commit_sha: str,
    phase: str,
) -> dict[str, Any]:
    score_total = _coalesce(obj, ["score_total", "trinity_total", "trinity_score", "score"])
    score_breakdown = _coalesce(obj, ["score_breakdown", "trinity_breakdown", "pillars", "breakdown"])
    best_id = _coalesce(obj, ["best_id", "best_candidate_id", "best", "optimized_id", "winner_id"])
    trial = _coalesce(obj, ["trial", "trial_idx", "t"])

    enriched: dict[str, Any] = dict(obj)
    enriched.setdefault("timestamp", enriched.get("ts"))
    enriched["commit_sha"] = commit_sha
    enriched["phase"] = phase
    enriched.setdefault("auto", enriched.get("auto"))
    enriched.setdefault("trial", trial)
    enriched.setdefault("score_total", score_total)
    enriched.setdefault("score_breakdown", score_breakdown)
    enriched.setdefault("best_id", best_id)
    return enriched


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--phase", default=os.environ.get("AFO_MIPRO_PHASE", "baseline"))
    ap.add_argument("--rewrite", action="store_true", help="rewrite original jsonl in-place (default: write _ssot.jsonl)")
    args, passthrough = ap.parse_known_args()

    if not RUNNER.exists():
        print(f"Runner not found: {RUNNER}", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    before = set(p.name for p in OUT_DIR.glob("*.jsonl"))

    cmd = [sys.executable, str(RUNNER), *passthrough]
    r = subprocess.run(cmd, cwd=str(ROOT))
    if r.returncode != 0:
        return r.returncode

    after_files = [p for p in OUT_DIR.glob("*.jsonl") if p.name not in before]
    latest = max(after_files, key=lambda p: p.stat().st_mtime) if after_files else _latest_jsonl(OUT_DIR)

    commit_sha = _git_sha()
    phase = args.phase

    out_path = latest if args.rewrite else latest.with_name(latest.stem + "_ssot.jsonl")

    with latest.open("r", encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            enriched = _enrich_line(obj, commit_sha=commit_sha, phase=phase)
            fout.write(json.dumps(enriched, ensure_ascii=False) + "\n")

    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
