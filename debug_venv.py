import sys

sys.path.insert(0, "packages/afo-core/AFO/multimodal")
from pathlib import Path

from mlx_musicgen_runner import _repo_root

print("🐛 Venv 경로 디버깅")
print("=" * 30)

root = _repo_root()
print(f"repo root: {root}")

venv_dir_input = Path("venv_musicgen")
print(f"venv_dir input: {venv_dir_input}")
print(f"venv_dir is_absolute: {venv_dir_input.is_absolute()}")

if not venv_dir_input.is_absolute():
    venv_dir_abs = (root / venv_dir_input).resolve()
    print(f"venv_dir absolute: {venv_dir_abs}")
    print(f"venv_dir exists: {venv_dir_abs.exists()}")

    python_path = (venv_dir_abs / "bin" / "python3").resolve()
    print(f"python_path: {python_path}")
    print(f"python_path exists: {python_path.exists()}")

    if not python_path.exists():
        print("❌ venv python3 not found, using system python")
        import sys

        sys_py = Path(sys.executable)
        print(f"system python: {sys_py}")
        print(f"system python exists: {sys_py.exists()}")
    else:
        print("✅ venv python3 found!")

# 실제 venv 디렉토리 확인
actual_venv = Path("venv_musicgen")
print("\nActual venv check:")
print(f"venv_musicgen exists: {actual_venv.exists()}")
if actual_venv.exists():
    bin_dir = actual_venv / "bin"
    print(f"bin dir exists: {bin_dir.exists()}")
    if bin_dir.exists():
        py3 = bin_dir / "python3"
        print(f"python3 exists: {py3.exists()}")
        if py3.exists():
            print(f"python3 resolved: {py3.resolve()}")
            print(f"is same as system?: {py3.resolve() == Path(sys.executable)}")
