"""
AFO 왕국 DSPy LM 라우터 - 작업별 최적 모델 자동 선택

현재 모델 포트폴리오:
- llama3.2:3b: 범용 텍스트 + 추론 작업
- llava:7b: 멀티모달 (이미지 + 텍스트) 작업
- nomic-embed-text:latest: 임베딩 작업
- moondream:latest: 경량 멀티모달 작업

라우팅 전략:
1. 이미지/비전 입력 → llava:7b (멀티모달 최적화)
2. 순수 텍스트/코딩 → llama3.2:3b (범용 최적화)
3. 추론/분석 → llama3.2:3b (추론 성능)
"""

import dspy


class KingdomRouter:
    """AFO 왕국 작업별 LM 자동 라우터"""

    def __init__(self, api_base: str = "http://localhost:11435"):
        """
        라우터 초기화

        Args:
            api_base: Ollama API 기본 URL (Docker 포트 매핑)
        """
        self.api_base = api_base

        # 모델 포트폴리오 초기화 (DSPy.LM 사용)
        self.models = {
            "text": dspy.LM(model="ollama_chat/llama3.2:3b", api_base=api_base),  # 범용 텍스트
            "multimodal": dspy.LM(model="ollama_chat/llava:7b", api_base=api_base),  # 멀티모달
            "reasoning": dspy.LM(model="ollama_chat/llama3.2:3b", api_base=api_base),  # 추론
            "coding": dspy.LM(model="ollama_chat/llama3.2:3b", api_base=api_base),  # 코딩
        }

        # 라우팅 룰 정의
        self.routing_rules = [
            # 멀티모달 키워드 우선
            (lambda q, img: bool(img) or self._has_vision_keywords(q), "multimodal"),
            # 코딩 관련 키워드
            (lambda q, img: self._has_coding_keywords(q), "coding"),
            # 추론 관련 키워드
            (lambda q, img: self._has_reasoning_keywords(q), "reasoning"),
            # 기본: 범용 텍스트
            (lambda q, img: True, "text"),
        ]

    def _has_vision_keywords(self, query: str) -> bool:
        """비전 관련 키워드 감지"""
        vision_keywords = [
            "이미지",
            "사진",
            "그림",
            "image",
            "photo",
            "picture",
            "시각",
            "비주얼",
            "visual",
            "vision",
            "img",
            "png",
            "jpg",
            "보여",
            "보이",
            "보여주",
            "show",
            "display",
            "view",
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in vision_keywords)

    def _has_coding_keywords(self, query: str) -> bool:
        """코딩 관련 키워드 감지"""
        coding_keywords = [
            "코드",
            "프로그래밍",
            "programming",
            "code",
            "function",
            "class",
            "함수",
            "메소드",
            "변수",
            "알고리즘",
            "algorithm",
            "script",
            "개발",
            "디버그",
            "debug",
            "컴파일",
            "compile",
            "실행",
            "run",
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in coding_keywords)

    def _has_reasoning_keywords(self, query: str) -> bool:
        """추론 관련 키워드 감지"""
        reasoning_keywords = [
            "분석",
            "analyze",
            "추론",
            "reasoning",
            "inference",
            "생각",
            "think",
            "판단",
            "judge",
            "평가",
            "evaluate",
            "결정",
            "decide",
            "논리",
            "logic",
            "증명",
            "prove",
            "해결",
            "solve",
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in reasoning_keywords)

    def route(self, query: str, image: str | None = None) -> str:
        """
        쿼리와 이미지에 따라 최적 LM 선택

        Args:
            query: 텍스트 쿼리
            image: base64 인코딩된 이미지 (선택사항)

        Returns:
            선택된 모델 타입 ("text", "multimodal", "reasoning", "coding")
        """
        for condition, model_type in self.routing_rules:
            if condition(query, image):
                return model_type

        return "text"  # 기본값

    def get_lm(self, query: str, image: str | None = None):
        """
        쿼리에 최적화된 LM 인스턴스 반환

        Args:
            query: 텍스트 쿼리
            image: base64 인코딩된 이미지 (선택사항)

        Returns:
            라우팅된 OllamaLocal 인스턴스
        """
        model_type = self.route(query, image)
        return self.models[model_type]

    def call(self, query: str, image: str | None = None, **kwargs) -> str:
        """
        라우팅된 LM으로 직접 호출

        Args:
            query: 텍스트 쿼리
            image: base64 인코딩된 이미지 (선택사항)
            **kwargs: 추가 파라미터

        Returns:
            LM 응답
        """
        lm = self.get_lm(query, image)
        model_type = self.route(query, image)

        with dspy.settings.context(lm=lm):
            # 기본 ChainOfThought로 호출
            signature = dspy.Signature(query=str, **({"image": str} if image else {}), answer=str)

            cot = dspy.ChainOfThought(signature)
            if image:
                result = cot(query=query, image=image, **kwargs)
            else:
                result = cot(query=query, **kwargs)

            return result.answer

    def __str__(self) -> str:
        """라우터 상태 문자열"""
        return f"KingdomRouter(models={list(self.models.keys())}, api_base={self.api_base})"


