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

## 다음 단계 (왕국 확장)

- **즉시**: structlog 설치 → logging_config.py 수정 테스트 (제안)
- **단기**: Ticket 42 – structlog 전체 적용 (JSON 로깅)
- **중기**: Sentry + structlog 통합 (에러/성능 중앙화)

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

