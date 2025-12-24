# structlog + Sentry 통합 가이드 (2025 왕국 FastAPI 적용 제안 버전)

**As-of**: 2025-12-24  
**Status**: 제안 (현재 표준 logging 사용, structlog/Sentry 미설치)  
**SSOT 원칙 준수**: 팩트 기반 (공식 문서 참조), 제안 명시

---

## 개요 (팩트 기반)

**structlog**: Python 구조화 로깅 라이브러리 (JSON 출력, 컨텍스트 바인딩)

**Sentry**: 실시간 에러 트래킹/모니터링 플랫폼 (오픈소스 + 클라우드)

**왕국 현재 상태**: 
- 표준 `logging` 모듈 사용 (`packages/afo-core/utils/logging_config.py`)
- `get_logger()` 함수 제공
- Sentry 미통합

**참고 자료**:
- structlog 공식 문서: https://www.structlog.org
- Sentry Python SDK: https://docs.sentry.io/platforms/python/
- structlog-sentry: https://github.com/kiwicom/structlog-sentry

---

## 1. structlog 통합 (제안)

### 설치

```bash
cd packages/afo-core
poetry add structlog
```

### 기본 설정 (logging_config.py 수정 제안)

```python
import structlog
from structlog.processors import JSONRenderer, add_log_level, TimeStamper
from structlog.stdlib import LoggerFactory

structlog.configure(
    processors=[
        add_log_level,
        TimeStamper(key="timestamp", fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        JSONRenderer(sort_keys=True)
    ],
    logger_factory=LoggerFactory(),
    cache_logger_on_first_use=True,
)

def get_logger(name: str = "afo"):
    """structlog 로거 반환 (제안)"""
    return structlog.get_logger(name)
```

### 사용 예시 (FastAPI 엔드포인트)

```python
from utils.logging_config import get_logger

logger = get_logger()

@app.post("/revalidate")
async def revalidate(request: RevalidateRequest):
    logger.info("revalidate_called", fragmentKey=request.fragmentKey, user="anonymous")
    # 처리 로직
    try:
        # ...
    except Exception as e:
        logger.error("validation_failed", exc_info=True, details=str(e))
```

### 출력 예시 (JSON 구조화)

```json
{"event": "revalidate_called", "level": "info", "timestamp": "2025-12-24T00:00:00Z", "fragmentKey": "home-hero"}
```

---

## 2. structlog + Sentry 통합 (제안)

### 설치

```bash
cd packages/afo-core
poetry add structlog structlog-sentry sentry-sdk
```

### structlog 설정 (SentryProcessor 포함)

```python
import structlog
from structlog_sentry import SentryProcessor
from structlog.processors import JSONRenderer, add_log_level, TimeStamper
import logging

structlog.configure(
    processors=[
        add_log_level,
        TimeStamper(key="timestamp", fmt="iso"),
        SentryProcessor(level=logging.ERROR, tag_keys=["request_id"]),  # error 레벨 Sentry 전송
        JSONRenderer()
    ],
)

def get_logger():
    """structlog 로거 반환 (Sentry 통합)"""
    return structlog.get_logger()
```

### Sentry 초기화 (main.py 제안)

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import ignore_logger

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,  # 프로덕션 0.2 권장
    environment=os.getenv("ENVIRONMENT", "development"),
)

# 중복 방지 (structlog-sentry 직접 처리)
ignore_logger("structlog")
```

### 사용 예시 (FastAPI 엔드포인트)

```python
from utils.logging_config import get_logger

logger = get_logger().bind(request_id="1234")

try:
    # 코드
except Exception:
    logger.error("revalidate_failed", exc_info=True, fragmentKey="home-hero")
    # 자동 Sentry 이벤트 + 구조화 데이터 (extra/tag)
```

### 출력/전송 예시

- **JSON 로그**: `{"event": "revalidate_failed", "level": "error", "request_id": "1234"}`
- **Sentry**: error 이벤트 + extra (request_id tag)

---

## 3. FastAPI Middleware 예시 (제안)

### LoggingMiddleware (structlog 컨텍스트 + Sentry tracing)

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import structlog
import sentry_sdk

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        # structlog 컨텍스트 바인딩
        bound_logger = logger.bind(request_id=request_id, path=request.url.path, method=request.method)

        bound_logger.info("request_started")

        # Sentry transaction 시작 (tracing)
        with sentry_sdk.start_transaction(op="http.server", name=request.url.path):
            response = await call_next(request)

        bound_logger.info("request_completed", status_code=response.status_code)
        return response

app = FastAPI()
app.add_middleware(LoggingMiddleware)
```

### CORS Middleware (참고용)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://afo.kingdom"],  # 왕국 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 4. Error Handling 예시 (제안)

### 글로벌 에러 핸들러 (main.py 제안)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import structlog

logger = structlog.get_logger()

app = FastAPI()

# Pydantic ValidationError 핸들러 (422 → 사용자 친화적)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error("validation_error", errors=exc.errors(), url=str(request.url))
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid input", "details": exc.errors()}
    )

# 일반 Exception 핸들러 (500)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("unexpected_error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

### 엔드포인트 에러 처리 예시

```python
from fastapi import HTTPException

@app.post("/revalidate")
async def revalidate(request: RevalidateRequest):
    try:
        # 재검증 로직
        revalidatePath(f"/fragments/{request.fragmentKey}.html")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("revalidate_failed", fragmentKey=request.fragmentKey, exc_info=e)
        raise HTTPException(status_code=500, detail="Revalidation failed")
    
    return {"revalidated": True}
```

---

## 5. Unit Test Cases (제안)

### 테스트 파일 (tests/test_revalidate.py)

```python
from fastapi.testclient import TestClient
from pydantic import ValidationError
from api.models.revalidate import RevalidateRequest
from main import app  # FastAPI app

client = TestClient(app)

def test_model_validation_success():
    """정상 입력 (fragmentKey 유효)"""
    data = {"fragmentKey": "home-hero", "pageSlug": "home"}
    model = RevalidateRequest.model_validate(data)
    assert model.fragmentKey == "home-hero"
    assert model.pageSlug == "home"

def test_model_validation_invalid_key():
    """불량 입력 (fragmentKey 정규식 위반)"""
    data = {"fragmentKey": "../evil"}
    try:
        RevalidateRequest.model_validate(data)
        assert False, "ValidationError expected"
    except ValidationError as e:
        assert "Invalid fragmentKey" in str(e)
        assert e.errors()[0]["type"] == "value_error"
        assert e.errors()[0]["loc"] == ("fragmentKey",)

def test_endpoint_success():
    """정상 POST 요청 (Secret 맞음)"""
    response = client.post(
        "/revalidate",
        json={"fragmentKey": "home-hero", "pageSlug": "home"},
        headers={"x-revalidate-secret": "test-secret", "content-type": "application/json"}
    )
    assert response.status_code == 200
    json = response.json()
    assert json["revalidated"] is True
    assert json["fragmentKey"] == "home-hero"
    assert json["pageSlug"] == "home"
    assert response.headers["content-type"] == "application/json"

def test_endpoint_invalid_secret():
    """Secret 불일치"""
    response = client.post(
        "/revalidate",
        json={"fragmentKey": "home-hero"},
        headers={"x-revalidate-secret": "wrong", "content-type": "application/json"}
    )
    assert response.status_code == 401
    assert "Invalid secret" in response.json()["detail"]

def test_endpoint_query_blocked():
    """Query parameter 사용 (GET 차단)"""
    response = client.get("/revalidate?fragmentKey=home-hero")
    assert response.status_code == 405
    assert "Method Not Allowed" in response.json()["error"]

def test_endpoint_validation_error():
    """ValidationError (입력 오류)"""
    response = client.post(
        "/revalidate",
        json={"fragmentKey": "../evil"},
        headers={"x-revalidate-secret": "test-secret", "content-type": "application/json"}
    )
    assert response.status_code == 400
    details = response.json()["details"]
    assert len(details) > 0
    assert details[0]["type"] == "value_error"
```

### 실행

```bash
pytest -v tests/test_revalidate.py --cov=api
```

---

## 왕국 적용 효과 (예상)

- 로그 검색 용이 (키-값 쿼리)
- Sentry 통합 향상 (구조화 에러)
- 디버깅 속도 향상 (컨텍스트 포함)
- 에러 중앙화 (통기율 100% 연계)

---

## 6. 고급 설정 (제안)

### Processors 체인 커스터마이징

```python
import structlog
from structlog.processors import JSONRenderer, add_log_level, TimeStamper, StackInfoRenderer, format_exc_info
from structlog.contextvars import merge_contextvars
from structlog_sentry import SentryProcessor
import logging

structlog.configure(
    processors=[
        merge_contextvars,  # contextvars 병합 (FastAPI 미들웨어 연계)
        add_log_level,
        TimeStamper(key="ts", fmt="iso"),
        StackInfoRenderer(),  # 개발 환경에서만 사용 권장
        format_exc_info,
        SentryProcessor(level=logging.ERROR, tag_keys=["request_id"]),  # Sentry 자동 전송
        JSONRenderer(sort_keys=True)  # 프로덕션 JSON
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,  # 성능 최적화
)
```

### Context Binding (요청 컨텍스트 자동 바인딩)

