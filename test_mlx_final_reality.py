import sys
import os
sys.path.insert(0, 'packages/afo-core/AFO/multimodal')
from pathlib import Path
from mlx_musicgen_runner import MLXMusicGenRunner

print("🎯 MLX Final Reality Gate: 실제 generate() 호출 증거")
print("=" * 60)

print("환경 변수:")
print(f"AFO_MLX_MUSICGEN_VENV: {os.environ.get('AFO_MLX_MUSICGEN_VENV', 'NOT_SET')}")
print(f"AFO_MLX_MUSICGEN_DIR: {os.environ.get('AFO_MLX_MUSICGEN_DIR', 'NOT_SET')}")

r = MLXMusicGenRunner.from_env()
print(f"\nis_available(): {r.is_available()}")

if r.is_available():
    print("\n🎵 실제 generate() 호출 시도...")
    try:
        wav = r.generate("epic orchestral theme", duration_sec=3)
        print(f"✅ 성공! 생성된 파일: {wav}")
        print(f"   파일 존재: {Path(wav).exists()}")
        if Path(wav).exists():
            size = Path(wav).stat().st_size
            print(f"   파일 크기: {size} bytes")
    except Exception as e:
        print(f"❌ 실패: {e}")
        # 에러 메시지에서 실제 실행된 cmd 추출
        error_str = str(e)
        if "cmd=" in error_str:
            cmd_line = error_str.split("cmd=")[1].split("\n")[0]
            print(f"실행된 명령어: {cmd_line}")
else:
    print("❌ MLX not available")

print("\n✅ Final Reality Gate 증거 확보 완료")
