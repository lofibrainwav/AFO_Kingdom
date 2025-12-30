# Skills 완벽 활용 가이드

> **眞善美孝永** - AFO 왕국의 스킬 레지스트리 시스템

> **⚠️ 중요**: 모든 import 경로는 [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) 문서를 참조하세요.

## 목차

1. [개요](#개요)
2. [아키텍처](#아키텍처)
3. [Skill Registry 사용법](#skill-registry-사용법)
4. [새로운 Skill 등록](#새로운-skill-등록)
5. [Skill 실행 및 모니터링](#skill-실행-및-모니터링)
6. [Chancellor Graph V2 통합](#chancellor-graph-v2-통합)
7. [실전 예제](#실전-예제)
8. [트러블슈팅](#트러블슈팅)

---

## 개요

AFO Skills Registry는 AFO 왕국의 **중앙 스킬 관리 시스템**입니다. 30개의 스킬을 등록하고 실행할 수 있으며, Trinity Score 기반 철학 정렬을 지원합니다.

### 핵심 특징

- ✅ **싱글톤 패턴**: 전역 단일 인스턴스
- ✅ **30개 스킬**: 다양한 카테고리로 분류
- ✅ **Trinity Score 평가**: 眞善美孝永 철학 정렬
- ✅ **Stage 2 Allowlist**: 보안 게이트 강제
- ✅ **Chancellor Graph 통합**: EXECUTE 노드에서 자동 실행

---

## 아키텍처

### 구성 요소

```
┌─────────────────────────────────────────┐
│  SkillRegistry (싱글톤)                 │
│  - 스킬 등록/조회                        │
│  - 필터링 및 검색                        │
│  - 실행 관리                             │
└──────────────┬──────────────────────────┘
               │
               ├─── Skills API Router (FastAPI)
               │    - /api/skills/list
               │    - /api/skills/detail/{skill_id}
               │    - /api/skills/execute
               │    - /api/skills/health
               │
               ├─── Skills Service (비즈니스 로직)
               │    - 스킬 등록 서비스
               │    - 실행 관리
               │
               └─── Chancellor Graph V2 통합
                    - EXECUTE 노드에서 실행
                    - Stage 2 Allowlist 검증
```

### 파일 구조

```
packages/afo-core/
├── afo_skills_registry.py          # Skill Registry 구현
├── api/
│   ├── routes/
│   │   └── skills.py              # API 라우터
│   ├── routers/
│   │   └── skills.py              # 라우터 (레거시)
│   └── services/
│       └── skills_service.py      # 비즈니스 로직
└── api/
    └── chancellor_v2/
        └── graph/
            └── nodes/
                └── execute_node.py  # Skills 실행 노드
```

---

## Skill Registry 사용법

### 기본 사용

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.afo_skills_registry import SkillRegistry, register_core_skills

# Skill Registry 가져오기 (싱글톤)
registry = SkillRegistry()

# Core Skills 등록 (처음 한 번만)
if registry.count() < 5:
    register_core_skills()

# 모든 스킬 목록 조회
all_skills = registry.list_all()
print(f"Total Skills: {len(all_skills)}")

# 특정 스킬 조회
skill = registry.get("skill_001_youtube_spec_gen")
if skill:
    print(f"Name: {skill.name}")
    print(f"Description: {skill.description}")
    print(f"Category: {skill.category}")
    print(f"Philosophy: {skill.philosophy_scores.summary}")
```

### 필터링 및 검색

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.afo_skills_registry import SkillFilterParams, SkillCategory

# 필터 파라미터 생성
filters = SkillFilterParams(
    category=SkillCategory.RAG_SYSTEMS,
    status=SkillStatus.ACTIVE,
    tags=["rag", "retrieval"],
    min_philosophy_avg=90,
    limit=10,
    offset=0
)

# 필터링된 스킬 조회
filtered_skills = registry.filter(filters)
for skill in filtered_skills:
    print(f"{skill.skill_id}: {skill.name} (Avg: {skill.philosophy_scores.average:.1f}%)")
```

### 카테고리 통계

```python
# 카테고리별 통계
stats = registry.get_category_stats()
for category, count in stats.items():
    print(f"{category}: {count} skills")

# 모든 카테고리 목록
categories = registry.get_categories()
print(f"Available Categories: {categories}")
```

---

## 새로운 Skill 등록

### 방법 1: 코드에서 직접 등록

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.afo_skills_registry import (
    AFOSkillCard,
    SkillCategory,
    ExecutionMode,
    PhilosophyScore,
    SkillIOSchema,
    SkillParameter,
    SkillRegistry
)

# 새 스킬 생성
new_skill = AFOSkillCard(
    skill_id="skill_022_custom_skill",
    name="Custom Skill",
    description="Custom skill description",
    category=SkillCategory.ANALYSIS_EVALUATION,
    tags=["custom", "analysis"],
    version="1.0.0",
    capabilities=["custom_analysis", "data_processing"],
    dependencies=["pandas", "numpy"],
    execution_mode=ExecutionMode.ASYNC,
    estimated_duration_ms=5000,
    input_schema=SkillIOSchema(
        parameters=[
            SkillParameter(
                name="input_data",
                type="dict",
                description="Input data dictionary",
                required=True
            )
        ],
        example={"input_data": {"key": "value"}}
    ),
    output_schema=SkillIOSchema(
        parameters=[
            SkillParameter(
                name="result",
                type="dict",
                description="Analysis result",
                required=True
            )
        ]
    ),
    philosophy_scores=PhilosophyScore(
        truth=90,
        goodness=85,
        beauty=80,
        serenity=90
    )
)

# 레지스트리에 등록
registry = SkillRegistry()
is_new = registry.register(new_skill)
if is_new:
    print(f"✅ New skill registered: {new_skill.skill_id}")
else:
    print(f"🔄 Skill updated: {new_skill.skill_id}")
```

### 방법 2: register_core_skills() 확장

`afo_skills_registry.py`의 `register_core_skills()` 함수에 스킬 추가:

```python
def register_core_skills() -> SkillRegistry:
    """Register AFO's core built-in skills"""
    registry = SkillRegistry()
    
    # 기존 스킬들...
    
    # 새 스킬 추가
    skill_022 = AFOSkillCard(
        skill_id="skill_022_custom_skill",
        # ... 스킬 정의
    )
    registry.register(skill_022)
    
    return registry
```

### 방법 3: Skills Service 사용

```python
from api.services.skills_service import SkillsService
from api.models.skills import SkillRequest

# Skills Service 초기화
service = SkillsService()

# 스킬 등록 요청
request = SkillRequest(
    skill_id="skill_022_custom_skill",
    name="Custom Skill",
    description="Custom skill description",
    category="analysis_evaluation",
    execution_mode="async",
    parameters={}
)

# 등록
response = await service.register_skill(request)
print(f"Registered: {response.skill_id}")
```

---

## Skill 실행 및 모니터링

### API를 통한 실행

**엔드포인트**: `POST /api/skills/execute`

**요청**:
```json
{
  "skill_id": "skill_001_youtube_spec_gen",
  "parameters": {
    "youtube_url": "https://www.youtube.com/watch?v=..."
  },
  "dry_run": false
}
```

**응답**:
```json
{
  "skill_id": "skill_001_youtube_spec_gen",
  "status": "completed",
  "result": {
    "message": "Skill executed successfully",
    "data": {...}
  },
  "dry_run": false
}
```

### Python에서 직접 실행

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.afo_skills_registry import SkillRegistry

registry = SkillRegistry()

# 스킬 실행
result = await registry.execute_skill(
    skill_id="skill_001_youtube_spec_gen",
    parameters={
        "youtube_url": "https://www.youtube.com/watch?v=..."
    },
    timeout_seconds=60
)

print(f"Status: {result.status}")
print(f"Result: {result.result}")
```

### DRY_RUN 실행

```python
# DRY_RUN 모드로 실행 (시뮬레이션)
result = await registry.execute_skill(
    skill_id="skill_001_youtube_spec_gen",
    parameters={"youtube_url": "..."},
    dry_run=True
)

if result.dry_run:
    print("✅ DRY_RUN 성공 - 실제 실행 가능")
else:
    print("⚠️ 실제 실행됨")
```

### Stage 2 Allowlist 검증

모든 스킬 실행은 Stage 2 Allowlist를 통과해야 합니다:

```python
from api.guards.skills_allowlist_guard import is_skill_allowed

# Allowlist 검증
allowed, reason = is_skill_allowed("skill_001_youtube_spec_gen")
if not allowed:
    print(f"❌ 실행 차단: {reason}")
else:
    print("✅ 실행 허용됨")
```

---

## Chancellor Graph V2 통합

### 자동 통합

Skills는 Chancellor Graph V2의 EXECUTE 노드에서 자동으로 실행됩니다.

### 실행 흐름

```
1. EXECUTE 노드 진입
   → state.plan에서 skill_id 추출
   
2. Stage 2 Allowlist 검증
   → is_skill_allowed(skill_id)
   → 차단 시 실행 중단
   
3. Skill 실행
   → registry.execute_skill(skill_id, parameters)
   → 결과를 state.outputs["EXECUTE"]에 저장
   
4. 결과 확인
   → state.outputs["EXECUTE"]["result"]
```

### 사용 예제

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

# Skill 실행을 포함한 입력
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
    "EXECUTE": execute_node,  # Skills 자동 실행
    "VERIFY": verify_node,
    "REPORT": report_node,
}

# 실행
state = run_v2(input_payload, nodes)

# 실행 결과 확인
execute_result = state.outputs.get("EXECUTE", {})
if execute_result.get("status") == "success":
    print(f"✅ Skill 실행 성공: {execute_result['skill_id']}")
    print(f"Result: {execute_result['result']}")
else:
    print(f"❌ Skill 실행 실패: {execute_result.get('reason', 'Unknown')}")
```

---

## 실전 예제

### 예제 1: YouTube 스펙 생성

```python
from AFO.afo_skills_registry import SkillRegistry

registry = SkillRegistry()

# YouTube 스펙 생성 스킬 실행
result = await registry.execute_skill(
    skill_id="skill_001_youtube_spec_gen",
    parameters={
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    },
    timeout_seconds=60
)

if result.status == "completed":
    n8n_spec = result.result.get("node_spec")
    print(f"✅ n8n 워크플로우 스펙 생성 완료")
    print(f"Spec: {n8n_spec}")
```

### 예제 2: RAG 시스템 구축

```python
from AFO.afo_skills_registry import SkillRegistry

registry = SkillRegistry()

# Ultimate RAG 스킬 실행
result = await registry.execute_skill(
    skill_id="skill_002_ultimate_rag",
    parameters={
        "query": "FastAPI 보안 best practices",
        "top_k": 5
    },
    timeout_seconds=30
)

if result.status == "completed":
    documents = result.result.get("documents", [])
    print(f"✅ {len(documents)}개 문서 검색 완료")
    for doc in documents:
        print(f"- {doc.get('title', 'Untitled')}")
```

### 예제 3: 시스템 건강 모니터링

```python
from AFO.afo_skills_registry import SkillRegistry

registry = SkillRegistry()

# Health Monitor 스킬 실행
result = await registry.execute_skill(
    skill_id="skill_003_health_monitor",
    parameters={},
    timeout_seconds=10
)

if result.status == "completed":
    health_data = result.result.get("data", {})
    trinity_score = health_data.get("trinity_score", 0)
    print(f"✅ 시스템 건강 점검 완료")
    print(f"Trinity Score: {trinity_score:.1f}/100")
```

### 예제 4: Chancellor Graph V2와 함께 사용

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

# Context7 + Sequential Thinking + Skills 통합 실행
input_payload = {
    "command": "YouTube 스펙 생성 후 RAG 검색",
    "skill_id": "skill_001_youtube_spec_gen",
    "parameters": {
        "youtube_url": "https://www.youtube.com/watch?v=..."
    }
}

nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,  # Context7 + Sequential Thinking 자동 적용
    "GOODNESS": goodness_node,  # Context7 + Sequential Thinking 자동 적용
    "BEAUTY": beauty_node,  # Context7 + Sequential Thinking 자동 적용
    "MERGE": merge_node,  # Context7 + Sequential Thinking 자동 적용
    "EXECUTE": execute_node,  # Skills 자동 실행
    "VERIFY": verify_node,  # Context7 + Sequential Thinking 자동 적용
    "REPORT": report_node,
}

state = run_v2(input_payload, nodes)

# 전체 결과 확인
print("=== Context7 주입 결과 ===")
for step, context in state.outputs.get("context7", {}).items():
    print(f"{step}: {context.get('context', '')[:100]}...")

print("\n=== Sequential Thinking 결과 ===")
for step, thinking in state.outputs.get("sequential_thinking", {}).items():
    print(f"{step}: Truth={thinking['metadata']['truth_impact']:.2f}, Serenity={thinking['metadata']['serenity_impact']:.2f}")

print("\n=== Skill 실행 결과 ===")
execute_result = state.outputs.get("EXECUTE", {})
print(f"Status: {execute_result.get('status')}")
print(f"Skill ID: {execute_result.get('skill_id')}")
print(f"Result: {execute_result.get('result', {})}")
```

---

## 트러블슈팅

### 문제 1: Skill을 찾을 수 없음

**증상**: `Skill '{skill_id}' not found`

**해결**:
1. 스킬 ID 확인:
   ```python
   registry = SkillRegistry()
   all_skills = registry.list_all()
   skill_ids = [s.skill_id for s in all_skills]
   print(f"Available Skills: {skill_ids}")
   ```

2. Core Skills 등록 확인:
   ```python
   from AFO.afo_skills_registry import register_core_skills
   
   registry = SkillRegistry()
   if registry.count() < 5:
       register_core_skills()
       print(f"✅ {registry.count()} skills registered")
   ```

### 문제 2: Stage 2 Allowlist 차단

**증상**: `EXECUTE blocked: {reason}`

**해결**:
1. Allowlist 확인:
   ```python
   from api.guards.skills_allowlist_guard import is_skill_allowed
   
   allowed, reason = is_skill_allowed("skill_id")
   if not allowed:
       print(f"❌ 차단 사유: {reason}")
   ```

2. Allowlist에 스킬 추가:
   - `api/guards/skills_allowlist_guard.py` 수정
   - 또는 환경 변수로 허용 목록 설정

### 문제 3: 실행 타임아웃

**증상**: `TimeoutError` 또는 실행이 완료되지 않음

**해결**:
1. 타임아웃 시간 증가:
   ```python
   result = await registry.execute_skill(
       skill_id="skill_id",
       parameters={},
       timeout_seconds=120  # 기본값 30초에서 증가
   )
   ```

2. 스킬 실행 모드 확인:
   ```python
   skill = registry.get("skill_id")
   if skill:
       print(f"Execution Mode: {skill.execution_mode}")
       print(f"Estimated Duration: {skill.estimated_duration_ms}ms")
   ```

### 문제 4: Philosophy Score가 낮음

**증상**: 스킬의 Trinity Score가 기준 미만

**해결**:
1. Philosophy Score 확인:
   ```python
   skill = registry.get("skill_id")
   if skill:
       print(f"Philosophy: {skill.philosophy_scores.summary}")
       print(f"Average: {skill.philosophy_scores.average:.1f}%")
   ```

2. 스킬 개선:
   - Truth: 기술적 정확성 향상
   - Goodness: 안정성 및 보안 강화
   - Beauty: 코드 구조 개선
   - Serenity: 사용 편의성 향상

---

## 최적화 팁

### 1. 싱글톤 패턴 활용

Skill Registry는 싱글톤이므로 여러 번 인스턴스화해도 성능 영향이 없습니다:

```python
# ✅ 좋은 예: 싱글톤 활용
registry1 = SkillRegistry()
registry2 = SkillRegistry()
assert registry1 is registry2  # 같은 인스턴스
```

### 2. 필터링 최적화

필터링을 사용하여 필요한 스킬만 조회:

```python
# ✅ 좋은 예: 필터링 사용
filters = SkillFilterParams(
    category=SkillCategory.RAG_SYSTEMS,
    min_philosophy_avg=90,
    limit=5
)
skills = registry.filter(filters)

# ❌ 나쁜 예: 전체 조회 후 필터링
all_skills = registry.list_all()
filtered = [s for s in all_skills if s.category == SkillCategory.RAG_SYSTEMS]
```

### 3. DRY_RUN 활용

실제 실행 전 DRY_RUN으로 검증:

```python
# ✅ 좋은 예: DRY_RUN 먼저
dry_result = await registry.execute_skill(
    skill_id="skill_id",
    parameters={},
    dry_run=True
)

if dry_result.status == "dry_run_success":
    # 실제 실행
    result = await registry.execute_skill(
        skill_id="skill_id",
        parameters={},
        dry_run=False
    )
```

---

## 참고 자료

- [Skill Registry 구현](../packages/afo-core/afo_skills_registry.py)
- [Skills API 라우터](../packages/afo-core/api/routes/skills.py)
- [Skills Service](../packages/afo-core/api/services/skills_service.py)
- [Chancellor Graph V2 EXECUTE 노드](../packages/afo-core/api/chancellor_v2/graph/nodes/execute_node.py)
- [Skills Marketplace](../skills/marketplace.json)

---

**작성일**: 2025-12-25  
**버전**: 1.0.0  
**Trinity Score**: 眞 90% | 善 85% | 美 90% | 孝 95% | 永 85%

