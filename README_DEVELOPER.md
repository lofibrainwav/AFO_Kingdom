# 🏗️ AFO 왕국 개발자 가이드 (Republic Edition)

> **개발자를 위한 실용적 가이드**
>
> **眞善美孝永 철학을 코드로 구현하는 기술 문서**

<div align="center">

## 🚀 빠른 시작 (Quick Start)

```bash
# 1. 환경 설정
git clone https://github.com/lofibrainwav/AFO_Kingdom.git
cd AFO_Kingdom

# 2. 의존성 설치
pip install -e ".[dev]"

# 3. 환경 변수 설정
cp .env.example .env
# API 키들을 설정하세요

# 4. 데이터베이스 초기화
docker-compose up -d postgres redis qdrant

# 5. 개발 서버 실행
uvicorn packages.afo_core.api.api_server:app --reload --port 8010

# 6. 테스트 실행
pytest packages/afo-core/tests/ -v --cov=packages/afo-core
```

</div>

---

## 📦 프로젝트 구조 (Architecture)

### 🏛️ 4계층 아키텍처

```
AFO_Kingdom/
├── packages/
│   ├── afo-core/           # 🧠 Domain + Application Layer
│   │   ├── AFO/           # 핵심 도메인 로직
│   │   │   ├── api/       # FastAPI 라우터 및 미들웨어
│   │   │   ├── llm/       # LLM 프로바이더 (Gemini, Claude, GPT)
│   │   │   ├── services/  # 비즈니스 서비스
│   │   │   └── trinity/   # 眞善美孝永 계산 엔진
│   │   └── tests/         # 단위/통합 테스트
│   │
│   ├── trinity-os/        # 🧪 Trinity OS 엔진
│   │   ├── trinity_os/    # 철학 계산 및 페르소나 관리
│   │   └── skills/        # 19개 스킬 구현체
│   │
│   └── dashboard/         # 🎨 Presentation Layer
│       ├── src/
│       │   ├── app/       # Next.js 16 App Router
│       │   ├── components/# React 컴포넌트
│       │   └── lib/       # 유틸리티 함수
│       └── public/        # 정적 파일
│
├── docs/                  # 📚 문서화
├── scripts/               # 🛠️ 자동화 스크립트
├── tests/                 # 🧪 E2E 테스트
└── tools/                 # 🔧 개발 도구
```

### 🔧 기술 스택

| 계층 | 기술 | 버전 | 목적 |
|-----|------|------|------|
| **Frontend** | Next.js | 16+ | React 기반 웹 애플리케이션 |
| | TypeScript | 5.x | 타입 안전성 |
| | Tailwind CSS | 4.x | 유틸리티 퍼스트 CSS |
| **Backend** | Python | 3.12+ | 핵심 언어 |
| | FastAPI | 0.104+ | REST API 프레임워크 |
| | LangGraph | 0.1.x | LLM 워크플로우 |
| | Pydantic | 2.x | 데이터 검증 |
| **Database** | PostgreSQL | 15+ | 관계형 데이터 |
| | Redis | 7+ | 캐시 및 세션 |
| | Qdrant | 1.7+ | 벡터 데이터베이스 |
| **Infrastructure** | Docker | 24+ | 컨테이너화 |
| | uv | 0.9+ | 패키지 관리자 |

---

## 🛠️ 개발 워크플로우 (Development Workflow)

### 📋 로컬 개발 환경 설정

```bash
# 1. Python 환경
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -e ".[dev]"

# 3. Pre-commit 훅 설치
pre-commit install

# 4. 환경 변수 복사 및 설정
cp .env.example .env
# .env 파일에 필요한 API 키들을 입력

# 5. 데이터베이스 실행
docker-compose up -d postgres redis qdrant

# 6. 마이그레이션 실행 (필요시)
alembic upgrade head
```

### 🚀 개발 서버 실행

```bash
# Backend API 서버 (포트 8010)
uvicorn packages.afo_core.api.api_server:app --reload

# Frontend 대시보드 (포트 3000)
cd packages/dashboard
npm run dev

# Trinity OS 서버 (포트 8011)
python -m packages.trinity_os.run_trinity_os
```

### 🧪 테스트 실행

```bash
# 전체 테스트 실행
pytest

# 특정 패키지 테스트
pytest packages/afo-core/tests/

# 커버리지 리포트
pytest --cov=packages/afo-core --cov-report=html
open htmlcov/index.html

# 특정 테스트만 실행
pytest packages/afo-core/tests/test_rag_streaming.py -v

# TDD 모드로 파일 변경 감지
pytest-watch
```

### 🔧 코드 품질 관리

