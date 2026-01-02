#!/usr/bin/env python3
"""TRINITY-OS Bridge Log Tracker

Bridge Log(브릿지의 시선)은 에이전트들이 남긴 발자취입니다.
이 스크립트는 TRINITY-OS/docs/bridge/*.yaml 로그를 모아
새로운 에이전트가 과거의 흐름을 따라가며 확장할 수 있도록
타임라인/요약을 제공합니다.

출력:
- 기본: JSON 요약 (LLM/툴이 바로 소비 가능)
- 옵션: Markdown 타임라인

의존성:
- 표준 라이브러리만 사용 (Dependency Truth 준수)
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

TRINITY_OS_ROOT = Path(__file__).resolve().parent.parent
BRIDGE_DIR = TRINITY_OS_ROOT / "docs" / "bridge"

_KEY_RE = re.compile(r"^(task_id|who|intent):\s*(.+)$")
_TOP_LEVEL_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:\s*")


def _extract_basic_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = _KEY_RE.match(line.strip())
        if m:
            key, raw_val = m.groups()
            val = raw_val.strip().strip('"').strip("'")
            fields[key] = val
        if len(fields) >= 3:
            break
    return fields


def _extract_bridges_view(text: str) -> list[str]:
    lines = text.splitlines()
    view: list[str] = []
    in_section = False
    for line in lines:
        if not in_section:
            if line.startswith("bridges_view:"):
                in_section = True
            continue
        if _TOP_LEVEL_KEY_RE.match(line):
            break
        item = re.match(r"^\s*-\s*(.+)$", line)
        if item:
            view.append(item.group(1).strip())
    return view


def _load_bridge_logs() -> list[dict[str, Any]]:
    if not BRIDGE_DIR.exists():
        return []

    logs: list[dict[str, Any]] = []
    for path in sorted(BRIDGE_DIR.glob("*.yaml")):
        if path.name == "BRIDGE_LOG_TEMPLATE.yaml":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue

        meta = _extract_basic_fields(text)
        task_id = meta.get("task_id", path.stem)
        if task_id.startswith("YYYY-"):
            # 템플릿/미작성 로그는 제외
            continue

        logs.append(
            {
                "file": str(path.relative_to(TRINITY_OS_ROOT)),
                "task_id": task_id,
                "who": meta.get("who", ""),
                "intent": meta.get("intent", ""),
                "modified_at": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                "bridges_view": _extract_bridges_view(text),
            }
        )

    logs.sort(key=lambda r: r["modified_at"], reverse=True)
    return logs


def _print_json(logs: list[dict[str, Any]]) -> None:
    payload = {"count": len(logs), "logs": logs}
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _print_markdown(logs: list[dict[str, Any]]) -> None:
    print("# Bridge Logs Timeline\n")
    if not logs:
        print("- (아직 기록된 Bridge Log가 없습니다.)")
        return

    for r in logs:
        task_id = r["task_id"]
        who = r["who"] or "unknown"
        intent = r["intent"] or "-"
        relpath = r["file"]
        print(f"- **{task_id}** `{relpath}` — {who} — {intent}")
        for v in r.get("bridges_view", []) or []:
            print(f"  - {v}")


def main() -> None:
    parser = argparse.ArgumentParser(description="List and summarize TRINITY-OS Bridge Logs.")
    parser.add_argument("--limit", type=int, default=10, help="Number of logs to show (default: 10).")
    parser.add_argument("--all", action="store_true", help="Show all logs (ignores --limit).")
    parser.add_argument(
        "--format",
        choices=["json", "md"],
        default="json",
        help="Output format: json (default) or md.",
    )
    args = parser.parse_args()

    logs = _load_bridge_logs()
    if not args.all:
        logs = logs[: max(args.limit, 0)]

    if args.format == "md":
        _print_markdown(logs)
    else:
        _print_json(logs)


if __name__ == "__main__":
    main()
