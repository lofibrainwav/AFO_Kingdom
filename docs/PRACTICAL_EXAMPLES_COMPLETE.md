# 실전 예제 완전 가이드

> **眞善美孝永** - Context7 + Sequential Thinking + Skills 통합 활용 실전 예제

## 목차

1. [예제 1: YouTube 스펙 생성](#예제-1-youtube-스펙-생성)
2. [예제 2: RAG 시스템 구축](#예제-2-rag-시스템-구축)
3. [예제 3: 디버깅 자동화](#예제-3-디버깅-자동화)
4. [예제 4: 시스템 건강 모니터링](#예제-4-시스템-건강-모니터링)
5. [예제 5: 코드 리뷰 자동화](#예제-5-코드-리뷰-자동화)

---

## 예제 1: YouTube 스펙 생성

### 시나리오

YouTube 튜토리얼 비디오를 n8n 워크플로우 스펙으로 변환하는 작업을 Context7, Sequential Thinking, 그리고 Skills를 활용하여 완벽하게 실행합니다.

### 구현

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
from AFO.services.context7_service import get_context7_instance
from AFO.services.mcp_stdio_client import call_tool
from AFO.afo_skills_registry import SkillRegistry, register_core_skills

# Step 1: Context7로 관련 지식 검색
context7 = get_context7_instance()
youtube_knowledge = context7.retrieve_context("YouTube API transcript extraction")
n8n_knowledge = context7.retrieve_context("n8n workflow specification")

print("=== Context7 지식 검색 ===")
print(f"YouTube 관련: {len(youtube_knowledge.get('results', []))}개 결과")
print(f"n8n 관련: {len(n8n_knowledge.get('results', []))}개 결과")

# Step 2: Sequential Thinking으로 단계별 계획 수립
thinking_steps = [
    "YouTube URL에서 트랜스크립트 추출 방법 분석",
    "트랜스크립트를 n8n 워크플로우 스펙으로 변환 전략 수립",
    "LLM을 활용한 스펙 생성 계획",
    "생성된 스펙 검증 및 최적화 계획",
    "최종 n8n 워크플로우 생성"
]

thinking_results = []
for i, step_thought in enumerate(thinking_steps, 1):
    result = call_tool(
        server_name="sequential-thinking",
        tool_name="sequentialthinking",
        arguments={
            "thought": step_thought,
            "thoughtNumber": i,
            "totalThoughts": len(thinking_steps),
            "nextThoughtNeeded": i < len(thinking_steps),
        },
    )
    thinking_results.append(result.get("result", {}))

print("\n=== Sequential Thinking ===")
for i, result in enumerate(thinking_results, 1):
    print(f"Step {i}: {result.get('thought_processed', '')[:100]}...")
    print(f"  Truth: {result['metadata']['truth_impact']:.2f}, Serenity: {result['metadata']['serenity_impact']:.2f}")

# Step 3: Chancellor Graph V2로 통합 실행
input_payload = {
    "command": "YouTube 스펙 생성",
    "skill_id": "skill_001_youtube_spec_gen",
    "parameters": {
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "knowledge": {
            "youtube": youtube_knowledge,
            "n8n": n8n_knowledge,
            "thinking": thinking_results
        }
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

# Step 4: 결과 확인
print("\n=== 실행 결과 ===")
print(f"Trace ID: {state.trace_id}")
print(f"Errors: {len(state.errors)}")

# Context7 주입 결과
print("\n=== Context7 주입 ===")
for step, context in state.outputs.get("context7", {}).items():
    print(f"{step}: {context.get('context', '')[:100]}...")

# Sequential Thinking 결과
print("\n=== Sequential Thinking ===")
for step, thinking in state.outputs.get("sequential_thinking", {}).items():
    print(f"{step}: {thinking.get('thought_processed', '')[:100]}...")

# Skill 실행 결과
print("\n=== Skill 실행 ===")
execute = state.outputs.get("EXECUTE", {})
print(f"Status: {execute.get('status')}")
if execute.get("status") == "success":
    result = execute.get("result", {})
    print(f"n8n Spec: {result.get('node_spec', {})}")

# 검증 결과
print("\n=== 검증 ===")
verify = state.outputs.get("VERIFY", {})
print(f"Status: {verify.get('status')}")
if verify.get("status") == "pass":
    print("✅ 모든 검증 통과")
else:
    print(f"❌ 검증 실패: {verify.get('issues', [])}")
```

### 실행 결과 예시

```
=== Context7 지식 검색 ===
YouTube 관련: 3개 결과
n8n 관련: 2개 결과

=== Sequential Thinking ===
Step 1: YouTube URL에서 트랜스크립트 추출 방법 분석...
  Truth: 0.85, Serenity: 0.90
Step 2: 트랜스크립트를 n8n 워크플로우 스펙으로 변환 전략 수립...
  Truth: 0.88, Serenity: 0.92
...

=== 실행 결과 ===
Trace ID: abc123def456
Errors: 0

=== Context7 주입 ===
KINGDOM_DNA: LangGraph state management patterns...
TRUTH: Python type checking best practices...
GOODNESS: FastAPI security guidelines...
...

=== Sequential Thinking ===
TRUTH: Evaluating technical truth for: skill_001_youtube_spec_gen...
GOODNESS: Checking ethical/security aspects for: skill_001_youtube_spec_gen...
...

=== Skill 실행 ===
Status: success
n8n Spec: {"nodes": [...], "connections": [...]}

=== 검증 ===
Status: pass
✅ 모든 검증 통과
```

---

## 예제 2: RAG 시스템 구축

### 시나리오

Ultimate RAG 시스템을 구축하여 FastAPI 보안 관련 문서를 검색하는 작업을 완벽하게 실행합니다.

### 구현

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *
from AFO.services.context7_service import get_context7_instance

# Step 1: Context7로 RAG 관련 지식 검색
context7 = get_context7_instance()
rag_knowledge = context7.retrieve_context("RAG retrieval augmented generation vector search", domain="technical")
security_knowledge = context7.retrieve_context("FastAPI security authentication authorization", domain="technical")

# Step 2: Chancellor Graph V2로 통합 실행
input_payload = {
    "command": "RAG 시스템으로 FastAPI 보안 문서 검색",
    "skill_id": "skill_002_ultimate_rag",
    "parameters": {
        "query": "FastAPI 보안 best practices",
        "top_k": 5,
        "knowledge": {
            "rag": rag_knowledge,
            "security": security_knowledge
        }
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

# Step 3: 결과 확인
execute_result = state.outputs.get("EXECUTE", {})
if execute_result.get("status") == "success":
    documents = execute_result.get("result", {}).get("documents", [])
    print(f"✅ {len(documents)}개 문서 검색 완료")
    
    for i, doc in enumerate(documents, 1):
        print(f"\n[{i}] {doc.get('title', 'Untitled')}")
        print(f"    Score: {doc.get('score', 0):.2f}")
        print(f"    Preview: {doc.get('content', '')[:200]}...")
```

---

## 예제 3: 디버깅 자동화

### 시나리오

에러 로그를 분석하고 자동으로 수정 사항을 제안하는 디버깅 자동화 작업을 완벽하게 실행합니다.

### 구현

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *
from AFO.services.context7_service import get_context7_instance
from AFO.services.mcp_stdio_client import call_tool

# Step 1: Context7로 디버깅 관련 지식 검색
context7 = get_context7_instance()
debug_knowledge = context7.retrieve_context("Python debugging error analysis stack trace", domain="technical")

# Step 2: Sequential Thinking으로 디버깅 프로세스 수립
error_log = """
Traceback (most recent call last):
  File "api/routes/context7.py", line 53, in search_context7
    results = context7.retrieve_context(q)
AttributeError: 'NoneType' object has no attribute 'retrieve_context'
"""

thinking_steps = [
    f"에러 로그 분석: {error_log[:100]}...",
    "에러 원인 파악: NoneType 객체에 대한 메서드 호출",
    "해결 방안 수립: Context7 인스턴스 초기화 확인",
    "코드 수정 계획: get_context7_instance() 호출 검증",
    "테스트 및 검증 계획"
]

thinking_results = []
for i, step in enumerate(thinking_steps, 1):
    result = call_tool(
        server_name="sequential-thinking",
        tool_name="sequentialthinking",
        arguments={
            "thought": step,
            "thoughtNumber": i,
            "totalThoughts": len(thinking_steps),
            "nextThoughtNeeded": i < len(thinking_steps),
        },
    )
    thinking_results.append(result.get("result", {}))

# Step 3: Chancellor Graph V2로 통합 실행
input_payload = {
    "command": "자동 디버깅",
    "skill_id": "skill_013_automated_debugging",
    "parameters": {
        "error_log": error_log,
        "code_path": "packages/afo-core/api/routes/context7.py",
        "knowledge": {
            "debugging": debug_knowledge,
            "thinking": thinking_results
        }
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

# Step 4: 결과 확인
execute_result = state.outputs.get("EXECUTE", {})
if execute_result.get("status") == "success":
    fixes = execute_result.get("result", {}).get("fixes_applied", [])
    print(f"✅ {len(fixes)}개 수정 사항 제안")
    for fix in fixes:
        print(f"\n- {fix.get('description', '')}")
        print(f"  File: {fix.get('file', '')}")
        print(f"  Line: {fix.get('line', '')}")
        print(f"  Fix: {fix.get('fix', '')}")
```

---

## 예제 4: 시스템 건강 모니터링

### 시나리오

시스템 전체 건강 상태를 모니터링하고 Trinity Score를 계산하는 작업을 완벽하게 실행합니다.

### 구현

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

# Step 1: Health Monitor Skill 실행
input_payload = {
    "command": "시스템 건강 모니터링",
    "skill_id": "skill_003_health_monitor",
    "parameters": {}
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

# Step 2: 결과 확인
execute_result = state.outputs.get("EXECUTE", {})
if execute_result.get("status") == "success":
    health_data = execute_result.get("result", {}).get("data", {})
    
    print("=== 시스템 건강 상태 ===")
    print(f"Trinity Score: {health_data.get('trinity_score', 0):.1f}/100")
    print(f"Decision: {health_data.get('decision', 'UNKNOWN')}")
    
    # 11-오장육부 상태
    organs = health_data.get("organs", {})
    print("\n=== 11-오장육부 상태 ===")
    for organ_name, organ_status in organs.items():
        status_icon = "✅" if organ_status.get("healthy", False) else "❌"
        print(f"{status_icon} {organ_name}: {organ_status.get('status', 'unknown')}")
    
    # Context7 주입 결과 확인
    print("\n=== Context7 주입 ===")
    context7_data = state.outputs.get("context7", {})
    print(f"Kingdom DNA: {len(context7_data.get('KINGDOM_DNA', {}).get('context', ''))} chars")
    print(f"Steps with Context: {len([k for k in context7_data.keys() if k != 'KINGDOM_DNA'])}")
    
    # Sequential Thinking 결과 확인
    print("\n=== Sequential Thinking ===")
    thinking_data = state.outputs.get("sequential_thinking", {})
    avg_truth = sum(t.get("metadata", {}).get("truth_impact", 0) for t in thinking_data.values()) / len(thinking_data) if thinking_data else 0
    avg_serenity = sum(t.get("metadata", {}).get("serenity_impact", 0) for t in thinking_data.values()) / len(thinking_data) if thinking_data else 0
    print(f"Average Truth Impact: {avg_truth:.2f}")
    print(f"Average Serenity Impact: {avg_serenity:.2f}")
```

---

## 예제 5: 코드 리뷰 자동화

### 시나리오

코드를 자동으로 리뷰하고 개선 사항을 제안하는 작업을 완벽하게 실행합니다.

### 구현

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *
from AFO.services.context7_service import get_context7_instance
from AFO.services.mcp_stdio_client import call_tool

# Step 1: 리뷰할 코드
code_to_review = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""

# Step 2: Context7로 코드 리뷰 관련 지식 검색
context7 = get_context7_instance()
review_knowledge = context7.retrieve_context("Python code review best practices type safety", domain="technical")

# Step 3: Sequential Thinking으로 리뷰 프로세스 수립
review_steps = [
    "코드 구문 및 타입 검사",
    "비즈니스 로직 정확성 검증",
    "보안 취약점 및 리스크 검토",
    "코드 품질 및 유지보수성 평가",
    "개선 사항 제안"
]

thinking_results = []
for i, step in enumerate(review_steps, 1):
    thought = f"[{step}]\n\n코드:\n{code_to_review}"
    result = call_tool(
        server_name="sequential-thinking",
        tool_name="sequentialthinking",
        arguments={
            "thought": thought,
            "thoughtNumber": i,
            "totalThoughts": len(review_steps),
            "nextThoughtNeeded": i < len(review_steps),
        },
    )
    thinking_results.append(result.get("result", {}))

# Step 4: Chancellor Graph V2로 통합 실행
input_payload = {
    "command": "코드 리뷰",
    "skill_id": "skill_014_code_quality",
    "parameters": {
        "code": code_to_review,
        "file_path": "example.py",
        "knowledge": {
            "review": review_knowledge,
            "thinking": thinking_results
        }
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

# Step 5: 결과 확인
execute_result = state.outputs.get("EXECUTE", {})
if execute_result.get("status") == "success":
    review_result = execute_result.get("result", {})
    
    print("=== 코드 리뷰 결과 ===")
    print(f"Overall Score: {review_result.get('overall_score', 0)}/100")
    
    # 개선 사항
    improvements = review_result.get("improvements", [])
    print(f"\n개선 사항: {len(improvements)}개")
    for imp in improvements:
        print(f"\n- {imp.get('type', 'code_improvement')}: {imp.get('description', '')}")
        print(f"  Priority: {imp.get('priority', 'medium')}")
        if imp.get("suggestion"):
            print(f"  Suggestion: {imp['suggestion']}")
    
    # Sequential Thinking 요약
    print("\n=== Sequential Thinking 요약 ===")
    for i, thinking in enumerate(thinking_results, 1):
        print(f"Step {i}: {thinking.get('thought_processed', '')[:100]}...")
```

---

## 통합 활용 패턴

### 패턴 1: Context7 → Sequential Thinking → Skill 실행

```python
# 1. Context7로 지식 검색
context7 = get_context7_instance()
knowledge = context7.retrieve_context("query")

# 2. Sequential Thinking으로 계획 수립
thinking_result = call_tool(
    server_name="sequential-thinking",
    tool_name="sequentialthinking",
    arguments={
        "thought": f"계획 수립: {knowledge}",
        "thoughtNumber": 1,
        "totalThoughts": 3,
        "nextThoughtNeeded": True,
    },
)

# 3. Skill 실행
registry = SkillRegistry()
result = await registry.execute_skill(
    skill_id="skill_id",
    parameters={"knowledge": knowledge, "plan": thinking_result},
)
```

### 패턴 2: Chancellor Graph V2 활용 (권장)

```python
# 모든 것이 자동으로 통합됨
state = run_v2(input_payload, nodes)

# 결과 확인
print(state.outputs["context7"])  # Context7 주입 결과
print(state.outputs["sequential_thinking"])  # Sequential Thinking 결과
print(state.outputs["EXECUTE"])  # Skill 실행 결과
```

---

## 참고 자료

- [Context7 완벽 활용 가이드](./CONTEXT7_COMPLETE_USAGE_GUIDE.md)
- [Sequential Thinking 완벽 활용 가이드](./SEQUENTIAL_THINKING_COMPLETE_USAGE_GUIDE.md)
- [Skills 완벽 활용 가이드](./SKILLS_COMPLETE_USAGE_GUIDE.md)
- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)

---

**작성일**: 2025-12-25  
**버전**: 1.0.0  
**Trinity Score**: 眞 95% | 善 90% | 美 90% | 孝 95% | 永 90%
