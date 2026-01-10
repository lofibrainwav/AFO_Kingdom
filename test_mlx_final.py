import sys
import subprocess
import os
from pathlib import Path

# Simple MLX MusicGen Runner for testing (no external dependencies)
class MLXMusicGenRunner:
    def __init__(self, config):
        self.config = config

    def _venv_python(self):
        venv_py = self.config.venv_dir / "bin" / "python3"
        if venv_py.exists():
            return str(venv_py)
        return sys.executable

    def _generate_py(self):
        return str(self.config.musicgen_dir / "generate.py")

    def is_available(self):
        venv_py = Path(self._venv_python())
        return venv_py.exists()

    def generate(self, prompt, duration_sec=10):
        # This is a test stub - real implementation would generate music
        return f"test_output_{duration_sec}s.wav"

class MLXMusicGenConfig:
    def __init__(self, venv_dir, musicgen_dir, model_name, steps_per_second, default_max_steps, timeout_sec):
        self.venv_dir = Path(venv_dir)
        self.musicgen_dir = Path(musicgen_dir)
        self.model_name = model_name
        self.steps_per_second = steps_per_second
        self.default_max_steps = default_max_steps
        self.timeout_sec = timeout_sec

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