```python
from fastapi import Request
import uuid
import structlog

@app.middleware("http")
async def add_request_context(request: Request, call_next):
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=str(uuid.uuid4()),
        method=request.method,
        path=request.url.path
    )
    response = await call_next(request)
    return response
```

### Custom Processor (사용자 정의 처리)

```python
class CustomTagProcessor:
    """커스텀 태그 추가 processor (제안)"""
    def __call__(self, logger, method_name, event_dict):
        event_dict["kingdom"] = "AFO"
        return event_dict

structlog.configure(
    processors=[
        CustomTagProcessor(),  # 커스텀 processor 추가
        # 기타 processors
    ],
)
```

---

## 7. 성능 최적화 (제안)

### 성능 최적화 팁

| **팁**                  | **상세 설명**                                      | **이점**                          | **코드 예시** |
|-------------------------|---------------------------------------------------|-----------------------------------|---------------|
| **Async Renderer**     | 비동기 로깅 (I/O 블로킹 방지)                     | 대량 요청 시 성능 향상            | `processors=[AsyncRenderer()]` |
| **Cache Logger**       | cache_logger_on_first_use=True                    | 로거 생성 오버헤드 제거           | `cache_logger_on_first_use=True` |
| **Processors 최소화**  | 불필요 processor 제거 (StackInfoRenderer 개발 시만) | CPU/메모리 절감                   | 프로덕션: JSONRenderer + TimeStamper만 |
| **Contextvars 사용**   | merge_contextvars (요청 컨텍스트 바인딩)         | 로깅 컨텍스트 자동 전파           | `processors=[merge_contextvars]` |
| **레벨 필터링**        | make_filtering_bound_logger (환경별 레벨)        | 불필요 로그 방지                  | 개발: DEBUG, 프로덕션: INFO+ |

### 비동기 로깅 설정 (대량 요청 제안)

```python
from structlog.processors import AsyncRenderer

structlog.configure(
    processors=[
        merge_contextvars,
        add_log_level,
        TimeStamper(key="ts", fmt="iso"),
        AsyncRenderer(),  # I/O 블로킹 방지
        JSONRenderer(sort_keys=True)
    ],
    cache_logger_on_first_use=True,
)
```

### 프로덕션 최적화 설정 (제안)

```python
import structlog
from structlog.processors import JSONRenderer, add_log_level, TimeStamper
from structlog.contextvars import merge_contextvars
from structlog_sentry import SentryProcessor
import logging

structlog.configure(
    processors=[
        merge_contextvars,  # 컨텍스트 바인딩
        add_log_level,
        TimeStamper(key="ts", fmt="iso"),
        SentryProcessor(level=logging.ERROR),  # error Sentry 전송
        JSONRenderer(sort_keys=True)  # JSON 최적화
    ],
    cache_logger_on_first_use=True,  # 로거 캐싱 (성능 향상)
)
```

---

## 8. 성능 벤치마크 (제안)

### AsyncRenderer 벤치마크 (제안)

**공식 문서 결론**: processor 체인이 예측 가능하고 외부 의존성 없으면 async 비용 불필요 (성능 저하 가능).

**참조 출처**:
- structlog 공식 문서 (performance 섹션): "moving log processing into separate threads [...] comes with a performance cost"
- structlog 공식 문서: https://www.structlog.org/en/stable/performance.html

#### 벤치마크 비교

| **항목**                  | **Sync 로깅**                                      | **AsyncRenderer**                          | **비교 결과 (공식 문서)**                  | **왕국 적용 추천** (FastAPI) |
|---------------------------|---------------------------------------------------|-------------------------------------------|-------------------------------------------|-----------------------------------|
| **성능 (throughput)**   | 높음 (직접 실행, 오버헤드 최소)                   | 낮음 (스레드 풀 오버헤드)                 | sync 1.5-2x 빠름 (processor 체인 단순 시) | sync 우선 (기본 JSONRenderer)    |
| **I/O 블로킹**           | 블로킹 가능 (파일/네트워크 I/O)                   | 비블로킹 (스레드 풀 처리)                 | async 우위 (대량 I/O 시)                  | async (Sentry/파일 로깅 많을 때) |
| **CPU 오버헤드**         | 낮음                                              | 높음 (스레드 컨텍스트 스위칭)             | sync 우위 (공식: "performance cost")      | sync (CPU 바운드)                 |
| **대량 요청 처리**       | 블로킹 위험                                       | 안전 (애플리케이션 지연 방지)             | async 우위 (high-throughput)              | async (왕국 대시보드 고부하)      |
| **예측 가능 체인**       | 최적                                              | 불필요 (공식 권장 피함)                   | sync 추천                                 | sync (기본 설정)                  |

#### 적용 추천

**sync 기본 (권장, 성능 최적)**:
```python
structlog.configure(
    processors=[
        add_log_level,
        TimeStamper(key="ts"),
        JSONRenderer()
    ],
    cache_logger_on_first_use=True  # 성능 향상
)
```

**async 적용 (I/O 많을 때 제안)**:
```python
from structlog.processors import AsyncRenderer

structlog.configure(
    processors=[
        AsyncRenderer(),  # 비동기 I/O 처리
        # 기타 processors
    ]
)
```

---

### Sentry 벤치마크 (제안)

**공식 문서 결론**: Sentry tracing은 minimal overhead 설계 (대부분 imperceptible to end users).

**주요 팩트** (공식 문서):
- Overhead: Minimal (imperceptible), backend backpressure 자동 조정
- CPU: 1-5% 목표 (profiling)
- Sampling: tracesSampleRate 0.2 권장 (production)

**참조 출처**:
- Sentry 공식 문서: https://docs.sentry.io/platforms/python/performance/
- Sentry 공식 문서: https://docs.sentry.io/product/performance/

#### 벤치마크 비교

| **항목**                  | **성능 영향**                                      | **권장 설정**                          | **왕국 적용 예상** (FastAPI/Next.js)                  |
|---------------------------|---------------------------------------------------|---------------------------------------|-------------------------------------------------------|
| **Tracing Overhead**     | Minimal (imperceptible)                           | tracesSampleRate 1.0 (dev), 0.2 (prod) | 초기 로드 영향 없음 (통기율 100% 유지)              |
| **CPU Usage**            | 1-5% (profiling 기준)                             | dynamic sampling 활성화               | 대량 요청 시 backpressure 자동 조정                  |
| **Memory**               | 낮음 (sampling으로 제어)                          | cache_logger_on_first_use             | MCP/Skills 처리 메모리 안정                         |
| **Throughput Impact**    | Low (sampling으로 제어)                           | high-load 시 0.1-0.2                 | 대시보드 고부하 안정 (INP <100ms 목표)              |
| **Distributed Tracing**  | Span 연결 오버헤드 낮음                          | propagation context                   | FastAPI → Next.js 호출 추적                         |

#### 적용 추천

- **Dev**: tracesSampleRate 1.0 (전체 캡처)
- **Prod**: 0.2 (비용/성능 균형)
- **효과**: 에러/성능 중앙화 (Sentry 대시보드 실시간)

---

### 시각화 참고 자료 (제안)

**참고**: 실제 그래프/이미지는 Sentry 대시보드에서 확인 가능합니다.

**Sentry Performance Tracing 시각화**:
- Transaction & Span Waterfall: Sentry 대시보드에서 자동 생성
- Performance Overhead Graph: Sentry Profiling에서 확인 가능

**참고 자료**:
- Sentry Performance 대시보드: https://docs.sentry.io/product/performance/
- Sentry Profiling: https://docs.sentry.io/product/profiling/

**인터랙티브 그래프 라이브러리 (참고용)**:
- Recharts: https://recharts.org/ (React 차트 라이브러리)
- Plotly: https://plotly.com/python/ (Python/JavaScript 차트)
- ECharts: https://echarts.apache.org/ (Apache ECharts)
- Chart.js: https://www.chartjs.org/ (JavaScript 차트)
- D3.js: https://d3js.org/ (데이터 시각화)

> **주의**: 위 라이브러리들은 "참고용"입니다. 실제 그래프 구현은 별도 작업이 필요합니다.

---

## 9. Datadog Tracing 통합 (제안)

### Datadog APM 개요 (팩트 기반)

**Datadog APM**: 분산 트레이싱 (trace/span)으로 병목 현상 추적

**참고 자료**:
- Datadog 공식 문서: https://docs.datadoghq.com/tracing/
- Datadog Python SDK: https://docs.datadoghq.com/tracing/setup_overview/setup/python/
- Datadog Next.js 통합: https://docs.datadoghq.com/tracing/setup_overview/setup/nodejs/

**왕국 현재 상태**: Sentry 미통합 (structlog 로깅만)

**Sentry vs Datadog 비교** (제안):

| **항목**                  | **Sentry**                                      | **Datadog**                          | **왕국 적용 추천**                  |
|---------------------------|------------------------------------------------|---------------------------------------|-----------------------------------|
| **에러 트래킹**          | 강점 (에러 그룹핑/스택 트레이스)                | 지원 (APM 통합)                      | Sentry (에러 중심)                 |
| **성능 트레이싱**        | 지원 (transaction)                             | 강점 (APM 대시보드)                  | Datadog (성능 중심)               |
| **비용**                 | 오픈소스 + 클라우드 (무료 티어 있음)            | 유료 (무료 티어 제한적)              | Sentry (비용 고려)                 |
| **통합**                 | structlog-sentry (간단)                        | ddtrace (자동 패치)                  | Sentry (구조화 로깅 연계)          |

