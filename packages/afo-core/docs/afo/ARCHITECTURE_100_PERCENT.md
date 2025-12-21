# 🏗️ AFO 왕국 아키텍처 100% 완전 분석

**작성일**: 2025-12-17
**목적**: 아키텍처 및 구현 100% 완전 이해
**범위**: 전체 시스템 아키텍처, 데이터 흐름, 컴포넌트 상호작용

---

## 📊 시스템 아키텍처 개요

### 계층 구조 (Layered Architecture)

```
┌─────────────────────────────────────────────────────────┐
│ Presentation Layer (API 레이어)                        │
│ - FastAPI 엔드포인트                                    │
│ - 라우터 (Routers)                                      │
│ - 요청/응답 모델 (Pydantic)                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Application Layer (비즈니스 로직)                       │
│ - 서비스 (Services)                                     │
│ - 스킬 레지스트리 (Skills Registry)                     │
│ - LLM 라우터 (LLM Router)                               │
│ - Chancellor Graph (LangGraph)                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Domain Layer (도메인 모델)                             │
│ - 5기둥 모델 (Pillars)                                  │
│ - 스킬 카드 (Skill Cards)                               │
│ - 상태 모델 (State Models)                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Infrastructure Layer (인프라)                          │
│ - 데이터베이스 (PostgreSQL)                             │
│ - 캐시 (Redis)                                          │
│ - 벡터 DB (Qdrant)                                     │
│ - 외부 API (OpenAI, Anthropic, etc.)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 데이터 흐름 (Data Flow)

### 1. API 요청 흐름

```
Client Request
    ↓
FastAPI (api_server.py)
    ├─ 미들웨어 (CORS, 로깅 등)
    ├─ 라우터 분기
    │   ├─ /api/health → health_router
    │   ├─ /api/skills → skills_router
    │   ├─ /api/5pillars → pillars_router
    │   ├─ /api/crag → crag_router
    │   ├─ /api/ragas → ragas_router
    │   ├─ /api/system → system_health_router
    │   └─ /chancellor → chancellor_router
    ↓
Service Layer
    ├─ SkillsService
    ├─ DatabaseService
    ├─ CacheService
    └─ LLMRouterService
    ↓
Infrastructure
    ├─ PostgreSQL (장기 기억)
    ├─ Redis (실시간 캐시)
    ├─ Qdrant (벡터 검색)
    └─ External APIs
    ↓
Response
```

### 2. Chancellor Graph 흐름

```
User Query
    ↓
Chancellor Graph (LangGraph)
    ├─ State Management (Redis Checkpoint)
    ├─ Routing Logic
    │   ├─ Trinity Score ≥ 90 & Risk ≤ 10 → AUTO_RUN
    │   └─ Otherwise → ASK
    ├─ 3 Strategists
    │   ├─ Zhuge Liang (眞) - Architecture & Strategy
    │   ├─ Sima Yi (善) - Risk & Ethics
    │   └─ Zhou Yu (美) - Narrative & UX
    └─ Final Response
```

### 3. RAG 시스템 흐름

```
User Query
    ↓
RAG Graph (LangGraph)
    ├─ Retrieve Node
    │   ├─ Qdrant Vector Search
    │   └─ Document Retrieval
    ├─ Generate Node
    │   ├─ LLM Router (Ollama → Gemini → Claude → OpenAI)
    │   └─ Answer Generation
    └─ Response
