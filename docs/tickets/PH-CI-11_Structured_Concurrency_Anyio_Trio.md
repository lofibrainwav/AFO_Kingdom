# PH-CI-11 — Structured Concurrency Gate (Anyio/Trio) — SSOT

## 목적
AFO 비동기 실행을 “작업 생명주기(생성→실행→취소/정리)”가 보장되는 구조로 고정한다.

## Gate 규율 (Hard Rule)
- **허용**: `anyio.create_task_group()` (표준)
- **권장**: `anyio.move_on_after()`, `anyio.fail_after()` (취소/타임아웃)
- **금지**: `asyncio.create_task()` (고아 task 위험)
- **예외**: 기존 레거시 호환이 필요한 경우, 반드시 “격리 영역 + 테스트 + 주석”으로 봉인

## 예외 전파 표준
- 병렬 실패는 `ExceptionGroup`으로 표준화한다.
- 테스트에서 `except*`로 분기 처리한다.

## Instrumentation 표준
- Task 시작/종료/취소를 로그로 남긴다.
- 가능하면 TraceContext(OTel)와 함께 로깅한다.

## 검증(Tests)
- 취소 전파: `move_on_after()`로 하위 task 정리 보장
- 다중 실패: TaskGroup에서 2개 이상 예외 발생 시 ExceptionGroup으로 수렴
- 정리 보장: `finally`/cleanup이 반드시 호출되는지 확인

## CI Structured Gate (Soft)
- PR 단계에서 `asyncio.create_task(` 사용 유무를 grep로 탐지하여 경고/차단(프로젝트 정책에 따라).
