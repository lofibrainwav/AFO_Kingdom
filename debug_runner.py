import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner, MLXMusicGenConfig

print("🐛 MLX Runner 환경 변수 디버깅")
print("=" * 40)

# 환경 변수 확인
print("환경 변수:")
print(f"AFO_MLX_MUSICGEN_VENV: {os.environ.get('AFO_MLX_MUSICGEN_VENV', 'NOT_SET')}")
print(f"AFO_MLX_MUSICGEN_DIR: {os.environ.get('AFO_MLX_MUSICGEN_DIR', 'NOT_SET')}")

# from_env() 결과 확인
print("\nfrom_env() 결과:")
r = MLXMusicGenRunner.from_env()
print(f"venv_python: {r._venv_python()}")
print(f"generate_py: {r._generate_py()}")
print(f"available: {r.is_available()}")

# 직접 설정 비교
print("\n직접 설정:")
cfg = MLXMusicGenConfig(
    venv_dir=Path("venv_musicgen"),
    musicgen_dir=Path("mlx-examples-official/musicgen"),
    model_name="facebook/musicgen-small",
    steps_per_second=50,
    default_max_steps=500,
    timeout_sec=600,
)

r2 = MLXMusicGenRunner(cfg)
print(f"venv_python: {r2._venv_python()}")
print(f"generate_py: {r2._generate_py()}")
print(f"available: {r2.is_available()}")

# 실제 venv 존재 확인
print("\n실제 파일 존재 확인:")
venv_py = Path("venv_musicgen/bin/python3")
gen_py = Path("mlx-examples-official/musicgen/generate.py")
print(f"venv_musicgen/bin/python3: {venv_py.exists()}")
print(f"mlx-examples-official/musicgen/generate.py: {gen_py.exists()}")

if venv_py.exists():
    print(f"venv python resolved: {venv_py.resolve()}")