```bash
# 린팅 및 포맷팅
ruff check packages/ --fix
ruff format packages/

# 타입 체크
mypy packages/afo-core --strict

# 보안 취약점 검사
trivy fs .

# 시크릿 검사
gitleaks detect --verbose --redact
```

---

## 📋 API 엔드포인트 (API Endpoints)

### 🔐 인증 및 권한

```bash
# API 키 검증
GET /api/auth/verify

# 사용자 권한 확인
GET /api/auth/permissions

# 세션 관리
POST /api/auth/session
DELETE /api/auth/session
```

### 🤖 RAG 스트리밍

```bash
# 스트리밍 시작
POST /api/rag/start
{
  "checkpoint_id": "cp_123",
  "fork_name": "feature_branch",
  "run_config": {...}
}

# 실시간 스트리밍
GET /api/rag/stream?run_id=run_456
# Server-Sent Events (SSE) 응답

# 스트리밍 중단
POST /api/rag/interrupt
{
  "run_id": "run_456"
}

# 스트리밍 재개
POST /api/rag/resume
{
  "run_id": "run_456"
}

# 상태 조회
GET /api/rag/status/{run_id}
```

### 📊 트리니티 메트릭

```bash
# 현재 5기둥 점수 조회
GET /api/5pillars/current

# 실시간 평가 시작
POST /api/5pillars/live

# 가족 허브 데이터
GET /api/5pillars/family/hub/data
POST /api/5pillars/family/hub/member/update
```

### 🔍 검색 및 분석

```bash
# 컨텍스트 검색
GET /api/search?q=query&context=true

# 코드 분석
POST /api/analyze/code
{
  "code": "def hello(): pass",
  "language": "python"
}

# Trinity 점수 계산
POST /api/trinity/calculate
{
  "actions": [...],
  "context": {...}
}
```

---

## 🔧 개발 도구 및 스크립트

### 📜 주요 스크립트

```bash
# 프로젝트 상태 점검
./scripts/health_check.sh

# CI 강화 게이트
./scripts/ci_hardening_gate.sh

# 문서 자동 생성
./scripts/generate_docs.py

# 데이터베이스 관리
./scripts/db_migrate.sh
./scripts/db_backup.sh

# 배포 준비
./scripts/build_production.sh
```

### 🐳 Docker 개발 환경

```bash
# 전체 스택 실행
docker-compose up -d

# 특정 서비스만 실행
docker-compose up postgres redis

# 로그 확인
docker-compose logs -f api

# 컨테이너 진입
docker-compose exec api bash
```

### 📊 모니터링 및 디버깅

```bash
# API 문서 (Swagger)
open http://localhost:8010/docs

# 대시보드
open http://localhost:3000

# 메트릭스
open http://localhost:8010/metrics

# 헬스 체크
curl http://localhost:8010/health

# 로그 스트리밍
tail -f logs/api.log
```

---

## 🧪 테스트 전략 (Testing Strategy)

### 🏗️ 테스트 피라미드

```
E2E Tests (10%)      ┌─────────────┐
Integration Tests    │     ███     │
Unit Tests (80%)     │   ███████   │
                     │ ██████████ │
                     └─────────────┘
```

### 📋 테스트 종류

```bash
# 단위 테스트 (Unit Tests)
pytest packages/afo-core/tests/unit/ -v

# 통합 테스트 (Integration Tests)
pytest packages/afo-core/tests/integration/ -v

# E2E 테스트 (End-to-End)
pytest tests/e2e/ -v

# 성능 테스트
pytest tests/performance/ -v --durations=10

# 스트리밍 테스트
pytest packages/afo-core/tests/test_rag_streaming.py -v
```

### 🎯 테스트 커버리지 목표

- **Backend**: 80% 이상
- **Frontend**: 70% 이상
- **Integration**: 90% 이상
- **Critical Path**: 95% 이상

---

## 🚀 배포 및 운영 (Deployment & Operations)

### 🏭 CI/CD 파이프라인

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        run: pytest --cov=packages --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
```

### 🐳 프로덕션 배포

```bash
# Docker 이미지 빌드
docker build -t afo-kingdom:latest .

# 컨테이너 실행
docker run -p 8010:8010 \
  -e DATABASE_URL=$DATABASE_URL \
  -e REDIS_URL=$REDIS_URL \
  afo-kingdom:latest

# Docker Compose (전체 스택)
docker-compose -f docker-compose.prod.yml up -d
```

### 📊 모니터링 및 로깅

```bash
# Prometheus 메트릭스
curl http://localhost:8010/metrics

# 헬스 체크
curl http://localhost:8010/health

