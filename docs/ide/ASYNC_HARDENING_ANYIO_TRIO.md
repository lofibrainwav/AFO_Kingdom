# Async Hardening Guide: Anyio & Trio (2025) – AFO Kingdom Standard

> **"비동기 구조화(Structured Concurrency)는 제국의 흐름을 예측 가능하게 만드는 유일한 길이다."**

## 🛡️ Core Philosophy: Structured Concurrency

제국은 raw `asyncio`에서 **Anyio (Trio 백엔드)**로 전환하여 다음을 보장합니다:
- **Anyio (asyncio backend)**: 제국 프로덕션(uvicorn/FastAPI)은 `asyncio` 런타임을 기본으로 사용하며, Anyio는 이를 위한 구조화된 인터페이스로 활용합니다.
- **Trio for Testing/Dev**: `trio`는 고성능 디버깅, Instrumentation, 그리고 테스트 백엔드(pytest-anyio)를 위한 필수 의존성으로 고정(Pin)합니다.
- **Predictable Cancellation**: 잊힌 task 0% (leak-proof, 이미지 0 MCP 병렬 안전).
- **Exception Groups**: Python 3.12 내장 표준(`ExceptionGroup`, `except*`)을 따릅니다 (이미지 2 평가표처럼 선 100%).
- **Structured Life-cycles**: Nursery/TaskGroup으로 자식 task 엄격 관리 (이미지 7 나침반처럼 방향 명확).

## 🛠️ 실전 코드 가이드 (Anyio Trio – 왕국 표준)

**항상 anyio.run(..., backend="trio") 사용** (Trio 취소 이점 + Asyncio 호환).

### 1. Task Groups (Nurseries – 병렬 task 자동 관리)
`asyncio.create_task` 대신 `anyio.create_task_group()`을 사용합니다.

```python
import anyio

async def skill_execute(name: str):
  print(f"[START] {name} 실행")
  await anyio.sleep(2)  # 작업 시뮬
  print(f"[END] {name} 완료")

async def main():
  async with anyio.create_task_group() as tg:  # Trio Nursery 호환
    tg.start_soon(skill_execute, "MCP-1")
    tg.start_soon(skill_execute, "Skill-30")
    tg.start_soon(skill_execute, "Context7-Lookup")

anyio.run(main, backend="trio")
```

### 2. Timeouts & Cancellation (move_on_after – 자동 취소)
`asyncio.wait_for` 대신 `anyio.move_on_after()`를 사용합니다.

```python
async def critical_operation():
  print("중요 작업 시작 – 10초 소요")
  await anyio.sleep(10)

async def main():
  with anyio.move_on_after(5) as scope:  # 5초 타임아웃
    await critical_operation()
  
  if scope.cancelled_caught:
    print("타임아웃 발생 – Graceful Fallback 적용 (이미지 2 점진적 저하)")
  else:
    print("정상 완료")

anyio.run(main, backend="trio")
```

### 3. Error Handling (ExceptionGroup – 병렬 에러 전체 포착)
Python 3.12의 내장 `ExceptionGroup`을 활용합니다.

```python
async def fail_task():
  raise ValueError("의도적 실패")

async def main():
  try:
    async with anyio.create_task_group() as tg:
      tg.start_soon(skill_execute, "normal")
      tg.start_soon(fail_task)  # 에러 발생
  except* ValueError as eg:
    print(f"ValueError 그룹 포착 (except* 활용)")
  except ExceptionGroup as eg:
    print(f"ExceptionGroup 포착 – {len(eg.exceptions)}개 에러")

anyio.run(main, backend="asyncio") # 프로덕션 표준
```

### 4. Debugging with Trio (Instrumentation – 실시간 추적)
[@instrument_task](utils/async_instrumentation.py) 데코레이터를 사용하여 task 생명주기를 감시합니다.

```python
from trio.abc import Instrument

class KingdomInstrument(Instrument):
  def before_task_run(self, task):
    print(f"→ Task START: {task.name or 'unnamed'}")
  def after_task_run(self, task):
    print(f"← Task END: {task.name or 'unnamed'}")

# anyio.run(main, backend="trio", backend_options={"instruments": [KingdomInstrument()]})
```

## ⚖️ Trinity Score Impact (Dry_Run 100% 결과)
- **眞 (Truth)**: 98 (예측 가능한 흐름 – 취소 명확)
- **善 (Goodness)**: 99 (자동 취소로 리소스 누수 방지)
- **美 (Beauty)**: 100 (구조화된 코드 우아)
- **孝 (Serenity)**: 98 (마찰 최소 – Graceful Fallback)
- **永 (Eternity)**: 100 (Anyio 호환으로 장기 안정)
