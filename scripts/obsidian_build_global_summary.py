from __future__ import annotations

import glob
import json
import os
import pathlib
import re
import time
from collections import Counter


H1 = re.compile(r"(?m)^#\s+(.+)$")
TAG = re.compile(r"(?:^|\s)#([A-Za-z0-9_-]{2,}|[가-힣]{2,})")


def main():
    vault = os.environ.get("AFO_OBSIDIAN_VAULT", "").strip()
    if not vault:
        raise SystemExit("Set AFO_OBSIDIAN_VAULT")

    max_files = int(os.environ.get("AFO_OBSIDIAN_SUMMARY_MAX_FILES", "800"))
    max_chars = int(os.environ.get("AFO_OBSIDIAN_SUMMARY_MAX_CHARS", "60000"))

    files = glob.glob(os.path.join(vault, "**/*.md"), recursive=True)[:max_files]
    tagc = Counter()
    h1c = Counter()
    total_chars = 0
    total_files = 0

    for fp in files:
        try:
            md = pathlib.Path(fp).read_text(encoding="utf-8")
        except Exception:
            continue
        total_files += 1
        total_chars += len(md)
        for t in TAG.findall(md):
            tagc[t.lower()] += 1
        for h in H1.findall(md):
            h1c[h.strip()] += 1
        if total_chars >= max_chars:
            break

    out = []
    out.append("# Obsidian Vault Global Summary")
    out.append(f"As-of: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    out.append("")
    out.append(f"- Files scanned: {total_files}")
    out.append(f"- Chars scanned: {total_chars}")
    out.append("")
    out.append("## Top Tags")
    for t, c in tagc.most_common(20):
        out.append(f"- #{t} ({c})")
    out.append("")
    out.append("## Top H1 Titles")
    for h, c in h1c.most_common(20):
        out.append(f"- {h} ({c})")

    os.makedirs("data/dspy", exist_ok=True)
    pathlib.Path("data/dspy/obsidian_global_summary.md").write_text(
        "\n".join(out) + "\n", encoding="utf-8"
    )

    meta = {
        "vault": vault,
        "files_scanned": total_files,
        "chars_scanned": total_chars,
    }
    with open("data/dspy/obsidian_global_summary.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("OK: global summary built")
    print("- data/dspy/obsidian_global_summary.md")


if __name__ == "__main__":
    main()
