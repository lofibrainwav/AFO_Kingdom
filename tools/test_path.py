import pathlib

current_path = pathlib.Path(
    "/Users/brnestrm/AFO_Kingdom/packages/afo-core/AFO/health/organs_truth.py"
).resolve()
print(f"Start: {current_path}")
repo_root = None
for parent in current_path.parents:
    print(f"Checking: {parent}")
    if (parent / ".git").exists() or (parent / "packages").exists():
        print("  -> Found Marker!")
        repo_root = parent
        break

if repo_root:
    ssot = repo_root / "docs" / "AFO_FINAL_SSOT.md"
    print(f"SSOT Path: {ssot}")
    print(f"Exists: {ssot.exists()}")
else:
    print("Repo Root Not Found")