# 전역 라우터 인스턴스
kingdom_router = KingdomRouter()


def get_optimal_lm(query: str, image: str | None = None):
    """
    편의 함수: 쿼리에 최적화된 LM 반환

    Args:
        query: 텍스트 쿼리
        image: base64 인코딩된 이미지 (선택사항)

    Returns:
        최적화된 OllamaLocal 인스턴스
    """
    return kingdom_router.get_lm(query, image)


def route_and_call(query: str, image: str | None = None, **kwargs) -> str:
    """
    편의 함수: 라우팅 후 직접 호출

    Args:
        query: 텍스트 쿼리
        image: base64 인코딩된 이미지 (선택사항)
        **kwargs: 추가 파라미터

    Returns:
        LM 응답
    """
    return kingdom_router.call(query, image, **kwargs)


# Trinity Score 기반 라우팅 (MIPROv2 통합용)
def get_trinity_weighted_lm(task_type: str = "general"):
    """
    Trinity Score 기반 LM 선택

    Args:
        task_type: 작업 타입 ("text", "multimodal", "reasoning", "coding")

    Returns:
        Trinity 가중치에 따른 최적 LM
    """
    # Trinity 가중치 기반 라우팅
    trinity_weights = {
        "眞": 0.35,  # Truth - 정확성
        "善": 0.35,  # Goodness - 안정성
        "美": 0.20,  # Beauty - 단순함
        "孝": 0.08,  # Serenity - 평온
        "永": 0.02,  # Eternity - 지속성
    }

    # 작업 타입별 모델 매핑
    task_model_map = {
        "text": "llama3.2:3b",  # 眞+善 최적화
        "multimodal": "llava:7b",  # 美+眞 최적화
        "reasoning": "llama3.2:3b",  # 眞+善 최적화
        "coding": "llama3.2:3b",  # 眞+孝 최적화
    }

    model_name = task_model_map.get(task_type, "llama3.2:3b")
    return dspy.LM(model=f"ollama_chat/{model_name}", api_base="http://localhost:11435")


if __name__ == "__main__":
    # 테스트
    router = KingdomRouter()

    # 텍스트 쿼리 테스트
    text_query = "파이썬 함수를 작성해주세요"
    text_lm = router.get_lm(text_query)
    print(f"Text query '{text_query}' -> {text_lm.model}")

    # 멀티모달 쿼리 테스트
    vision_query = "이 이미지를 분석해주세요"
    vision_lm = router.get_lm(vision_query, image="base64_data")
    print(f"Vision query '{vision_query}' -> {vision_lm.model}")

    # 코딩 쿼리 테스트
    code_query = "버그를 디버그하는 방법은?"
    code_lm = router.get_lm(code_query)
    print(f"Code query '{code_query}' -> {code_lm.model}")

    print(f"Router: {router}")
