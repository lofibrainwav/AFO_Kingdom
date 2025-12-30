# Chancellor Graph V2 완전 가이드

> **眞善美孝永** - Context7 + Sequential Thinking + Skills 완벽 통합

> **⚠️ 중요**: 
> - 모든 import 경로는 [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) 문서를 참조하세요.
> - 실패 시 규정은 [Failure Mode Matrix](./FAILURE_MODE_MATRIX.md)를 참조하세요.
> - 데이터 계약은 [GraphState Contract](./GRAPH_STATE_CONTRACT.md)를 참조하세요.

## 목차

1. [개요](#개요)
2. [아키텍처](#아키텍처)
3. [실행 흐름](#실행-흐름)
4. [노드 상세](#노드-상세)
5. [통합 활용](#통합-활용)
6. [커스텀 워크플로우](#커스텀-워크플로우)
7. [체크포인트 및 롤백](#체크포인트-및-롤백)
8. [관찰 가능성](#관찰-가능성)
9. [실전 예제](#실전-예제)
10. [트러블슈팅](#트러블슈팅)

---

## 개요

Chancellor Graph V2는 AFO 왕국의 **핵심 오케스트레이션 엔진**입니다. Context7, Sequential Thinking, 그리고 Skills를 **하드 컨트랙트**로 통합하여, 모든 실행이 최신 지식 기반과 단계별 사고 프로세스를 거치도록 보장합니다.

### 핵심 특징

- ✅ **하드 컨트랙트**: Context7과 Sequential Thinking은 필수, 우회 불가
- ✅ **자동 통합**: 별도 설정 없이 모든 기능 자동 적용
- ✅ **체크포인트 시스템**: 각 단계별 상태 저장 및 롤백 지원
- ✅ **관찰 가능성**: 모든 실행 추적 및 메트릭 수집
- ✅ **Stage 2 Allowlist**: 보안 게이트 강제

---

## 아키텍처

### 전체 구조

```
┌─────────────────────────────────────────────────┐
│  Chancellor Graph V2 Runner                     │
│  - run_v2(input_payload, nodes)                 │
│  - 하드 컨트랙트 강제                            │
└──────────────┬──────────────────────────────────┘
               │
               ├─── Kingdom DNA 주입 (트레이스 시작)
               │    → inject_kingdom_dna(state)
               │
               └─── 각 노드 실행 루프
                    │
                    ├─── Sequential Thinking 적용
                    │    → apply_sequential_thinking(state, step)
                    │
                    ├─── Context7 컨텍스트 주입
                    │    → inject_context(state, step)
                    │
                    └─── 노드 실행
                         → fn(state)
```

### 노드 실행 순서

```
ORDER = [
    "CMD",      # 명령 수신
    "PARSE",    # 명령 파싱
    "TRUTH",    # 제갈량 (眞) - 기술적 검증
    "GOODNESS", # 사마의 (善) - 윤리/보안 검토
    "BEAUTY",   # 주유 (美) - UX/미학 평가
    "MERGE",    # 3책사 종합
    "EXECUTE",  # Skills 실행
    "VERIFY",   # 결과 검증
    "REPORT",   # 최종 보고
]
```

### 파일 구조

```
packages/afo-core/api/chancellor_v2/
├── graph/
│   ├── runner.py              # 메인 실행 엔진
│   ├── state.py                # GraphState 정의
│   ├── store.py                # 체크포인트/이벤트 저장
│   └── nodes/
│       ├── execute_node.py     # Skills 실행
│       ├── verify_node.py      # 결과 검증
│       └── rollback_node.py    # 롤백 처리
├── context7.py                 # Context7 통합
├── thinking.py                 # Sequential Thinking 통합
├── metrics.py                  # Prometheus 메트릭
└── observability.py            # 추적 도구
```

---

## 실행 흐름

### 기본 실행

```python
# ✅ 공식 경로 (SSOT Import Path)
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import (
    cmd_node,
    parse_node,
    truth_node,
    goodness_node,
    beauty_node,
    merge_node,
    execute_node,
    verify_node,
    report_node,
)

# 입력 페이로드
input_payload = {
    "command": "YouTube 스펙 생성",
    "skill_id": "skill_001_youtube_spec_gen",
    "parameters": {
        "youtube_url": "https://www.youtube.com/watch?v=..."
    }
}

# 노드 정의
nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,
    "GOODNESS": goodness_node,
    "BEAUTY": beauty_node,
    "MERGE": merge_node,
    "EXECUTE": execute_node,
    "VERIFY": verify_node,
    "REPORT": report_node,
}

# 실행 (Context7 + Sequential Thinking 자동 적용)
state = run_v2(input_payload, nodes)

# 결과 확인
print(f"Trace ID: {state.trace_id}")
print(f"Errors: {state.errors}")
print(f"Outputs: {list(state.outputs.keys())}")
```

### 자동 적용되는 기능

1. **Kingdom DNA 주입** (트레이스 시작 시)
   ```python
   state.outputs["context7"]["KINGDOM_DNA"] = {
       "library_id": "/langchain-ai/langgraphjs",
       "topic": "state management checkpoint workflow agent patterns",
       "context": "...",
       "injected": True
   }
   ```

2. **Sequential Thinking** (각 노드 실행 전)
   ```python
   state.outputs["sequential_thinking"][step] = {
       "thought_processed": "...",
       "step": "1/1",
       "progress": 1.0,
       "metadata": {
           "truth_impact": 0.85,
           "serenity_impact": 0.90
       }
   }
   ```

3. **Context7 컨텍스트** (각 노드 실행 전)
   ```python
   state.outputs["context7"][step] = {
       "library_id": "/python/python",
       "topic": "type checking",
       "context": "...",
       "length": 500
   }
   ```

---

## 노드 상세

### CMD 노드

**역할**: 명령 수신 및 초기 검증

**입력**: `state.input`

**출력**: `state.outputs["CMD"]`

**자동 적용**:
- Sequential Thinking: "Command received: {input}"
- Context7: 일반 컨텍스트

### PARSE 노드

**역할**: 명령 파싱 및 실행 계획 수립

**입력**: `state.input`

**출력**: `state.plan` (skill_id, parameters, timeout 등)

**자동 적용**:
- Sequential Thinking: "Parsing commander request: {input}"
- Context7: langchain, agents

### TRUTH 노드 (제갈량 - 眞)

**역할**: 기술적 타당성 검증

**입력**: `state.plan`

**출력**: `state.outputs["TRUTH"]` (기술적 평가 결과)

**자동 적용**:
- Sequential Thinking: "Evaluating technical truth for: {skill_id}"
- Context7: python, type checking

### GOODNESS 노드 (사마의 - 善)

**역할**: 윤리/보안/리스크 검토

**입력**: `state.plan`

**출력**: `state.outputs["GOODNESS"]` (윤리적 평가 결과)

**자동 적용**:
- Sequential Thinking: "Checking ethical/security aspects for: {skill_id}"
- Context7: fastapi, security

### BEAUTY 노드 (주유 - 美)

**역할**: UX/미학적 영향 평가

**입력**: `state.plan`

**출력**: `state.outputs["BEAUTY"]` (미학적 평가 결과)

**자동 적용**:
- Sequential Thinking: "Assessing UX/aesthetic impact for: {skill_id}"
- Context7: react, components

### MERGE 노드

**역할**: 3책사 결과 종합

**입력**: `state.outputs["TRUTH"]`, `state.outputs["GOODNESS"]`, `state.outputs["BEAUTY"]`

**출력**: `state.outputs["MERGE"]` (종합 평가 및 Trinity Score)

**자동 적용**:
- Sequential Thinking: "Synthesizing 3 strategists: T={truth}, G={goodness}, B={beauty}"
- Context7: langchain, chains

### EXECUTE 노드

**역할**: Skills 실행

**입력**: `state.plan["skill_id"]`, `state.plan["parameters"]`

**출력**: `state.outputs["EXECUTE"]` (실행 결과)

**자동 적용**:
- Sequential Thinking: "Preparing execution for: {skill_id}"
- Context7: langchain, tools
- **Stage 2 Allowlist 검증**: `is_skill_allowed(skill_id)`

**실행 로직**:
```python
# 1. Allowlist 검증
allowed, reason = is_skill_allowed(skill_id)
if not allowed:
    state.outputs["EXECUTE"] = {"status": "blocked", "reason": reason}
    return state

# 2. Skill 실행
result = await registry.execute_skill(
    skill_id=skill_id,
    parameters=parameters,
    timeout_seconds=timeout
)

# 3. 결과 저장
state.outputs["EXECUTE"] = {
    "status": "success",
    "skill_id": skill_id,
    "result": result
}
```

### VERIFY 노드

**역할**: 실행 결과 검증

**입력**: `state.outputs`, `state.errors`

**출력**: `state.outputs["VERIFY"]` (pass/fail)

**검증 항목**:
1. 에러 없음 (`state.errors` 비어있음)
2. EXECUTE 상태가 "success" 또는 "skip"
3. 3책사 모두 출력 생성 (TRUTH, GOODNESS, BEAUTY)

**자동 적용**:
- Sequential Thinking: "Verifying execution results: errors={count}"
- Context7: pytest, testing

### REPORT 노드

**역할**: 최종 보고서 생성

**입력**: 전체 `state`

**출력**: `state.outputs["REPORT"]` (최종 보고서)

---

## 통합 활용

### 패턴 1: 기본 실행 (권장)

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

# 모든 것이 자동으로 통합됨
state = run_v2(input_payload, nodes)

# 결과 확인
print("=== Context7 주입 ===")
for step, context in state.outputs.get("context7", {}).items():
    print(f"{step}: {context.get('context', '')[:100]}...")

print("\n=== Sequential Thinking ===")
for step, thinking in state.outputs.get("sequential_thinking", {}).items():
    print(f"{step}: {thinking.get('thought_processed', '')[:100]}...")

print("\n=== Skill 실행 ===")
execute = state.outputs.get("EXECUTE", {})
print(f"Status: {execute.get('status')}")
print(f"Result: {execute.get('result', {})}")
```

### 패턴 2: 커스텀 노드 작성

```python
def custom_node(state: GraphState) -> GraphState:
    """커스텀 노드 예제"""
    
    # Context7 컨텍스트 활용
    context = state.outputs.get("context7", {}).get("TRUTH", {})
    knowledge = context.get("context", "")
    
    # Sequential Thinking 결과 활용
    thinking = state.outputs.get("sequential_thinking", {}).get("TRUTH", {})
    thought = thinking.get("thought_processed", "")
    
    # 커스텀 로직 실행
    result = {
        "custom_analysis": "Custom analysis result",
        "knowledge_used": knowledge[:200],
        "thought": thought
    }
    
    state.outputs["CUSTOM"] = result
    return state

# 커스텀 노드 사용
nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,
    "CUSTOM": custom_node,  # 커스텀 노드 추가
    "EXECUTE": execute_node,
    "VERIFY": verify_node,
    "REPORT": report_node,
}
```

### 패턴 3: 조건부 실행

```python
def conditional_execute_node(state: GraphState) -> GraphState:
    """조건부 실행 노드"""
    
    # MERGE 결과 확인
    merge_result = state.outputs.get("MERGE", {})
    trinity_score = merge_result.get("trinity_score", 0)
    
    # Trinity Score가 90 이상일 때만 실행
    if trinity_score >= 90:
        return execute_node(state)
    else:
        state.outputs["EXECUTE"] = {
            "status": "skipped",
            "reason": f"Trinity Score {trinity_score} < 90"
        }
        return state

# 조건부 실행 노드 사용
nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,
    "GOODNESS": goodness_node,
    "BEAUTY": beauty_node,
    "MERGE": merge_node,
    "EXECUTE": conditional_execute_node,  # 조건부 실행
    "VERIFY": verify_node,
    "REPORT": report_node,
}
```

---

## 커스텀 워크플로우

### 워크플로우 1: 간소화된 실행

```python
# 필수 노드만 포함
nodes = {
    "PARSE": parse_node,
    "EXECUTE": execute_node,
    "VERIFY": verify_node,
}

state = run_v2(input_payload, nodes)
# Context7 + Sequential Thinking은 여전히 자동 적용됨
```

### 워크플로우 2: 확장된 검증

```python
def extended_verify_node(state: GraphState) -> GraphState:
    """확장된 검증 노드"""
    
    # 기본 검증
    state = verify_node(state)
    
    # 추가 검증
    if state.outputs.get("VERIFY", {}).get("status") == "pass":
        # Context7 주입 품질 검증
        context7_quality = len(state.outputs.get("context7", {}))
        if context7_quality < 5:
            state.outputs["VERIFY"]["status"] = "fail"
            state.outputs["VERIFY"]["issues"].append("Insufficient Context7 injection")
    
    return state

# 확장된 검증 사용
nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,
    "GOODNESS": goodness_node,
    "BEAUTY": beauty_node,
    "MERGE": merge_node,
    "EXECUTE": execute_node,
    "VERIFY": extended_verify_node,  # 확장된 검증
    "REPORT": report_node,
}
```

---

## 체크포인트 및 롤백

### 체크포인트 시스템

각 노드 실행 후 자동으로 체크포인트가 저장됩니다:

```python
# 체크포인트 로드
from api.chancellor_v2.graph.store import load_checkpoint, list_checkpoints

# 특정 단계 체크포인트 로드
checkpoint = load_checkpoint(trace_id, "MERGE")
if checkpoint:
    print(f"Plan: {checkpoint['plan']}")
    print(f"Outputs: {checkpoint['outputs']}")

# 모든 체크포인트 목록
checkpoints = list_checkpoints(trace_id)
print(f"Available checkpoints: {checkpoints}")
```

### 롤백 처리

VERIFY 실패 시 자동 롤백:

```python
from api.chancellor_v2.graph.nodes import rollback_node

# VERIFY 실패 후 롤백
if state.outputs.get("VERIFY", {}).get("status") == "fail":
    state = rollback_node(state)
    
    rollback_result = state.outputs.get("ROLLBACK", {})
    if rollback_result.get("status") == "success":
        print(f"✅ 롤백 성공: {rollback_result['restored_from']}에서 복원")
    else:
        print(f"❌ 롤백 실패: {rollback_result.get('reason')}")
```

### 안전한 롤백 지점

다음 단계들은 안전한 롤백 지점으로 간주됩니다:

```python
SAFE_ROLLBACK_STEPS = [
    "MERGE",    # 3책사 종합 후
    "BEAUTY",   # 미학 평가 후
    "GOODNESS", # 윤리 검토 후
    "TRUTH",    # 기술 검증 후
    "PARSE",    # 파싱 후
    "CMD",      # 명령 수신 후
]
```

---

## 관찰 가능성

### 이벤트 추적

```python
from api.chancellor_v2.observability import (
    list_traces,
    get_trace_events,
    format_trace_timeline,
    format_trace_summary
)

# 모든 트레이스 목록
traces = list_traces()
print(f"Total traces: {len(traces)}")

# 특정 트레이스 이벤트
events = get_trace_events(trace_id)
for event in events:
    print(f"{event['step']}: {event['event']} ({'✅' if event['ok'] else '❌'})")

# 타임라인 포맷
timeline = format_trace_timeline(trace_id)
print(timeline)

# 요약 포맷
summary = format_trace_summary(trace_id)
print(summary)
```

### 메트릭 수집

```python
from api.chancellor_v2.metrics import (
    chancellor_v2_trace_created_total,
    chancellor_v2_verify_pass_total,
    chancellor_v2_verify_fail_total,
    chancellor_v2_execute_success_total,
    update_artifact_metrics
)

# 메트릭 업데이트
update_artifact_metrics()

# 메트릭 확인 (Prometheus가 설정된 경우)
# http://localhost:9090/metrics 에서 확인 가능
```

---

## 실전 예제

### 예제 1: YouTube 스펙 생성 (완전 통합)

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

input_payload = {
    "command": "YouTube 스펙 생성",
    "skill_id": "skill_001_youtube_spec_gen",
    "parameters": {
        "youtube_url": "https://www.youtube.com/watch?v=..."
    }
}

nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,
    "GOODNESS": goodness_node,
    "BEAUTY": beauty_node,
    "MERGE": merge_node,
    "EXECUTE": execute_node,
    "VERIFY": verify_node,
    "REPORT": report_node,
}

state = run_v2(input_payload, nodes)

# 전체 결과 확인
print("=== Kingdom DNA ===")
print(state.outputs["context7"]["KINGDOM_DNA"]["context"][:200])

print("\n=== Sequential Thinking ===")
for step, thinking in state.outputs["sequential_thinking"].items():
    print(f"{step}: Truth={thinking['metadata']['truth_impact']:.2f}")

print("\n=== Context7 주입 ===")
for step, context in state.outputs["context7"].items():
    if step != "KINGDOM_DNA":
        print(f"{step}: {context['context'][:100]}...")

print("\n=== Skill 실행 ===")
execute = state.outputs["EXECUTE"]
print(f"Status: {execute['status']}")
print(f"Result: {execute.get('result', {})}")

print("\n=== 검증 ===")
verify = state.outputs["VERIFY"]
print(f"Status: {verify['status']}")
if verify['status'] == "fail":
    print(f"Issues: {verify['issues']}")
```

### 예제 2: RAG 시스템 구축

```python
input_payload = {
    "command": "RAG 시스템 구축",
    "skill_id": "skill_002_ultimate_rag",
    "parameters": {
        "query": "FastAPI 보안 best practices",
        "top_k": 5
    }
}

state = run_v2(input_payload, nodes)

# RAG 결과 확인
execute_result = state.outputs["EXECUTE"]["result"]
documents = execute_result.get("documents", [])
print(f"✅ {len(documents)}개 문서 검색 완료")
```

### 예제 3: 디버깅 자동화

```python
input_payload = {
    "command": "자동 디버깅",
    "skill_id": "skill_013_automated_debugging",
    "parameters": {
        "error_log": "...",
        "code_path": "packages/afo-core/api/routes/..."
    }
}

state = run_v2(input_payload, nodes)

# 디버깅 결과 확인
debug_result = state.outputs["EXECUTE"]["result"]
print(f"✅ 디버깅 완료: {debug_result.get('fixes_applied', 0)}개 수정")
```

---

## 트러블슈팅

### 문제 1: Context7 실패로 실행 중단

**증상**: `RuntimeError: MCP Context7 get-library-docs failed`

**해결**:
1. MCP 서버 상태 확인:
   ```bash
   cat .cursor/mcp.json | grep context7
   ```

2. MCP 서버 재시작:
   - Cursor IDE 재시작
   - MCP 서버 로그 확인

### 문제 2: Sequential Thinking 실패로 실행 중단

**증상**: `RuntimeError: MCP sequential_thinking failed`

**해결**:
1. MCP 서버 상태 확인:
   ```bash
   cat .cursor/mcp.json | grep sequential-thinking
   ```

2. MCP 서버 재시작

### 문제 3: VERIFY 실패

**증상**: `state.outputs["VERIFY"]["status"] == "fail"`

**해결**:
1. 이슈 확인:
   ```python
   issues = state.outputs["VERIFY"]["issues"]
   print(f"Issues: {issues}")
   ```

2. 롤백:
   ```python
   from api.chancellor_v2.graph.nodes import rollback_node
   state = rollback_node(state)
   ```

3. 문제 해결 후 재실행

### 문제 4: EXECUTE 차단

**증상**: `state.outputs["EXECUTE"]["status"] == "blocked"`

**해결**:
1. 차단 사유 확인:
   ```python
   reason = state.outputs["EXECUTE"]["reason"]
   print(f"Blocked: {reason}")
   ```

2. Allowlist 확인:
   ```python
   from api.guards.skills_allowlist_guard import is_skill_allowed
   allowed, reason = is_skill_allowed(skill_id)
   ```

3. Allowlist에 스킬 추가 (필요 시)

---

## 최적화 팁

### 1. 체크포인트 활용

불필요한 재실행을 방지하기 위해 체크포인트를 활용:

```python
# 이전 체크포인트 확인
checkpoint = load_checkpoint(trace_id, "MERGE")
if checkpoint and checkpoint.get("outputs", {}).get("MERGE", {}).get("trinity_score", 0) >= 90:
    # 이전 결과 재사용 가능
    pass
```

### 2. 이벤트 로그 분석

이벤트 로그를 분석하여 병목 지점 파악:

```python
events = get_trace_events(trace_id)
for i, event in enumerate(events[1:], 1):
    prev_event = events[i-1]
    duration = event["ts"] - prev_event["ts"]
    if duration > 1.0:  # 1초 이상 소요
        print(f"⚠️ Slow step: {prev_event['step']} → {event['step']} ({duration:.2f}s)")
```

### 문제 3: 메트릭 모니터링

Prometheus 메트릭을 모니터링하여 시스템 건강도 추적:

```python
from api.chancellor_v2.metrics import update_artifact_metrics

# 주기적으로 메트릭 업데이트
update_artifact_metrics()
```

---

## 참고 자료

- [Chancellor Graph V2 Runner](../packages/afo-core/api/chancellor_v2/graph/runner.py)
- [Context7 통합](../packages/afo-core/api/chancellor_v2/context7.py)
- [Sequential Thinking 통합](../packages/afo-core/api/chancellor_v2/thinking.py)
- [EXECUTE 노드](../packages/afo-core/api/chancellor_v2/graph/nodes/execute_node.py)
- [VERIFY 노드](../packages/afo-core/api/chancellor_v2/graph/nodes/verify_node.py)
- [관찰 가능성 도구](../packages/afo-core/api/chancellor_v2/observability.py)

---

**작성일**: 2025-12-25  
**버전**: 1.0.0  
**Trinity Score**: 眞 95% | 善 90% | 美 90% | 孝 95% | 永 90%

