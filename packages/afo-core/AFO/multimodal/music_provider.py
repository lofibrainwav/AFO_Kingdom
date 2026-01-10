"""
MusicProvider Interface - 오픈소스 음악 생성 서비스 통합
AFO 왕국의 멀티모달 음악 생성을 위한 통합 인터페이스

지원 Provider:
- AudioCraft (Meta): 고품질 + 세부 제어 (메인)
- MusicGen (Meta): 빠른 생성 + 간단 API (백업)
- Stable Audio Open (Stability AI): 안정적 + 유연한 길이 (보조)
- Suno (외부 API): 상용 서비스 (옵션)
"""

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from typing import Union as UnionType
else:
    UnionType = Union

logger = logging.getLogger(__name__)


class MusicProvider(ABC):
    """
    음악 생성 Provider의 표준 인터페이스
    모든 음악 생성 서비스는 이 인터페이스를 구현해야 함
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider 이름"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Provider 버전"""
        pass

    @abstractmethod
    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        TimelineState를 기반으로 음악 생성

        Args:
            timeline_state: TimelineState dict
            **kwargs: Provider별 추가 파라미터

        Returns:
            생성 결과 dict
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> dict[str, Any]:
        """
        Provider의 기능/제한사항 반환

        Returns:
            capabilities dict
        """
        pass

    @abstractmethod
    def estimate_cost(self, timeline_state: dict[str, Any]) -> float:
        """
        음악 생성 비용 추정 (로컬은 0, API는 실제 비용)

        Args:
            timeline_state: TimelineState dict

        Returns:
            예상 비용 (USD)
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Provider가 사용 가능한지 확인

        Returns:
            사용 가능 여부
        """
        pass