```

---

## 🧩 핵심 컴포넌트

### 1. API 서버 (`api_server.py`)

**역할**: FastAPI 애플리케이션 진입점

**주요 구성**:
- FastAPI 앱 인스턴스
- 라우터 등록
- 미들웨어 설정
- CORS 설정

**등록된 라우터**:
- `health_router` - `/health`
- `root_router` - `/`
- `chancellor_router` - `/chancellor`
- `skills_router` - `/api/skills`
- `pillars_router` - `/api/5pillars`
- `crag_router` - `/api/crag`
- `ragas_router` - `/api/ragas`
- `system_health_router` - `/api/system`

### 2. 라우터 구조

#### `api/routers/` (기본 라우터)
- `health.py` - 시스템 건강 체크
- `root.py` - 루트 엔드포인트
- `chancellor_router.py` - Chancellor Graph 호출

#### `api/routes/` (기능별 라우터)
- `skills.py` - 스킬 레지스트리
- `pillars.py` - 5기둥 API
- `crag.py` - CRAG (Corrective RAG)
- `ragas.py` - RAG 평가
- `system_health.py` - 시스템 메트릭
- `wallet/` - API Wallet 관련

### 3. 서비스 레이어

#### `AFO/services/`
- `database.py` - PostgreSQL 연결 관리
- `hybrid_rag.py` - 하이브리드 RAG 서비스
- `skills_service.py` - 스킬 실행 서비스

### 4. 유틸리티

#### `AFO/utils/`
- `redis_connection.py` - Redis 연결 관리
- `cache_utils.py` - 캐시 유틸리티
- `container_detector.py` - 컨테이너 감지
- `dry_run.py` - DRY_RUN 유틸리티
- `exponential_backoff.py` - 재시도 로직
- `framework_selector.py` - 프레임워크 선택
- `friction_calibrator.py` - 마찰 보정
- `lazy_imports.py` - 지연 로딩

### 5. 설정 관리

#### `config/`
- `settings.py` - 기본 설정 (30+ 항목)
- `settings_dev.py` - 개발 환경
- `settings_prod.py` - 프로덕션 환경
- `settings_test.py` - 테스트 환경
- `antigravity.py` - AntiGravity 설정

---

## 🔌 통합 포인트

### 1. 데이터베이스 통합

**PostgreSQL**:
- 연결: `AFO/services/database.py::get_db_connection()`
- 설정: `config/settings.py::POSTGRES_*`
- 포트: 15432 (Docker 포트 포워딩)

**Redis**:
- 연결: `AFO/utils/redis_connection.py::get_redis_client()`
- 설정: `config/settings.py::REDIS_*`
- 포트: 6379

**Qdrant**:
- 연결: 직접 `QdrantClient` 사용
- 설정: `config/settings.py::QDRANT_URL`
- 포트: 6333

### 2. 외부 API 통합

**LLM Router** (`llm_router.py`):
- 순서: Ollama → Gemini → Claude → OpenAI
- 폴백 메커니즘
- 비용 최적화

**API Wallet**:
- 엔드포인트: `config/settings.py::API_WALLET_URL`
- 키 관리: PostgreSQL 저장
- 암호화: `API_WALLET_ENCRYPTION_KEY`

### 3. LangGraph 통합

**Chancellor Graph**:
- 파일: `chancellor_graph.py`
- 상태 관리: Redis Checkpoint
- 라우팅: Trinity Score 기반

**RAG Graph**:
- 파일: `scripts/rag/rag_graph.py`
- 노드: retrieve, generate
- 벡터 검색: Qdrant

---

## 📡 API 엔드포인트 전체 목록

### 루트 및 기본
- `GET /` - 루트 엔드포인트 (API 메타데이터)
- `GET /health` - 시스템 건강 체크 (11-오장육부)
- `GET /health_old` - 레거시 헬스체크 (하위 호환성)

### Health & System (`/api/system`)
- `GET /api/system/metrics` - 시스템 메트릭 (메모리, 디스크, Redis 등)
- `GET /api/system/logs/stream` - 로그 스트리밍 (SSE)

### Skills (`/api/skills`)
- `GET /api/skills/list` - 스킬 목록 (필터링, 페이지네이션)
- `GET /api/skills/{skill_id}` - 스킬 상세 조회
- `POST /api/skills/` - 스킬 등록
- `POST /api/skills/{skill_id}/execute` - 스킬 실행
- `DELETE /api/skills/{skill_id}` - 스킬 삭제
- `GET /api/skills/stats` - 스킬 통계
- `GET /api/skills/categories` - 카테고리 목록
- `GET /api/skills/health` - 스킬 서비스 헬스체크

### 5 Pillars (`/api/5pillars`)
- `GET /api/5pillars/current` - 현재 5기둥 점수
- `POST /api/5pillars/live` - 실시간 5기둥 평가 (LangFlow 연동)
- `GET /api/5pillars/family/hub` - 가족 허브 전체 상태

### RAG (`/api/crag`, `/api/ragas`)
- `POST /api/crag` - CRAG 질의 (문서 채점 + 웹 검색 fallback)
- `POST /api/ragas/evaluate` - Ragas 평가
- `POST /api/ragas/benchmark` - Ragas 벤치마크
- `GET /api/ragas/metrics` - Ragas 메트릭 조회

### Chancellor (`/chancellor`)
- `POST /chancellor/invoke` - Chancellor Graph 호출 (LangGraph)

### Wallet (`/api/wallet`)
- `GET /api/wallet/keys` - 키 조회
- `POST /api/wallet/keys` - 키 추가
- `GET /api/wallet/billing` - 결제 정보
- `POST /api/wallet/browser_bridge` - 브라우저 브릿지

### 기타 (api_server.py 직접 정의)
- `POST /api/command` - 명령 실행
- `POST /api/rag/query` - RAG 질의
- `POST /api/browser/click` - 브라우저 클릭
- `POST /api/browser/type` - 브라우저 타이핑
- `POST /api/browser/key` - 브라우저 키 입력
- `POST /api/browser/scroll` - 브라우저 스크롤
- `POST /api/crewai/execute` - CrewAI 실행
- `POST /api/langchain/tools` - LangChain 도구
- `POST /api/langchain/retrieval-qa` - LangChain Retrieval QA

---

## 🧠 11-오장육부 시스템

### 장기 매핑

| 장기 | 역할 | 메트릭 | 상태 확인 |
|------|------|--------|----------|
| **Brain** | 장기 기억 | PostgreSQL | `get_db_connection()` |
| **Heart** | 실시간 캐시 | Redis | `get_redis_client()` |
| **Lungs** | 벡터 DB | Qdrant | `QdrantClient` |
| **Digestive** | 내부 지력 | Ollama | `/api/tags` |
| **Immune** | 보호 시스템 | General | - |
| **Musculoskeletal** | 인프라 | General | - |
| **Endocrine** | 스케줄링 | General | - |
| **Nervous** | 네트워크/API | API Server | `/health` |
| **Reproductive** | 백업 | General | - |
| **Circulatory** | 데이터 흐름 | Redis | - |
| **Integumentary** | 방화벽/게이트웨이 | General | - |

### 건강 점수 계산

```python
# Brain (Memory)
brain_score = max(0, 100 - memory_percent)

