#!/usr/bin/env bash
set -euo pipefail
OUT="artifacts/housekeeping/tree.txt"
mkdir -p artifacts/housekeeping
python - << 'PY'
import os
EXC={".git",".venv","node_modules","dist","build","__pycache__",".pytest_cache",".mypy_cache",".ruff_cache","artifacts"}
ROOT="."
MAX_DEPTH=6
lines=[]
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel=os.path.relpath(dirpath, ROOT)
    depth=0 if rel=="." else rel.count(os.sep)+1
    if depth>MAX_DEPTH:
        dirnames[:] = []
        continue
    dirnames[:] = [d for d in dirnames if d not in EXC]
    if rel==".":
        continue
    indent="  "*(depth-1)
    lines.append(f"{indent}{os.path.basename(dirpath)}/\n")
    for fn in sorted(filenames):
        if fn in {".DS_Store"}: 
            continue
        if fn.endswith((".pyc",".pyo")):
            continue
        if depth==MAX_DEPTH and fn:
            continue
        lines.append(f"{indent}  {fn}\n")
open("artifacts/housekeeping/tree.txt","w",encoding="utf-8").writelines(lines)
print("artifacts/housekeeping/tree.txt")
PY