class AudioCraftProvider(MusicProvider):
    """
    AudioCraft (Meta) Provider
    고품질 음악 생성 + 세부 시간 제어
    """

    @property
    def name(self) -> str:
        return "AudioCraft"

    @property
    def version(self) -> str:
        return "v1.4.1"

    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        AudioCraft를 사용한 음악 생성
        TimelineState의 시간별 세그먼트를 개별로 생성하고 합성
        """
        try:
            # AudioCraft import 시도
            from audiocraft.data.audio import audio_write
            from audiocraft.models import MusicGen

            # 모델 로드 (lazy loading)
            model = MusicGen.get_pretrained("facebook/musicgen-melody")
            model.set_generation_params(duration=30)  # 기본 30초

            # TimelineState 처리
            sections = timeline_state.get("sections", [])
            if not sections:
                return {"error": "No sections in timeline_state"}

            # 각 섹션별 프롬프트 생성
            prompts = []
            for section in sections:
                text = section.get("text", "")
                directive = section.get("music_directive", "epic orchestral")
                prompt = f"{directive}, {text}" if text else directive
                prompts.append(prompt)

            # 배치 생성
            if len(prompts) == 1:
                wav = model.generate([prompts[0]], progress=True)
            else:
                # 멀티 프롬프트 처리 (실험적)
                combined_prompt = " | ".join(prompts[:4])  # 최대 4개
                wav = model.generate([combined_prompt], progress=True)

            # 오디오 저장
            output_path = kwargs.get("output_path", "artifacts/audiocraft_output.wav")
            audio_write(
                output_path, wav[0].cpu(), model.sample_rate, strategy="loudness"
            )

            return {
                "success": True,
                "provider": self.name,
                "output_path": output_path,
                "duration": wav[0].shape[1] / model.sample_rate,
                "sample_rate": model.sample_rate,
            }

        except ImportError:
            return {
                "success": False,
                "error": "AudioCraft not installed. Run: pip install audiocraft",
                "provider": self.name,
            }
        except Exception as e:
            logger.error(f"AudioCraft generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": self.name,
            }

    def get_capabilities(self) -> dict[str, Any]:
        return {
            "timeline_control": True,  # 세부 시간 제어 가능
            "quality": "high",  # 고품질
            "speed": "medium",  # 중간 속도
            "max_sections": 4,  # 최대 4개 섹션
            "requires_gpu": True,  # GPU 필요
            "local_only": True,  # 로컬 실행만
        }

    def estimate_cost(self, timeline_state: dict[str, Any]) -> float:
        # 로컬 실행이므로 비용 0
        return 0.0

    def is_available(self) -> bool:
        try:
            import audiocraft

            return True
        except ImportError:
            return False


class MusicGenProvider(MusicProvider):
    """
    MusicGen (Meta) Provider
    빠른 음악 생성 + 간단 API
    """

    @property
    def name(self) -> str:
        return "MusicGen"

    @property
    def version(self) -> str:
        return "v1.2.0"

    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        MusicGen을 사용한 음악 생성
        빠르고 간단한 텍스트-음악 변환
        """
        try:
            # MusicGen import 시도
            import torch
            from audiocraft.models import MusicGen

            # 모델 선택 (small/medium/large)
            model_size = kwargs.get("model_size", "medium")
            model = MusicGen.get_pretrained(f"facebook/musicgen-{model_size}")

            # TimelineState에서 통합 프롬프트 생성
            sections = timeline_state.get("sections", [])
            music = timeline_state.get("music", {})

            if sections:
                # 섹션별 프롬프트 결합
                prompts = []
                for section in sections:
                    text = section.get("text", "")
                    directive = section.get("music_directive", "instrumental")
                    prompt = f"{directive} {text}".strip()
                    prompts.append(prompt)

                # 가장 빈번한 directive를 메인으로
                from collections import Counter

                directives = [
                    s.get("music_directive", "instrumental") for s in sections
                ]
                main_directive = Counter(directives).most_common(1)[0][0]

                final_prompt = f"{main_directive}, {len(sections)} sections composition"
            else:
                final_prompt = music.get("prompt", "epic orchestral music")

            # 음악 생성
            model.set_generation_params(
                duration=kwargs.get("duration", 30),
                temperature=kwargs.get("temperature", 0.8),
            )

            wav = model.generate([final_prompt], progress=True)

            # 오디오 저장
            from audiocraft.data.audio import audio_write

            output_path = kwargs.get("output_path", "artifacts/musicgen_output.wav")
            audio_write(
                output_path, wav[0].cpu(), model.sample_rate, strategy="loudness"
            )

            return {
                "success": True,
                "provider": self.name,
                "output_path": output_path,
                "duration": wav[0].shape[1] / model.sample_rate,
                "sample_rate": model.sample_rate,
                "model_size": model_size,
            }

        except ImportError:
            return {
                "success": False,
                "error": "MusicGen not installed. Run: pip install audiocraft",
                "provider": self.name,
            }
        except Exception as e:
            logger.error(f"MusicGen generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": self.name,
            }

    def get_capabilities(self) -> dict[str, Any]:
        return {
            "timeline_control": False,  # 세부 시간 제어 제한적
            "quality": "good",  # 좋은 품질
            "speed": "fast",  # 빠른 생성
            "max_sections": 1,  # 통합 생성
            "requires_gpu": True,  # GPU 필요
            "local_only": True,  # 로컬 실행만
            "model_sizes": ["small", "medium", "large"],
        }

    def estimate_cost(self, timeline_state: dict[str, Any]) -> float:
        # 로컬 실행이므로 비용 0
        return 0.0

    def is_available(self) -> bool:
        try:
            import audiocraft

            return True
        except ImportError:
            return False


