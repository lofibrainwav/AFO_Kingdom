# ⚙️ AFO Core API 하위 헌법: AGENTS.md

이 문서는 `afo-core` 영역 내에서 에이전트가 준수해야 할 기술적 세부 규칙을 정의합니다.

## 1. 기술 표준 (Technical Standards)
*   **Language**: Python 3.12+ 필수.
*   **Typing**: `typing` 모듈을 사용한 Strict Typing 준수. MyPy 통과 필수.
*   **Validation**: 모든 입출력 데이터는 `Pydantic v2` 모델로 래핑되어야 합니다.
*   **Async**: I/O 바운드 작업은 반드시 `async/await`를 사용합니다.

## 2. 에이전트 인터페이스 (Agent Interfaces)
*   모든 코어 에이전트는 `strategists.base.robust_execute`를 사용하여 Graceful Degradation을 구현해야 합니다.
*   실행 로그는 반드시 `utils.logging.log_sse`를 통해 스트리밍 포맷으로 출력합니다.

## 3. 데이터 보안 (Data Security)
*   민감한 정보는 ` vault_manager`를 통해서만 접근합니다.
*   `.env` 파일에 직접적인 하드코딩은 금지됩니다.