---

### 통합 단계별 가이드 (제안)

#### 1. 설치

**FastAPI/Python**:
```bash
cd packages/afo-core
poetry add ddtrace
```

**Next.js**:
```bash
cd packages/dashboard
pnpm add dd-trace
```

#### 2. 기본 설정 (Python/FastAPI 제안)

```python
from ddtrace import patch_all, config

patch_all()  # 자동 패치 (FastAPI, SQLAlchemy 등)

config.fastapi["service_name"] = "afo-kingdom-api"
config.fastapi["trace_query_string"] = True  # 쿼리 문자열 추적 (보안 주의)
```

**또는 수동 tracer**:
```python
from ddtrace import tracer

@tracer.wrap(name="revalidate.process")
def process_revalidate():
    # 로직
    pass
```

#### 3. Next.js 통합 (제안)

```typescript
// next.config.js
const { withDatadog } = require('next-datadog');

module.exports = withDatadog({
  // 기존 설정
});
```

#### 4. 커스텀 Span 추가

**FastAPI**:
```python
from ddtrace import tracer

with tracer.trace("mcp.call", service="afo-mcp"):
    # MCP 호출
    fetch_mcp()
```

**Next.js**:
```typescript
import { tracer } from 'dd-trace';

tracer.trace('skills.fetch', async () => {
  // Skills 처리
});
```

#### 5. 환경 변수 (Datadog Agent 필요)

```bash
DD_AGENT_HOST=localhost
DD_TRACE_AGENT_PORT=8126
DD_ENV=production
DD_SERVICE_NAME=afo-kingdom-api
DD_VERSION=1.0.0
```

---

### 9.1 Datadog Tracing Code Examples (제안)

**Datadog Tracing Code**: ddtrace 라이브러리로 자동/커스텀 span 생성

**참고 자료**:
- Datadog Tracing: https://docs.datadoghq.com/tracing/
- Datadog Python SDK: https://docs.datadoghq.com/tracing/setup_overview/setup/python/
- Datadog Next.js 통합: https://docs.datadoghq.com/tracing/setup_overview/setup/nodejs/

**Code Examples 테이블** (제안):

| **카테고리**              | **설명**                                      | **왕국 적용 예시** (FastAPI/Next.js)                  | **코드 예시** |
|---------------------------|-----------------------------------------------|-------------------------------------------------------|---------------|
| **기본 초기화**          | ddtrace.patch_all() 또는 tracer 초기화        | FastAPI 전체 자동 트레이싱                           | `from ddtrace import patch_all; patch_all()` |
| **자동 Tracing**         | FastAPI/Starlette 통합                        | 엔드포인트 자동 transaction                          | `from ddtrace import config; config.fastapi["service_name"] = "afo-api"` |
| **커스텀 Span**          | tracer.trace() 또는 start_span                | MCP 호출 상세 추적                                   | `with tracer.trace("mcp.call", service="afo-mcp"): ...` |
| **태그/컨텍스트**        | span.set_tag(key, value)                      | fragmentKey/request_id 태그                          | `span.set_tag("fragmentKey", "home-hero")` |
| **에러 처리**            | record_exception(e)                           | 예외 자동 캡처                                       | `span.record_exception(e)` |
| **Next.js 통합**         | dd-trace 라이브러리                            | 페이지/라우트 트레이싱                               | `import { tracer } from 'dd-trace'; tracer.trace('page.load', () => {...})` |
| **분산 트레이싱**        | propagation context 자동                      | FastAPI → Next.js 호출 연결                          | 자동 (header 전파)        |

**FastAPI 커스텀 Span + 에러 처리 예시** (제안):
```python
from ddtrace import tracer
from fastapi import HTTPException

@app.post("/revalidate")
async def revalidate(request: RevalidateRequest):
    with tracer.trace("revalidate.process", service="afo-api") as span:
        span.set_tag("fragmentKey", request.fragmentKey)
        try:
            # 재검증 로직
            revalidatePath(f"/fragments/{request.fragmentKey}.html")
        except Exception as e:
            span.record_exception(e)
            span.set_tag("error", True)
            raise HTTPException(status_code=500, detail=str(e))
        return {"revalidated": True}
```

**Next.js 커스텀 Span 예시** (제안):
```typescript
import { tracer } from 'dd-trace';

async function fetchSkills() {
  return tracer.trace('skills.fetch', async (span) => {
    span?.setTag('type', 'mcp');
    // Skills 호출
    const res = await fetch('/api/skills');
    return res.json();
  });
}
```

---

### 9.2 Datadog APM Integration Details (제안)

**Datadog APM**: 분산 트레이싱 + 메트릭스 모니터링

**참고 자료**:
- Datadog APM: https://docs.datadoghq.com/tracing/
- Datadog Python SDK: https://docs.datadoghq.com/tracing/setup_overview/setup/python/
- Datadog Next.js 통합: https://docs.datadoghq.com/tracing/setup_overview/setup/nodejs/

**통합 단계별 가이드** (제안):

#### 1. 설치

**FastAPI/Python**:
```bash
cd packages/afo-core
poetry add ddtrace
```

**Next.js**:
```bash
cd packages/dashboard
pnpm add dd-trace
```

#### 2. 기본 초기화 (FastAPI main.py 제안)

```python
from ddtrace import patch_all, config

patch_all()  # 자동 통합 (FastAPI, SQLAlchemy, Redis 등)

config.fastapi["service_name"] = "afo-kingdom-api"
config.fastapi["distributed_tracing"] = True  # 분산 트레이싱 활성화
config.traces_sample_rate = 1.0  # dev: 1.0, prod: 0.2 권장
```

#### 3. Next.js 초기화 (next.config.js 제안)

```javascript
const { withDatadog } = require('next-datadog');

module.exports = withDatadog({
  // 기존 Next.js 설정
  // datadog: {
  //   apiKey: process.env.DATADOG_API_KEY,
  //   site: process.env.DATADOG_SITE,
  //   service: process.env.DATADOG_SERVICE_NAME || 'afo-kingdom-dashboard',
  //   env: process.env.NODE_ENV,
  //   version: process.env.APP_VERSION,
  // },
});
```

#### 4. 커스텀 Span 추가 (제안)

**FastAPI**:
```python
from ddtrace import tracer

with tracer.trace("mcp.call", service="afo-mcp"):
    # MCP 호출 로직
    fetch_mcp_data()
```

**Next.js**:
```typescript
import { tracer } from 'dd-trace';

tracer.trace('skills.fetch', async (span) => {
  span?.setTag('type', 'mcp');
  // Skills 로직
});
```

#### 5. 환경 변수 (Datadog Agent 필요)

```bash
DD_AGENT_HOST=localhost
DD_TRACE_AGENT_PORT=8126
DD_ENV=production
DD_SERVICE_NAME=afo-kingdom-api
DD_VERSION=1.0.0
```

---

### 왕국 적용 효과 (예상)

- MCP 9/Skills 19 호출 지연 추적 (통기율 영향 분석)
- 분산 트레이싱 (FastAPI → Next.js)
- Datadog 대시보드 실시간 (Grafana 연계 가능)
- 커스텀 span으로 상세 추적 (MCP/DB 쿼리)

---

### Sentry vs Datadog 선택 가이드 (제안)

**Sentry 추천**:
- 에러 트래킹 중심
- 오픈소스 + 무료 티어
- structlog-sentry 간단 통합

**Datadog 추천**:
- 성능 모니터링 중심
- APM 대시보드 강점
- 유료 (비용 고려 필요)

**하이브리드** (제안):
- Sentry: 에러 트래킹 (structlog-sentry)
- Datadog: 성능 모니터링 (APM)

---

### Custom Metrics (제안)

**Datadog Custom Metrics**: 사용자 정의 메트릭스 전송 (count/gauge/distribution/histogram)

**참고 자료**:
- Datadog Custom Metrics: https://docs.datadoghq.com/metrics/custom_metrics/
- Datadog StatsD: https://docs.datadoghq.com/developers/dogstatsd/

#### Custom Metrics 종류 및 적용 테이블

| **메트릭스 타입**        | **설명**                                      | **이점**                          | **왕국 적용 예시** (FastAPI/Next.js)                  | **코드 예시** |
|---------------------------|-----------------------------------------------|-----------------------------------|-------------------------------------------------------|---------------|
| **Count**                | 이벤트 카운트 (increment/decrement)           | 발생 횟수 추적                    | MCP 호출 횟수 (revalidate 요청 수)                   | `statsd.increment("mcp.calls", tags=["endpoint:revalidate"])` |
| **Gauge**                | 현재 값 (업/다운 가능)                        | 상태 값 모니터링                  | 활성 사용자 수, Skills 처리 큐 길이                    | `statsd.gauge("active.users", value)` |
| **Distribution**         | 분포 통계 (평균/백분위/최대)                  | 지연 시간 분석 (p95 등)           | 엔드포인트 응답 시간                                  | `statsd.distribution("response.time", ms, tags=["endpoint:/revalidate"])` |
| **Histogram**            | 분포 (백분위 자동)                            | 성능 분포 분석                    | DB 쿼리 시간 분포                                    | `statsd.histogram("db.query.time", ms)` |
| **Set**                  | 고유 값 카운트                                | 고유 사용자/ID 추적               | 고유 fragmentKey 수                                   | `statsd.set("unique.fragments", key)` |

