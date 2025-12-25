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
    exclude_dirs = {
        ".venv",
        "__pycache__",
        "node_modules",
        ".next",
        ".git",
        "build",
        "dist",
    }
    project_files = [
        f
        for f in python_files
        if not any(excluded in f.parts for excluded in exclude_dirs)
    ]

    print(f"AFO 왕국 Syntax 검증: {len(project_files)}개 파일 검사 중...")

    errors = []
    for py_file in project_files:
        try:
            content = Path(py_file).read_text(encoding="utf-8")
            compile(content, str(py_file), "exec")
        except UnicodeDecodeError:
            print(f"⚠️  건너뜀 (디코딩 실패): {py_file}")
            continue
        except SyntaxError as e:
            errors.append(f"{py_file}: {e}")
        except Exception as e:
            errors.append(f"{py_file}: 알 수 없는 오류 - {e}")

    if errors:
        print("❌ Syntax 오류 발견:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("✅ 모든 Python 파일 Syntax 정상!")


if __name__ == "__main__":
    main()
