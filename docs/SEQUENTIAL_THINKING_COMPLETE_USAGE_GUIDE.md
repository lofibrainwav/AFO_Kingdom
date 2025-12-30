# Sequential Thinking 완벽 활용 가이드

> **眞善美孝永** - AFO 왕국의 단계별 사고 방법론

> **⚠️ 중요**: 모든 import 경로는 [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) 문서를 참조하세요.

## 목차

1. [개요](#개요)
2. [아키텍처](#아키텍처)
3. [MCP 도구 사용법](#mcp-도구-사용법)
4. [Chancellor Graph V2 통합](#chancellor-graph-v2-통합)
5. [단계별 사고 프로세스 설계](#단계별-사고-프로세스-설계)
6. [커스터마이징](#커스터마이징)
7. [실전 예제](#실전-예제)
8. [트러블슈팅](#트러블슈팅)

---

## 개요

Sequential Thinking은 AFO 왕국의 **단계별 사고 방법론**을 구현한 MCP 도구입니다. 체계적인 문제 해결과 Trinity Score 기반 사고 품질 평가를 제공합니다.

### 핵심 특징

- ✅ **단계별 사고 기록**: 사고 과정을 체계적으로 관리
- ✅ **Trinity Score 평가**: 眞(Truth)과 孝(Serenity) 영향 평가
- ✅ **세션 기반 추적**: 세션별 사고 과정 추적
- ✅ **하드 컨트랙트**: Chancellor Graph V2에서 필수, 우회 불가

---

## 아키텍처

### 구성 요소

```
┌─────────────────────────────────────────┐
│  SequentialThinkingMCP (MCP 서버)       │
│  - 사고 처리 (process_thought)          │
│  - Truth/Serenity 평가                  │
│  - 사고 기록 저장                        │
│  - 세션 관리                             │
└──────────────┬──────────────────────────┘
               │
               ├─── MCP Stdio Client
               │    - JSON-RPC 2.0 통신
               │    - 도구 호출
               │
               └─── Chancellor Graph V2 통합
                    - 각 노드 실행 전 자동 적용
                    - 실패 시 실행 중단
```

### 파일 구조

```
packages/
├── trinity-os/
│   └── trinity_os/
│       └── servers/
│           └── sequential_thinking_mcp.py  # MCP 서버 구현
└── afo-core/
    └── api/
        └── chancellor_v2/
            └── thinking.py                 # Chancellor 통합
```

---

## MCP 도구 사용법

### 기본 사용

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.services.mcp_stdio_client import call_tool

# Sequential Thinking 호출
resp = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": "FastAPI 엔드포인트 보안 강화 방안 검토",
        "thoughtNumber": 1,
        "totalThoughts": 3,
        "nextThoughtNeeded": True,
    },
)

# 결과 확인
result = resp.get("result", {})
print(f"Processed: {result.get('thought_processed')}")
print(f"Progress: {result.get('progress')}")
print(f"Truth Impact: {result['metadata']['truth_impact']}")
print(f"Serenity Impact: {result['metadata']['serenity_impact']}")
```

### 다단계 사고 프로세스

```python
from AFO.services.mcp_stdio_client import call_tool

# 1단계: 문제 정의
step1 = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": "FastAPI 엔드포인트에 인증이 필요한지 분석",
        "thoughtNumber": 1,
        "totalThoughts": 5,
        "nextThoughtNeeded": True,
    },
)

# 2단계: 옵션 탐색
step2 = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": "JWT, OAuth2, API Key 중 적절한 인증 방식 선택",
        "thoughtNumber": 2,
        "totalThoughts": 5,
        "nextThoughtNeeded": True,
    },
)

# 3단계: 구현 계획
step3 = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": "FastAPI Security 모듈을 사용한 JWT 구현 계획",
        "thoughtNumber": 3,
        "totalThoughts": 5,
        "nextThoughtNeeded": True,
    },
)

# 4단계: 검증 계획
step4 = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": "인증 테스트 케이스 작성 및 보안 스캔 계획",
        "thoughtNumber": 4,
        "totalThoughts": 5,
        "nextThoughtNeeded": True,
    },
)