#### 적용 코드 예시 (제안)

**FastAPI Custom Metrics**:
```python
from ddtrace import statsd
import time

@app.post("/revalidate")
async def revalidate(request: RevalidateRequest):
    statsd.increment("revalidate.calls", tags=["fragmentKey:" + request.fragmentKey])
    
    start = time.time()
    # 재검증 로직
    duration = time.time() - start
    
    statsd.distribution("revalidate.duration", duration * 1000, tags=["success:true"])
    return {"revalidated": True}
```

**Next.js Custom Metrics** (제안):
```typescript
import { statsd } from 'dd-trace';

async function fetchMCP() {
  statsd.increment('mcp.fetch');
  const start = performance.now();
  // MCP 호출
  const duration = performance.now() - start;
  statsd.distribution('mcp.fetch.duration', duration);
}
```

**태그 추가 (컨텍스트)**:
```python
statsd.gauge("skills.count", 19, tags=["kingdom:afo", "version:2025"])
```

---

### 9.3 Datadog Metrics Alerting Setup (제안)

**Datadog Metrics Alerting**: 커스텀 메트릭스 기준 이상치 알림

**참고 자료**:
- Datadog Monitors: https://docs.datadoghq.com/monitors/
- Datadog Metric Monitors: https://docs.datadoghq.com/monitors/types/metric/
- Datadog Notification Channels: https://docs.datadoghq.com/monitors/notify/

**왕국 현재 상태**: Datadog 미통합 (Custom Metrics 제안 상태)

**Alerting Setup 단계별 가이드** (제안):

#### 1. Monitor 생성 (Datadog UI)

- Monitors → New Monitor → Metric
- Query: 커스텀 메트릭스 선택 (e.g., `mcp.calls.total`)

#### 2. 쿼리 및 조건 설정 (예시)

**통기율 <100% 알림**:
```
Query: 100 - (avg:mcp.errors.total{*} / avg:mcp.calls.total{*}) * 100
Condition: avg(last_5m) < 100
```

**MCP 호출 급증**:
```
Query: avg:mcp.calls.total{*}
Condition: change(last_5m) > 50% (급증 감지)
```

**지연 p95 >2s**:
```
Query: p95:request.latency{*}
Condition: avg(last_5m) > 2
```

#### 3. 알림 채널 (Notification)

- @slack-#afo-alerts
- @email (on-call)
- Message 템플릿:
  ```
  @all 통기율 저하 감지!
  현재: {{value}}%
  클러스터: {{cluster.name}}
  ```

#### 4. Multi-Alert & Grouping

- Group by: `cluster`, `endpoint` (다중 클러스터 알림 분리)

#### 5. Thresholds & Recovery

- Critical: <100%
- Warning: <99%
- No Data: 10m (데이터 미수집 알림)

**왕국 적용 효과 (예상)**:
- 통기율 100% 실시간 보호 (저하 즉시 알림)
- MCP/Skills 메트릭스 이상치 감지
- Slack 연계 (왕국 채널 실시간)

---

### 9.4 Datadog Anomaly Detection (제안)

**Datadog Anomaly Detection**: 메트릭스 과거 패턴 기반 이상치 탐지

**참고 자료**:
- Datadog Anomaly Monitors: https://docs.datadoghq.com/monitors/types/anomaly/
- Datadog Anomaly Detection Algorithm: https://docs.datadoghq.com/monitors/types/anomaly/#anomaly-detection-algorithm

**왕국 현재 상태**: Datadog 미통합

**Anomaly Detection 기능 테이블** (제안):

| **기능**                  | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Custom Metrics)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|-------------------------------------------------------|------------|
| **Algorithm**            | Seasonal (주기성), Algorithmic (비주기성) 선택   | 패턴 맞춤 탐지                    | MCP 호출 (주간 패턴 seasonal)                        | Algorithm: Seasonal |
| **Deviation Bands**      | 정상 범위 밴드 (rolling median + deviation)       | 이상치 강조                       | 통기율 100% 밖 변화 빨강 표시                        | Sensitivity: Medium |
| **Window**               | 학습 기간 (1w/4w 등)                              | 과거 데이터 기반                   | 최근 4주 MCP 트렌드 학습                             | Lookback: 4 weeks |
| **Alert Conditions**     | Above/Below/Both bands                            | 방향성 알림                       | 통기율 below band (저하 알림)                        | Alert when: Below band |
| **Recovery**             | 정상 복귀 알림                                    | 빠른 대응                         | 통기율 복구 시 알림                                  | Notify on recovery |
| **Multi-Alert**          | 라벨별 그룹화                                     | 클러스터별 알림                   | cluster="afo" 별 MCP 이상                            | Group by: cluster |
| **Seasonality**          | Daily/Weekly/Monthly 자동 감지                    | 주기성 패턴 처리                  | 주말 MCP 호출 감소 예상                              | Seasonality: Weekly |

**왕국 적용 추천 Monitor (UI 설정 제안)**:

**통기율 Anomaly Monitor**:
```
Query: avg:last_1h):100 - (sum:mcp.errors.total{*} by {cluster} / sum:mcp.calls.total{*} by {cluster}) * 100
Algorithm: Seasonal
Sensitivity: High (급락 즉시 감지)
Alert when: Below lower band
Notification: @slack-#afo-alerts "통기율 이상 감지: {{value.name}} = {{value}}%"
```

**MCP 호출 Anomaly Monitor**:
```
Query: avg:last_1h):mcp.calls.total{*} by {type}
Algorithm: Algorithmic (비주기성)
Alert when: Above upper band (급증)
```

**왕국 적용 효과 (예상)**:
- 예상 밖 통기율 저하 자동 알림 (100% 유지)
- MCP/Skills 호출 이상 패턴 탐지 (시즌성 고려)
- Datadog 대시보드 + Alert (실시간 대응)

---

## 10. Prometheus 메트릭스 통합 (제안)

### Prometheus 개요 (팩트 기반)

**Prometheus**: 오픈소스 모니터링 시스템 (pull 기반 메트릭스 수집)

**참고 자료**:
- Prometheus 공식 문서: https://prometheus.io/docs/
- Prometheus Python Client: https://github.com/prometheus/client_python
- FastAPI Prometheus 통합: https://github.com/trallnag/prometheus-fastapi-instrumentator

**왕국 현재 상태**: 
- Prometheus 부분 통합됨
  - `packages/afo-core/api/middleware/prometheus.py` (PrometheusMiddleware)
  - `packages/afo-core/utils/metrics.py` (메트릭스 정의)
  - `packages/afo-core/domain/metrics/prometheus.py` (Trinity 메트릭스)
  - `prometheus-client>=0.19.0` 설치됨
- Sentry/Datadog 제안 상태

**Sentry/Datadog vs Prometheus 비교** (제안):

| **항목**                  | **Sentry/Datadog**                                      | **Prometheus**                          | **왕국 적용 추천**                  |
|---------------------------|------------------------------------------------|---------------------------------------|-----------------------------------|
| **아키텍처**              | Push 기반 (에이전트 → 클라우드)                | Pull 기반 (Prometheus → 서비스)      | Prometheus (오픈소스, 자체 호스팅) |
| **비용**                 | Sentry 무료 티어 / Datadog 유료                | 무료 (오픈소스)                       | Prometheus (비용 고려)             |
| **통합**                 | structlog-sentry / ddtrace                      | prometheus-client (간단)              | Prometheus (간단 통합)             |
| **대시보드**              | Sentry/Datadog 대시보드                         | Grafana (강력한 시각화)               | Prometheus + Grafana (유연성)      |

---

### 통합 단계별 가이드 (제안)

#### 1. 설치 (이미 설치됨)

**현재 상태**: `prometheus-client>=0.19.0` 이미 설치됨 (`packages/afo-core/requirements.txt`)

**추가 설치 필요 시**:
```bash
cd packages/afo-core
poetry add prometheus-client
```

#### 2. 기본 설정 (현재 구현 참고)

**현재 구현**: `packages/afo-core/api/middleware/prometheus.py`에 `PrometheusMiddleware` 존재

**현재 구현된 메트릭스** (참고):
```python
# packages/afo-core/api/middleware/prometheus.py
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code", "service"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint", "status_code", "service"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
)

TRINITY_SCORE = Gauge(
    "trinity_score",
    "Current Trinity score (Truth/Goodness/Beauty)",
    ["pillar", "service"],
)

SKILLS_EXECUTIONS = Counter(
    "skills_executions_total",
    "Total number of skill executions",
    ["skill_id", "category", "status"],
)
```

**기본 설정 예시** (제안, 현재 구현 확장):

```python
from prometheus_client import Counter, Gauge, Histogram, make_asgi_app
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

# 메트릭스 정의 (현재 구현 참고)
REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request Latency', ['endpoint'])
MCP_CALLS = Counter('mcp_calls_total', 'MCP Calls Total', ['type'])

app = FastAPI()

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        response = await call_next(request)
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=response.status_code).inc()
    return response

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

#### 3. 커스텀 메트릭스 추가 (현재 구현 참고)

**현재 구현**: `packages/afo-core/utils/metrics.py`에 메트릭스 정의됨

**엔드포인트 예시** (제안, 현재 구현 확장):

```python
@app.post("/revalidate")
async def revalidate(request: RevalidateRequest):
    MCP_CALLS.labels(type="revalidate").inc()
    ACTIVE_USERS.inc()  # 활성 사용자 증가
    # 로직
    ACTIVE_USERS.dec()  # 완료 시 감소
    return {"revalidated": True}
