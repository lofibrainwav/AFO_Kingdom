"""
DSPy MIPROv2 최적화 모듈 - AFO 왕국 Trinity Score 통합
"""

try:
    import dspy  # noqa: F401 - used conditionally with DSPY_AVAILABLE flag
    from dspy.teleprompt import MIPROv2

    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False

    # DSPy가 설치되지 않은 경우 모의 클래스 제공
    class MIPROv2:
        def __init__(self, **kwargs):
            pass

        def compile(self, program, trainset=None, valset=None):
            return program


class AFOMIPROv2(MIPROv2):
    """AFO 왕국 MIPROv2 최적화 클래스 - Trinity Score 통합"""

    def __init__(self, trinity_score: float = 78.3, auto: str = "medium"):
        if not DSPY_AVAILABLE:
            self.trinity_score = trinity_score
            return

        super().__init__(metric=trinity_metric, auto=auto)
        self.trinity_score = trinity_score

    def compile(self, program, trainset=None, valset=None):
        """Trinity Score를 반영한 최적화 컴파일"""
        if not DSPY_AVAILABLE:
            # DSPy가 없으면 기본 프로그램 반환 (Trinity Score 로깅)
            print(f"⚠️  DSPy 미설치: Trinity Score {self.trinity_score}로 기본 최적화")
            return program

        # 실제 MIPROv2 최적화 (Optuna TPE 기반)
        optimized_program = super().compile(program, trainset=trainset, valset=valset)

        # Trinity Score 적용
        return self._apply_trinity_score(optimized_program)

    def _apply_trinity_score(self, program):
        """Trinity Score 기반 최적화 후처리"""
        if hasattr(program, "signature"):
            # DSPy 프로그램에 Trinity Score 메타데이터 추가
            program._trinity_score = self.trinity_score
            program._optimized_by = "AFOMIPROv2"

        print(f"🏰 AFOMIPROv2 최적화 완료 - Trinity Score: {self.trinity_score}")
        return program


def optimize_rag_with_mipro_v2(rag_module, trainset, eval_fn=None, trinity_score: float = 78.3):
    """
    RAG 모듈 MIPROv2 최적화 (DSPy + Trinity Score)

    Args:
        rag_module: 최적화할 RAG 모듈
        trainset: 학습 데이터셋
        eval_fn: 평가 함수
        trinity_score: 현재 Trinity Score

    Returns:
        최적화된 RAG 모듈
    """

    if not DSPY_AVAILABLE:
        print(f"⚠️  DSPy 미설치: Trinity Score {trinity_score}로 기본 RAG 반환")
        return rag_module

    # AFOMIPROv2 최적화 실행
    optimizer = AFOMIPROv2(trinity_score=trinity_score, auto="medium")

    try:
        optimized_rag = optimizer.compile(rag_module, trainset=trainset)
        print(f"✅ RAG MIPROv2 최적화 성공 - Trinity Score: {trinity_score}")
        return optimized_rag

    except Exception as e:
        print(f"❌ MIPROv2 최적화 실패: {e}")
        print("🔄 기본 RAG 모듈 반환")
        return rag_module


# Trinity Score 기반 메트릭 함수
def trinity_metric(example, prediction, trinity_score: float = 78.3):
    """
    Trinity Score 기반 평가 메트릭

    DSPy MIPROv2에서 사용되는 메트릭 함수
    """
    # 기본 정확도 평가 (실제로는 더 복잡한 Trinity Score 계산)
    accuracy = len(prediction.split()) / max(len(example.get("question", "").split()), 1)

    # Trinity Score 가중치 적용
    weighted_score = accuracy * (trinity_score / 100.0)

    return weighted_score


# 사용 예시 (DSPy 설치된 경우)
if __name__ == "__main__":
    if DSPY_AVAILABLE:
        # 실제 DSPy MIPROv2 사용
        optimizer = AFOMIPROv2(trinity_score=87.3)
        print(f"🏰 AFO MIPROv2 준비 완료 - Trinity Score: {optimizer.trinity_score}")
    else:
        # DSPy 미설치 시뮬레이션
        print("⚠️  DSPy 미설치 - 시뮬레이션 모드")
        optimizer = AFOMIPROv2(trinity_score=78.3)
        print(f"🏰 AFO MIPROv2 시뮬레이션 - Trinity Score: {optimizer.trinity_score}")