# 5단계: 최종 검토
step5 = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": "전체 프로세스 검토 및 최종 승인",
        "thoughtNumber": 5,
        "totalThoughts": 5,
        "nextThoughtNeeded": False,
    },
)

# 요약 확인
if "summary" in step5.get("result", {}):
    print(step5["result"]["summary"])
```

---

## Chancellor Graph V2 통합

### 자동 통합

Sequential Thinking은 Chancellor Graph V2에 **하드 컨트랙트**로 통합되어 있습니다. 각 노드 실행 전 자동으로 적용됩니다.

### 실행 흐름

```
각 노드 실행 전:
1. apply_sequential_thinking(state, step)
   → 단계별 사고 생성
   → MCP 도구 호출
   → 결과를 state.outputs에 저장

2. 노드 실행
   → 실제 로직 실행

3. 결과 확인
   → state.outputs["sequential_thinking"][step]
```

### 단계별 사고 생성

각 노드마다 자동으로 생성되는 사고:

- **PARSE**: "Parsing commander request: {input}"
- **TRUTH**: "Evaluating technical truth for: {skill_id}"
- **GOODNESS**: "Checking ethical/security aspects for: {skill_id}"
- **BEAUTY**: "Assessing UX/aesthetic impact for: {skill_id}"
- **MERGE**: "Synthesizing 3 strategists: T={truth}, G={goodness}, B={beauty}"
- **EXECUTE**: "Preparing execution for: {skill_id}"
- **VERIFY**: "Verifying execution results: errors={count}"

### 결과 확인

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

state = run_v2(input_payload, nodes)

# Sequential Thinking 결과 확인
for step, thinking_result in state.outputs.get("sequential_thinking", {}).items():
    print(f"Step: {step}")
    print(f"Thought: {thinking_result.get('thought_processed')}")
    print(f"Truth Impact: {thinking_result['metadata']['truth_impact']}")
    print(f"Serenity Impact: {thinking_result['metadata']['serenity_impact']}")
```

---

## 단계별 사고 프로세스 설계

### 패턴 1: 문제 해결 프로세스

```python
def solve_problem(problem: str) -> dict[str, Any]:
    """5단계 문제 해결 프로세스"""
    
    steps = [
        "문제 정의 및 범위 설정",
        "가능한 해결책 탐색",
        "최적 해결책 선택",
        "구현 계획 수립",
        "검증 및 최종 승인"
    ]
    
    results = []
    for i, step_description in enumerate(steps, 1):
        thought = f"[{step_description}] {problem}"
        result = call_tool(
            server_name="sequential-thinking",
            tool_name="sequentialthinking",
            arguments={
                "thought": thought,
                "thoughtNumber": i,
                "totalThoughts": len(steps),
                "nextThoughtNeeded": i < len(steps),
            },
        )
        results.append(result.get("result", {}))
    
    return {
        "problem": problem,
        "steps": results,
        "final_summary": results[-1].get("summary", "")
    }
```

### 패턴 2: 코드 리뷰 프로세스

```python
def review_code(code: str) -> dict[str, Any]:
    """코드 리뷰 4단계 프로세스"""
    
    steps = [
        ("구문 분석", "코드 구문 및 타입 검사"),
        ("로직 검증", "비즈니스 로직 정확성 검증"),
        ("보안 검토", "보안 취약점 및 리스크 검토"),
        ("품질 평가", "코드 품질 및 유지보수성 평가")
    ]
    
    results = []
    for i, (step_name, step_desc) in enumerate(steps, 1):
        thought = f"[{step_name}] {step_desc}\n\n코드:\n{code[:500]}"
        result = call_tool(
            server_name="sequential-thinking",
            tool_name="sequentialthinking",
            arguments={
                "thought": thought,
                "thoughtNumber": i,
                "totalThoughts": len(steps),
                "nextThoughtNeeded": i < len(steps),
            },
        )
        results.append({
            "step": step_name,
            "result": result.get("result", {})
        })
    
    return {
        "code_preview": code[:200],
        "review_steps": results
    }
```

