import glob
import json
import os
from datetime import UTC, datetime


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ART = os.path.join(ROOT, "artifacts")


def newest(patterns):
    paths = []
    for p in patterns:
        paths += glob.glob(os.path.join(ART, p))
    paths = [p for p in paths if os.path.isfile(p)]
    if not paths:
        return None
    return max(paths, key=lambda x: os.path.getmtime(x))


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f if _.strip())


def safe_stat(path):
    try:
        st = os.stat(path)
        return {"size": st.st_size, "mtime": st.st_mtime}
    except FileNotFoundError:
        return None


bundle = {
    "as_of_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    "paths": {},
    "ticket023_releases": [],
    "latest": {},
}

t020 = newest(["ticket020*quality*ssot*.jsonl", "ticket020*ssot*.jsonl"])
t021 = newest(["ticket021*ssot*.jsonl"])
t019_log = newest(["ticket019*train*.log", "ticket019*lora*train*.log"])

bundle["paths"]["ticket020_ssot"] = t020
bundle["paths"]["ticket021_ssot"] = t021
bundle["paths"]["ticket019_log"] = t019_log
for k, v in list(bundle["paths"].items()):
    if v:
        bundle["paths"][k] = os.path.relpath(v, ROOT)

rel_dirs = sorted(glob.glob(os.path.join(ART, "ticket023_release_*")), reverse=True)
for d in rel_dirs[:5]:
    manifest = os.path.join(d, "manifest.json")
    sha = os.path.join(d, "adapter_sha256.txt")
    row = {
        "dir": os.path.relpath(d, ROOT),
        "manifest": os.path.relpath(manifest, ROOT) if os.path.isfile(manifest) else None,
        "adapter_sha256": os.path.relpath(sha, ROOT) if os.path.isfile(sha) else None,
        "adapter_sha256_lines": count_lines(sha) if os.path.isfile(sha) else 0,
        "manifest_stat": safe_stat(manifest),
        "adapter_sha256_stat": safe_stat(sha),
    }
    if os.path.isfile(manifest):
        try:
            row["manifest_json"] = read_json(manifest)
        except Exception:
            row["manifest_json"] = None
    bundle["ticket023_releases"].append(row)

if bundle["ticket023_releases"]:
    bundle["latest"]["ticket023"] = bundle["ticket023_releases"][0]

out = os.path.join(ART, "ticket024_dashboard_bundle.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(bundle, f, ensure_ascii=False, separators=(",", ":"))
print(out)