# Heart (Redis)
heart_score = 100 if redis_connected else 0

# Lungs (Qdrant)
lungs_score = max(0, 100 - swap_percent)

# Digestive (Ollama)
digestive_score = max(0, 100 - disk_percent)
```

---

## 🔄 LLM Router 동작 원리

### 라우팅 순서

1. **Ollama** (로컬, 무료)
   - URL: `OLLAMA_BASE_URL` (기본: http://localhost:11434)
   - 모델: `OLLAMA_MODEL` (기본: llama3.2)
   - 실패 시 → 다음 단계

2. **Gemini** (Google)
   - API Key: `GEMINI_API_KEY` 또는 `GOOGLE_API_KEY`
   - 실패 시 → 다음 단계

3. **Claude** (Anthropic)
   - API Key: `ANTHROPIC_API_KEY`
   - 실패 시 → 다음 단계

4. **OpenAI** (최종 폴백)
   - API Key: `OPENAI_API_KEY`
   - 모델: GPT-4o-mini (기본)

### 비용 최적화
- 로컬 우선 (Ollama)
- 저비용 모델 우선
- 실패 시에만 다음 단계

---

## 🎯 스킬 시스템

### 스킬 레지스트리 구조

```python
AFOSkillCard(
    skill_id: str
    name: str
    description: str
    category: str
    execution_mode: str
    parameters: dict
    philosophy_scores: {
        "truth": float
        "goodness": float
        "beauty": float
        "serenity": float
    }
)
```

### 스킬 실행 흐름

```
Skill Execute Request
    ↓
SkillsService.execute_skill()
    ├─ 스킬 검증
    ├─ 파라미터 검증
    ├─ 실행 모드 확인
    │   ├─ sync → 직접 실행
    │   ├─ async → 비동기 실행
    │   └─ mcp → MCP 서버 실행
    └─ 결과 반환
