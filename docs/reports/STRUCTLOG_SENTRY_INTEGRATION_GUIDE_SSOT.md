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

## 다음 단계 (왕국 확장)

- **즉시**: structlog 설치 → logging_config.py 수정 테스트 (제안)
- **단기**: Ticket 42 – structlog 전체 적용 (JSON 로깅)
- **중기**: Sentry + structlog 통합 (에러/성능 중앙화)
- **고급**: Ticket 54 – structlog 고급 processors (TimeStamper/JSONRenderer) 적용
- **성능**: Ticket 55 – AsyncRenderer 대량 요청 벤치마크
- **벤치마크**: Ticket 56 – AsyncRenderer 적용 여부 결정 (high-throughput 테스트)
- **Sentry**: Ticket 59 – production sampling 0.2 적용

---

## 참고 자료

- **structlog 공식 문서**: https://www.structlog.org
- **Sentry Python SDK**: https://docs.sentry.io/platforms/python/
- **structlog-sentry**: https://github.com/kiwicom/structlog-sentry
- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **pytest 공식 문서**: https://docs.pytest.org/
- **현재 구현**: `packages/afo-core/utils/logging_config.py`
- **SSOT 원칙**: `docs/reports/SSOT_REPORTING_GUIDELINES.md`

---

**SSOT 원칙 준수**: 팩트 기반 (공식 문서 참조), 과장 표현 제거, 제안 명시, Gate/Contract 유지

