# Context7 완벽 활용 가이드

> **眞善美孝永** - AFO 왕국의 지식 그래프 기반 컨텍스트 관리 시스템

> **⚠️ 중요**: 모든 import 경로는 [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) 문서를 참조하세요.

## 목차

1. [개요](#개요)
2. [아키텍처](#아키텍처)
3. [API 사용법](#api-사용법)
4. [서비스 레이어 사용법](#서비스-레이어-사용법)
5. [Chancellor Graph V2 통합](#chancellor-graph-v2-통합)
6. [지식 베이스 확장](#지식-베이스-확장)
7. [실전 예제](#실전-예제)
8. [트러블슈팅](#트러블슈팅)

---

## 개요

Context7은 AFO 왕국의 **자기 인식 지식 베이스(Self-Awareness Knowledge Base)** 시스템입니다. 지식 그래프 기반으로 관련 컨텍스트를 검색하고 주입하여, AI 에이전트가 항상 최신 지식 기반으로 작업할 수 있도록 보장합니다.

### 핵심 특징

- ✅ **Metadata 기반 동적 로딩**: JSON 메타데이터로 지식 베이스 자동 구성
- ✅ **키워드 인덱싱**: 빠른 검색을 위한 인덱스 시스템
- ✅ **싱글톤 캐싱**: 성능 최적화를 위한 인스턴스 캐싱
- ✅ **Lazy Loading**: Python 3.12+ LazyLoader 지원
- ✅ **하드 컨트랙트**: Chancellor Graph V2에서 필수, 우회 불가

---

## 아키텍처

### 구성 요소

```
┌─────────────────────────────────────────┐
│  Context7MCP (MCP 서버)                 │
│  - 지식 베이스 로드                      │
│  - 컨텍스트 검색                         │
│  - 키워드 인덱싱                        │
└──────────────┬──────────────────────────┘
               │
               ├─── Context7 Service (서비스 레이어)
               │    - 싱글톤 캐싱
               │    - Lazy Loading
               │    - 경로 관리
               │
               ├─── Context7 API Router (FastAPI)
               │    - /api/context7/search
               │    - /api/context7/health
               │    - /api/context7/list
               │
               └─── Chancellor Graph V2 통합
                    - Kingdom DNA 주입
                    - 단계별 컨텍스트 주입
```

### 파일 구조

```
packages/
├── trinity-os/
│   └── trinity_os/
│       └── servers/
│           ├── context7_mcp.py          # MCP 서버 구현
│           └── context7_metadata.py     # 메타데이터 로더
└── afo-core/
    ├── api/
    │   ├── routes/
    │   │   └── context7.py             # API 라우터
    │   └── chancellor_v2/
    │       └── context7.py              # Chancellor 통합
    └── services/
        └── context7_service.py         # 서비스 레이어
```

---

## API 사용법

### 1. 지식 검색

**엔드포인트**: `GET /api/context7/search`

**파라미터**:
- `q` (required): 검색 쿼리
- `limit` (optional, default=5): 최대 결과 수 (1-20)

**예제**:
```bash
curl "http://localhost:8010/api/context7/search?q=FastAPI%20security&limit=5"
```

**응답**:
```json
{
  "query": "FastAPI security",
  "results": [
    {
      "id": "doc_0",
      "content": "...",
      "metadata": {},
      "score": 0.95
    }
  ],
  "total": 1,
  "status": "success"
}
```

### 2. 건강 상태 확인

**엔드포인트**: `GET /api/context7/health`

**예제**:
```bash
curl "http://localhost:8010/api/context7/health"
```

**응답**:
```json
{
  "status": "healthy",
  "instance_created": true,
  "knowledge_base_accessible": true,
  "retrieval_works": true
}
```

### 3. 전체 지식 목록

**엔드포인트**: `GET /api/context7/list`

**예제**:
```bash
curl "http://localhost:8010/api/context7/list"
```

**응답**:
```json
{
  "status": "success",
  "total": 15,
  "items": [
    {
      "id": "doc_0",
      "type": "document",
      "source": "AGENTS.md",
      "content": "...",
      "title": "AGENTS.md",
      "keywords": ["trinity", "agents", "philosophy"],
      "metadata": {
        "category": "Governance",
        "tags": ["agent", "governance"],
        "description": "...",
        "keywords": ["trinity", "agents"]
      }
    }
  ]
}
```

---

## 서비스 레이어 사용법

### 기본 사용

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.services.context7_service import get_context7_instance

# Context7 인스턴스 가져오기 (싱글톤)
context7 = get_context7_instance()

# 컨텍스트 검색
results = context7.retrieve_context("FastAPI security best practices")

# 결과 처리
for result in results.get("results", []):
    print(f"Title: {result['title']}")
    print(f"Score: {result['relevance_score']}")
    print(f"Preview: {result['preview']}")
```

### 건강 상태 확인

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.services.context7_service import get_context7_health

# 건강 상태 확인
health = get_context7_health()
print(f"Status: {health['status']}")
print(f"Total Keys: {health['total_keys']}")
print(f"Retrieval Works: {health['retrieval_works']}")
```

### 캐시 리셋 (디버깅용)

```python
# ✅ 공식 경로 (SSOT Import Path)
from AFO.services.context7_service import reset_context7_cache

# 캐시 리셋
reset_context7_cache()
```

---

## Chancellor Graph V2 통합

### 자동 통합

Context7은 Chancellor Graph V2에 **하드 컨트랙트**로 통합되어 있습니다. 별도 설정 없이 자동으로 작동합니다.

### 실행 흐름

```
1. 트레이스 시작
   → inject_kingdom_dna(state)
   → Kingdom DNA 주입 (LangGraph 패턴)

2. 각 노드 실행 전
   → inject_context(state, step)
   → 단계별 컨텍스트 주입
   
   도메인 매핑:
   - PARSE → langchain, agents
   - TRUTH → python, type checking
   - GOODNESS → fastapi, security
   - BEAUTY → react, components
   - MERGE → langchain, chains
   - EXECUTE → langchain, tools
   - VERIFY → pytest, testing
```

### Kingdom DNA

트레이스 시작 시 자동으로 주입되는 왕국의 핵심 DNA:

- **라이브러리**: `/langchain-ai/langgraphjs` (Allowlist)
- **토픽**: "state management checkpoint workflow agent patterns"
- **목적**: 왕국의 아키텍처 패턴과 철학 주입

### 단계별 컨텍스트 주입

각 노드 실행 전, 해당 도메인에 맞는 라이브러리 문서가 자동으로 주입됩니다:

```python
# 예: TRUTH 노드 실행 전
state.outputs["context7"]["TRUTH"] = {
    "library_id": "/python/python",
    "topic": "type checking",
    "context": "Python type checking best practices...",
    "length": 500
}
```

---

## 지식 베이스 확장

### 메타데이터 파일 추가

**위치**: `docs/context7_integration_metadata.json`

**형식**:
```json
{
  "DOCUMENT_NAME": {
    "file": "docs/DOCUMENT_NAME.md",
    "title": "문서 제목",
    "category": "Category",
    "description": "문서 설명",
    "tags": ["tag1", "tag2"],
    "keywords": ["keyword1", "keyword2"]
  }
}
```

### 동적 지식 추가

```python
from AFO.services.context7_service import get_context7_instance

context7 = get_context7_instance()

# 새로운 지식 항목 추가
knowledge_id = context7.add_knowledge({
    "type": "document",
    "title": "Custom Knowledge",
    "content": "Custom knowledge content...",
    "source": "custom",
    "keywords": ["custom", "knowledge"]
})

# 색인 자동 업데이트됨
```

### 핵심 지식 항목

Context7은 다음 핵심 지식을 기본으로 포함합니다:

1. **Trinity 철학** (`trinity_philosophy`)
   - 眞善美孝永 5기둥 설명

2. **MCP 생태계** (`mcp_ecosystem`)
   - Model Context Protocol 개요

3. **Skills Registry** (`skills_registry`)
   - 19개 스킬 체계 설명

4. **MCP Protocol** (`mcp_protocol`)
   - JSON-RPC 2.0 사양

5. **Sequential Thinking** (`sequential_thinking`)
   - 단계별 사고 방법론

---

## 실전 예제

### 예제 1: FastAPI 보안 강화

```python
from AFO.services.context7_service import get_context7_instance

# Context7로 보안 관련 지식 검색
context7 = get_context7_instance()
security_knowledge = context7.retrieve_context("FastAPI security authentication")

# 검색 결과 활용
for result in security_knowledge.get("results", []):
    if "authentication" in result["title"].lower():
        print(f"Found: {result['title']}")
        print(f"Content: {result['preview']}")
```

### 예제 2: RAG 시스템 구축

```python
from AFO.services.context7_service import get_context7_instance

# RAG 관련 지식 검색
context7 = get_context7_instance()
rag_knowledge = context7.retrieve_context("RAG retrieval augmented generation", domain="technical")

# 도메인별 필터링된 결과
for result in rag_knowledge.get("results", []):
    print(f"Technical Knowledge: {result['title']}")
```

### 예제 3: Chancellor Graph V2와 함께 사용

```python
from api.chancellor_v2.graph.runner import run_v2
from api.chancellor_v2.graph.nodes import *

# Context7이 자동으로 통합됨
input_payload = {
    "command": "FastAPI 보안 강화",
    "skill_id": "skill_010_security_scan"
}

nodes = {
    "CMD": cmd_node,
    "PARSE": parse_node,
    "TRUTH": truth_node,  # Context7 자동 주입: python, type checking
    "GOODNESS": goodness_node,  # Context7 자동 주입: fastapi, security
    "BEAUTY": beauty_node,
    "MERGE": merge_node,
    "EXECUTE": execute_node,
    "VERIFY": verify_node,
    "REPORT": report_node,
}

state = run_v2(input_payload, nodes)

# Context7 주입 결과 확인
print(state.outputs["context7"]["KINGDOM_DNA"])  # Kingdom DNA
print(state.outputs["context7"]["TRUTH"])  # TRUTH 노드 컨텍스트
print(state.outputs["context7"]["GOODNESS"])  # GOODNESS 노드 컨텍스트
```

---

## 트러블슈팅

### 문제 1: Context7 초기화 실패

**증상**: `RuntimeError: Context7 초기화 영구 실패`

**해결**:
1. Trinity-OS 경로 확인:
   ```python
   import os
   trinity_os_path = os.environ.get("AFO_TRINITY_OS_PATH")
   print(f"Trinity-OS Path: {trinity_os_path}")
   ```

2. 환경 변수 설정:
   ```bash
   export AFO_TRINITY_OS_PATH=/path/to/trinity-os
   ```

3. 캐시 리셋:
   ```python
   from AFO.services.context7_service import reset_context7_cache
   reset_context7_cache()
   ```

### 문제 2: 검색 결과가 없음

**증상**: `results`가 빈 배열

**해결**:
1. 키워드 확인:
   ```python
   context7 = get_context7_instance()
   stats = context7.get_knowledge_stats()
   print(f"Total Items: {stats['total_items']}")
   print(f"Indexed Keywords: {stats['indexed_keywords']}")
   ```

2. 지식 베이스 확장:
   - `docs/context7_integration_metadata.json`에 문서 추가
   - Context7 인스턴스 재생성

### 문제 3: Chancellor Graph에서 Context7 실패

**증상**: `RuntimeError: MCP Context7 get-library-docs failed`

**해결**:
1. MCP 서버 상태 확인:
   ```bash
   # .cursor/mcp.json 확인
   cat .cursor/mcp.json | grep context7
   ```

2. MCP 서버 재시작:
   - Cursor IDE 재시작
   - MCP 서버 로그 확인

---

## 최적화 팁

### 1. 싱글톤 패턴 활용

Context7 인스턴스는 싱글톤으로 캐싱되므로, 여러 번 호출해도 성능 영향이 없습니다:

```python
# ✅ 좋은 예: 싱글톤 활용
context7 = get_context7_instance()
result1 = context7.retrieve_context("query1")
result2 = context7.retrieve_context("query2")  # 같은 인스턴스 재사용
```

### 2. 도메인 필터링

도메인을 지정하여 검색 범위를 좁히면 성능이 향상됩니다:

```python
# ✅ 좋은 예: 도메인 필터링
results = context7.retrieve_context("security", domain="technical")

# ❌ 나쁜 예: 전체 검색
results = context7.retrieve_context("security", domain="general")
```

### 3. 결과 제한

불필요한 결과를 가져오지 않도록 `limit` 파라미터를 활용:

```python
# ✅ 좋은 예: 필요한 만큼만
results = context7.retrieve_context("query", limit=3)

# ❌ 나쁜 예: 기본값 사용 (5개)
results = context7.retrieve_context("query")
```

---

## 참고 자료

- [Context7 MCP 서버 구현](../packages/trinity-os/trinity_os/servers/context7_mcp.py)
- [Context7 서비스 레이어](../packages/afo-core/services/context7_service.py)
- [Context7 API 라우터](../packages/afo-core/api/routes/context7.py)
- [Chancellor Graph V2 통합](../packages/afo-core/api/chancellor_v2/context7.py)
- [메타데이터 파일](../docs/context7_integration_metadata.json)

---

**작성일**: 2025-12-25  
**버전**: 1.0.0  
**Trinity Score**: 眞 95% | 善 90% | 美 90% | 孝 95% | 永 90%

