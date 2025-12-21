#!/usr/bin/env python3
"""
AFO 왕국 Syntax 검증 스크립트
pre-commit hook용 간단한 syntax checker
"""

import sys
from pathlib import Path


def main():
    project_root = Path()
    python_files = list(project_root.rglob("*.py"))
    project_files = [f for f in python_files if ".venv" not in str(f)]

    print(f"AFO 왕국 Syntax 검증: {len(project_files)}개 파일 검사 중...")

    errors = []
    for py_file in project_files:
        try:
            compile(Path(py_file).open(encoding="utf-8").read(), str(py_file), "exec")
        except SyntaxError as e:
            errors.append(f"{py_file}: {e}")

    if errors:
        print("❌ Syntax 오류 발견:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("✅ 모든 Python 파일 Syntax 정상!")


if __name__ == "__main__":
    main()
