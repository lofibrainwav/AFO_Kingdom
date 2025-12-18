# TRINITY Graph Toolflow v1 — Search → Card → Gate → (DryRun?) → Execute

## Scope
- 목적: MCP의 **Tool Search + Programmatic Calling** 흐름을 AFO에 **컨텍스트 절약형**으로 이식
- 원칙: **점수/판정 새로 만들지 않음**  
  - Skills Registry / Serenity Gate / Proxy는 기존 SSOT를 그대로 호출
- 종료 상태: AUTO_RUN 실행 결과 / ASK 승인 패킷 / BLOCK 사유 카드

---

## I/O Contract

### Input
- `user_prompt: string`
- `top_k: int` (default 5)
- (optional) `query: string` (default = user_prompt)

### Output (one of)
- `result_card` (AUTO_RUN executed)
- `approval_packet` (ASK)
- `block_card` (BLOCK)
- `no_candidates_card` (검색 결과 없음)

---

## State Schema (minimal)

```yaml
state:
  user_prompt: str
  query: str
  top_k: int
  candidates: list[Candidate]
  selected_skill_id: str
  skill_card: dict
  decision: "AUTO_RUN" | "ASK" | "BLOCK"
  dry_run_supported: bool
  dry_run_result: dict
  exec_result: dict
  approval_packet: dict
  final_card: dict

Candidate:
  skill_id: str
  title: str
  score_hint: float | null
  tags: list[str] | null
  reason: str | null
```

---

## Nodes (thin layer)

1) **TOOL_SEARCH**
- call: `tool_search(query, top_k)`
- out: `candidates[]`

2) **SELECT**
- rule:
  - `candidates == []` → `FINAL_NO_CANDIDATES`
  - else pick `candidates[0]` as default
  - ambiguity guard(권장): top2가 비슷하거나 프롬프트가 모호하면 `decision="ASK"`

3) **GET_CARD**
- call: `get_skill_card(selected_skill_id)`
- out: `skill_card`

4) **SERENITY_GATE**
- call: `serenity_gate_existing({user_prompt, skill_card})`
- out: `decision ∈ {AUTO_RUN, ASK, BLOCK}`

5) **DRY_RUN (optional)**
- call: `execute_skill_proxy(skill_id, {mode:"dry_run", args: from_skill_card})`
- out: `dry_run_result`
- set: `dry_run_supported = true/false`

6) **EXECUTE**
- call: `execute_skill_proxy(skill_id, {mode:"execute", args: from_skill_card})`
- out: `exec_result`

7) **ASK**
- build: `approval_packet`

8) **FINAL**
- build: `final_card` (status + next_actions)

---

## Edges / Routing (deterministic)

```
ENTRY → TOOL_SEARCH → SELECT → GET_CARD → SERENITY_GATE
```

**SERENITY_GATE 분기**
- `decision == "BLOCK"` → `FINAL_BLOCK`
- `decision == "ASK"`   → `ASK` → END
- `decision == "AUTO_RUN"`:
  - `dry_run_supported` → `DRY_RUN` → `EXECUTE` → `FINAL_OK` → END
  - else               → `EXECUTE` → `FINAL_OK` → END

---

## Approval Packet Schema (ASK)

```yaml
approval_packet:
  skill_id: str
  title: str
  why_this: str
  required_inputs: dict
  proposed_args: dict
  risk_notes: list[str]
  rollback: str
  choices:
    - "Approve & Execute"
    - "Edit Inputs"
    - "Cancel"
```

---

## Final Cards (compact)

```yaml
FINAL_OK:
  status: "OK"
  skill_id: str
  summary: str
  next_actions:
    - "Run another tool_search"
    - "Save to SSOT"
    - "Open logs"

FINAL_BLOCK:
  status: "BLOCK"
  reason: str
  next_actions:
    - "Revise prompt"
    - "Run tool_search with tighter query"

FINAL_NO_CANDIDATES:
  status: "NO_CANDIDATES"
  next_actions:
    - "Try different keywords"
    - "Increase top_k"
```

---

## Non‑negotiables (AFO Gate Discipline)
- “Backup → Check → Execute → Verify” 루프는 **`execute_skill_proxy` 내부 표준**을 그대로 따른다.
- 이 그래프는 **조립/분기만 담당**한다. (점수/판정은 기존 컴포넌트가 담당)

---

## Serenity Gate Adapter (SSOT 인용 규칙)

`serenity_gate_existing`은 **새 점수/판정을 발명하지 않고**, 기존 SSOT의 근거만 인용해 결정을 내린다.

1. **Force Override (테스트 전용)**
   - 환경변수 `TRINITY_TOOLFLOW_FORCE_DECISION ∈ {AUTO_RUN, ASK, BLOCK}`가 있으면 그 값으로 즉시 결정한다.

2. **기존 Serenity Gate 우선 호출**
   - AFO 내부의 게이트 함수가 import 가능하고 `decision/mode`를 반환하면 그 결과를 그대로 사용한다.

3. **Quantum Balance Lock Fallback**
   - 위 게이트가 없을 때만, `afo_soul_engine.core.quantum_balance_lock.get_gate_verdict / should_auto_run`을 사용한다.
   - 총점 근거는 `logs/trinity_health_*.json` 최신 파일의 `overall_trinity_score`를 읽어 **인용**한다.

4. **Health First (스코어 신선도)**
   - 스코어가 오래되면 AUTO_RUN 근거로 쓰지 않는다.
   - `TRINITY_TOOLFLOW_MAX_SCORE_AGE_MINUTES` (기본 60분) 초과 시 **ASK로 전환**한다.

5. **Risk Unknown 기본값**
   - SSOT에서 `risk_score`가 넘어오지 않으면 unknown으로 보고 AUTO_RUN을 금지한다.
   - 결과적으로 `gate_status=OK`라도 기본 결정은 ASK이며, Commander 승인 후에만 실행된다.

6. **CLI Risk Auto‑Injection (선택)**
   - `run_toolflow.py`는 `--risk-score`가 없을 때 `tools.guardian_sentinel.get_current_risk_score()`를
     **SSOT 근거로 인용**해 자동 주입할 수 있다.
   - `TRINITY_TOOLFLOW_DISABLE_AUTO_RISK=1`이면 이 자동 주입을 끄고 unknown→ASK 기본으로 돌아간다.