```

#### 4. 노출 엔드포인트 (/metrics)

**현재 구현**: `make_asgi_app()` 또는 `start_http_server()` 사용

- `http://localhost:8000/metrics` 방문 → Prometheus 형식 출력
- 또는 FastAPI에 마운트: `app.mount("/metrics", metrics_app)`

#### 5. Prometheus 설정 (prometheus.yml 제안)

```yaml
scrape_configs:
  - job_name: 'afo-kingdom'
    static_configs:
      - targets: ['host:8000']
```

---

### Grafana 연계 (참고용)

**Grafana**: Prometheus 데이터 시각화 대시보드

**참고 자료**:
- Grafana 공식 문서: https://grafana.com/docs/
- Grafana Prometheus 데이터 소스: https://grafana.com/docs/grafana/latest/datasources/prometheus/

**설정 예시** (제안):
1. Grafana 설치/설정
2. Prometheus 데이터 소스 추가
3. 대시보드 생성 (메트릭스 시각화)

---

### 왕국 적용 효과 (예상)

- 요청 수/지연 실시간 모니터링 (Grafana 대시보드)
- MCP/Skills 커스텀 메트릭스 (통기율 연계)
- 알림 설정 (메트릭스 기준 초과)

---

## 11. Grafana Dashboard 가이드 (제안)

### Grafana Dashboard 개요 (팩트 기반)

**Grafana**: Prometheus 데이터 시각화 대시보드

**참고 자료**:
- Grafana 공식 문서: https://grafana.com/docs/
- Grafana Prometheus 데이터 소스: https://grafana.com/docs/grafana/latest/datasources/prometheus/
- Grafana Panels: https://grafana.com/docs/grafana/latest/panels-visualizations/

**왕국 현재 상태**: Grafana 미통합 (Prometheus 제안 상태)

---

### 11.1 Dashboard Panel List (초간결 버전)

**Panel List** (제안):

| **패널 타입**    | **지표**                          | **설명**                          |
|------------------|-----------------------------------|-----------------------------------|
| Timeseries      | 요청 지연 (LCP/INP)               | 응답 시간 트렌드                  |
| Gauge           | 활성 사용자 / MCP 큐              | 현재 상태                         |
| Stat            | 통기율 / 총 요청 수               | 핵심 KPI                          |
| Heatmap         | 응답 시간 분포 (p95)               | 지연 히트맵                       |
| Table           | 상세 로그/메트릭스                | 필터링 테이블                     |
| Bar Gauge       | MCP 호출 수 (type별)              | 카테고리 비교                     |
| Pie Chart       | 에러 타입 분포                    | 에러 비율                         |
| Logs            | structlog JSON 로그               | 검색 가능 로그                    |

**적용 추천** (제안):
- Prometheus 메트릭스 연계 (request_count, request_latency 등)
- Hover/zoom 인터랙티브 (Grafana 기본)

---

### 11.2 Timeseries Panel 상세 설명 (제안)

**Timeseries Panel**: 시간 기반 메트릭스 시각화

**참고 자료**:
- Grafana Timeseries: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/time-series/

**Timeseries Panel 기능 테이블** (제안):

| **기능**                  | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|----------------------------------------------------------|------------|
| **Graph Style**          | Line/Area/Bar/Points 선택                         | 트렌드/분포 시각화                | 요청 지연 (Line), MCP 호출 누적 (Area)                   | Graph style: Line |
| **Legend**               | Table/Right/List 모드, 계산 (avg/max)             | 메트릭스 라벨링                   | endpoint별 latency legend                               | Mode: Table, Calculations: avg |
| **Tooltip**              | Hover 상세 (value/time)                           | 상세 분석                         | hover 시 p95 지연 확인                                  | Mode: All series |
| **Axis**                 | Y축 왼쪽/오른쪽, 단위 (s/ms), 스케일 (log/linear) | 다중 메트릭스 비교                | 왼쪽: latency (ms), 오른쪽: calls (count)               | Left Y: ms, Right Y: none |
| **Thresholds**           | 색상 기준선 (alert)                               | 이상치 강조                       | latency >2s 빨강 표시                                   | Thresholds: 2s (red) |
| **Fill/Gradient**        | 면적 채우기 (gradient)                            | 시각 강조                         | Area 그래프 gradient                                    | Fill opacity: 0.5, Gradient |
| **Stacking**             | 누적 그래프                                       | 비율 분석                         | endpoint별 호출 누적                                     | Stacking: Normal |
| **Null Value**           | 연결/0/break 처리                                 | 데이터 결측 처리                  | 결측 시 break                                           | Null value: connected |

**Prometheus 쿼리 예시** (제안):
- **요청 지연**:
  ```
  histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, endpoint))
  ```
- **MCP 호출 수**:
  ```
  rate(mcp_calls_total[5m])
  ```

---

### 11.3 Heatmap Panel 상세 설명 (제안)

**Heatmap Panel**: 값 분포를 색상으로 시각화

**참고 자료**:
- Grafana Heatmap: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/heatmaps/

**Heatmap Panel 기능 테이블** (제안):

| **기능**                  | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|----------------------------------------------------------|------------|
| **Data Format**          | Bucket 기반 (histogram)                           | 분포 분석 (p50/p95)               | request_latency_seconds_bucket                          | Format as: Heatmap |
| **Color Mode**           | Spectrum/Opacity                                  | 강도 시각화                       | 지연 높을수록 빨강                                       | Color scheme: Reds |
| **Y-Axis Buckets**       | Bucket 크기/수 설정                               | 세밀 분포                         | latency 0-50ms, 50-100ms 등 bucket                      | Calculate from data |
| **X-Axis**               | 시간 간격 (1m/5m)                                 | 트렌드 분석                       | 시간별 지연 분포 변화                                   | Interval: 5m |
| **Cell Values**          | Count/Sum/Mean                                    | 메트릭스 종류 선택                | 호출 수 (count) 또는 평균 지연                           | Value: Count |
| **Tooltip**              | Hover 상세 (bucket 값)                            | 상세 분석                         | hover 시 p95 지연 확인                                  | Mode: All series |
| **Legend**               | 색상 스케일 표시                                  | 기준 이해                         | 색상별 지연 범위 표시                                   | Show legend: true |

**Prometheus 쿼리 예시** (제안):
```
sum by (le) (rate(request_latency_seconds_bucket[5m]))
```

---

### 11.4 Stat Panel 상세 설명 (제안)

**Stat Panel**: 단일 값/KPI 시각화

**참고 자료**:
- Grafana Stat: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/

**Stat Panel 기능 테이블** (제안):

| **기능**                  | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|----------------------------------------------------------|------------|
| **Value Mode**           | Text/Value/Graph (sparkline) 선택                  | KPI 강조                          | 통기율 (Text), MCP 수 (Value)                            | Value mode: Text |
| **Color Mode**           | Value/Background/Thresholds                       | 상태 시각화                       | 통기율 100% 녹색, <100% 빨강                            | Color mode: Thresholds |
| **Thresholds**           | 값 기준 색상 변경                                 | 이상치 강조                       | latency >2s 빨강                                        | Thresholds: 2s (red) |
| **Sparkline**            | 미니 트렌드 그래프                                | 변화 추적                         | 최근 1h 호출 수 트렌드                                   | Show sparkline: true |
| **Unit/Decimals**        | 단위 (percent/seconds) + 소수점                   | 가독성 향상                       | 통기율 % 표시                                           | Unit: percent (0-100) |
| **Text Size**            | Title/Value 크기 조정                             | 강조 효과                         | "통기율 100%" 크게 표시                                 | Text size: 200% |
| **Orientation**          | Auto/Horizontal/Vertical                           | 레이아웃 최적화                   | 대시보드 그리드 배치                                    | Orientation: Auto |

**Prometheus 쿼리 예시** (제안):
- **통기율**:
  ```
  100 - (sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))) * 100
  ```
- **MCP 수**:
  ```
  mcp_count
  ```

---

### 11.5 Grafana Alerting Features (제안)

**Grafana Alerting**: 메트릭스 기준 이상치 자동 알림

**참고 자료**:
- Grafana Alerting: https://grafana.com/docs/grafana/latest/alerting/

**Alerting Features 테이블** (제안):

| **기능**                  | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|----------------------------------------------------------|------------|
| **Alert Rule**           | 쿼리 + 조건 (reduce/when)                         | 이상치 조건 정의                  | 통기율 <100% (reduce: last)                             | Query: 통기율 쿼리, When: is below 100 |
| **Evaluation**           | 간격/시간 설정                                    | 주기적 평가                       | 1m 간격 평가                                            | Evaluation interval: 1m |
| **Notification Policy**  | 라우팅/그룹화 (label matcher)                     | 알림 채널 분리                    | 지연 알림 Slack, 에러 알림 Email                        | Matcher: {severity="critical"} |
| **Contact Point**        | Slack/Email/Webhook 등                            | 다채널 알림                       | Slack webhook                                           | Type: Slack, URL: webhook |
| **Mute Timings**         | 시간대 알림 뮤트                                  | 야간 알림 방지                    | 주말/야간 뮤트                                          | Mute: weekends |
| **Alert Groups**         | 유사 알림 그룹화                                  | 노이즈 감소                       | 동일 엔드포인트 지연 그룹                               | Group interval: 5m |
| **Silence**              | 일시 알림 중지                                    | 유지보수 시 사용                  | 배포 중 알림 silence                                    | Silence duration: 1h |
| **Labels/Annotations**   | 커스텀 라벨/설명 추가                             | 알림 컨텍스트                     | runbook_url, severity                                   | Labels: severity=critical |

