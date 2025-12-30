# Failure Mode Matrix

> **As-of: 2025-12-29 | Version: v1.1**
> **眞善美孝영** - 하드 컨트랙트 실패 시 규정 및 대응 전략

## 개요

Chancellor Graph V2의 하드 컨트랙트(Context7, Sequential Thinking) 실패 시 동작 규정 및 대응 전략을 정의합니다.

---

## 실패 모드 분류

### 1. Context7 실패

#### 실패 시나리오

| 시나리오 | 원인 | 영향 범위 | 대응 전략 |
|---------|------|----------|----------|
| MCP 서버 연결 실패 | Context7 MCP 서버 다운 | 전체 실행 중단 | **BLOCK** - 실행 즉시 중단 |
| `get-library-docs` 실패 | MCP 도구 호출 실패 | 해당 노드 컨텍스트 주입 실패 | **BLOCK** - 실행 즉시 중단 |
| 지식 베이스 로드 실패 | Metadata 파일 없음/손상 | 초기화 실패 | **BLOCK** - 실행 즉시 중단 |
| 검색 결과 없음 | 쿼리 매칭 실패 | 컨텍스트 부족 | **DEGRADED** - 경고 후 계속 진행 |

#### 대응 규정

```python
# Context7 실패 시 동작 (api/chancellor_v2/context7.py)

def _call_context7_docs(library_id: str, topic: str) -> dict[str, Any]:
    """Call MCP get-library-docs for actual knowledge injection.
    
    Contract: If MCP fails for any reason, raises RuntimeError.
    NO BYPASS. NO DISABLED MODE.
    """
    # 실패 시 RuntimeError 발생 → 실행 중단
    if "error" in resp:
        raise RuntimeError(f"MCP Context7 get-library-docs failed: {resp['error']}")
```

**규정**:
- **BLOCK**: MCP 실패 시 즉시 `RuntimeError` 발생, 실행 중단
- **RETRY**: 자동 재시도 없음 (하드 컨트랙트)
- **DEGRADED**: 검색 결과 없음은 경고만, 실행 계속

---

### 2. Sequential Thinking 실패

#### 실패 시나리오

| 시나리오 | 원인 | 영향 범위 | 대응 전략 |
|---------|------|----------|----------|
| MCP 서버 연결 실패 | Sequential Thinking MCP 서버 다운 | 전체 실행 중단 | **BLOCK** - 실행 즉시 중단 |
| `sequentialthinking` 도구 실패 | MCP 도구 호출 실패 | 해당 노드 사고 처리 실패 | **BLOCK** - 실행 즉시 중단 |
| 사고 처리 타임아웃 | 응답 지연 | 해당 노드 사고 처리 실패 | **BLOCK** - 실행 즉시 중단 |

#### 대응 규정

```python
# Sequential Thinking 실패 시 동작 (api/chancellor_v2/thinking.py)

def _call_sequential_thinking(...) -> dict[str, Any]:
    """Call MCP sequential_thinking tool.
    
    Contract: If MCP fails for any reason, raises RuntimeError.
    NO BYPASS. NO PASSTHROUGH.
    """
    # 실패 시 RuntimeError 발생 → 실행 중단
    if "error" in resp:
        raise RuntimeError(f"MCP sequential_thinking failed: {resp['error']}")
```

**규정**:
- **BLOCK**: MCP 실패 시 즉시 `RuntimeError` 발생, 실행 중단
- **RETRY**: 자동 재시도 없음 (하드 컨트랙트)
- **DEGRADED**: 없음 (모든 실패는 BLOCK)

---

### 3. Skills Allowlist 실패

#### 실패 시나리오

| 시나리오 | 원인 | 영향 범위 | 대응 전략 |
|---------|------|----------|----------|
| Skill이 Allowlist에 없음 | 보안 정책 위반 | EXECUTE 노드만 차단 | **BLOCKED** - 해당 Skill만 차단, 실행 계속 |
| Allowlist 검증 실패 | Guard 로직 오류 | EXECUTE 노드만 차단 | **BLOCKED** - 해당 Skill만 차단, 실행 계속 |

#### 대응 규정

```python
# Skills Allowlist 실패 시 동작 (api/chancellor_v2/graph/nodes/execute_node.py)

async def execute_node(state: GraphState) -> GraphState:
    # Stage 2 Allowlist Enforcement
    allowed, reason = is_skill_allowed(skill_id)
    if not allowed:
        state.errors.append(f"EXECUTE blocked: {reason}")
        state.outputs["EXECUTE"] = {"status": "blocked", "reason": reason}
        return state  # 실행 계속 (Skill만 차단)
```

