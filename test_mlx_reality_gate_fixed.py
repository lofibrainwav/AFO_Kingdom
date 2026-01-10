import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner

print("🎯 MLX Reality Gate: 실제 python 경로 증거 테스트")
print("=" * 60)

print("환경 변수:")
print(f"AFO_MLX_MUSICGEN_VENV: {os.environ.get('AFO_MLX_MUSICGEN_VENV', 'NOT_SET')}")
print(f"AFO_MLX_MUSICGEN_DIR: {os.environ.get('AFO_MLX_MUSICGEN_DIR', 'NOT_SET')}")

print("\nRunner 생성 및 _venv_python() 호출:")
r = MLXMusicGenRunner.from_env()
venv_py = r._venv_python()

print(f"\n최종 반환 경로: {venv_py}")
print(f"경로 존재: {venv_py.exists()}")
print(f"실행 가능: {os.access(venv_py, os.X_OK)}")

print("\n✅ Reality Gate 증거 수집 완료")
