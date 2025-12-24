# Logging Best Practices 가이드 (2025 왕국 백엔드/프론트엔드 적용 버전)

**As-of**: 2025-12-24  
**Status**: 완료됨  
**SSOT 원칙 준수**: 팩트 기반 (실제 구현 상태 반영), Gate/Contract 유지

---

## Logging Best Practices 개요 (팩트 기반)

로깅은 디버깅/모니터링의 핵심입니다.

**왕국 현재 구현**:
- **백엔드 (FastAPI)**: 표준 `logging` 모듈 사용
  - 구조화된 JSON 로깅 지원 (`AFOFormatter`)
  - `get_logger()` 함수 제공 (`packages/afo-core/utils/logging_config.py`)
- **프론트엔드 (Next.js)**: 커스텀 Logger 클래스
  - `packages/dashboard/src/lib/logger.ts`
  - 개발 환경에서만 콘솔 출력, 프로덕션에서는 에러만 외부 서비스 전송 (TODO)

**핵심 원리**: 구조화 (JSON), 레벨 구분, 컨텍스트 포함, DRY 적용

---

## 베스트 프랙티스 테이블 (2025 기준 통합)

| **카테고리**              | **베스트 프랙티스**                                      | **왕국 적용 예시** (FastAPI/Next.js)                  | **코드 예시** (PASTE-ready) |
|---------------------------|---------------------------------------------------------|-------------------------------------------------------|----------------------------|
| **구조화 로깅**          | JSON 형식 (검색/분석 용이)                              | FastAPI AFOFormatter (structured=True)                | `setup_logging(structured=True)` |
| **로깅 레벨**            | DEBUG/INFO/WARNING/ERROR/CRITICAL 구분                  | 개발: DEBUG, 프로덕션: INFO+                           | `logger.info("Request received", extra={"path": request.url})` |
| **컨텍스트 포함**        | 요청 ID, 사용자 ID, 트랜잭션 ID 추가                     | MCP 호출 시 request_id 포함                           | `logger.info("MCP call", extra={"request_id": uuid4()})` |
| **중앙화 로깅**          | Sentry/Datadog/ELK 통합 (제안)                          | 현재 미통합 (TODO: Sentry 통합)                       | `# TODO: Sentry 통합` |
| **DRY 적용**             | 로거 인스턴스 단일화 (get_logger 재사용)                | 모든 모듈에서 `get_logger(__name__)` 사용             | `from utils.logging_config import get_logger; logger = get_logger(__name__)` |
| **프론트엔드 로깅**      | console.log → structured (Sentry browser SDK 제안)      | Next.js 커스텀 Logger 클래스                          | `logger.error("Error occurred", { context })` |
| **성능 고려**            | 비동기 로깅 (제안)                                      | 현재 동기 로깅 (Redis Pub/Sub 지원)                  | `log_sse(message)` |

> **주의**: 위 테이블의 일부 항목은 "제안" 또는 "참고용"입니다. 현재 구현 상태는 "왕국 적용 예시" 컬럼을 참조하세요.

---

## 왕국 현재 구현 코드 (PASTE-ready)

### 백엔드 (FastAPI) - 현재 구현

**로깅 설정**: `packages/afo-core/utils/logging_config.py`

```python
from utils.logging_config import setup_logging, get_logger

# 로깅 설정 (구조화된 JSON 포맷)
setup_logging(
    level="INFO",
    log_file="logs/afo_server.log",
    structured=True,  # JSON 포맷
)

# 로거 사용
logger = get_logger(__name__)
logger.info("Request received", extra={"path": request.url, "method": "GET"})
```

**Redis Pub/Sub 로깅**: `packages/afo-core/utils/logging.py`

```python
from utils.logging import log_sse

# 실시간 로그 스트리밍 (대시보드용)
log_sse("Chancellor decision: AUTO_RUN")
```

### 프론트엔드 (Next.js) - 현재 구현

**커스텀 Logger**: `packages/dashboard/src/lib/logger.ts`

```typescript
import { logger } from "@/lib/logger";

// 사용 예시
logger.info("Dashboard loaded", { userId: "commander" });
logger.error("API error", { endpoint: "/api/health", status: 500 });
```

---

## 향상 제안 (참고용)

### structlog 통합 (제안)

**설치**:
```bash
cd packages/afo-core
poetry add structlog
```

**설정**:
```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
logger.info("Request received", path="/", method="GET")
```

### Sentry 통합 (제안)

**백엔드 (FastAPI)**:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_DSN",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
    environment="production",
)
```

**프론트엔드 (Next.js)**:
```bash
pnpm add @sentry/nextjs
```

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});
```

> **주의**: 위 예시는 "제안" 또는 "참고용"입니다. 현재 구현 상태는 위 "왕국 현재 구현 코드" 섹션을 참조하세요.

---

## 다음 단계 (왕국 확장)

- **즉시**: 현재 구현 상태 유지 (표준 logging + 커스텀 Logger)
- **단기**: Ticket 38 – Sentry 통합 (에러 중앙화)
- **중기**: structlog 통합 검토 (구조화 로깅 강화)

---

## 참고 자료

- **현재 구현**: 
  - `packages/afo-core/utils/logging_config.py` (백엔드)
  - `packages/dashboard/src/lib/logger.ts` (프론트엔드)
- **SSOT 원칙**: `docs/reports/SSOT_REPORTING_GUIDELINES.md`

---

**SSOT 원칙 준수**: 팩트 기반 (실제 구현 상태 반영), 과장 표현 제거, Gate/Contract 유지