### 패턴 3: 아키텍처 설계 프로세스

```python
def design_architecture(requirements: str) -> dict[str, Any]:
    """아키텍처 설계 6단계 프로세스"""
    
    steps = [
        "요구사항 분석 및 제약사항 파악",
        "아키텍처 패턴 선택",
        "컴포넌트 설계",
        "인터페이스 정의",
        "데이터 모델 설계",
        "배포 전략 수립"
    ]
    
    results = []
    for i, step in enumerate(steps, 1):
        thought = f"[{step}]\n\n요구사항:\n{requirements}"
        result = call_tool(
            server_name="sequential-thinking",
            tool_name="sequentialthinking",
            arguments={
                "thought": thought,
                "thoughtNumber": i,
                "totalThoughts": len(steps),
                "nextThoughtNeeded": i < len(steps),
            },
        )
        results.append(result.get("result", {}))
    
    return {
        "requirements": requirements,
        "design_steps": results,
        "architecture_summary": results[-1].get("summary", "")
    }
```

---

## 커스터마이징

### Truth/Serenity 평가 커스터마이징

Sequential Thinking은 키워드 기반으로 Truth와 Serenity를 평가합니다. 커스터마이징하려면 `sequential_thinking_mcp.py`를 수정:

```python
# Truth 지표 키워드 추가
truth_indicators = [
    "fact", "evidence", "data", "logic",
    "사실", "증거", "데이터", "논리",
    # 커스텀 키워드 추가
    "custom_keyword1", "custom_keyword2"
]

# Serenity 지표 키워드 추가
serenity_indicators = [
    "calm", "stable", "balanced",
    "평온", "안정", "균형",
    # 커스텀 키워드 추가
    "custom_serenity_keyword"
]
```

### 세션 관리

```python
from AFO.services.mcp_stdio_client import call_tool

# 세션 시작 (직접 구현 필요)
session_id = f"session_{int(time.time())}"

# 세션별 사고 추적
for i in range(5):
    result = call_tool(
        server_name="sequential-thinking",
        tool_name="sequentialthinking",
        arguments={
            "thought": f"Step {i+1} thought",
            "thoughtNumber": i+1,
            "totalThoughts": 5,
            "nextThoughtNeeded": i < 4,
        },
    )
    # 세션 ID를 메타데이터에 포함
    print(f"Session: {result['result']['metadata']['session_id']}")
```

---

## 실전 예제

### 예제 1: FastAPI 엔드포인트 설계

```python
from AFO.services.mcp_stdio_client import call_tool

def design_endpoint(endpoint_name: str, requirements: str) -> dict[str, Any]:
    """엔드포인트 설계 프로세스"""
    
    steps = [
        f"엔드포인트 '{endpoint_name}' 요구사항 분석",
        "HTTP 메서드 및 경로 설계",
        "요청/응답 스키마 정의",
        "비즈니스 로직 설계",
        "에러 처리 및 검증 로직 설계"
    ]
    
    results = []
    for i, step in enumerate(steps, 1):
        thought = f"[{step}]\n\n요구사항:\n{requirements}"
        result = call_tool(
            server_name="sequential-thinking",
            tool_name="sequentialthinking",
            arguments={
                "thought": thought,
                "thoughtNumber": i,
                "totalThoughts": len(steps),
                "nextThoughtNeeded": i < len(steps),
            },
        )
        results.append(result.get("result", {}))
    
    return {
        "endpoint": endpoint_name,
        "design_steps": results
    }
```

### 예제 2: Chancellor Graph V2와 함께 사용

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

# Sequential Thinking이 자동으로 통합됨
input_payload = {
    "command": "FastAPI 보안 강화",
    "skill_id": "skill_010_security_scan"
}

nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,  # Sequential Thinking 자동 적용
    "GOODNESS": goodness_node,  # Sequential Thinking 자동 적용
    "BEAUTY": beauty_node,  # Sequential Thinking 자동 적용
    "MERGE": merge_node,  # Sequential Thinking 자동 적용
    "EXECUTE": execute_node,  # Sequential Thinking 자동 적용
    "VERIFY": verify_node,  # Sequential Thinking 자동 적용
    "REPORT": report_node,
}