**규정**:
- **BLOCKED**: Skill만 차단, 실행은 계속 (VERIFY에서 검증)
- **RETRY**: 없음
- **DEGRADED**: 없음

---

### 4. VERIFY 실패

#### 실패 시나리오

| 시나리오 | 원인 | 영향 범위 | 대응 전략 |
|---------|------|----------|----------|
| 에러 누적 | 이전 노드에서 에러 발생 | 전체 검증 실패 | **FAIL** - 자동 롤백 트리거 |
| EXECUTE 상태 실패 | Skill 실행 실패/차단 | 전체 검증 실패 | **FAIL** - 자동 롤백 트리거 |
| 3책사 출력 누락 | TRUTH/GOODNESS/BEAUTY 중 하나 이상 누락 | 전체 검증 실패 | **FAIL** - 자동 롤백 트리거 |

#### 대응 규정

```python
# VERIFY 실패 시 동작 (api/chancellor_v2/graph/nodes/verify_node.py)

def verify_node(state: GraphState) -> GraphState:
    issues: list[str] = []
    
    # 검증 항목 확인
    if state.errors:
        issues.append(f"Errors present: {len(state.errors)}")
    if execute_status not in ("success", "skip"):
        issues.append(f"EXECUTE status: {execute_status}")
    for strategist in ("TRUTH", "GOODNESS", "BEAUTY"):
        if strategist not in state.outputs:
            issues.append(f"Missing {strategist} output")
    
    # FAIL 판정
    if issues:
        state.outputs["VERIFY"] = {
            "status": "fail",
            "issues": issues,
        }
        # 자동 롤백 트리거 (다음 단계)
```

**규정**:
- **FAIL**: 검증 실패 시 `status: "fail"` 설정
- **ROLLBACK**: 자동 롤백 트리거 (ROLLBACK 노드 실행)
- **ALERT**: 운영자 알림 (Prometheus 메트릭)

---

### 5. 롤백 처리

#### 롤백 시나리오

| 시나리오 | 원인 | 영향 범위 | 대응 전략 |
|---------|------|----------|----------|
| VERIFY 실패 | 검증 실패 | 전체 실행 실패 | **ROLLBACK** - 안전한 체크포인트로 복원 |
| 안전한 체크포인트 없음 | 모든 체크포인트 손상/없음 | 롤백 불가 | **ERROR** - 수동 개입 필요 |

#### 대응 규정

```python
# 롤백 처리 (api/chancellor_v2/graph/nodes/rollback_node.py)

SAFE_ROLLBACK_STEPS = ["MERGE", "BEAUTY", "GOODNESS", "TRUTH", "PARSE", "CMD"]

def rollback_node(state: GraphState) -> GraphState:
    verify_result = state.outputs.get("VERIFY", {})
    if verify_result.get("status") != "fail":
        return state  # 롤백 불필요
    
    # 안전한 체크포인트 찾기
    checkpoints = list_checkpoints(state.trace_id)
    # ... 복원 로직
```

---

## 실패 모드 매트릭스 요약

| 컴포넌트 | 실패 유형 | 대응 전략 | 자동 재시도 | 알림 |
|---------|----------|----------|------------|------|
| Context7 | MCP 연결 실패 | **BLOCK** | ❌ 없음 | ✅ Prometheus |
| Context7 | 검색 결과 없음 | **DEGRADED** | ❌ 없음 | ⚠️ 경고만 |
| Sequential Thinking | MCP 연결 실패 | **BLOCK** | ❌ 없음 | ✅ Prometheus |
| Skills | Allowlist 차단 | **BLOCKED** | ❌ 없음 | ✅ Prometheus |
| VERIFY | 검증 실패 | **FAIL** → **ROLLBACK** | ✅ 자동 롤백 | ✅ Prometheus |
| ROLLBACK | 체크포인트 없음 | **ERROR** | ❌ 없음 | ✅ 긴급 알림 |

---

## 참고 자료

- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md) | [Local](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)
- [Context7 완벽 활용 가이드](./CONTEXT7_COMPLETE_USAGE_GUIDE.md) | [Local](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CONTEXT7_COMPLETE_USAGE_GUIDE.md)
- [Sequential Thinking 완벽 활용 가이드](./SEQUENTIAL_THINKING_COMPLETE_USAGE_GUIDE.md) | [Local](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SEQUENTIAL_THINKING_COMPLETE_USAGE_GUIDE.md)
- [Skills 완벽 활용 가이드](./SKILLS_COMPLETE_USAGE_GUIDE.md) | [Local](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SKILLS_COMPLETE_USAGE_GUIDE.md)

---

**Trinity Score**: 眞 95% | 善 100% | 美 90% | 孝 95% | 永 100%