---

### 11.6 Prometheus Alertmanager (제안)

**Alertmanager**: Prometheus 알림 관리

**참고 자료**:
- Prometheus Alertmanager: https://prometheus.io/docs/alerting/latest/alertmanager/

**Alertmanager 기능 테이블** (제안):

| **기능**                  | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|----------------------------------------------------------|------------|
| **Grouping**             | 동일 알림 그룹화 (group_by)                       | 노이즈 감소                       | endpoint별 지연 그룹 (5m 간격)                           | group_by: ['endpoint'] |
| **Inhibition**           | 상위 알림 시 하위 억제                            | 불필요 알림 방지                  | instance down 시 service 알림 억제                      | inhibit_rules |
| **Receiver**             | 알림 채널 (Slack/Email/Webhook)                   | 다채널 알림                       | Slack (왕국 채널), Email (on-call)                      | receivers: - name: slack |
| **Routing**              | 라벨 매처 (route)                                 | 우선순위 알림                     | severity=critical → Slack 즉시                           | match: {severity: "critical"} |
| **Silence**              | 시간대 알림 뮤트                                  | 야간/유지보수 알림 방지           | 주말 뮤트                                               | silence (duration: 8h) |
| **Repeat Interval**      | 알림 반복 간격                                    | 지속 알림                         | 4h 반복 (해결 안 될 시)                                 | repeat_interval: 4h |

**alertmanager.yml 예시** (제안):
```yaml
global:
  slack_api_url: 'YOUR_SLACK_WEBHOOK'

route:
  group_by: ['endpoint']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'slack'

receivers:
  - name: 'slack'
    slack_configs:
      - channel: '#afo-alerts'
        text: 'Alert: {{ .CommonAnnotations.summary }}'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
```

---

### 11.7 Prometheus Federation Setup (제안)

**Prometheus Federation**: 계층적 메트릭스 수집

**참고 자료**:
- Prometheus Federation: https://prometheus.io/docs/prometheus/latest/federation/

**Federation Setup 단계별 가이드** (제안):

1. **하위 Prometheus 설정** (지역/서비스별):
   - /metrics 엔드포인트 노출 (기본)

2. **상위 Prometheus 설정** (prometheus.yml 제안):
   ```yaml
   scrape_configs:
     - job_name: 'federate-regional'
       honor_labels: true
       metrics_path: '/federate'
       params:
         'match[]':
           - '{job="node"}'
           - '{__name__=~"^request_.*"}'
       static_configs:
         - targets:
             - 'regional-prometheus-1:9090'
             - 'regional-prometheus-2:9090'
   ```

3. **하위 Prometheus federation 엔드포인트 활성화** (제안):
   ```bash
   --web.enable-lifecycle
   ```

4. **쿼리 필터** (match[] 예시):
   - '{job="mcp"}' : MCP 메트릭스만
   - '{__name__=~"request_latency_.*"}' : 지연 메트릭스

---

### 11.8 Advanced match[] Filters (제안)

**Advanced match[]**: Federation /federate 엔드포인트에서 메트릭스 필터링

**참고 자료**:
- Prometheus Federation: https://prometheus.io/docs/prometheus/latest/federation/

**Advanced match[] 기능 테이블** (제안):

| **Matcher 타입**         | **구문**                                      | **설명**                          | **왕국 적용 예시** (메트릭스 필터)                  | **yaml 예시** |
|---------------------------|-----------------------------------------------|-----------------------------------|-----------------------------------------------------|---------------|
| **Exact Match**          | label="value"                                 | 정확 일치                         | job="mcp" (MCP 메트릭스만)                        | - '{job="mcp"}' |
| **Not Equal**            | label!="value"                                | 제외                              | job!="prometheus" (자기 메트릭스 제외)            | - '{job!="prometheus"}' |
| **Regex Match**          | label=~"regex"                                | 정규식 일치                       | __name__=~"request_latency_.*" (지연 메트릭스)   | - '{__name__=~"request_latency_.*"}' |
| **Regex Not Match**      | label!~"regex"                                | 정규식 제외                       | job!~"test|dev" (테스트 제외)                     | - '{job!~"test|dev"}' |
| **Multiple Conditions**  | 다중 match[] 배열                             | OR 조건 (union)                   | job="mcp" 또는 __name__=~"skills_.*"             | - '{job="mcp"}'<br>- '{__name__=~"skills_.*"}' |
| **All Metrics**          | __name__=~".+"                                | 모든 메트릭스 (주의: 과부하)      | 전체 federation (권장 아님)                              | - '{__name__=~".+"}' |
| **Non-empty Matcher**    | 최소 하나 non-empty                           | 안전 규칙 (empty matcher 금지)    | __name__=~".+" 필수 (empty 방지)                 | - '{__name__=~".+"}' |

**prometheus.yml 예시** (제안):
```yaml
scrape_configs:
  - job_name: 'federate-afo'
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="mcp"}'
        - '{job="skills"}'
        - '{__name__=~"request_latency_.*"}'
        - '{__name__=~"up|node_.*"}'
    static_configs:
      - targets:
          - 'local-prometheus:9090'
          - 'remote-prometheus:9090'
```

---

### 11.9 Grafana Federation Dashboard (제안)

**Grafana Federation Dashboard**: Prometheus federation을 통해 다중 클러스터/인스턴스 메트릭스를 단일 Grafana에서 시각화

**참고 자료**:
- Prometheus Federation: https://prometheus.io/docs/prometheus/latest/federation/
- Grafana Multi-datasource: https://grafana.com/docs/grafana/latest/datasources/

**왕국 현재 상태**: 단일 Prometheus 제안 (federation 미설정)

**Federation Setup + Grafana Dashboard 단계별 가이드** (제안):

1. **하위 Prometheus 설정** (지역/패키지별):
   - prometheus.yml 기본 /metrics 노출 (federate 엔드포인트 자동)

2. **중앙 Prometheus 설정** (prometheus.yml federation job, 제안):
   ```yaml
   scrape_configs:
     - job_name: 'federation-afo'
       honor_labels: true
       scrape_interval: 15s
       metrics_path: '/federate'
       params:
         'match[]':
           - '{job="mcp"}'
           - '{job="skills"}'
           - '{__name__=~"request_latency_.*"}'
           - '{__name__=~"up|node_memory_.*"}'
       static_configs:
         - targets:
             - 'dashboard-prometheus:9090'
             - 'afo-core-prometheus:9090'
       labels:
         cluster: 'afo-kingdom'
   ```

3. **Grafana 데이터소스 추가** (중앙 Prometheus):
   - Grafana UI → Configuration → Data Sources → Add → Prometheus
   - URL: http://central-prometheus:9090
   - Multi-cluster 쿼리: cluster="afo-kingdom" 라벨 필터

4. **Federation Dashboard 예시** (Grafana JSON 임포트, 제안):
   ```json
   {
     "title": "AFO Kingdom Federation Dashboard",
     "panels": [
       {
         "title": "MCP Calls by Cluster",
         "type": "timeseries",
         "targets": [{"expr": "rate(mcp_calls_total[5m]) by (cluster, job)"}]
       },
       {
         "title": "통기율 (Federated)",
         "type": "stat",
         "targets": [{"expr": "100 - (sum(rate(errors_total[5m])) by (cluster) / sum(rate(requests_total[5m])) by (cluster)) * 100"}],
         "thresholds": [{"color": "green", "value": null}, {"color": "red", "value": 95}]
       },
       {
         "title": "Latency Heatmap (Multi-Cluster)",
         "type": "heatmap",
         "targets": [{"expr": "sum by (le, cluster) (rate(request_latency_seconds_bucket[5m]))"}]
       }
     ]
   }
   ```

5. **Multi-Cluster 쿼리 예시** (Grafana 패널 쿼리, 제안):
   - MCP 호출: `rate(mcp_calls_total{cluster="afo-kingdom"}[5m]) by (job)`
   - 통기율: `100 - (sum(rate(errors_total{cluster="afo-kingdom"}[5m])) / sum(rate(requests_total{cluster="afo-kingdom"}[5m]))) * 100`
   - Latency p95: `histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket{cluster="afo-kingdom"}[5m])) by (le))`

---

### 11.10 Thanos for Long-term Storage (제안)

**Thanos**: Prometheus 장기 저장/고가용성 솔루션

**참고 자료**:
- Thanos 공식 문서: https://thanos.io/
- CNCF Thanos: https://www.cncf.io/projects/thanos/

**왕국 현재 상태**: Prometheus 단기 저장 (2주 기본)

**Thanos 구성 요소 테이블** (제안):

