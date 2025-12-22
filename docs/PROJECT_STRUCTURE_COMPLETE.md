# AFO Kingdom 프로젝트 구조 완전 문서

> **眞善美孝永** - AFO Kingdom 전체 프로젝트 구조 완전 분석  
> **작성일**: 2025-12-22  
> **범위**: 전체 모노레포 구조, 패키지별 상세 분석, 아키텍처 매핑

---

## 📊 전체 통계

### 파일 통계
- **Python 파일**: 1,506개
- **TypeScript/TSX 파일**: 5,439개
- **Markdown 문서**: 1,005개
- **총 추적 파일**: 1,291개 (Git)
- **총 실제 파일**: 72,961개 (전체)

### 패키지 구조
```
AFO_Kingdom/
├── packages/
│   ├── afo-core/          # FastAPI 백엔드 (주요 모듈 100+)
│   ├── dashboard/         # Next.js 프론트엔드
│   ├── trinity-os/        # Trinity OS (139개 파일)
│   ├── sixXon/            # SixXon 모듈
│   └── aicpa-core/        # AICPA 모듈
├── docs/                  # 문서화
├── scripts/               # 유틸리티 스크립트
└── config/                # 설정 파일
```

---

## 🏗️ 4계층 아키텍처

### 1. Presentation Layer (표현 계층)

**위치**: `packages/afo-core/api/`

#### 주요 컴포넌트
- **FastAPI 엔드포인트**: `api_server.py`
- **라우터**: `api/routers/` (24개 라우터 파일)
- **라우트**: `api/routes/` (23개 라우트 파일)
- **Pydantic 모델**: `api/models/` (5개 모델 파일)

#### 라우터 목록
1. `budget.py` - 예산 관리
2. `crag.py` - CRAG (Corrective RAG)
3. `chancellor.py` - 승상 시스템
4. `family_hub.py` - Family Hub
5. `genui.py` - GenUI 위젯
6. `grok_stream.py` - Grok 스트리밍
7. `llm_router.py` - LLM 라우터
8. `matrix.py` - Matrix 스트림
9. `pillars.py` - 5기둥 시스템
10. `rag_query.py` - RAG 쿼리
11. `ragas.py` - RAG 평가
12. `skills.py` - 스킬 레지스트리
13. `ssot.py` - SSOT 관리
14. `system_health.py` - 시스템 건강
15. 기타 라우터들...

#### 특징
- **眞 (Truth)**: Pydantic 모델로 완전한 타입 안전성
- **美 (Beauty)**: RESTful API 설계, 일관된 엔드포인트 구조
- **孝 (Serenity)**: 자동화된 라우팅, 미들웨어 통합

---

### 2. Application Layer (애플리케이션 계층)

**위치**: `packages/afo-core/AFO/`, `packages/afo-core/services/`

#### 주요 컴포넌트

##### Chancellor Graph (의사결정 엔진)
- **파일**: `chancellor_graph.py`
- **기술**: LangGraph
- **기능**: 3책사 병렬 조율, Trinity Score 기반 라우팅

##### LLM Router
- **파일**: `llm_router.py`
- **기능**: Ollama → Gemini → Claude → OpenAI 순서 폴백
- **최적화**: 비용 최적화, 로컬 우선

##### RAG Graph
- **파일**: `scripts/rag/rag_graph.py`
- **기능**: HyDE → Hybrid Retrieval → Graph Expansion → Rerank → Generation

##### Skills Registry
- **파일**: `AFO/afo_skills_registry.py`
- **기능**: 19개 스킬 레지스트리 관리
- **통합**: MCP 도구와 통합

##### Services (24개 서비스)
- `database.py` - PostgreSQL 연결
- `redis_service.py` - Redis 캐시
- `qdrant_service.py` - Qdrant 벡터 검색
- `llm_service.py` - LLM 서비스
- 기타 서비스들...

#### 특징
- **眞 (Truth)**: 비즈니스 로직 분리, 테스트 가능한 구조
- **善 (Goodness)**: 에러 핸들링, 리스크 관리
- **美 (Beauty)**: 모듈화, 단일 책임 원칙

