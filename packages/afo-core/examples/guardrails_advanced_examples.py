"""Advanced Guardrails SDK usage scenarios with graceful fallbacks.

형님이 바로 붙여넣어 실행할 수 있도록, 각 예제는 실제 Guardrails SDK가
설치되어 있을 때는 진짜 호출을 시도하고, 그렇지 않으면 친절한 안내만
출력하도록 구성했습니다. `ENABLE_GUARDRAILS=true` 와
`OPENAI_API_KEY=...` 를 `.env` 에 넣어 두면 동일한 설정을 재사용할 수
있습니다.

실행 방법:
    poetry shell / venv 활성화 후
    python -m afo_soul_engine.examples.guardrails_advanced_examples
"""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

try:
    from guardrails import CustomGuard, GuardrailsOpenAI
except ModuleNotFoundError:  # pragma: no cover - 환경에 따라 설치 미완료 가능
    GuardrailsOpenAI = None  # type: ignore
    CustomGuard = None  # type: ignore

# 스트리밍 전용 클래스는 프리뷰 단계에서 이름이 바뀔 수 있어 optional import 처리
try:  # pragma: no cover - SDK 버전에 따라 달라짐
    from guardrails import StreamingGuardrailsOpenAI
except ModuleNotFoundError:
    StreamingGuardrailsOpenAI = None  # type: ignore


def _require_guardrails() -> bool:
    if GuardrailsOpenAI is None:
        print(
            "⚠️ Guardrails SDK가 설치되어 있지 않습니다. `pip install openai-guardrails` 후 다시 실행하세요."
        )
        return False
    return True


def _build_base_config() -> dict[str, Any]:
    """기본 파이프라인 설정. 필요하면 JSON 파일을 따로 전달해도 됩니다."""

    return {
        "input": [
            {"name": "Moderation", "config": {"categories": ["harassment", "hate", "self-harm"]}}
        ],
        "output": [{"name": "PII", "config": {"action": "block"}}],
    }


def example_parallel_input_output() -> None:
    """입력과 출력 가드를 동시에 적용하는 예제."""

    if not _require_guardrails():
        return

    config = _build_base_config()
    client = GuardrailsOpenAI(
        config=config,
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("GUARDRAILS_MODEL", "gpt-4o-mini"),
    )

    print("[예제1] 입력/출력 병렬 가드 시험")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "내 주민번호는 123-45-6789 이야."}]
    )
    print("  → 응답:", response.choices[0].message.content)


def example_multi_agent_handoff() -> None:
    """에이전트 간 핸드오프를 시뮬레이션 (간단 버전)."""

    if not _require_guardrails():
        return

    print("[예제2] 멀티 에이전트 핸드오프")
    reviewer = GuardrailsOpenAI(
        config={"input": [{"name": "Moderation"}]},
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("GUARDRAILS_MODEL", "gpt-4o-mini"),
    )
    fixer = GuardrailsOpenAI(
        config={"output": [{"name": "PII"}]},
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("GUARDRAILS_MODEL", "gpt-4o-mini"),
    )

    first = reviewer.chat.completions.create(
        messages=[{"role": "user", "content": "악의적인 표현이 섞인 코드를 검토해줘"}]
    )
    intermediary = first.choices[0].message.content
    print("  → 1차 검토 결과:", intermediary)

    second = fixer.chat.completions.create(
        messages=[
            {"role": "system", "content": "불필요한 민감 정보는 모두 제거하라"},
            {"role": "user", "content": intermediary},
        ]
    )
    print("  → 2차 정리 결과:", second.choices[0].message.content)


def example_streaming_guard() -> None:
    """스트리밍 모드에서 토큰을 실시간 검증하는 예제."""

    if StreamingGuardrailsOpenAI is None:
        print(
            "⚠️ StreamingGuardrailsOpenAI 클래스를 찾을 수 없습니다. SDK 프리뷰 버전을 확인하세요."
        )
        return

    client = StreamingGuardrailsOpenAI(
        config={"output": [{"name": "StreamingModeration", "config": {"threshold": "low"}}]},
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("GUARDRAILS_MODEL", "gpt-4o-mini"),
    )

    print("[예제3] 스트리밍 가드")
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": "폭력적인 이야기를 길게 써줘"}],
        stream=True,
    )

    for chunk in stream:
        if "tripwire" in chunk:
            print("\n  → ⚠️ 위험 감지:", chunk["tripwire"]["message"])
            break
        delta = chunk.choices[0].delta.content
        if delta:
            sys.stdout.write(delta)
            sys.stdout.flush()
    print()


def example_custom_guard() -> None:
    """사용자 정의 규칙을 적용하는 예제."""

    if not _require_guardrails():
        return
    if CustomGuard is None:
        print("⚠️ CustomGuard 클래스를 불러올 수 없습니다. SDK 버전을 업데이트하세요.")
        return

    class BrandGuard(CustomGuard):
        def validate(self, text: str) -> bool:  # type: ignore[override]
            return "brand_name" not in text.lower()

    config = {"output": [{"name": "Custom", "guard": BrandGuard()}]}
    client = GuardrailsOpenAI(
        config=config,
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("GUARDRAILS_MODEL", "gpt-4o-mini"),
    )

    print("[예제4] 커스텀 가드")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "brand_name 제품 후기를 써줘"}]
    )
    print("  → 결과:", response.choices[0].message.content)


EXAMPLES: dict[str, Callable[[], None]] = {
    "parallel": example_parallel_input_output,
    "handoff": example_multi_agent_handoff,
    "streaming": example_streaming_guard,
    "custom": example_custom_guard,
}


def run_all_examples() -> None:
    for key, runner in EXAMPLES.items():
        print("=" * 60)
        print(f"실행: {key}")
        try:
            runner()
        except Exception as exc:  # pragma: no cover - 실행 시 안내용
            print(f"  → 예제 실행 중 오류 발생: {exc}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "all":
        run_all_examples()
    else:
        runner = EXAMPLES.get(target)
        if runner is None:
            print(f"알 수 없는 예제입니다: {target}. 사용 가능: {', '.join(EXAMPLES)}")
            sys.exit(1)
        runner()
