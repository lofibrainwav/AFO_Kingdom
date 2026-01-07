import sys
sys.path.insert(0, 'packages/afo-core')
from pathlib import Path
from AFO.multimodal.mlx_musicgen_runner import MLXMusicGenRunner

r = MLXMusicGenRunner.from_env()
print("available:", r.is_available())
wav = r.generate("epic orchestral cinematic, heroic victory theme", duration_sec=6)
print("wav:", wav, "exists:", Path(wav).exists())