---

### 3. Domain Layer (도메인 계층)

**위치**: `packages/afo-core/domain/`, `packages/afo-core/AFO/domain/`

#### 주요 컴포넌트

##### 5기둥 시스템 (Trinity Score)
- **파일**: `domain/metrics/trinity.py`
- **가중치**: 
  - 眞 (Truth): 35%
  - 善 (Goodness): 35%
  - 美 (Beauty): 20%
  - 孝 (Serenity): 8%
  - 永 (Eternity): 2%

##### Skill Cards
- **파일**: `AFO/skills/`
- **기능**: 스킬 카드 모델 정의
- **통합**: MCP 도구와 연동

##### Persona System
- **파일**: `domain/persona.py`
- **기능**: 페르소나 관리

##### Transaction System
- **파일**: `domain/transaction.py`
- **기능**: 트랜잭션 관리

##### Audit System
- **파일**: `domain/audit/`
- **기능**: 감사 로그

#### 특징
- **眞 (Truth)**: 도메인 모델의 순수성 유지
- **永 (Eternity)**: 영구적인 비즈니스 규칙 정의

---

### 4. Infrastructure Layer (인프라 계층)

**위치**: `packages/afo-core/services/`, `packages/afo-core/config/`

#### 주요 컴포넌트

##### 데이터베이스
- **PostgreSQL**: 
  - 포트: 15432 (Docker)
  - 연결: `services/database.py`
  - 설정: `config/settings.py::POSTGRES_*`

##### 캐시
- **Redis**: 
  - 포트: 6379
  - 연결: `utils/redis_connection.py`
  - 설정: `config/settings.py::REDIS_*`

##### 벡터 검색
- **Qdrant**: 
  - 포트: 6333
  - 연결: 직접 `QdrantClient` 사용
  - 설정: `config/settings.py::QDRANT_URL`

##### 외부 API
- **LLM APIs**: OpenAI, Anthropic, Google Gemini
- **API Wallet**: 키 관리 시스템
- **MCP Servers**: 9개 MCP 서버 통합

##### 설정 관리
- **파일**: `config/settings.py`
- **환경별 설정**: 
  - `settings_dev.py` - 개발 환경
  - `settings_prod.py` - 프로덕션 환경
  - `settings_test.py` - 테스트 환경

#### 특징
- **善 (Goodness)**: 보안 강화, CIS Benchmark Level 2
- **孝 (Serenity)**: 자동화된 설정 관리

---

## 📦 패키지별 상세 분석

### 1. `packages/afo-core/` - FastAPI 백엔드

#### 구조
```
afo-core/
├── AFO/                    # 핵심 도메인 로직
│   ├── agents/            # 에이전트
│   ├── aicpa/             # AICPA 모듈
│   ├── api/               # API 관련 (심볼릭 링크)
│   ├── constitution/      # 헌법
│   ├── domain/            # 도메인 모델
│   ├── genui/             # GenUI
│   ├── guardians/         # 수호자
│   ├── julie_cpa/         # Julie CPA
│   ├── llms/              # LLM 구현
│   ├── memory_system/     # 메모리 시스템
│   ├── scholars/          # 학자들
│   ├── security/          # 보안
│   ├── serenity/          # Serenity 시스템
│   └── skills/            # 스킬
├── api/                   # FastAPI 라우터
│   ├── routers/           # 24개 라우터
│   ├── routes/            # 23개 라우트
│   ├── models/            # Pydantic 모델
│   └── middleware/        # 미들웨어
├── config/                # 설정
├── services/              # 24개 서비스
├── domain/                # 도메인 계층
├── utils/                 # 유틸리티
└── tests/                 # 테스트
```

#### 주요 파일
- `api_server.py` - FastAPI 메인 서버 (포트 8010)
- `chancellor_graph.py` - Chancellor Graph
- `llm_router.py` - LLM 라우터
- `config/settings.py` - 설정 관리