```

---

## 🔐 인증 및 보안

### API Wallet
- 키 저장: PostgreSQL 암호화 저장
- 키 추출: `scripts/export_keys.py`
- 브라우저 인증: `browser_auth/` 모듈

### 환경 변수 관리
- 중앙 설정: `config/settings.py`
- 환경별 분리: dev, prod, test
- 암호화 키: `API_WALLET_ENCRYPTION_KEY`

---

## 📊 모니터링 및 로깅

### 메트릭 수집
- 시스템 메트릭: `api/routes/system_health.py`
- 5기둥 점수: `api/routes/pillars.py`
- 스킬 통계: `api/routes/skills.py`

### 로깅
- 구조화된 로깅
- Redis 기반 로그 스트리밍
- SSE (Server-Sent Events) 지원

---

## 🚀 배포 및 실행

### 개발 환경
- 설정: `settings_dev.py`
- 포트: 8010 (API Server)
- Mock 모드: 활성화

### 프로덕션 환경
- 설정: `settings_prod.py`
- 포트: 8010 (API Server)
- Mock 모드: 비활성화
- Sentry: 활성화

### 테스트 환경
- 설정: `settings_test.py`
- 포트: 15433 (PostgreSQL)
- Mock 모드: 활성화

---

## 🔗 저장소 간 통합

### AFO ↔ TRINITY-OS
- TRINITY-OS의 Personas 시스템
- AFO의 API 서버
- Bridge 로깅 통합

### AFO ↔ SixXon
- SixXon Auth Broker
- AFO API Wallet
- MCP 통합

---

## 📈 성능 최적화

### 캐싱 전략
- Redis 캐시 (TTL: 300초)
- 함수 결과 캐싱 (`@cached` 데코레이터)
- 스킬 결과 캐싱

### 비동기 처리
- FastAPI 비동기 엔드포인트
- asyncpg (PostgreSQL 비동기)
- Redis 비동기 클라이언트

### 연결 풀링
- PostgreSQL 연결 풀
- Redis 연결 재사용
- 싱글톤 패턴

---

## 🎯 핵심 설계 원칙

### 1. 중앙 집중식 설정
- 모든 설정을 `config/settings.py`에서 관리
- 환경별 오버라이드 지원
- Fallback 메커니즘

### 2. 모듈화
- 라우터 분리
- 서비스 분리
- 유틸리티 분리

### 3. 타입 안전성
- Pydantic 모델
- 타입 힌트
- MyPy 검증

### 4. 에러 처리
- Graceful degradation
- Fallback 메커니즘
- 상세한 에러 메시지

### 5. 테스트 가능성
- 의존성 주입
- Mock 지원
- 테스트 환경 분리

---

## 🔍 완전한 데이터 흐름 예시

### 예시: 스킬 실행 요청

```
1. Client → POST /api/skills/{skill_id}/execute
   ↓
2. FastAPI → skills_router.execute_skill()
   ↓
3. SkillsService.execute_skill()
   ├─ 스킬 조회 (PostgreSQL 또는 메모리)
   ├─ 파라미터 검증
   └─ 실행 모드 확인
   ↓
4. 실행 모드별 분기
   ├─ sync → 직접 실행
   ├─ async → 비동기 실행
   └─ mcp → MCP 서버 호출
   ↓
5. 결과 반환
   ├─ 캐싱 (Redis, TTL: 300초)
   └─ 응답 생성
   ↓
6. Client ← JSON Response
```

### 예시: RAG 질의

```
1. Client → POST /api/crag
   ↓
2. FastAPI → crag_router.crag_endpoint()
   ↓
3. CRAG 파이프라인
   ├─ grade_documents() → LLM Router
   ├─ perform_web_fallback() → Tavily (필요 시)
   └─ generate_answer() → LLM Router
   ↓
4. LLM Router
   ├─ Ollama 시도
   ├─ Gemini 시도 (실패 시)
   ├─ Claude 시도 (실패 시)
   └─ OpenAI 시도 (최종)
   ↓
5. 결과 반환
   └─ Client ← CragResponse
```

---

## 🎯 眞善美孝永 구현

### 眞 (Truth) - 기술적 확실성
- ✅ 타입 힌트 (MyPy 검증)
- ✅ Pydantic 모델 검증
- ✅ 에러 처리 및 로깅
- ✅ 테스트 커버리지

### 善 (Goodness) - 윤리·안정성
- ✅ DRY_RUN 메커니즘
- ✅ 권한 검증
- ✅ 비용 최적화
- ✅ 안전한 폴백

### 美 (Beauty) - 단순함·우아함
- ✅ 모듈화된 구조
- ✅ 명확한 API
- ✅ 일관된 네이밍
- ✅ 간결한 코드

### 孝 (Serenity) - 평온·연속성
- ✅ 자동화 (AntiGravity)
- ✅ 마찰 제거 (중앙 설정)
- ✅ 빠른 피드백 (병렬 실행)
- ✅ 롤백 가능 (Git)

### 永 (Eternity) - 영속성
- ✅ 문서화
- ✅ 버전 관리
- ✅ 재현 가능성
- ✅ 지속 가능한 아키텍처

---

**상태**: ✅ 아키텍처 100% 완전 이해
**구현**: ✅ 구현 100% 완전 이해
