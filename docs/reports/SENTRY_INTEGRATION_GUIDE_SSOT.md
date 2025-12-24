# Sentry Integration Guide (2025 왕국 백엔드/프론트엔드 적용 버전)

**As-of**: 2025-12-24  
**Status**: 완료됨 (PASTE-ready, 제안 가이드)  
**SSOT 원칙 준수**: 팩트 기반 (공식 문서 참조), Gate/Contract 유지

---

## Sentry 개요 (팩트 기반)

Sentry는 실시간 에러 트래킹/모니터링 플랫폼입니다 (오픈소스 + 클라우드).

**주요 기능**:
- 에러 그룹핑/스택 트레이스
- 성능 트레이싱 (transaction)
- 알림 (Slack/Email)

**왕국 현재 상태**: **미통합** (제안 가이드)

---

## 통합 단계별 가이드 (제안)

### 1. Sentry 프로젝트 생성 (sentry.io)

1. 새 프로젝트 → Python (FastAPI) / JavaScript (Next.js)
2. DSN 복사 (예: `https://o123.ingest.sentry.io/123`)

### 2. 백엔드 (FastAPI) 통합

**설치**:
```bash
cd packages/afo-core
poetry add sentry-sdk
```

**설정** (`packages/afo-core/AFO/api_server.py` 또는 startup):
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration(), StarletteIntegration()],
    traces_sample_rate=1.0,  # 프로덕션 0.2 권장
    environment=os.getenv("ENVIRONMENT", "development"),
)
```

**에러 캡처 예시**:
```python
try:
    # 코드
except Exception as e:
    sentry_sdk.capture_exception(e)
    raise
```

### 3. 프론트엔드 (Next.js) 통합

**설치**:
```bash
cd packages/dashboard
pnpm add @sentry/nextjs
```

**설정** (`packages/dashboard/sentry.config.ts`):
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});
```

**Next.js wrapper** (`packages/dashboard/next.config.ts`):
```typescript
import { withSentryConfig } from "@sentry/nextjs";

export default withSentryConfig({
  // 기존 설정
}, {
  // Sentry 설정
  silent: true,
  org: "your-org",
  project: "your-project",
});
```

**에러 캡처 예시**:
```typescript
try {
  // 코드
} catch (error) {
  Sentry.captureException(error);
  throw error;
}
```

### 4. 검증

1. 의도적 에러 발생 → Sentry 대시보드 확인
2. 성능 트레이싱 (transaction) → 페이지 로드 시간 모니터링

---

## 왕국 적용 효과 (예상)

- 에러 중앙화 (통기율 100% 연계)
- 알림 (Slack 통합 가능)
- 성능 모니터링 (CWV 연계)

---

## 다음 단계 (왕국 확장)

- **즉시**: Sentry DSN 설정 → FastAPI/Next.js 적용 (제안)
- **단기**: Ticket 39 – Sentry 알림 (Slack/Email) 통합
- **중기**: Performance tracing (INP/LCP 자동 모니터링)

---

## 참고 자료

- **Sentry 공식 문서**: https://docs.sentry.io/
- **FastAPI 통합**: https://docs.sentry.io/platforms/python/integrations/fastapi/
- **Next.js 통합**: https://docs.sentry.io/platforms/javascript/guides/nextjs/
- **SSOT 원칙**: `docs/reports/SSOT_REPORTING_GUIDELINES.md`

---

**SSOT 원칙 준수**: 팩트 기반 (공식 문서 참조), 과장 표현 제거, Gate/Contract 유지, "제안" 명시