| **컴포넌트**             | **상세 설명**                                      | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스)                  | **설정 팁** |
|---------------------------|---------------------------------------------------|-----------------------------------|----------------------------------------------------------|------------|
| **Sidecar**              | Prometheus와 함께 실행 (메트릭스 업로드)         | 장기 저장 자동                    | MCP/Skills 메트릭스 S3 업로드                           | --tsdb.path + --objstore.config |
| **Store Gateway**        | object storage 쿼리 게이트웨이                    | 장기 메트릭스 읽기                | 1년 전 통기율 조회                                      | store: s3 bucket |
| **Query**                | 글로벌 쿼리 (deduplication)                       | 고가용성 쿼리                     | 다중 Prometheus 통합 쿼리                               | query: --store |
| **Compactor**            | downsampling + compaction                         | 저장 비용 절감                    | 5m → 1h downsampling (장기 데이터)                      | compactor: --downsample |
| **Ruler**                | 알림 규칙 평가                                    | 분산 알림                         | 통기율 <100% 알림 (Grafana 연계)                        | ruler: --rule.file |
| **Receiver**             | 원격 쓰기 (remote write)                          | 메트릭스 수집                     | 외부 시스템 메트릭스 왕국으로                            | receiver: --remote-write |

**s3.yaml (object storage 설정, 제안)**:
```yaml
type: S3
config:
  bucket: "afo-kingdom-metrics"
  endpoint: "s3.amazonaws.com"
  access_key: "YOUR_ACCESS_KEY"
  secret_key: "YOUR_SECRET_KEY"
  # 또는 AWS IAM 역할 사용 시 access_key/secret_key 생략 가능
```

**docker-compose.yml (전체 구성 예시, 제안)**:
```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=15d'
    networks:
      - thanos

  thanos-sidecar:
    image: quay.io/thanos/thanos:v0.32.0
    command:
      - "sidecar"
      - "--prometheus.url=http://prometheus:9090"
      - "--objstore.config-file=/etc/thanos/s3.yaml"
      - "--tsdb.path=/prometheus"
    volumes:
      - ./s3.yaml:/etc/thanos/s3.yaml
      - prometheus-data:/prometheus
    depends_on:
      - prometheus
    networks:
      - thanos

  thanos-store:
    image: quay.io/thanos/thanos:v0.32.0
    command:
      - "store"
      - "--objstore.config-file=/etc/thanos/s3.yaml"
      - "--data-dir=/var/thanos/store"
      - "--grpc-address=0.0.0.0:10901"
      - "--http-address=0.0.0.0:10902"
    volumes:
      - ./s3.yaml:/etc/thanos/s3.yaml
      - thanos-store-data:/var/thanos/store
    ports:
      - "10901:10901"
      - "10902:10902"
    networks:
      - thanos

  thanos-query:
    image: quay.io/thanos/thanos:v0.32.0
    command:
      - "query"
      - "--store=thanos-store:10901"
      - "--store=thanos-sidecar:10901"
      - "--http-address=0.0.0.0:10902"
      - "--grpc-address=0.0.0.0:10901"
    ports:
      - "10902:10902"
      - "10901:10901"
    depends_on:
      - thanos-store
      - thanos-sidecar
    networks:
      - thanos

  thanos-compactor:
    image: quay.io/thanos/thanos:v0.32.0
    command:
      - "compact"
      - "--objstore.config-file=/etc/thanos/s3.yaml"
      - "--data-dir=/var/thanos/compact"
      - "--retention.resolution-raw=15d"
      - "--retention.resolution-5m=90d"
      - "--retention.resolution-1h=2y"
      - "--downsample"
    volumes:
      - ./s3.yaml:/etc/thanos/s3.yaml
      - thanos-compact-data:/var/thanos/compact
    networks:
      - thanos
    # Compactor는 싱글톤 배포 필수 (replicas: 1)

volumes:
  prometheus-data:
  thanos-store-data:
  thanos-compact-data:

networks:
  thanos:
    driver: bridge
```

**각 컴포넌트별 주요 옵션** (제안):

- **Sidecar**: `--prometheus.url`, `--objstore.config-file`, `--tsdb.path`, `--http-address`, `--grpc-address`
- **Store**: `--objstore.config-file`, `--data-dir`, `--grpc-address`, `--http-address`
- **Query**: `--store` (다중), `--http-address`, `--grpc-address`
- **Compactor**: `--objstore.config-file`, `--retention.resolution-*`, `--downsample`, `--data-dir`

#### Grafana 연계 (제안)

**Thanos Query를 Grafana 데이터소스로 추가**:
1. Grafana UI → Configuration → Data Sources → Add → Prometheus
2. URL: `http://thanos-query:10902`
3. Thanos Query는 Prometheus API 호환 (Grafana에서 직접 사용 가능)

**쿼리 예시** (Grafana 패널, 제안):
- **통기율 (장기)**: `100 - (sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))) * 100`
- **MCP 호출 (1년 전)**: `rate(mcp_calls_total[5m])` (Thanos Query가 자동으로 Store Gateway에서 조회)

#### 왕국 적용 효과 (예상)
- 메트릭스 무한 저장 (S3 비용 효율).
- downsampling으로 장기 데이터 효율.
- Grafana + Thanos Query로 통기율 100% 장기 시각화.
- 다중 Prometheus 통합 쿼리 (Query 컴포넌트).

---

### 11.11 Thanos Downsampling Techniques (제안)

**Thanos Downsampling**: Prometheus TSDB 블록 compaction + downsampling

**참고 자료**:
- Thanos Compactor: https://thanos.io/components/compact/

**Downsampling Techniques 테이블** (제안):

| **Technique**            | **설명**                                      | **타이밍/조건**                          | **이점**                          | **왕국 적용 예시** (Prometheus 메트릭스) | **yaml 예시** |
|--------------------------|-----------------------------------------------|-----------------------------------------|-----------------------------------|------------------------------------------|---------------|
| **5m Downsampling**     | raw (1m/15s) → 5m 해상도 집계                | 40시간 후 자동 (Compactor)               | 쿼리 속도 향상                | 최근 2주 latency p95 분석                | --retention.resolution-5m=90d |
| **1h Downsampling**     | 5m → 1h 해상도 집계                          | 10일 후 자동                             | 쿼리 속도 향상, 저장 증가 | 장기 (1년) MCP 호출 트렌드               | --retention.resolution-1h=2y |
| **Compaction**          | 블록 병합 (공통 구조 공유)                    | 지속 (Compactor 싱글톤)                  | 저장 효율화                       | Skills 19개 메트릭스 블록 최적화         | --retention.resolution-raw=15d |
| **Downsampling Query**  | 쿼리 시 자동 (Thanos Query --query.auto-downsampling) | 장기 범위 쿼리                           | 쿼리 비용 감소 (주의: 값 부풀림 가능) | Grafana 30일 latency 히트맵             | query.auto-downsampling=true |
| **Retention Policy**    | 해상도별 보관 기간 설정                        | Compactor flag                           | 비용 최적화 (tiered retention)    | raw 15d, 5m 90d, 1h 2y                  | --retention.resolution-raw=15d --retention.resolution-5m=90d |

**thanos-compactor.yaml 예시** (제안):
```yaml
retentionResolutionRaw: 15d
retentionResolution5m: 90d
retentionResolution1h: 2y
objstoreConfig:
  type: S3
  config:
    bucket: afo-kingdom-metrics
# Compactor 싱글톤 배포
replicas: 1
```

**주의 사항** (공식 문서 기준):
- Downsampling 정확성을 위해 5 시리즈 생성 (저장 증가)
- auto-downsampling 쿼리 값 부풀림 가능 (비활성화 권장)
- Compactor singleton 필수 (concurrency safe 아님)

---

### 11.12 Grafana Dashboard Examples 확장 (제안)

**확장된 Dashboard Examples**: 왕국 Prometheus 메트릭스를 위한 추가 패널 예시

**각 패널 타입별 JSON 설정 예시** (제안):

#### 1. Timeseries 패널 (요청 지연 트렌드 – LCP/INP 연계)

**Prometheus 쿼리**:
```
histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, endpoint))
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "Request Latency (p95)",
  "type": "timeseries",
  "targets": [
    {
      "expr": "histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, endpoint))",
      "legendFormat": "{{endpoint}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "ms",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": null, "color": "green"},
          {"value": 1000, "color": "yellow"},
          {"value": 2000, "color": "red"}
        ]
      }
    }
  }
}
```

#### 2. Heatmap 패널 (응답 시간 분포 – p95 강조)

**Prometheus 쿼리**:
```
sum by (le) (rate(request_latency_seconds_bucket[5m]))
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "Latency Distribution (Heatmap)",
  "type": "heatmap",
  "targets": [
    {
      "expr": "sum by (le) (rate(request_latency_seconds_bucket[5m]))",
      "format": "heatmap"
    }
  ],
  "options": {
    "color": {
      "mode": "spectrum",
      "scheme": "Reds"
    }
  }
}
```

#### 3. Stat 패널 (통기율 100% / MCP 수 강조)

**Prometheus 쿼리**:
```
100 - (sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))) * 100
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "통기율",
  "type": "stat",
  "targets": [
    {
      "expr": "100 - (sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))) * 100"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": null, "color": "red"},
          {"value": 95, "color": "yellow"},
          {"value": 100, "color": "green"}
        ]
      }
    }
  },
  "options": {
    "graphMode": "area",
    "colorMode": "thresholds"
  }
}
```