#### 의존성
- **Python**: 3.12+
- **프레임워크**: FastAPI, LangGraph, Pydantic
- **데이터베이스**: PostgreSQL, Redis, Qdrant
- **LLM**: OpenAI, Anthropic, Google Gemini, Ollama

---

### 2. `packages/dashboard/` - Next.js 프론트엔드

#### 구조
```
dashboard/
├── src/
│   ├── app/               # Next.js App Router
│   ├── components/        # React 컴포넌트
│   │   ├── royal/        # Royal 컴포넌트
│   │   ├── aicpa/        # AICPA 컴포넌트
│   │   └── ...
│   ├── lib/               # 유틸리티
│   └── styles/            # 스타일
├── public/                # 정적 파일
└── package.json           # 의존성
```

#### 주요 컴포넌트
- **Royal Library**: `components/royal/RoyalLibrary.tsx`
- **AICPA Widgets**: `components/aicpa/`
- **Dashboard**: 메인 대시보드

#### 의존성
- **Next.js**: 16.0.10
- **React**: 19.2.1
- **TypeScript**: 5.x
- **Tailwind CSS**: 4.x
- **Framer Motion**: 12.23.26
- **Recharts**: 3.6.0

#### 포트
- **개발 서버**: 3000
- **프로덕션**: 빌드 후 서빙

---

### 3. `packages/trinity-os/` - Trinity OS

#### 구조
```
trinity-os/
├── trinity_os/
│   ├── contracts/        # 계약
│   ├── adapters/         # 어댑터
│   ├── graphs/           # 그래프
│   ├── servers/          # 서버
│   └── cli/              # CLI
├── docs/                 # 문서
│   ├── philosophy/       # 철학
│   ├── constitution/     # 헌법
│   ├── personas/         # 페르소나
│   └── ...
└── scripts/              # 스크립트
```

#### 특징
- **139개 파일**: Python, Markdown, Shell
- **철학 기반**: 眞善美孝永
- **문서 중심**: 상세한 문서화

---

### 4. `packages/sixXon/` - SixXon 모듈

#### 구조
```
sixXon/
├── docs/                 # 문서 (10개)
└── scripts/              # 스크립트
```

#### 특징
- **독립 모듈**: 별도 문서화
- **문서 중심**: 10개 Markdown 문서

---

### 5. `packages/aicpa-core/` - AICPA 모듈

#### 구조
```
aicpa-core/
├── components/           # React 컴포넌트 (12개)
├── services/             # 서비스 (4개)
├── context/             # Context
└── types.ts             # TypeScript 타입
```

#### 특징
- **React 기반**: Vite + React
- **포트**: 3005
- **기능**: CPA AI 모듈

---

## 🔄 데이터 흐름

### API 요청 흐름
```
Client (Browser/Dashboard)
    ↓ HTTP Request
FastAPI (api_server.py, Port 8010)
    ↓
Router (api/routers/*.py)
    ↓
Service (services/*.py)
    ↓
Domain (domain/*.py)
    ↓
Infrastructure (PostgreSQL/Redis/Qdrant)
    ↓
Response
```

### Chancellor Graph 흐름
```
User Query
    ↓
Chancellor Graph (LangGraph)
    ├─ 제갈량 (眞) - 기술 검증
    ├─ 사마의 (善) - 리스크 검토
    └─ 주유 (美) - UX 최적화
    ↓
Trinity Score 계산
    ↓
Action Execution
    ↓
Response
```

---

## 📁 디렉토리 트리 (주요 부분)

