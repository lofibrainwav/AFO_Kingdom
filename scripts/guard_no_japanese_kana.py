from __future__ import annotations

import re
import sys
from pathlib import Path


KANA_RANGES = [
    (0x3040, 0x309F),  # Hiragana
    (0x30A0, 0x30FF),  # Katakana
    (0x31F0, 0x31FF),  # Katakana Phonetic Extensions
]


def has_kana(s: str) -> bool:
    for ch in s:
        o = ord(ch)
        for a, b in KANA_RANGES:
            if a <= o <= b:
                return True
    return False


def has_multilang_slogan(s: str) -> bool:
    """Detect multilingual slogans (English + Japanese/Chinese)"""
    # English uppercase slogan pattern (3+ uppercase letters + exclamation)
    en_slogan = re.search(r"[A-Z]{3,}.*!", s) is not None
    # Combined with Japanese/Chinese characters
    has_cjk = any(ord(c) > 0x2E00 for c in s)  # CJK Unified Ideographs start

    return en_slogan and has_cjk


def main() -> int:
    roots = [Path("AGENTS.md"), Path("docs"), Path("tickets"), Path("artifacts")]
    targets: list[Path] = []
    for r in roots:
        if r.is_file():
            targets.append(r)
        elif r.is_dir():
            targets.extend([p for p in r.rglob("*.md") if p.is_file()])

    bad: list[tuple[str, int, str]] = []
    for p in sorted(set(targets)):
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if has_kana(line):
                bad.append((str(p), i, line.strip()))

    if bad:
        print("[FAIL] Japanese kana detected:")
        for fp, ln, line in bad[:200]:
            print(f"  {fp}:{ln}: {line}")
        return 1

    print("[OK] No Japanese kana detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
