#!/usr/bin/env python3
# Language: ko-KR (AFO SSOT)
"""
Markdown Clinical Cleaner - '美' (Beauty) 기둥 수호 도구
사용법: python scripts/md_clinical_clean.py <file_path>
"""

import os
import pathlib
import re
import sys


def clean_markdown(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    content = pathlib.Path(file_path).read_text(encoding="utf-8")

    # MD030: Spaces after list markers (Expected: 1, Actual: >1)
    # 1.  Text -> 1. Text
    # -   Text -> - Text
    content = re.sub(r"(^[ ]*(\d+\.|-|[*]|\+))[ ]{2,}", r"\1 ", content, flags=re.MULTILINE)

    pathlib.Path(file_path).write_text(content, encoding="utf-8")

    print(f"✅ {file_path} clinically cleaned (美).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/md_clinical_clean.py <file_path>")
    else:
        clean_markdown(sys.argv[1])
