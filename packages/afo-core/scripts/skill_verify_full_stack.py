import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

SOUL = os.getenv("SOUL_ENGINE_URL", "http://127.0.0.1:8010").rstrip("/")
DASH = os.getenv("DASHBOARD_URL", "http://127.0.0.1:3000").rstrip("/")


def sh(cmd: str) -> str:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.stdout.strip()


def run() -> dict:
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    evidence_dir = Path("artifacts/trinity") / ts
    evidence_dir.mkdir(parents=True, exist_ok=True)

    health = sh(f"curl -s {SOUL}/health")
    health_j = json.loads(health) if health else {}
    b_keys = sorted(list((health_j.get("organs") or {}).keys()))

    ks = sh(
        f"curl -s {SOUL}/health | jq -r '.organs | keys | length' 2>/dev/null || true"
    )
    ks = int(ks) if ks.isdigit() else None

    ks2 = sh(f"curl -s {DASH}/api/kingdom-status")
    ks2_j = json.loads(ks2) if ks2 else {}
    f_organs = ks2_j.get("organs") or []
    f_names = [o.get("name") for o in f_organs if isinstance(o, dict)]

    route_path = Path("packages/dashboard/src/app/api/kingdom-status/route.ts")
    route_txt = route_path.read_text(encoding="utf-8") if route_path.exists() else ""
    has_try = "try" in route_txt
    has_catch = "catch" in route_txt and "Backend fetch failed" in route_txt
    has_return = "return NextResponse.json" in route_txt

    out = {
        "asof": ts,
        "backend": {
            "url": SOUL,
            "health_http_head": sh(f'curl -s -D- {SOUL}/health | sed -n "1,5p"'),
            "organs_keys": b_keys,
            "organs_keys_length": ks,
        },
        "frontend": {
            "url": DASH,
            "kingdom_status_http_head": sh(
                f'curl -s -D- {DASH}/api/kingdom-status | sed -n "1,5p"'
            ),
            "organs_len": len(f_organs),
            "organs_names": f_names,
        },
        "t20_ssot_checks": {
            "backend_organs_4": (ks == 4),
            "frontend_organs_5": (len(f_organs) == 5),
            "frontend_has_eyes": ("Eyes" in f_names),
            "route_try_catch_return": (has_try and has_catch and has_return),
        },
    }

    (evidence_dir / "full_stack_verify.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
