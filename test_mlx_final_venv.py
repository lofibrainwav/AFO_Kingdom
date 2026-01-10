import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner, MLXMusicGenConfig

print("🎯 MLX MusicGen Runner venv 절대 경로 테스트")
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
venv_py = r._venv_python()
print(f"venv_python: {venv_py}")
print(f"venv exists: {venv_py.exists()}")

if venv_py.exists():
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
        print("🔧 Checking what venv python has...")
        import subprocess
        try:
            result = subprocess.run([str(venv_py), "--version"], 
                                  capture_output=True, text=True, timeout=5)
            print(f"venv python version: {result.stdout.strip()}")
            
            result = subprocess.run([str(venv_py), "-c", "import sys; print(sys.path[:3])"], 
                                  capture_output=True, text=True, timeout=5)
            print(f"venv python sys.path: {result.stdout.strip()}")
            
        except Exception as ve:
            print(f"venv python check failed: {ve}")
else:
    print(f"❌ venv python3 not found at {venv_py}")
    print("   Checking venv directory...")
    venv_dir = Path("venv_musicgen")
    print(f"   venv_dir exists: {venv_dir.exists()}")
    if venv_dir.exists():
        bin_dir = venv_dir / "bin"
        print(f"   bin dir exists: {bin_dir.exists()}")
        if bin_dir.exists():
            py3 = bin_dir / "python3"
            print(f"   python3 exists: {py3.exists()}")
            if py3.exists():
                print(f"   python3 path: {py3.resolve()}")
