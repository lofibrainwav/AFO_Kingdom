# 통합 최적화 가이드

> **眞善美孝永** - Context7 + Sequential Thinking + Skills 성능 최적화

## 목차

1. [개요](#개요)
2. [Context7 캐싱 전략](#context7-캐싱-전략)
3. [Sequential Thinking 배치 처리](#sequential-thinking-배치-처리)
4. [Skills 병렬 실행](#skills-병렬-실행)
5. [Chancellor Graph V2 최적화](#chancellor-graph-v2-최적화)
6. [실전 최적화 예제](#실전-최적화-예제)
7. [성능 모니터링](#성능-모니터링)

---

## 개요

Context7, Sequential Thinking, 그리고 Skills를 완벽히 활용하면서도 성능을 최적화하는 방법을 다룹니다.

### 최적화 목표

- ✅ **Context7**: 싱글톤 캐싱 및 지연 로딩
- ✅ **Sequential Thinking**: 배치 처리 및 결과 재사용
- ✅ **Skills**: 병렬 실행 및 타임아웃 관리
- ✅ **Chancellor Graph V2**: 체크포인트 활용 및 이벤트 최적화

---

## Context7 캐싱 전략

### 싱글톤 패턴 활용

Context7은 이미 싱글톤 패턴으로 구현되어 있습니다:

```python
from AFO.services.context7_service import get_context7_instance

# ✅ 좋은 예: 싱글톤 활용
context7 = get_context7_instance()  # 첫 호출 시 초기화
result1 = context7.retrieve_context("query1")
result2 = context7.retrieve_context("query2")  # 같은 인스턴스 재사용

# ❌ 나쁜 예: 매번 새 인스턴스 생성 (비효율)
from trinity_os.servers.context7_mcp import Context7MCP
context7_1 = Context7MCP()  # 불필요한 초기화
context7_2 = Context7MCP()  # 불필요한 초기화
```

### Redis 캐싱 추가

Context7 검색 결과를 Redis에 캐싱하여 성능 향상:

```python
from AFO.services.redis_cache_service import RedisCacheService
from AFO.services.context7_service import get_context7_instance

cache = RedisCacheService()
context7 = get_context7_instance()

def cached_retrieve_context(query: str, ttl: int = 300) -> dict[str, Any]:
    """Redis 캐싱을 활용한 Context7 검색"""
    
    # 캐시 키 생성
    cache_key = f"context7:search:{hash(query)}"
    
    # 캐시에서 조회
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # 캐시 미스: 실제 검색
    result = context7.retrieve_context(query)
    
    # 캐시에 저장 (TTL 300초)
    cache.set(cache_key, result, ttl=ttl)
    
    return result

# 사용
result = cached_retrieve_context("FastAPI security", ttl=600)  # 10분 캐싱
```

### 지식 베이스 사전 로딩

애플리케이션 시작 시 지식 베이스를 사전 로딩:

```python
from AFO.services.context7_service import get_context7_instance

# 애플리케이션 시작 시
context7 = get_context7_instance()  # 지식 베이스 자동 로드

# 핵심 지식 사전 검색 (워밍업)
warmup_queries = [
    "Trinity philosophy",
    "MCP protocol",
    "Skills registry",
    "FastAPI security",
    "Python type checking"
]

for query in warmup_queries:
    context7.retrieve_context(query)  # 캐시 워밍업
```

---

## Sequential Thinking 배치 처리

### 다단계 사고 배치 처리

여러 단계를 한 번에 처리하여 성능 향상:

```python
from AFO.services.mcp_stdio_client import call_tool

def batch_sequential_thinking(thoughts: list[str]) -> list[dict[str, Any]]:
    """여러 사고를 배치로 처리"""
    
    results = []
    total = len(thoughts)
    
    for i, thought in enumerate(thoughts, 1):
        result = call_tool(
            server_name="sequential-thinking",
            tool_name="sequentialthinking",
            arguments={
                "thought": thought,
                "thoughtNumber": i,
                "totalThoughts": total,
                "nextThoughtNeeded": i < total,
            },
        )
        results.append(result.get("result", {}))
    
    return results

# 사용
thoughts = [
    "Step 1: 문제 정의",
    "Step 2: 해결책 탐색",
    "Step 3: 최적 해결책 선택",
    "Step 4: 구현 계획",
    "Step 5: 검증 계획"
]

results = batch_sequential_thinking(thoughts)
```

### 결과 재사용

동일한 사고 프로세스 결과를 재사용:

```python
from functools import lru_cache
from AFO.services.mcp_stdio_client import call_tool

@lru_cache(maxsize=100)
def cached_sequential_thinking(thought: str, thought_number: int, total_thoughts: int) -> dict[str, Any]:
    """LRU 캐시를 활용한 Sequential Thinking"""
    
    result = call_tool(
        server_name="sequential-thinking",
        tool_name="sequentialthinking",
        arguments={
            "thought": thought,
            "thoughtNumber": thought_number,
            "totalThoughts": total_thoughts,
            "nextThoughtNeeded": False,
        },
    )
    return result.get("result", {})

# 사용
result1 = cached_sequential_thinking("FastAPI 보안 강화", 1, 1)
result2 = cached_sequential_thinking("FastAPI 보안 강화", 1, 1)  # 캐시에서 반환
```

---

## Skills 병렬 실행

### 비동기 병렬 실행

여러 스킬을 동시에 실행:

```python
import asyncio
from AFO.afo_skills_registry import SkillRegistry

async def parallel_skill_execution(skill_configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """여러 스킬을 병렬로 실행"""
    
    registry = SkillRegistry()
    
    # 모든 스킬 실행 태스크 생성
    tasks = [
        registry.execute_skill(
            skill_id=config["skill_id"],
            parameters=config.get("parameters", {}),
            timeout_seconds=config.get("timeout", 30)
        )
        for config in skill_configs
    ]
    
    # 병렬 실행
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 결과 처리
    execution_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            execution_results.append({
                "skill_id": skill_configs[i]["skill_id"],
                "status": "error",
                "error": str(result)
            })
        else:
            execution_results.append({
                "skill_id": skill_configs[i]["skill_id"],
                "status": "success",
                "result": result
            })
    
    return execution_results

# 사용
skill_configs = [
    {"skill_id": "skill_001_youtube_spec_gen", "parameters": {"url": "..."}},
    {"skill_id": "skill_002_ultimate_rag", "parameters": {"query": "..."}},
    {"skill_id": "skill_003_health_monitor", "parameters": {}}
]

results = await parallel_skill_execution(skill_configs)
for result in results:
    print(f"{result['skill_id']}: {result['status']}")
```

### 타임아웃 관리

각 스킬에 적절한 타임아웃 설정:

```python
from AFO.afo_skills_registry import SkillRegistry

registry = SkillRegistry()

# 스킬별 권장 타임아웃
SKILL_TIMEOUTS = {
    "skill_001_youtube_spec_gen": 60,  # LLM 처리 시간 고려
    "skill_002_ultimate_rag": 30,     # 벡터 검색
    "skill_003_health_monitor": 10,   # 빠른 건강 체크
    "skill_013_automated_debugging": 45,  # 코드 분석
}

def execute_skill_with_timeout(skill_id: str, parameters: dict[str, Any]) -> dict[str, Any]:
    """스킬별 적절한 타임아웃으로 실행"""
    
    timeout = SKILL_TIMEOUTS.get(skill_id, 30)  # 기본값 30초
    
    return await registry.execute_skill(
        skill_id=skill_id,
        parameters=parameters,
        timeout_seconds=timeout
    )
```

---

## Chancellor Graph V2 최적화

### 체크포인트 활용

불필요한 재실행을 방지하기 위해 체크포인트 활용:

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.store import load_checkpoint, list_checkpoints
from api.chancellor_v2.graph.nodes import *

def optimized_run_v2(input_payload: dict[str, Any], nodes: dict[str, NodeFn], use_cache: bool = True) -> GraphState:
    """체크포인트를 활용한 최적화된 실행"""
    
    # 이전 실행 결과 확인 (선택적)
    if use_cache:
        # 동일한 입력에 대한 이전 트레이스 검색 (간단한 예제)
        # 실제로는 더 정교한 캐시 키 생성 필요
        pass
    
    # 정상 실행
    state = run_v2(input_payload, nodes)
    
    # 성공 시 체크포인트 저장 (이미 자동으로 저장됨)
    if state.outputs.get("VERIFY", {}).get("status") == "pass":
        # 추가 최적화: 성공한 실행 결과를 캐시에 저장
        pass
    
    return state
```

### 이벤트 로그 최적화

이벤트 로그 크기 최적화:

```python
from api.chancellor_v2.observability import get_trace_events

def analyze_trace_performance(trace_id: str) -> dict[str, Any]:
    """트레이스 성능 분석"""
    
    events = get_trace_events(trace_id)
    
    # 단계별 소요 시간 계산
    step_durations = {}
    for i, event in enumerate(events[1:], 1):
        prev_event = events[i-1]
        if prev_event["event"] == "enter" and event["event"] == "exit":
            step = prev_event["step"]
            duration = event["ts"] - prev_event["ts"]
            step_durations[step] = duration
    
    # 병목 지점 식별
    bottlenecks = {
        step: duration
        for step, duration in step_durations.items()
        if duration > 1.0  # 1초 이상 소요
    }
    
    return {
        "total_duration": events[-1]["ts"] - events[0]["ts"] if events else 0,
        "step_durations": step_durations,
        "bottlenecks": bottlenecks
    }

# 사용
performance = analyze_trace_performance(trace_id)
print(f"Total Duration: {performance['total_duration']:.2f}s")
print(f"Bottlenecks: {performance['bottlenecks']}")
```

---

## 실전 최적화 예제

### 예제 1: 통합 캐싱 레이어

```python
from AFO.services.redis_cache_service import RedisCacheService
from AFO.services.context7_service import get_context7_instance
from AFO.services.mcp_stdio_client import call_tool
from AFO.afo_skills_registry import SkillRegistry

class OptimizedIntegrationLayer:
    """통합 최적화 레이어"""
    
    def __init__(self):
        self.cache = RedisCacheService()
        self.context7 = get_context7_instance()
        self.registry = SkillRegistry()
    
    async def optimized_execution(
        self,
        command: str,
        skill_id: str,
        parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """최적화된 통합 실행"""
        
        # 1. Context7 검색 (캐싱)
        cache_key_context7 = f"context7:{hash(command)}"
        knowledge = self.cache.get(cache_key_context7)
        if not knowledge:
            knowledge = self.context7.retrieve_context(command)
            self.cache.set(cache_key_context7, knowledge, ttl=300)
        
        # 2. Sequential Thinking (배치)
        thinking_result = call_tool(
            server_name="sequential-thinking",
            tool_name="sequentialthinking",
            arguments={
                "thought": f"계획 수립: {command}",
                "thoughtNumber": 1,
                "totalThoughts": 1,
                "nextThoughtNeeded": False,
            },
        )
        
        # 3. Skill 실행 (타임아웃 관리)
        result = await self.registry.execute_skill(
            skill_id=skill_id,
            parameters={
                **parameters,
                "knowledge": knowledge,
                "thinking": thinking_result
            },
            timeout_seconds=60
        )
        
        return {
            "knowledge": knowledge,
            "thinking": thinking_result,
            "skill_result": result
        }

# 사용
layer = OptimizedIntegrationLayer()
result = await layer.optimized_execution(
    command="YouTube 스펙 생성",
    skill_id="skill_001_youtube_spec_gen",
    parameters={"youtube_url": "..."}
)
```

### 예제 2: 병렬 스킬 실행 파이프라인

```python
import asyncio
from AFO.afo_skills_registry import SkillRegistry

async def parallel_pipeline(input_data: dict[str, Any]) -> dict[str, Any]:
    """병렬 스킬 실행 파이프라인"""
    
    registry = SkillRegistry()
    
    # Step 1: Context7 검색 (병렬)
    context7_tasks = [
        get_context7_instance().retrieve_context(query)
        for query in input_data.get("queries", [])
    ]
    knowledge_results = await asyncio.gather(*context7_tasks)
    
    # Step 2: Skills 실행 (병렬)
    skill_tasks = [
        registry.execute_skill(
            skill_id=config["skill_id"],
            parameters=config.get("parameters", {})
        )
        for config in input_data.get("skills", [])
    ]
    skill_results = await asyncio.gather(*skill_tasks, return_exceptions=True)
    
    return {
        "knowledge": knowledge_results,
        "skills": skill_results
    }

# 사용
input_data = {
    "queries": [
        "FastAPI security",
        "RAG systems",
        "Python type checking"
    ],
    "skills": [
        {"skill_id": "skill_001_youtube_spec_gen", "parameters": {...}},
        {"skill_id": "skill_002_ultimate_rag", "parameters": {...}}
    ]
}

results = await parallel_pipeline(input_data)
```

---

## 성능 모니터링

### 메트릭 수집

```python
from api.chancellor_v2.metrics import (
    chancellor_v2_trace_created_total,
    chancellor_v2_execute_success_total,
    update_artifact_metrics
)
import time

def monitored_execution(input_payload: dict[str, Any], nodes: dict[str, NodeFn]) -> GraphState:
    """메트릭 수집을 포함한 실행"""
    
    start_time = time.time()
    
    # 실행
    state = run_v2(input_payload, nodes)
    
    # 메트릭 업데이트
    execution_time = time.time() - start_time
    chancellor_v2_trace_created_total.inc()
    
    if state.outputs.get("EXECUTE", {}).get("status") == "success":
        chancellor_v2_execute_success_total.inc()
    
    # 아티팩트 메트릭 업데이트
    update_artifact_metrics()
    
    # 성능 로그
    print(f"Execution Time: {execution_time:.2f}s")
    print(f"Trace ID: {state.trace_id}")
    
    return state
```

### 성능 프로파일링

```python
import cProfile
import pstats
from io import StringIO

def profiled_execution(input_payload: dict[str, Any], nodes: dict[str, NodeFn]) -> tuple[GraphState, str]:
    """프로파일링을 포함한 실행"""
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    state = run_v2(input_payload, nodes)
    
    profiler.disable()
    
    # 프로파일 결과 문자열로 변환
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # 상위 20개 함수
    
    profile_output = stream.getvalue()
    
    return state, profile_output

# 사용
state, profile = profiled_execution(input_payload, nodes)
print(profile)  # 성능 병목 지점 확인
```

---

## 최적화 체크리스트

### Context7 최적화

- [ ] 싱글톤 패턴 활용 (`get_context7_instance()`)
- [ ] Redis 캐싱 추가 (검색 결과)
- [ ] 지식 베이스 사전 로딩 (워밍업)
- [ ] 도메인 필터링 활용
- [ ] 결과 제한 (`limit` 파라미터)

### Sequential Thinking 최적화

- [ ] 배치 처리 활용
- [ ] 결과 재사용 (LRU 캐시)
- [ ] 사고 내용 최적화 (키워드 포함)
- [ ] 단계 수 최적화 (3-7단계)

### Skills 최적화

- [ ] 병렬 실행 활용 (`asyncio.gather`)
- [ ] 타임아웃 관리 (스킬별 적절한 값)
- [ ] DRY_RUN 활용 (실제 실행 전 검증)
- [ ] Stage 2 Allowlist 준수

### Chancellor Graph V2 최적화

- [ ] 체크포인트 활용 (재실행 방지)
- [ ] 이벤트 로그 분석 (병목 지점 파악)
- [ ] 메트릭 모니터링 (Prometheus)
- [ ] 프로파일링 (성능 병목 식별)

---

## 참고 자료

- [Context7 완벽 활용 가이드](./CONTEXT7_COMPLETE_USAGE_GUIDE.md)
- [Sequential Thinking 완벽 활용 가이드](./SEQUENTIAL_THINKING_COMPLETE_USAGE_GUIDE.md)
- [Skills 완벽 활용 가이드](./SKILLS_COMPLETE_USAGE_GUIDE.md)
- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)
- [Redis Cache Service](../packages/afo-core/services/redis_cache_service.py)

---

**작성일**: 2025-12-25  
**버전**: 1.0.0  
**Trinity Score**: 眞 90% | 善 85% | 美 90% | 孝 95% | 永 85%