state = run_v2(input_payload, nodes)

# Sequential Thinking 결과 확인
for step, thinking in state.outputs.get("sequential_thinking", {}).items():
    print(f"\n[{step}]")
    print(f"Thought: {thinking.get('thought_processed', '')[:100]}")
    print(f"Truth: {thinking['metadata']['truth_impact']:.2f}")
    print(f"Serenity: {thinking['metadata']['serenity_impact']:.2f}")
```

---

## 트러블슈팅

### 문제 1: MCP 서버 연결 실패

**증상**: `RuntimeError: MCP sequential_thinking failed`

**해결**:
1. MCP 서버 설정 확인:
   ```bash
   cat .cursor/mcp.json | grep sequential-thinking
   ```

2. MCP 서버 재시작:
   - Cursor IDE 재시작
   - MCP 서버 로그 확인

### 문제 2: Truth/Serenity 점수가 낮음

**증상**: 평가 점수가 항상 낮게 나옴

**해결**:
1. 사고 내용에 키워드 포함:
   ```python
   # ✅ 좋은 예: 키워드 포함
   thought = "FastAPI 보안 강화를 위한 **증거** 기반 **분석** 및 **검증** 계획"
   
   # ❌ 나쁜 예: 키워드 없음
   thought = "FastAPI 보안 강화"
   ```

2. 사고 내용을 구체적으로 작성:
   ```python
   # ✅ 좋은 예: 구체적
   thought = "FastAPI 엔드포인트에 JWT 인증을 추가하기 위한 단계별 계획: 1) 의존성 설치 2) 미들웨어 구현 3) 테스트 작성"
   
   # ❌ 나쁜 예: 추상적
   thought = "인증 추가"
   ```

### 문제 3: 세션 관리 문제

**증상**: 사고 기록이 섞임

**해결**:
1. 세션 ID 명시적 관리:
   ```python
   # 각 프로세스마다 고유 세션 ID 사용
   session_id = f"process_{uuid.uuid4().hex[:8]}"
   ```

2. 사고 기록 초기화:
   ```python
   # 프로세스 시작 전 기록 초기화 (직접 구현 필요)
   # SequentialThinkingMCP 인스턴스의 clear_history() 호출
   ```

---

## 최적화 팁

### 1. 단계 수 최적화

너무 많은 단계는 오히려 비효율적입니다:

```python
# ✅ 좋은 예: 적절한 단계 수 (3-7단계)
steps = ["분석", "설계", "구현", "검증"]  # 4단계

# ❌ 나쁜 예: 너무 많은 단계
steps = [f"Step {i}" for i in range(20)]  # 20단계 (과도함)
```

### 2. 사고 내용 최적화

구체적이고 키워드가 포함된 사고가 높은 점수를 받습니다:

```python
# ✅ 좋은 예: 구체적 + 키워드
thought = "FastAPI 보안 강화를 위한 **증거** 기반 **분석**: JWT vs OAuth2 비교 및 **검증** 계획"

# ❌ 나쁜 예: 추상적
thought = "보안 강화"
```

### 3. 진행률 추적

`progress` 필드를 활용하여 진행 상황을 추적:

```python
result = call_tool(...)
progress = result["result"]["progress"]  # 0.0 ~ 1.0
print(f"Progress: {progress * 100:.1f}%")
```

---

## 참고 자료

- [Sequential Thinking MCP 서버 구현](../packages/trinity-os/trinity_os/servers/sequential_thinking_mcp.py)
- [Chancellor Graph V2 통합](../packages/afo-core/api/chancellor_v2/thinking.py)
- [MCP Stdio Client](../packages/afo-core/services/mcp_stdio_client.py)

---

**작성일**: 2025-12-25  
**버전**: 1.0.0  
**Trinity Score**: 眞 90% | 善 85% | 美 90% | 孝 95% | 永 85%

