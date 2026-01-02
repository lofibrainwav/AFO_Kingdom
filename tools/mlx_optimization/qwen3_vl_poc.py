#!/usr/bin/env python3
"""
Qwen3-VL MLX PoC 구현 (Apple Silicon M4 최적화)

이 모듈은 Qwen3-VL 비전-언어 모델을 MLX 프레임워크로 실행하는 PoC입니다.
이미지 분석 + 텍스트 생성 체인을 구현합니다.

사용법:
    python qwen3_vl_poc.py --image path/to/image.png --prompt "이미지 분석해줘"
"""

import argparse
import logging
import os
import time

# MLX-VLM imports
try:
    from mlx_lm import generate as llm_generate
    from mlx_lm import load
    from mlx_vlm import generate as vlm_generate

    MLX_VLM_AVAILABLE = True
except ImportError:
    print("mlx-vlm not available. Please install: pip install mlx-vlm")
    MLX_VLM_AVAILABLE = False

# 메모리 모니터링
import psutil

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Qwen3VLMLXPOC:
    """
    Qwen3-VL MLX PoC 클래스

    Apple Silicon M4에서 Qwen3-VL을 MLX로 실행합니다.
    """

    def __init__(self, model_name: str = "mlx-community/Qwen3-VL-8B-Instruct-4bit"):
        """
        PoC 초기화

        Args:
            model_name: 사용할 Qwen3-VL 모델 이름
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.llm_model = None
        self.llm_tokenizer = None
        self.initialized = False

        logger.info("Qwen3-VL MLX PoC initialized with model: %s", model_name)

    def check_memory(self) -> dict:
        """현재 메모리 상태 확인"""
        mem = psutil.virtual_memory()
        return {
            "total_gb": mem.total / (1024**3),
            "used_gb": mem.used / (1024**3),
            "available_gb": mem.available / (1024**3),
            "percentage": mem.percent,
        }

    def initialize_models(self) -> bool:
        """
        Qwen3-VL과 Llama 모델 초기화

        Returns:
            초기화 성공 여부
        """
        if not MLX_VLM_AVAILABLE:
            logger.error("mlx-vlm not available")
            return False

        try:
            # 메모리 체크 (초기화 전)
            mem_before = self.check_memory()
            logger.info(
                f"Memory before initialization: {mem_before['used_gb']:.1f}GB used"
            )

            # Qwen3-VL은 mlx_vlm.generate()로 직접 사용하므로 별도 로드 불필요
            logger.info("Qwen3-VL ready for generation (mlx_vlm.generate)")

            # Llama 3.1 모델 로드 (체인용)
            llama_model = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"
            logger.info("Loading Llama model: %s", llama_model)
            self.llm_model, self.llm_tokenizer = load(llama_model)

            # 메모리 체크 (초기화 후)
            mem_after = self.check_memory()
            logger.info(
                f"Memory after initialization: {mem_after['used_gb']:.1f}GB used"
            )
            logger.info(
                f"Memory delta: {mem_after['used_gb'] - mem_before['used_gb']:.1f}GB"
            )

            self.initialized = True
            return True

        except Exception as e:
            logger.error("Model initialization failed: %s", e)
            return False

    def analyze_image(
        self, image_paths: list[str], prompt: str, max_tokens: int = 512
    ) -> str | None:
        """
        이미지 분석 수행

        Args:
            image_paths: 분석할 이미지 파일 경로들
            prompt: 분석 프롬프트
            max_tokens: 최대 생성 토큰 수

        Returns:
            분석 결과 텍스트
        """
        if not self.initialized:
            logger.error("Models not initialized")
            return None

        if not MLX_VLM_AVAILABLE:
            return "mlx-vlm not available"

        try:
            # 메모리 체크
            mem_before = self.check_memory()
            logger.info(f"Memory before image analysis: {mem_before['used_gb']:.1f}GB")

            # 이미지 파일 존재 확인
            for img_path in image_paths:
                if not os.path.exists(img_path):
                    logger.error("Image file not found: %s", img_path)
                    return f"Image file not found: {img_path}"

            # Qwen3-VL로 이미지 분석
            start_time = time.time()
            logger.info(f"Analyzing {len(image_paths)} image(s) with Qwen3-VL...")

            result = vlm_generate(
                model=self.model_name,
                image=image_paths,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.1,  # 낮은 temperature로 정확한 분석
            )

            analysis_time = time.time() - start_time
            logger.info(f"Image analysis completed in {analysis_time:.2f}s")

            # 메모리 체크
            mem_after = self.check_memory()
            logger.info(f"Memory after analysis: {mem_after['used_gb']:.1f}GB")

            return result

        except Exception as e:
            logger.error("Image analysis failed: %s", e)
            return f"Analysis failed: {e!s}"

    def generate_followup(
        self, visual_analysis: str, followup_prompt: str, max_tokens: int = 512
    ) -> str | None:
        """
        시각 분석 결과를 바탕으로 후속 텍스트 생성 (Llama 체인)

        Args:
            visual_analysis: Qwen3-VL의 시각 분석 결과
            followup_prompt: 후속 프롬프트
            max_tokens: 최대 생성 토큰 수

        Returns:
            후속 생성 결과
        """
        if not self.initialized or not self.llm_model or not self.llm_tokenizer:
            logger.error("Llama model not initialized")
            return None

        try:
            # 체인 프롬프트 구성
            chain_prompt = f"""시각 분석 결과:
{visual_analysis}

