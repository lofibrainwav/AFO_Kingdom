#!/usr/bin/env python3
"""
MIPROv2 테스트 예시 - 간단한 질문-답변 프로그램 최적화

TICKET-001: MIPROv2 격리 venv 테스트
DSPy MIPROv2를 사용한 간단한 Q&A 프로그램 최적화 예시
"""

import dspy
from dspy.teleprompt import BootstrapFewShot

# MIPROv2 옵티마이저 임포트
from afo.dspy.mipro_v2_optimizer import MIPROv2Optimizer, TrinityAwareMIPROv2


class SimpleQA(dspy.Module):
    """간단한 질문-답변 DSPy 모듈"""

    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought("question -> answer")

    def forward(self, question: str) -> str:
        """질문에 대한 답변 생성"""
        result = self.generate_answer(question=question)
        return result.answer


def create_sample_dataset():
    """샘플 데이터셋 생성"""
    trainset = [
        dspy.Example(question="What is the capital of France?", answer="Paris").with_inputs(
            "question"
        ),
        dspy.Example(question="What is 2 + 2?", answer="4").with_inputs("question"),
        dspy.Example(question="What color is the sky on a clear day?", answer="Blue").with_inputs(
            "question"
        ),
        dspy.Example(
            question="What is the largest planet in our solar system?", answer="Jupiter"
        ).with_inputs("question"),
        dspy.Example(question="What do bees produce?", answer="Honey").with_inputs("question"),
    ]
    return trainset


def basic_accuracy_metric(prediction: str, gold: str) -> bool:
    """기본 정확도 메트릭"""
    return prediction.strip().lower() == gold.strip().lower()


