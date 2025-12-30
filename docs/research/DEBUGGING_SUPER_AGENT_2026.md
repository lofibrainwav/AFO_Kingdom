# 🧠 Research: Debugging Super Agent 2026 (Active Inference & Self-Healing)

## 1. Core Philosophy: Active Inference (FEP)

2026년의 디버깅 에이전트는 단순한 "반응형(Reactive)" 도구가 아니라, **"능동적 추론(Active Inference)"**을 통해 시스템의 무결성을 유지하는 자율 존재입니다.

- **Objective**: Minimize Variational Free Energy (Surprise/Entropy).
- **Loop**: `Observation` (Logs/Metrics) -> `Internal Model` (Update Belief) -> `Action` (Fix/Probe) -> `Outcome`.
- **SSOT**: The agent's internal model *is* the runtime representation of the [AFO_FINAL_SSOT.md](../../AFO_FINAL_SSOT.md).

## 2. Architecture: MCP-Native & Multi-Agent

### 2.1 Agent Persona: "The Supervisor (감찰관)"
- **Role**: Detect, Diagnose, and Heal.
- **Tools (MCP)**:
  - `fetch_metrics`: Prometheus/Sentry status.
  - `read_logs`: Access logs via `read_resource`.
  - `run_diagnostics`: Execute `pytest`, `ruff`.
  - `apply_patch`: Hot-patch code (controlled).

### 2.2 Structural Concurrency (Anyio TaskGroup)
The agent itself runs as a persistent, structured background service.

```python
async def supervisor_loop():
    async with anyio.create_task_group() as tg:
        tg.start_soon(log_monitor_agent)
        tg.start_soon(metric_observer_agent)
        tg.start_soon(auto_healer_agent)
```

## 3. Capabilities (2026 Features)

### 3.1 Self-Healing (자동 치유)
- **Scenario**: `DTZ005` error detected in CI.
- **Action**: Agent parses error, identifies `datetime.now()`, inserts `import timezone`, and replaces with `datetime.now(timezone.utc)`.
- **Validation**: Re-runs `ruff check` to confirm fix.

### 3.2 Predictive Debugging (예지)
- Analyzing trends in `sentry_sdk` events to predict upcoming failures (e.g., "Memory usage increasing 5% per hour -> OOM in 4 hours").

### 3.3 Context-Aware Explanation
- When reporting to the Commander, it references the specific *Concept* (Truth/Goodness/Beauty) violated, not just the code error.

## 4. Implementation Plan (Prototype)

We will implement `packages/afo-core/services/debugging_agent.py` which:
1. Connects to **Sentry** and **Prometheus**.
2. Monitors **Anyio TaskGroups** via `@instrument_task`.
3. Uses a **LangGraph** workflow to Reason and Act on errors.

---

> **"The best debugger is one that fixes the bug before you see it."**
