import os

import dspy


def configure_default_lm():
    """AFO 왕국 DSPy LM 설정 - 환경변수 기반 자동 구성

    환경변수 우선순위:
    1. AFO_DSPY_PROVIDER: "ollama" | "openai_compat" | "openai"
    2. AFO_DSPY_LM: 모델명
    3. AFO_DSPY_API_BASE: API 기본 URL
    4. AFO_DSPY_API_KEY: API 키 (Ollama는 빈 문자열)

    기본값: Ollama llama3.2
    """
    provider = os.getenv("AFO_DSPY_PROVIDER", "ollama").lower()

    if provider == "ollama":
        # DSPy 공식 Ollama 지원 (ollama_chat/<model>)
        # 현재 Docker 컨테이너의 실제 존재하는 모델 사용 (llama3.2:3b 기본, 멀티모달은 llava:7b)
        model = os.getenv("AFO_DSPY_LM", "ollama_chat/llama3.2:3b")
        api_base = os.getenv("AFO_DSPY_API_BASE", "http://localhost:11435")  # Docker 포트 매핑
        api_key = os.getenv("AFO_DSPY_API_KEY", "")
        lm = dspy.LM(model, api_base=api_base, api_key=api_key)
        dspy.configure(lm=lm)
        return lm

    if provider == "openai_compat":
        # Ollama의 OpenAI 호환 엔드포인트(/v1) 사용
        model = os.getenv("AFO_DSPY_LM", "openai/llama3.2")
        api_base = os.getenv("AFO_DSPY_API_BASE", "http://localhost:11434/v1")
        api_key = os.getenv("AFO_DSPY_API_KEY", "")
        lm = dspy.LM(model, api_base=api_base, api_key=api_key, model_type="chat")
        dspy.configure(lm=lm)
        return lm

    # 기본: OpenAI (필요한 경우에만)
    model = os.getenv("AFO_DSPY_LM", "openai/gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY", os.getenv("AFO_DSPY_API_KEY", ""))
    lm = dspy.LM(model, api_key=api_key)
    dspy.configure(lm=lm)
    return lm
