import sys
import subprocess
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner, MLXMusicGenConfig

print("🎯 MLX MusicGen Runner 최종 테스트")
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
print(f"generate_py: {r._generate_py()}")
print(f"available: {r.is_available()}")

if r.is_available():
    print("✅ Ready for music generation!")
    print("🎵 Generating test music (6 seconds)...")
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
        # venv에서 직접 테스트
        print("🔧 Testing venv directly...")
        subprocess.run(["venv_musicgen/bin/python3", "--version"], check=False)
        py = "venv_musicgen/bin/python3"
        r = subprocess.run([py, "-c", 'import numpy; print("numpy OK")'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        print(r.stdout.strip() if r.returncode == 0 else "numpy missing")
        r = subprocess.run([py, "-c", 'import mlx; print("mlx OK")'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        print(r.stdout.strip() if r.returncode == 0 else "mlx missing")
else:
    print("❌ MLX MusicGen Runner not available")
    print("   Check venv and musicgen paths")
