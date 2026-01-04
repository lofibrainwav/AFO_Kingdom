import json, time
from pathlib import Path

def main():
    out = Path("artifacts/mipro_runs") / f"mipro_light_{int(time.time())}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    # TODO: 여기에 형님 왕국의 unoptimized_rag / trinity_metric / trainset 연결
    # 지금은 러너 뼈대만 SSOT로 봉인합니다.
    record = {"ts": time.time(), "status": "runner_created", "auto": "light", "num_trials": 20}
    out.write_text(json.dumps(record) + "\n", encoding="utf-8")
    print(str(out))

if __name__ == "__main__":
    main()


# === SSOT_MIPRO_RESULT_LOGGING_V1 ===

def _ssot_latest_jsonl():
    from pathlib import Path
    out_dir = Path("artifacts/mipro_runs")
    out_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(out_dir.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)
    return files[0] if files else None

def _ssot_git_sha():
    import subprocess
    try:
        r = subprocess.run(["git","rev-parse","--short","HEAD"], check=True, capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return "unknown"

def _ssot_append(obj: dict):
    import json, time
    path = _ssot_latest_jsonl()
    if path is None:
        return
    obj.setdefault("ts", time.time())
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def _ssot_pick_best_from_optimizer(opt):
    best_score = None
    best_id = None
    breakdown = None

    for k in ["best_score", "best_metric", "best"]:
        v = getattr(opt, k, None)
        if isinstance(v, (int, float)):
            best_score = float(v)
            break

    for k in ["best_id", "best_candidate_id", "winner_id", "best_program_id"]:
        v = getattr(opt, k, None)
        if isinstance(v, str):
            best_id = v
            break

    for k in ["trials", "trial_results", "results", "history"]:
        v = getattr(opt, k, None)
        if isinstance(v, list) and v:
            for item in v:
                if not isinstance(item, dict):
                    continue
                sc = None
                for kk in ["score_total","trinity_total","trinity_score","score","metric","value"]:
                    if isinstance(item.get(kk), (int,float)):
                        sc = float(item[kk])
                        break
                if sc is None:
                    continue
                if best_score is None or sc > best_score:
                    best_score = sc
                    best_id = str(item.get("id") or item.get("best_id") or item.get("trial") or best_id)
                    bd = item.get("score_breakdown") or item.get("trinity_breakdown") or item.get("pillars")
                    if isinstance(bd, dict):
                        breakdown = bd

    return best_score, breakdown, best_id

def _ssot_finalize_mipro_run(auto=None, num_trials=None):
    opt = None
    opt = None

    best_score = None
    best_breakdown = None
    best_id = None
    if opt is not None:
        best_score, best_breakdown, best_id = _ssot_pick_best_from_optimizer(opt)

    _ssot_append({
        "status": "run_result",
        "commit_sha": _ssot_git_sha(),
        "auto": auto,
        "num_trials": num_trials,
        "score_total": best_score,
        "score_breakdown": best_breakdown,
        "best_id": best_id,
    })

import atexit as _ssot_atexit  # noqa: E402

def _ssot_try_finalize_on_exit():
    auto = globals().get("auto", None) or globals().get("AUTO", None)
    num_trials = globals().get("num_trials", None) or globals().get("NUM_TRIALS", None)
    _ssot_finalize_mipro_run(auto=auto, num_trials=num_trials)

_ssot_atexit.register(_ssot_try_finalize_on_exit)
# === END SSOT_MIPRO_RESULT_LOGGING_V1 ===
