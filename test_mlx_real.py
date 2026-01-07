import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner

print("🎯 MLX MusicGen Runner 실음 생성 테스트")
print("=" * 50)

r = MLXMusicGenRunner.from_env()
print(f"available: {r.is_available()}")

if r.is_available():
    print("🎵 MLX MusicGen available! Generating real music...")
    try:
        wav = r.generate("epic orchestral cinematic, heroic victory theme", duration_sec=6)
        print(f"✅ Success: {wav}")
        print(f"   exists: {Path(wav).exists()}")
        if Path(wav).exists():
            size = Path(wav).stat().st_size
            print(f"   size: {size} bytes ({size/1024:.1f} KB)")
            print("🎉 MLX 실음 생성 성공!")
        else:
            print("❌ File not created")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ MLX MusicGen not available")