# 로그 수집
docker-compose logs -f | tee logs/production.log

# 성능 모니터링
python -m py-spy top --pid $(pgrep uvicorn)
```

---

## 🤝 기여 가이드 (Contributing Guide)

### 📋 코드 스타일

```python
# ✅ Good: 명확하고 간결한 코드
def calculate_trinity_score(actions: list[dict], context: dict) -> float:
    """Calculate Trinity Score based on actions and context."""
    truth_score = sum(action.get('truth', 0) for action in actions)
    goodness_score = sum(action.get('goodness', 0) for action in actions)
    beauty_score = sum(action.get('beauty', 0) for action in actions)

    # 眞善美孝永 가중치 적용
    weights = {'truth': 0.35, 'goodness': 0.35, 'beauty': 0.20}
    total = sum(scores[k] * weights[k] for k in weights.keys())

    return min(100.0, max(0.0, total))
```

### 🔄 풀 리퀘스트 프로세스

1. **이슈 생성**: 문제를 명확히 설명
2. **브랜치 생성**: `feature/`, `fix/`, `docs/` 접두사 사용
3. **커밋**: 의미 있는 단위로 분리
4. **테스트**: 모든 테스트 통과 확인
5. **PR 생성**: 템플릿 준수
6. **리뷰**: 최소 1명 승인
7. **머지**: Squash and merge

### 📝 커밋 메시지 규칙

```
type(scope): description

[optional body]

[optional footer]
```

**타입 예시:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드/도구 변경

---

## 🆘 문제 해결 (Troubleshooting)

### 🚨 자주 발생하는 문제

#### 1. Import 에러
```bash
# PYTHONPATH 설정 확인
export PYTHONPATH="$PWD/packages:$PYTHONPATH"

# 의존성 재설치
pip install -e . --force-reinstall
```

#### 2. 데이터베이스 연결 실패
```bash
# PostgreSQL 상태 확인
docker-compose ps postgres

# 로그 확인
docker-compose logs postgres

# 재시작
docker-compose restart postgres
```

#### 3. Redis 연결 실패
```bash
# Redis 상태 확인
docker-compose ps redis

# 테스트 연결
redis-cli -h localhost ping
```

#### 4. 테스트 실패
```bash
# 캐시 삭제
pytest --cache-clear

# 특정 테스트 디버그
pytest -xvs packages/afo-core/tests/test_rag_streaming.py::test_streaming
```

---

## 📚 추가 리소스 (Additional Resources)

### 🎯 필독 문서
- **[왕국의 철학](README.md)** - AFO 왕국의 비전과 정신
- **[아키텍처 맵](docs/ARCHITECTURE_MAP.md)** - 시스템 전체 구조
- **[API 레퍼런스](docs/API_ENDPOINTS_REFERENCE.md)** - 상세 엔드포인트 문서
- **[보안 가이드](SECURITY.md)** - 보안 정책 및 절차

### 🔧 개발 도구
- **[Cursor IDE](https://cursor.sh/)** - 추천 개발 환경
- **[uv](https://github.com/astral-sh/uv)** - 초고속 패키지 관리자
- **[Ruff](https://github.com/astral-sh/ruff)** - 빠른 린터/포맷터
- **[MyPy](https://mypy-lang.org/)** - 정적 타입 체커

### 📊 모니터링 도구
- **Prometheus**: 메트릭스 수집
- **Grafana**: 시각화 대시보드
- **Sentry**: 에러 트래킹
- **DataDog**: 전체 모니터링

---

## 🎯 다음 단계 (Next Steps)

### 🚀 초보자용
1. [빠른 시작](#빠른-시작-quick-start) 따라하기
2. 간단한 API 엔드포인트 추가해보기
3. 테스트 작성해보기
4. PR 제출하기

### 🏆 고급 사용자용
1. 새로운 LLM 프로바이더 추가
2. 커스텀 미들웨어 구현
3. 성능 최적화
4. 새로운 Trinity 메트릭 개발

### 🤝 기여자용
1. [기여 가이드](CONTRIBUTING.md) 숙지
2. 이슈 할당받기
3. 코드 리뷰 참여
4. 문서화 개선

---

<div align="center">

## 🎭 개발자의 서약

**"코드로 세상을 바꾸는 것은 책임이자 특권이다."**

**함께 AFO 왕국의 미래를 만들어 나갑시다!** ⚔️🛡️⚖️♾️

</div>

---

**📅 마지막 업데이트**: 2026년 1월 3일  
**👥 기여자**: AFO 왕국 개발팀  
**📧 문의**: [GitHub Issues](https://github.com/lofibrainwav/AFO_Kingdom/issues)
