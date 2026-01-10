import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner

r = MLXMusicGenRunner.from_env()
print("available:", r.is_available())

# 환경 정보 출력
print("venv_python:", r._venv_python())
print("generate_py:", r._generate_py())
print("venv exists:", r._venv_python().exists())
print("gen exists:", r._generate_py().exists())

if r.is_available():
    print("🎵 MLX MusicGen available, generating test music...")
    wav = r.generate("epic orchestral cinematic, heroic victory theme", duration_sec=6)
    print("wav:", wav, "exists:", Path(wav).exists())
    if Path(wav).exists():
        size = Path(wav).stat().st_size
        print(f"file size: {size} bytes")
else:
    print("❌ MLX MusicGen not available")