#### 4. Gauge 패널 (활성 사용자 / 큐 길이)

**Prometheus 쿼리**:
```
active_connections{service="afo-kingdom-api"}
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "Active Connections",
  "type": "gauge",
  "targets": [
    {
      "expr": "active_connections{service=\"afo-kingdom-api\"}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": null, "color": "green"},
          {"value": 50, "color": "yellow"},
          {"value": 80, "color": "red"}
        ]
      }
    }
  }
}
```

#### 5. Table 패널 (상세 메트릭스 테이블)

**Prometheus 쿼리**:
```
sum by (endpoint, method) (rate(http_requests_total[5m]))
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "Requests by Endpoint",
  "type": "table",
  "targets": [
    {
      "expr": "sum by (endpoint, method) (rate(http_requests_total[5m]))",
      "format": "table"
    }
  ],
  "options": {
    "showHeader": true,
    "sortBy": [
      {
        "displayName": "Value",
        "desc": true
      }
    ]
  }
}
```

#### 6. Logs 패널 (JSON 구조화 로그)

**참고**: Logs 패널은 Loki 데이터소스 필요 (Prometheus 직접 연계 불가)

**Grafana 패널 JSON** (제안, Loki 연계):
```json
{
  "title": "Application Logs",
  "type": "logs",
  "targets": [
    {
      "expr": "{job=\"afo-kingdom\"} |= \"error\"",
      "refId": "A"
    }
  ],
  "options": {
    "dedupStrategy": "none",
    "enableLogDetails": true,
    "prettifyLogMessage": true,
    "showCommonLabels": false,
    "showLabels": false,
    "showTime": true,
    "sortOrder": "Descending"
  }
}
```

#### 7. Bar Gauge 패널 (카테고리 비교)

**Prometheus 쿼리**:
```
sum by (type) (rate(mcp_calls_total[5m]))
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "MCP Calls by Type",
  "type": "bargauge",
  "targets": [
    {
      "expr": "sum by (type) (rate(mcp_calls_total[5m]))",
      "legendFormat": "{{type}}"
    }
  ],
  "options": {
    "orientation": "horizontal",
    "displayMode": "gradient"
  },
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "palette-classic"
      }
    }
  }
}
```

#### 8. Pie Chart 패널 (에러 분포)

**Prometheus 쿼리**:
```
sum by (error_type) (rate(api_errors_total[5m]))
```

**Grafana 패널 JSON** (제안):
```json
{
  "title": "Error Distribution",
  "type": "piechart",
  "targets": [
    {
      "expr": "sum by (error_type) (rate(api_errors_total[5m]))",
      "legendFormat": "{{error_type}}"
    }
  ],
  "options": {
    "legend": {
      "displayMode": "table",
      "placement": "right"
    },
    "pieType": "pie",
    "tooltip": {
      "mode": "single"
    }
  }
}
```

#### 9. 전체 대시보드 레이아웃 예시

**Grafana Dashboard JSON** (제안, 통합 예시):
```json
{
  "title": "AFO Kingdom Dashboard",
  "tags": ["afo", "prometheus"],
  "timezone": "browser",
  "panels": [
    {
      "id": 1,
      "title": "통기율",
      "type": "stat",
      "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4},
      "targets": [
        {
          "expr": "100 - (sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))) * 100"
        }
      ]
    },
    {
      "id": 2,
      "title": "Request Latency (p95)",
      "type": "timeseries",
      "gridPos": {"x": 6, "y": 0, "w": 12, "h": 8},
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, endpoint))",
          "legendFormat": "{{endpoint}}"
        }
      ]
    },
    {
      "id": 3,
      "title": "MCP Calls by Type",
      "type": "bargauge",
      "gridPos": {"x": 0, "y": 4, "w": 6, "h": 4},
      "targets": [
        {
          "expr": "sum by (type) (rate(mcp_calls_total[5m]))",
          "legendFormat": "{{type}}"
        }
      ]
    },
    {
      "id": 4,
      "title": "Latency Distribution",
      "type": "heatmap",
      "gridPos": {"x": 6, "y": 8, "w": 12, "h": 8},
      "targets": [
        {
          "expr": "sum by (le) (rate(request_latency_seconds_bucket[5m]))",
          "format": "heatmap"
        }
      ]
    }
  ],
  "refresh": "30s",
  "time": {
    "from": "now-6h",
    "to": "now"
  }
}
```

**참고**: 위 JSON은 Grafana Dashboard Import 기능으로 직접 임포트 가능합니다 (Grafana UI → Dashboards → Import → JSON 붙여넣기).

---

## 다음 단계 (왕국 확장)

- **즉시**: structlog 설치 → logging_config.py 수정 테스트 (제안)
- **단기**: Ticket 42 – structlog 전체 적용 (JSON 로깅)
- **중기**: Sentry + structlog 통합 (에러/성능 중앙화)
- **고급**: Ticket 54 – structlog 고급 processors (TimeStamper/JSONRenderer) 적용
- **성능**: Ticket 55 – AsyncRenderer 대량 요청 벤치마크
- **벤치마크**: Ticket 56 – AsyncRenderer 적용 여부 결정 (high-throughput 테스트)
- **Sentry**: Ticket 59 – production sampling 0.2 적용
- **Datadog**: Ticket 61 – Datadog APM tracing (span 자동 캡처, 제안)
- **Custom Metrics**: Ticket 64 – Custom metrics 대시보드 (MCP 호출 수, 제안)
- **Prometheus**: Ticket 65 – Prometheus 메트릭스 통합 (MCP 호출 수, 제안)
- **Grafana**: Ticket 68 – Grafana Dashboard Panel List 적용 (제안)
- **Grafana**: Ticket 69 – Timeseries 패널 (latency p95 + calls rate, 제안)
- **Grafana**: Ticket 70 – Heatmap 패널 (p95 지연 강조, 제안)
- **Grafana**: Ticket 71 – Stat 패널 (통기율 100% 강조, 제안)
- **Grafana**: Ticket 72 – Alert Policy (Slack 연계, 제안)
- **Alertmanager**: Ticket 73 – Slack receiver 설정 (제안)
- **Federation**: Ticket 74 – Federation (하위/상위 Prometheus, 제안)
- **Federation**: Ticket 75 – Advanced match[] (MCP/Skills 필터, 제안)
- **Federation Dashboard**: Ticket 76 – Federation Dashboard JSON 임포트 (MCP/통기율 패널, 제안)
- **Thanos**: Ticket 77 – Thanos Store/Compactor 적용 (제안)
- **Thanos Downsampling**: Ticket 78 – Downsampling retention (5m 90d, 1h 2y, 제안)
- **Dashboard Examples**: Ticket 79 – More Panels (Heatmap/Table) 추가 (제안)
- **Visual Examples**: Ticket 80 – Visual Examples (Heatmap/Table) 적용 (제안)
- **선택**: Sentry vs Datadog vs Prometheus 비교 (왕국 모니터링 선택, 제안)

---

## 참고 자료

- **structlog 공식 문서**: https://www.structlog.org
- **Sentry Python SDK**: https://docs.sentry.io/platforms/python/
- **structlog-sentry**: https://github.com/kiwicom/structlog-sentry
- **Datadog APM**: https://docs.datadoghq.com/tracing/
- **Datadog Python SDK**: https://docs.datadoghq.com/tracing/setup_overview/setup/python/
- **Datadog Next.js 통합**: https://docs.datadoghq.com/tracing/setup_overview/setup/nodejs/
- **Datadog Custom Metrics**: https://docs.datadoghq.com/metrics/custom_metrics/
- **Datadog StatsD**: https://docs.datadoghq.com/developers/dogstatsd/
- **Prometheus 공식 문서**: https://prometheus.io/docs/
- **Prometheus Python Client**: https://github.com/prometheus/client_python
- **FastAPI Prometheus 통합**: https://github.com/trallnag/prometheus-fastapi-instrumentator
- **Grafana 공식 문서**: https://grafana.com/docs/
- **Grafana Prometheus 데이터 소스**: https://grafana.com/docs/grafana/latest/datasources/prometheus/
- **Grafana Panels**: https://grafana.com/docs/grafana/latest/panels-visualizations/
- **Grafana Timeseries**: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/time-series/
- **Grafana Heatmap**: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/heatmaps/
- **Grafana Stat**: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/stat/
- **Grafana Alerting**: https://grafana.com/docs/grafana/latest/alerting/
- **Prometheus Alertmanager**: https://prometheus.io/docs/alerting/latest/alertmanager/
- **Prometheus Federation**: https://prometheus.io/docs/prometheus/latest/federation/
- **Grafana Multi-datasource**: https://grafana.com/docs/grafana/latest/datasources/
- **Thanos 공식 문서**: https://thanos.io/
- **CNCF Thanos**: https://www.cncf.io/projects/thanos/
- **Thanos Compactor**: https://thanos.io/components/compact/
- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **pytest 공식 문서**: https://docs.pytest.org/
- **현재 구현**: `packages/afo-core/utils/logging_config.py`
- **SSOT 원칙**: `docs/reports/SSOT_REPORTING_GUIDELINES.md`

---

**SSOT 원칙 준수**: 팩트 기반 (공식 문서 참조), 과장 표현 제거, 제안 명시, Gate/Contract 유지

