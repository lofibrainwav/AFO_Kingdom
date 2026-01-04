import os, re, json
from datetime import datetime

ROOT = os.getcwd()
OUT_MD = os.path.join("artifacts","housekeeping","docs_index.md")
OUT_JSON = os.path.join("artifacts","housekeeping","docs_index.json")

INCLUDE_DIRS = ["docs","tickets"]
EXCLUDE_DIRS = {".git",".venv","node_modules","dist","build","__pycache__",".pytest_cache",".mypy_cache",".ruff_cache","artifacts"}

def walk():
    rows=[]
    for top in INCLUDE_DIRS:
        if not os.path.isdir(top):
            continue
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fn in filenames:
                if not fn.lower().endswith(".md"):
                    continue
                p = os.path.join(dirpath, fn)
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        first = f.readline().strip()
                    title = re.sub(r"^#+\s*", "", first) if first.startswith("#") else ""
                except Exception:
                    title = ""
                st = os.stat(p)
                rows.append({
                    "path": p.replace("\\","/"),
                    "title": title,
                    "bytes": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                })
    rows.sort(key=lambda r: r["path"])
    return rows

rows = walk()
os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"generated_at": datetime.now().isoformat(timespec="seconds"), "count": len(rows), "items": rows}, f, ensure_ascii=False, indent=2)

lines = []
lines.append("# Docs Index (SSOT)\n")
lines.append(f"- Generated: {datetime.now().isoformat(timespec='seconds')}\n")
lines.append(f"- Count: {len(rows)}\n\n")
lines.append("| Path | Title | Size | Modified |\n")
lines.append("|---|---|---:|---|\n")
for r in rows:
    title = r["title"].replace("|","\\|")
    lines.append(f"| `{r['path']}` | {title} | {r['bytes']} | {r['mtime']} |\n")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(OUT_MD)
print(OUT_JSON)
