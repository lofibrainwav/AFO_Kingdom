from __future__ import annotations

import argparse
import json
import os

from trinity_os.adapters.afo_ultimate_mcp_deps_v1 import build_deps_v1
from trinity_os.graphs.trinity_toolflow_graph_v1 import build_trinity_toolflow_graph, run_trinity_toolflow


def main() -> int:
    ap = argparse.ArgumentParser(description="TRINITY Toolflow v1 Runner")
    ap.add_argument("prompt", type=str, help="User prompt")
    ap.add_argument(
        "--query", type=str, default="", help="Optional search query override"
    )
    ap.add_argument(
        "--top-k", type=int, default=5, help="Number of candidates to fetch"
    )
    ap.add_argument(
        "--risk-score",
        type=float,
        default=None,
        help=(
            "Optional SSOT risk_score evidence (0~100). If omitted, Serenity Gate treats risk as unknown and will ASK."
        ),
    )
    ap.add_argument(
        "--force",
        type=str,
        default="",
        choices=["", "AUTO_RUN", "ASK", "BLOCK"],
        help="Force Serenity Gate decision (test-only)",
    )
    args = ap.parse_args()

    if args.force:
        os.environ["TRINITY_TOOLFLOW_FORCE_DECISION"] = args.force

    # SSOT Risk Auto-Injection (optional, frictionless default)
    # - risk_score를 직접 계산하지 않고 SSOT guardian_sentinel 결과를 인용한다.
    # - 필요 시 TRINITY_TOOLFLOW_DISABLE_AUTO_RISK=1 로 비활성화 가능.
    disable_auto_risk = os.environ.get("TRINITY_TOOLFLOW_DISABLE_AUTO_RISK") == "1"
    if args.risk_score is None and not disable_auto_risk:
        try:
            from tools.guardian_sentinel import get_current_risk_score

            args.risk_score = float(get_current_risk_score())
        except Exception:
            args.risk_score = None

    try:
        deps = build_deps_v1()
        app = build_trinity_toolflow_graph(deps)
    except ImportError as e:
        print(
            json.dumps(
                {
                    "status": "BLOCK",
                    "reason": f"Missing dependency: {e}",
                    "next_actions": [
                        "python3.12 -m pip install -r TRINITY-OS/requirements.txt",
                        "retry the command",
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 3
    except Exception as e:
        print(
            json.dumps(
                {"status": "BLOCK", "reason": str(e)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    out = run_trinity_toolflow(
        app,
        args.prompt,
        query=(args.query or None),
        top_k=args.top_k,
        risk_score=args.risk_score,
    )

    print(json.dumps(out.get("final_card") or out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
