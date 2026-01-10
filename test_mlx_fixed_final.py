import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner, MLXMusicGenConfig

print("🎯 MLX MusicGen Runner venv 수정 테스트")
print("=" * 50)

# 직접 venv 경로 지정
cfg = MLXMusicGenConfig(
    venv_dir=Path("venv_musicgen"),
    musicgen_dir=Path("mlx-examples-official/musicgen"),
    model_name="facebook/musicgen-small",
    steps_per_second=50,
    default_max_steps=500,
    timeout_sec=600,
)

r = MLXMusicGenRunner(cfg)
print(f"venv_python: {r._venv_python()}")
print(f"venv exists: {r._venv_python().exists()}")

if r._venv_python().exists():
    print("✅ venv python3 exists!")
    print("🎵 Testing music generation (6 seconds)...")
    try:
        wav = r.generate("epic orchestral cinematic, heroic victory theme", duration_sec=6)
        print(f"✅ Success: {wav}")
        print(f"   exists: {Path(wav).exists()}")
        if Path(wav).exists():
            size = Path(wav).stat().st_size
            print(f"   size: {size} bytes ({size/1024:.1f} KB)")
            print("🎉 MLX MusicGen Runner 완전 성공!")
        else:
            print("❌ File was not created")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        print("🔧 Checking venv modules...")
        import subprocess
        try:
            result = subprocess.run([str(r._venv_python()), "-c", "import numpy, mlx; print('Modules OK')"], 
                                  capture_output=True, text=True, timeout=10)
            print(f"venv modules: {result.stdout.strip()}")
        except Exception as ve:
            print(f"venv check failed: {ve}")
else:
    print("❌ venv python3 not found")
