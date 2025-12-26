import os, subprocess, sys, time, pathlib

WARN_LINES = int(os.getenv("REFACTOR_WARN_LINES", "400"))
BLOCK_LINES = int(os.getenv("REFACTOR_BLOCK_LINES", "1200"))
WARN_BYTES = int(os.getenv("REFACTOR_WARN_BYTES", "80000"))
BLOCK_BYTES = int(os.getenv("REFACTOR_BLOCK_BYTES", "200000"))

EXCLUDE_PREFIXES = (
  "artifacts/", ".git/", "node_modules/", ".next/", "dist/", "build/",
  ".venv/", "venv/", "__pycache__/"
)

def sh(cmd: list[str]) -> str:
  return subprocess.check_output(cmd, text=True).strip()

def staged_paths() -> list[str]:
  out = sh(["git","diff","--cached","--name-only","--diff-filter=AM"])
  return [p for p in out.splitlines() if p]

def has_override_staged() -> bool:
  out = sh(["git","diff","--cached","--name-only","--diff-filter=AM"])
  for p in out.splitlines():
    if p.startswith("docs/overrides/OVERRIDE_") and p.endswith(".md"):
      return True
    if p.startswith("OVERRIDE_") and p.endswith(".md"):
      return True
  return False

def append_queue(rows: list[str]) -> None:
  q = pathlib.Path("docs/refactor_queue.md")
  q.parent.mkdir(parents=True, exist_ok=True)
  if not q.exists():
    q.write_text("# Refactor Queue\n\n")
  with q.open("a", encoding="utf-8") as f:
    for r in rows:
      f.write(r + "\n")

def main() -> int:
  paths = staged_paths()
  rows = []
  hard_block = False

  for p in paths:
    if p.startswith(EXCLUDE_PREFIXES):
      continue
    fp = pathlib.Path(p)
    if not fp.exists() or fp.is_dir():
      continue
    try:
      data = fp.read_bytes()
    except Exception:
      continue

    size = len(data)
    try:
      lines = data.decode("utf-8", errors="ignore").count("\n") + 1
    except Exception:
      lines = 0

    if lines >= WARN_LINES or size >= WARN_BYTES:
      rows.append(f"- {p} | {lines} lines | {size} bytes | queued {time.strftime('%Y-%m-%d %H:%M:%S')}")

    if lines >= BLOCK_LINES or size >= BLOCK_BYTES:
      hard_block = True

  if rows:
    append_queue(rows)
    print("REFACTOR_GUARD: queued -> docs/refactor_queue.md")

  if hard_block and not has_override_staged():
    print("REFACTOR_GUARD: BLOCK (too large). Add override file docs/overrides/OVERRIDE_<TS>.md to proceed.")
    return 1

  if hard_block and has_override_staged():
    print("REFACTOR_GUARD: OVERRIDE accepted (override file staged).")
  return 0

if __name__ == "__main__":
  sys.exit(main())
