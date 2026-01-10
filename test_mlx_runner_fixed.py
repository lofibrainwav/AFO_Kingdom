import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner

print("🔧 MLX MusicGen Runner 환경 검증")
print("=" * 50)

r = MLXMusicGenRunner.from_env()
print(f"available: {r.is_available()}")
print(f"venv_python: {r._venv_python()}")
print(f"generate_py: {r._generate_py()}")

# venv 경로 확인 및 수정
venv_path = Path("venv_musicgen/bin/python3")
if venv_path.exists():
    print(f"✅ venv exists: {venv_path}")
    os.environ["AFO_MLX_MUSICGEN_VENV"] = "venv_musicgen"
    
    # 새 인스턴스 생성
    r2 = MLXMusicGenRunner.from_env()
    print(f"venv_python (fixed): {r2._venv_python()}")
    
    if r2.is_available():
        print("✅ MLX MusicGen Runner ready!")
        print("🎵 Testing music generation...")
        try:
            wav = r2.generate("epic orchestral cinematic, heroic victory theme", duration_sec=6)
            print(f"✅ Success: {wav}")
            print(f"   exists: {Path(wav).exists()}")
            if Path(wav).exists():
                print(f"   size: {Path(wav).stat().st_size} bytes")
        except Exception as e:
            print(f"❌ Generation failed: {e}")
    else:
        print("❌ MLX MusicGen Runner not available")
else:
    print(f"❌ venv not found: {venv_path}")