{followup_prompt}

답변:"""

            start_time = time.time()
            logger.info("Generating followup with Llama...")

            result = llm_generate(
                self.llm_model,
                self.llm_tokenizer,
                prompt=chain_prompt,
                max_tokens=max_tokens,
                temperature=0.7,
            )

            generation_time = time.time() - start_time
            logger.info(f"Followup generation completed in {generation_time:.2f}s")

            return result

        except Exception as e:
            logger.error("Followup generation failed: %s", e)
            return f"Followup failed: {e!s}"

    def run_visual_debugging_chain(self, image_paths: list[str]) -> dict | None:
        """
        완전한 비주얼 디버깅 체인 실행

        Args:
            image_paths: 분석할 이미지들

        Returns:
            체인 실행 결과
        """
        # 1단계: 이미지 분석 (Qwen3-VL)
        analysis_prompt = """이 이미지(들)을 철저히 분석해서 다음 정보를 추출해줘:
1. UI/대시보드 구성 요소 (버튼, 차트, 텍스트 등)
2. 데이터 값과 메트릭 (숫자, 퍼센트, 상태 등)
3. 잠재적 문제나 에러 징후
4. 전반적인 시스템 상태

한국어로 자세히 설명해줘."""

        visual_result = self.analyze_image(image_paths, analysis_prompt)
        if not visual_result:
            return {"error": "Image analysis failed"}

        # 2단계: 체인 분석 (Llama)
        followup_prompt = """위 시각 분석 결과를 바탕으로:

1. 시스템 건강 상태 평가 (EXCELLENT/GOOD/FAIR/POOR)
2. 발견된 문제점과 개선 제안
3. 추가 모니터링이 필요한 부분
4. Trinity Score (眞善美孝永) 기반 종합 평가

형님에게 보고하는 형식으로 정리해줘."""

        chain_result = self.generate_followup(visual_result, followup_prompt)
        if not chain_result:
            return {"error": "Chain analysis failed", "visual_analysis": visual_result}

        return {
            "visual_analysis": visual_result,
            "chain_analysis": chain_result,
            "timestamp": time.time(),
            "model": self.model_name,
            "images_processed": len(image_paths),
        }


def main():
    """메인 함수 - CLI 인터페이스"""
    parser = argparse.ArgumentParser(description="Qwen3-VL MLX PoC")
    parser.add_argument(
        "--images", nargs="+", required=True, help="Path to image file(s)"
    )
    parser.add_argument(
        "--prompt", default="이 이미지들을 분석해서 요약해줘", help="Analysis prompt"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=512, help="Max tokens to generate"
    )
    parser.add_argument(
        "--model", default="mlx-community/Qwen3-VL-8B-Instruct-4bit", help="Model name"
    )

    args = parser.parse_args()

    # PoC 인스턴스 생성
    poc = Qwen3VLMLXPOC(args.model)

    # 모델 초기화
    print("🔧 Initializing models...")
    if not poc.initialize_models():
        print("❌ Model initialization failed")
        return

    print("✅ Models initialized successfully")

    # 메모리 상태 확인
    mem_info = poc.check_memory()
    print(f"Total memory: {mem_info['total_gb']:.1f} GB")
    print(f"Available memory: {mem_info['available_gb']:.1f} GB")
    # 이미지 분석 실행
    print(f"\n🖼️  Analyzing {len(args.images)} image(s)...")
    result = poc.run_visual_debugging_chain(args.images)

    if result and "error" not in result:
        print("\n🎯 Visual Debugging Chain Result:")
        print("=" * 50)
        print("VISUAL ANALYSIS:")
        print(result["visual_analysis"])
        print("\n" + "=" * 50)
        print("CHAIN ANALYSIS:")
        print(result["chain_analysis"])
        print("=" * 50)

        # 최종 메모리 상태
        final_mem = poc.check_memory()
        print(f"Final memory usage: {final_mem['used_gb']:.1f} GB")
    else:
        print(f"❌ Chain execution failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