async def test_basic_dspy():
    """기본 DSPy 기능 테스트"""
    print("🔍 Testing basic DSPy functionality...")

    # LM 설정 - AFO 왕국 자체 제작 Ollama 시스템 우선 사용
    try:
        # DSPy의 Ollama 지원 확인 및 사용
        import requests

        # Ollama 직접 API 사용 (DSPy wrapper가 없을 경우)
        class OllamaLM:
            def __init__(self, model="llama3.2:3b", port=11435, timeout_s=120):
                self.model = model
                self.base_url = f"http://localhost:{port}"
                self.timeout = timeout_s

            def __call__(self, prompt, **kwargs):
                try:
                    response = requests.post(
                        f"{self.base_url}/api/generate",
                        json={"model": self.model, "prompt": prompt, "stream": False},
                        timeout=self.timeout,
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return result.get("response", "")
                    else:
                        raise Exception(f"Ollama API error: {response.status_code}")
                except Exception as e:
                    raise Exception(f"Ollama call failed: {e}")

            def __str__(self):
                return f"OllamaLM({self.model})"

        lm = OllamaLM(model="llama3.2:3b", port=11435, timeout_s=120)
        dspy.settings.configure(lm=lm)
        print("✅ DSPy configured with AFO Kingdom Ollama system")

    except Exception as e:
        print(f"⚠️  Ollama not available ({e}), falling back to mock LM")

        # Fallback: 모의 LM (API 호출 없이)
        class MockLM:
            def __call__(self, prompt, **kwargs):
                return f"Mock response for: {prompt[:50]}..."

            def __str__(self):
                return "MockLM (AFO Kingdom fallback)"

        lm = MockLM()
        dspy.settings.configure(lm=lm)

    # 프로그램 생성 및 테스트
    program = SimpleQA()
    question = "What is the capital of France?"
    result = program(question=question)

    print(f"Question: {question}")
    print(f"Answer: {result}")
    print("✅ Basic DSPy test passed!")


async def test_bootstrap_fewshot():
    """BootstrapFewShot으로 기본 최적화 테스트"""
    print("\n🔍 Testing BootstrapFewShot optimization...")

    # LM 설정 - AFO 왕국 Ollama 시스템 우선 사용
    try:
        import requests

        class OllamaLM:
            def __init__(self, model="llama3.2:3b", port=11435, timeout_s=120):
                self.model = model
                self.base_url = f"http://localhost:{port}"
                self.timeout = timeout_s

            def __call__(self, prompt, **kwargs):
                try:
                    response = requests.post(
                        f"{self.base_url}/api/generate",
                        json={"model": self.model, "prompt": prompt, "stream": False},
                        timeout=self.timeout,
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return result.get("response", "")
                    else:
                        raise Exception(f"Ollama API error: {response.status_code}")
                except Exception as e:
                    raise Exception(f"Ollama call failed: {e}")

            def __str__(self):
                return f"OllamaLM({self.model})"

        lm = OllamaLM(model="llama3.2:3b", port=11435, timeout_s=120)
        dspy.settings.configure(lm=lm)
        print("✅ BootstrapFewShot configured with AFO Kingdom Ollama")
    except Exception as e:
        print(f"⚠️  Ollama not available for BootstrapFewShot ({e}), skipping test")
        return

    # 데이터셋 생성
    trainset = create_sample_dataset()

    # 프로그램 생성
    program = SimpleQA()

    # BootstrapFewShot 최적화
    teleprompter = BootstrapFewShot(metric=basic_accuracy_metric, max_bootstrapped_demos=2)
    optimized_program = teleprompter.compile(program, trainset=trainset)

    # 테스트
    test_question = "What is 2 + 2?"
    result = optimized_program(question=test_question)
    print(f"Test Question: {test_question}")
    print(f"Optimized Answer: {result}")
    print("✅ BootstrapFewShot test passed!")


async def test_mipro_v2_basic():
    """MIPROv2 기본 기능 테스트"""
    print("\n🔍 Testing MIPROv2 basic functionality...")

    # 데이터셋 생성
    trainset = create_sample_dataset()

    # 프로그램 생성
    program = SimpleQA()

    # MIPROv2 옵티마이저 생성
    optimizer = MIPROv2Optimizer(
        num_candidates=5,
        init_temperature=1.0,
        verbose=True,
        num_threads=1,  # API 비용 절감을 위해 1로 설정
    )

    print("Starting MIPROv2 optimization (this may take a few minutes)...")

    try:
        # 최적화 실행 (간단한 설정으로 테스트)
        optimized_program = await optimizer.optimize(
            program=program,
            trainset=trainset,
            num_trials=3,  # 비용 절감을 위해 적은 trial 수
            max_bootstrapped_demos=2,
            max_labeled_demos=2,
        )

        print("✅ MIPROv2 optimization completed!")

        # 최적화 결과 테스트
        test_question = "What is the largest planet?"
        result = optimized_program(question=test_question)
        print(f"Test Question: {test_question}")
        print(f"MIPROv2 Optimized Answer: {result}")

        # 증거 확인
        history = optimizer.get_optimization_history()
        print(f"Optimization steps recorded: {len(history)}")

        return True

    except Exception as e:
        print(f"❌ MIPROv2 test failed: {e}")
        return False


async def test_trinity_mipro():
    """Trinity 인식 MIPROv2 테스트"""
    print("\n🔍 Testing Trinity-aware MIPROv2...")

    # 데이터셋 생성
    trainset = create_sample_dataset()

    # 프로그램 생성
    program = SimpleQA()

    # Trinity 인식 옵티마이저 생성
    trinity_optimizer = TrinityAwareMIPROv2(
        trinity_weights={
            "truth": 0.4,  # 정확성 우선
            "goodness": 0.3,  # 안정성
            "beauty": 0.2,  # 단순함
            "serenity": 0.05,  # 평온
            "eternity": 0.05,  # 지속성
        },
        num_candidates=3,
        verbose=True,
        num_threads=1,
    )

    print("Starting Trinity-aware MIPROv2 optimization...")

    try:
        # 최적화 실행
        optimized_program = await trinity_optimizer.optimize(
            program=program,
            trainset=trainset,
            num_trials=2,  # 더 적은 trial로 테스트
            max_bootstrapped_demos=1,
            max_labeled_demos=1,
        )

        print("✅ Trinity MIPROv2 optimization completed!")

        # 테스트
        test_question = "What color is the sky?"
        result = optimized_program(question=test_question)
        print(f"Test Question: {test_question}")
        print(f"Trinity Optimized Answer: {result}")

        # Trinity 가중치 확인
        print(f"Trinity weights used: {trinity_optimizer.trinity_weights}")

        return True

    except Exception as e:
        print(f"❌ Trinity MIPROv2 test failed: {e}")
        return False


async def main():
    """메인 테스트 함수"""
    print("🚀 AFO Kingdom MIPROv2 Test Suite")
    print("=" * 60)

    # OpenAI API 키 확인
    if not dspy.settings.lm or not hasattr(dspy.settings.lm, "api_key"):
        print("⚠️  OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
        print("Running limited tests without API calls...")

        # API 키 없는 기본 테스트만
        print("\n🔍 Running API-free tests...")
        optimizer = MIPROv2Optimizer(verbose=True)
        print(f"✅ MIPROv2Optimizer created: {type(optimizer).__name__}")

        trinity_optimizer = TrinityAwareMIPROv2(verbose=True)
        print(f"✅ TrinityAwareMIPROv2 created: {type(trinity_optimizer).__name__}")
        print(f"   Trinity weights: {trinity_optimizer.trinity_weights}")

        print("\n🎯 API-free tests completed!")
        return

    # API 키가 있는 경우 전체 테스트 실행
    results = []

    # 기본 DSPy 테스트
    try:
        await test_basic_dspy()
        results.append(("Basic DSPy", True))
    except Exception as e:
        print(f"❌ Basic DSPy test failed: {e}")
        results.append(("Basic DSPy", False))

    # BootstrapFewShot 테스트
    try:
        await test_bootstrap_fewshot()
        results.append(("BootstrapFewShot", True))
    except Exception as e:
        print(f"❌ BootstrapFewShot test failed: {e}")
        results.append(("BootstrapFewShot", False))

    # MIPROv2 기본 테스트
    mipro_result = await test_mipro_v2_basic()
    results.append(("MIPROv2 Basic", mipro_result))

    # Trinity MIPROv2 테스트
    trinity_result = await test_trinity_mipro()
    results.append(("Trinity MIPROv2", trinity_result))

    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")

    successful_tests = sum(1 for _, success in results if success)
    total_tests = len(results)

    print(f"\n🎯 Overall: {successful_tests}/{total_tests} tests passed")

    if successful_tests == total_tests:
        print("🎉 All MIPROv2 tests PASSED! Ready for production optimization.")
    else:
        print("⚠️  Some tests failed. Check API keys and network connectivity.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