class StableAudioProvider(MusicProvider):
    """
    Stable Audio Open (Stability AI) Provider
    안정적인 오픈소스 음악 생성
    """

    @property
    def name(self) -> str:
        return "Stable Audio Open"

    @property
    def version(self) -> str:
        return "v1.0.0"

    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        Stable Audio Open을 사용한 음악 생성
        """
        try:
            # Stable Audio Open import 시도
            from stable_audio_tools import get_pretrained_model
            from stable_audio_tools.inference import generate_audio

            # 모델 로드
            model, processor = get_pretrained_model("stabilityai/stable-audio-open-1.0")

            # TimelineState에서 프롬프트 생성
            sections = timeline_state.get("sections", [])
            music = timeline_state.get("music", {})

            if sections:
                # 첫 번째 섹션의 directive 사용
                first_section = sections[0]
                directive = first_section.get("music_directive", "instrumental")
                text = first_section.get("text", "")
                prompt = f"{directive} {text}".strip() if text else directive
            else:
                prompt = music.get("prompt", "instrumental music")

            # 음악 생성
            duration = kwargs.get("duration", 10)  # 1-47초 지원
            sample_rate = 44100

            output = generate_audio(
                model=model,
                processor=processor,
                prompt=prompt,
                duration=duration,
                num_samples=1,
            )

            # 오디오 저장
            import torchaudio

            output_path = kwargs.get("output_path", "artifacts/stable_audio_output.wav")
            torchaudio.save(output_path, output[0], sample_rate)

            return {
                "success": True,
                "provider": self.name,
                "output_path": output_path,
                "duration": duration,
                "sample_rate": sample_rate,
            }

        except ImportError:
            return {
                "success": False,
                "error": "Stable Audio Open not installed. Run: pip install stable-audio-tools",
                "provider": self.name,
            }
        except Exception as e:
            logger.error(f"Stable Audio generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": self.name,
            }

    def get_capabilities(self) -> dict[str, Any]:
        return {
            "timeline_control": False,  # 단일 프롬프트 기반
            "quality": "good",  # 좋은 품질
            "speed": "medium",  # 중간 속도
            "max_sections": 1,  # 단일 생성
            "requires_gpu": True,  # GPU 필요
            "local_only": True,  # 로컬 실행만
            "duration_range": [1, 47],  # 1-47초 지원
        }

    def estimate_cost(self, timeline_state: dict[str, Any]) -> float:
        # 로컬 실행이므로 비용 0
        return 0.0

    def is_available(self) -> bool:
        try:
            import stable_audio_tools

            return True
        except ImportError:
            return False


class MLXMusicGenProvider(MusicProvider):
    """
    MLX MusicGen Provider
    Apple Silicon 최적화된 고성능 음악 생성
    """

    def __init__(self):
        self.venv_path = "venv_musicgen"
        self.model = None
        self.sample_rate = None

    @property
    def name(self) -> str:
        return "MLX MusicGen"

    @property
    def version(self) -> str:
        return "v1.0.0"

    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        MLX MusicGen을 사용한 음악 생성
        venv 환경에서 Apple Silicon 최적화 모델 실행
        """
        try:
            import json
            import os
            import subprocess
            import tempfile

            # TimelineState에서 프롬프트 생성
            sections = timeline_state.get("sections", [])
            music = timeline_state.get("music", {})

            if sections:
                # 첫 번째 섹션의 directive를 메인으로 사용
                first_section = sections[0]
                directive = first_section.get("music_directive", "epic orchestral")
                text = first_section.get("text", "")
                prompt = f"{directive} {text}".strip() if text else directive
            else:
                prompt = music.get("prompt", "epic orchestral music")

            # MLX MusicGen 실행 스크립트 생성
            script_content = f"""
import sys
import json
sys.path.insert(0, "/Users/brnestrm/AFO_Kingdom/mlx-examples-official/musicgen")

try:
    from musicgen import MusicGen
    import numpy as np

    # 모델 로드
    model = MusicGen.from_pretrained("facebook/musicgen-small")
    print(f"Model loaded with sample rate: {{model.sampling_rate}}")

    # 음악 생성 (MLX API에 맞게 수정)
    prompt = "{prompt}"
    print(f"Generating music for prompt: {{prompt}}")

    # duration을 max_steps로 변환 (대략적인 계산)
    duration = {kwargs.get("duration", 30)}
    max_steps = min(int(duration * 50), 1000)  # 대략 50 steps per second, max 1000
    print(f"Duration: {{duration}}s -> max_steps: {{max_steps}}")

    audio = model.generate([prompt], max_steps=max_steps)
    print(f"Generated audio shape: {{audio.shape}}")

    # numpy array로 변환
    audio_np = np.array(audio).squeeze()
    print(f"Audio numpy shape: {{audio_np.shape}}")

    # WAV 파일로 저장
    import scipy.io.wavfile
    output_path = "{kwargs.get("output_path", "artifacts/mlx_music_output.wav")}"
    scipy.io.wavfile.write(output_path, model.sampling_rate, audio_np)

    result = {{
        "success": True,
        "output_path": output_path,
        "duration": len(audio_np) / model.sampling_rate,
        "sample_rate": model.sampling_rate,
        "prompt": prompt,
        "max_steps": max_steps
    }}
    print(json.dumps(result))

except Exception as e:
    import traceback
    error_result = {{
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc()
    }}
    print(json.dumps(error_result))
"""

            # 임시 스크립트 파일 생성
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(script_content)
                script_path = f.name

            # venv에서 스크립트 실행
            venv_python = f"{self.venv_path}/bin/python3"
            if not os.path.exists(venv_python):
                return {
                    "success": False,
                    "error": f"MLX venv not found at {venv_python}",
                    "provider": self.name,
                }

            cmd = [venv_python, script_path]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5분 타임아웃
                cwd="/Users/brnestrm/AFO_Kingdom",
            )

            # 임시 파일 정리
            os.unlink(script_path)

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"MLX execution failed: {result.stderr}",
                    "stdout": result.stdout,
                    "provider": self.name,
                }

            # JSON 결과 파싱 (마지막 줄만 파싱 - 다른 출력 무시)
            try:
                # stdout의 마지막 줄만 JSON으로 파싱
                lines = result.stdout.strip().split("\n")
                json_line = None
                for line in reversed(lines):
                    line = line.strip()
                    if line.startswith("{") and line.endswith("}"):
                        json_line = line
                        break

                if json_line:
                    output_data = json.loads(json_line)
                    if output_data.get("success"):
                        return {
                            "success": True,
                            "provider": self.name,
                            "output_path": output_data["output_path"],
                            "duration": output_data["duration"],
                            "sample_rate": output_data["sample_rate"],
                            "prompt": output_data["prompt"],
                        }
                    else:
                        return {
                            "success": False,
                            "error": output_data.get("error", "Unknown MLX error"),
                            "traceback": output_data.get("traceback"),
                            "provider": self.name,
                        }
                else:
                    return {
                        "success": False,
                        "error": f"No JSON found in MLX output: {result.stdout}",
                        "provider": self.name,
                    }
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Failed to parse MLX JSON: {e}",
                    "stdout": result.stdout,
                    "provider": self.name,
                }

        except Exception as e:
            logger.error(f"MLX MusicGen generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": self.name,
            }

    def get_capabilities(self) -> dict[str, Any]:
        return {
            "timeline_control": False,  # 통합 프롬프트 기반
            "quality": "excellent",  # Apple Silicon 최적화
            "speed": "fast",  # MPS 가속
            "max_sections": 1,  # 단일 프롬프트
            "requires_gpu": True,  # Apple Silicon GPU
            "local_only": True,  # 로컬 실행
            "model_sizes": ["small", "medium", "large"],
            "apple_silicon_optimized": True,
        }

    def estimate_cost(self, timeline_state: dict[str, Any]) -> float:
        # 로컬 실행이므로 비용 0
        return 0.0

    def is_available(self) -> bool:
        """MLX venv 환경과 MusicGen 사용 가능 여부 확인"""
        try:
            import os
            import subprocess

            venv_python = f"{self.venv_path}/bin/python3"
            if not os.path.exists(venv_python):
                return False

            # MLX import 테스트
            result = subprocess.run(
                [venv_python, "-c", "import mlx; print('MLX OK')"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return False

            # MusicGen import 테스트
            result = subprocess.run(
                [
                    venv_python,
                    "-c",
                    "import sys; sys.path.insert(0, '/Users/brnestrm/AFO_Kingdom/mlx-examples-official/musicgen'); from musicgen import MusicGen; print('MusicGen OK')",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            return result.returncode == 0

        except Exception:
            return False


class SunoProvider(MusicProvider):
    """
    Suno (외부 API) Provider
    기존 SunoBranch를 Provider 인터페이스로 래핑
    """

    @property
    def name(self) -> str:
        return "Suno"

    @property
    def version(self) -> str:
        return "API"

    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        Suno API를 통한 음악 생성
        기존 suno_branch 모듈 활용
        """
        try:
            from .suno_branch import run_suno_pipeline

            result = run_suno_pipeline(
                timeline_state,
                dry_run=False,
                target_av_duration_sec=kwargs.get("duration"),
                video_path_for_fusion=None,  # 오디오만 생성
            )

            if result.get("success"):
                return {
                    "success": True,
                    "provider": self.name,
                    "output_path": result.get("outputs", {}).get("audio_raw"),
                    "duration": (
                        result.get("outputs", {}).get("audio_aligned") and "aligned"
                    )
                    or "original",
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown Suno error"),
                    "provider": self.name,
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": self.name,
            }

    def get_capabilities(self) -> dict[str, Any]:
        return {
            "timeline_control": True,  # 고급 파라미터 지원
            "quality": "excellent",  # 상용 서비스 수준
            "speed": "slow",  # API 호출 시간
            "max_sections": 10,  # 다중 섹션 지원
            "requires_gpu": False,  # 클라우드에서 실행
            "local_only": False,  # API 서비스
        }

    def estimate_cost(self, timeline_state: dict[str, Any]) -> float:
        # Suno API 비용 (예상)
        sections = len(timeline_state.get("sections", []))
        return sections * 0.08  # $0.08 per generation

    def is_available(self) -> bool:
        # API 키 존재 여부로 판단
        import os

        return bool(os.getenv("SUNO_API_KEY"))


class MusicProviderRouter:
    """
    MusicProvider 자동 라우터
    품질/속도/비용 기반으로 최적 Provider 선택
    """

    def __init__(self):
        self.providers: dict[str, MusicProvider] = {}
        self._load_providers()

    def _load_providers(self):
        """사용 가능한 Provider들 로드"""
        candidates = [
            AudioCraftProvider(),
            MusicGenProvider(),
            StableAudioProvider(),
            SunoProvider(),
        ]

        for provider in candidates:
            if provider.is_available():
                self.providers[provider.name] = provider
                logger.info(
                    f"Loaded music provider: {provider.name} v{provider.version}"
                )

    def get_available_providers(self) -> list[str]:
        """사용 가능한 Provider 이름 목록"""
        return list(self.providers.keys())

    def select_provider(self, requirements: dict[str, Any]):
        """
        요구사항에 맞는 최적 Provider 선택

        Args:
            requirements: 선택 기준
                - quality: "high", "medium", "low"
                - speed: "fast", "medium", "slow"
                - local_only: True/False
                - max_cost: 최대 비용

        Returns:
            선택된 Provider 또는 None
        """
        quality_pref = requirements.get("quality", "medium")
        speed_pref = requirements.get("speed", "medium")
        local_only = requirements.get("local_only", False)
        max_cost = requirements.get("max_cost", float("inf"))

        candidates = []
        for name, provider in self.providers.items():
            caps = provider.get_capabilities()

            # 필터링
            if local_only and not caps.get("local_only", False):
                continue

            if max_cost < 0.01 and not caps.get("local_only", False):  # 비용 0 = 로컬만
                continue

            # 점수 계산
            score = 0

            # 품질 점수
            quality_map = {"high": 3, "good": 2, "medium": 1, "low": 0}
            score += quality_map.get(caps.get("quality", "medium"), 1) * 2

            # 속도 점수 (역점수 - 빠를수록 좋음)
            speed_map = {"fast": 3, "medium": 2, "slow": 1}
            score += speed_map.get(caps.get("speed", "medium"), 1)

            candidates.append((score, provider))

        if not candidates:
            return None

        # 최고 점수 Provider 선택
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def generate_music(
        self, timeline_state: dict[str, Any], **kwargs
    ) -> dict[str, Any]:
        """
        자동 Provider 선택 후 음악 생성

        Args:
            timeline_state: TimelineState dict
            **kwargs: 라우터 옵션 + Provider 파라미터

        Returns:
            생성 결과
        """
        # Provider 선택
        requirements = {
            "quality": kwargs.get("quality", "high"),
            "speed": kwargs.get("speed", "medium"),
            "local_only": kwargs.get("local_only", True),  # 기본 로컬 우선
            "max_cost": kwargs.get("max_cost", 0.0),  # 기본 무료만
        }

        provider = self.select_provider(requirements)
        if not provider:
            return {
                "success": False,
                "error": f"No suitable provider found for requirements: {requirements}",
                "available_providers": self.get_available_providers(),
            }

        logger.info(f"Selected music provider: {provider.name} v{provider.version}")

        # Provider별 kwargs 분리
        provider_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ["quality", "speed", "local_only", "max_cost"]
        }

        # 음악 생성
        result = provider.generate_music(timeline_state, **provider_kwargs)

        # 결과에 Provider 정보 추가
        result["selected_provider"] = {
            "name": provider.name,
            "version": provider.version,
            "capabilities": provider.get_capabilities(),
            "estimated_cost": provider.estimate_cost(timeline_state),
        }

        return result


# 글로벌 Router 인스턴스
_music_router = None


def get_music_router() -> MusicProviderRouter:
    """글로벌 MusicProviderRouter 인스턴스"""
    global _music_router
    if _music_router is None:
        _music_router = MusicProviderRouter()
    return _music_router


def generate_music_with_router(
    timeline_state: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """
    MusicProviderRouter를 사용한 음악 생성 편의 함수

    Args:
        timeline_state: TimelineState dict
        **kwargs: 라우터 옵션

    Returns:
        생성 결과
    """
    router = get_music_router()
    return router.generate_music(timeline_state, **kwargs)


# 테스트 함수
def test_music_providers():
    """사용 가능한 Provider들 테스트"""
    router = get_music_router()

    print("🎵 MusicProvider 테스트")
    print(f"사용 가능한 Provider들: {router.get_available_providers()}")

    # 테스트 TimelineState
    test_timeline = {
        "title": "AFO Test Music",
        "sections": [
            {
                "start": 0,
                "end": 3,
                "text": "Epic intro",
                "music_directive": "slow_build",
            },
            {
                "start": 3,
                "end": 6,
                "text": "Action scene",
                "music_directive": "drop_beat",
            },
        ],
    }

    # 각 Provider 테스트
    for provider_name in router.get_available_providers():
        print(f"\n🔍 Testing {provider_name}...")
        try:
            result = router.generate_music(test_timeline, local_only=True, max_cost=0.0)
            if result.get("success"):
                print(f"  ✅ {provider_name}: 성공 - {result.get('output_path')}")
            else:
                print(f"  ❌ {provider_name}: 실패 - {result.get('error')}")
        except Exception as e:
            print(f"  ❌ {provider_name}: 예외 - {e}")


if __name__ == "__main__":
    test_music_providers()