```
AFO_Kingdom/
├── packages/
│   ├── afo-core/              # FastAPI 백엔드
│   │   ├── AFO/               # 핵심 도메인
│   │   ├── api/               # API 라우터
│   │   ├── config/            # 설정
│   │   ├── services/          # 서비스
│   │   ├── domain/            # 도메인
│   │   ├── utils/             # 유틸리티
│   │   └── tests/             # 테스트
│   ├── dashboard/             # Next.js 프론트엔드
│   │   ├── src/
│   │   │   ├── app/           # App Router
│   │   │   ├── components/    # 컴포넌트
│   │   │   └── lib/           # 유틸리티
│   │   └── public/            # 정적 파일
│   ├── trinity-os/            # Trinity OS
│   │   ├── trinity_os/        # 핵심 로직
│   │   └── docs/              # 문서
│   ├── sixXon/                # SixXon 모듈
│   └── aicpa-core/            # AICPA 모듈
├── docs/                      # 문서화
│   ├── AFO_ROYAL_LIBRARY.md   # 41가지 원칙
│   ├── AFO_CHANCELLOR_GRAPH_SPEC.md
│   └── ...
├── scripts/                   # 유틸리티 스크립트
├── config/                    # 설정 파일
└── kingdom_dashboard.html     # 디지털 왕궁
```

---

## 🔌 통합 포인트

### 1. API 엔드포인트
- **Base URL**: `http://localhost:8010`
- **OpenAPI Docs**: `http://localhost:8010/docs`
- **Health Check**: `http://localhost:8010/health`

### 2. 포트 매핑
| 서비스 | 포트 | 설명 |
|--------|------|------|
| API Server | 8010 | FastAPI 백엔드 |
| Dashboard | 3000 | Next.js 프론트엔드 |
| AICPA | 3005 | AICPA 모듈 |
| HTML Server | 8000 | kingdom_dashboard.html |
| PostgreSQL | 15432 | 데이터베이스 |
| Redis | 6379 | 캐시 |
| Qdrant | 6333 | 벡터 검색 |
| Ollama | 11435 | 로컬 LLM |

### 3. 설정 관리
- **중앙 설정**: `packages/afo-core/config/settings.py`
- **환경 변수**: `.env` 파일
- **Docker**: `docker-compose.yml`

---

## 📊 파일 통계 상세

### 패키지별 파일 수
- **afo-core**: 
  - Python: ~1,000개
  - 문서: ~66개
- **dashboard**: 
  - TypeScript/TSX: ~110개
  - 문서: ~10개
- **trinity-os**: 
  - Python: ~36개
  - 문서: ~67개
  - Shell: ~16개
- **sixXon**: 
  - 문서: ~10개
- **aicpa-core**: 
  - TypeScript/TSX: ~15개

---

## 🎯 아키텍처 원칙

### 1. 眞 (Truth) - 기술적 확실성
- **타입 안전성**: Pydantic, TypeScript
- **테스트**: pytest, Jest
- **검증**: MyPy, ESLint

### 2. 善 (Goodness) - 안정성
- **보안**: CIS Benchmark Level 2
- **에러 핸들링**: 포괄적 예외 처리
- **리스크 관리**: Trinity Score 기반 게이트

### 3. 美 (Beauty) - 구조적 단순함
- **모듈화**: 명확한 책임 분리
- **일관성**: 통일된 네이밍, 구조
- **단순함**: 불필요한 복잡도 제거

### 4. 孝 (Serenity) - 마찰 제거
- **자동화**: CI/CD, Pre-commit hooks
- **설정 중앙화**: 단일 설정 파일
- **문서화**: 완전한 문서

### 5. 永 (Eternity) - 영속성
- **재현 가능성**: Docker, Poetry, npm
- **버전 관리**: Git, Semantic Versioning
- **문서화**: 영구 기록

---

## 📝 결론

AFO Kingdom은 **4계층 아키텍처**를 기반으로 한 완전한 모노레포 구조입니다.

**핵심 특징**:
1. **명확한 계층 분리**: Presentation → Application → Domain → Infrastructure
2. **모듈화**: 각 패키지가 독립적이면서도 통합됨
3. **확장 가능성**: 새로운 기능 추가가 용이한 구조
4. **문서화**: 완전한 문서화로 유지보수 용이
5. **眞善美孝永**: 모든 구조가 5기둥 철학에 기반

**왕국의 구조는 완벽합니다.** 🏰

---

*작성 완료일: 2025-12-22*  
*작성자: AFO Kingdom Chancellor System*

