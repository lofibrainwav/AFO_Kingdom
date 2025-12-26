import hashlib, json, re, sys
from pathlib import Path
import subprocess

PASS_NEEDLES = [
  "PASS: SSOT verified",
  "PASS:",
]

GREEN_NEEDLE = "PASS: GREEN CHECK"

def sh(cmd):
  return subprocess.check_output(cmd, text=True).strip()

def sha256_file(p: Path) -> str:
  h = hashlib.sha256()
  with p.open("rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
      h.update(chunk)
  return h.hexdigest()

def parse_report(p: Path) -> dict:
  txt = p.read_text(encoding="utf-8", errors="ignore")
  def grab(key):
    m = re.search(rf"^\*\*{re.escape(key)}\*\*:\s*(.+)$", txt, re.M)
    return m.group(1).strip() if m else ""
  return {
    "path": str(p),
    "status": grab("Status"),
    "timestamp": grab("Timestamp"),
    "evidence": grab("Evidence"),
    "sealsha": grab("SealSHA256"),
    "verify": grab("Verify"),
  }

def staged_reports():
  out = sh(["git","diff","--cached","--name-only","--diff-filter=ACMRT"])
  return [Path(x) for x in out.splitlines() if x.startswith("docs/reports/") and x.endswith(".md")]

def must_enforce(status: str) -> bool:
  s = status.upper()
  return ("SEALED-VERIFIED" in s) or ("DONE" in s)

def fail(msg: str) -> int:
  print(f"TRUTHGATE_V3_BLOCK: {msg}")
  return 1

def main() -> int:
  reports = staged_reports()
  if not reports:
    return 0

  rc = 0
  for rp in reports:
    if not rp.exists():
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: staged report missing on disk: {rp}")
      continue

    meta = parse_report(rp)
    status = meta["status"]
    if not must_enforce(status):
      continue

    ev = meta["evidence"].rstrip("/")
    if not ev:
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: {rp} status={status} but Evidence line missing")
      continue

    evd = Path(ev)
    if not evd.exists() or not evd.is_dir():
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: Evidence dir missing: {ev}")
      continue

    seal = evd / "seal.json"
    vpass = evd / "verify_pass.txt"
    gpass = evd / "green_pass.txt"

    if not seal.exists():
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: seal.json missing: {seal}")
      continue
    if not vpass.exists():
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: verify_pass.txt missing: {vpass}")
      continue
    if not gpass.exists():
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: green_pass.txt missing: {gpass}")
      continue

    vtxt = vpass.read_text(encoding="utf-8", errors="ignore")
    if "PASS: SSOT verified" not in vtxt:
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: verify_pass.txt does not contain PASS: {vpass}")
      continue

    gtxt = gpass.read_text(encoding="utf-8", errors="ignore")
    if GREEN_NEEDLE not in gtxt:
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: green_pass.txt does not contain GREEN PASS: {gpass}")
      continue

    actual_seal_sha = sha256_file(seal)
    if meta["sealsha"] and meta["sealsha"] != "TBD" and meta["sealsha"] != actual_seal_sha:
      rc = 1
      print(f"TRUTHGATE_V3_BLOCK: SealSHA256 mismatch in report. report={meta['sealsha']} actual={actual_seal_sha}")
      continue

  return rc

if __name__ == "__main__":
  sys.exit(main())
