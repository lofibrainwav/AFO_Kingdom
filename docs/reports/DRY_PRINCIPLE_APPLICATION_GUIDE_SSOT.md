# DRY 원칙 적용 가이드 (2025 왕국 코드베이스 적용 버전)

**As-of**: 2025-12-24  
**Status**: 완료됨  
**SSOT 원칙 준수**: 팩트 기반 (원저자 정의 참조), 과장 표현 제거

---

## DRY 원칙 개요 (팩트 기반)

DRY (Don't Repeat Yourself)는 코드/지식 중복 제거 원칙입니다.

**출처**: Andy Hunt & Dave Thomas, "The Pragmatic Programmer" (1999)

**핵심 원칙**: 모든 지식/코드는 단일 소스(SSOT)에서 관리되어야 합니다.

**왕국 적용**: 
- AntiGravity/DRY_RUN 강조 – 중복 제거로 버그 감소, 유지보수성 향상
- 과도 적용 시 추상화 과잉 주의 (WET: Write Everything Twice 허용 경우 존재)

---

## DRY 적용 베스트 프랙티스 테이블 (간결 버전, 왕국 코드베이스 기준)

| **카테고리**              | **적용 방법**                                      | **왕국 적용 예시** (대시보드/FastAPI/MCP)                  |
|---------------------------|---------------------------------------------------|-----------------------------------------------------------|
| **코드 중복**            | 함수/클래스 추출, 모듈화                          | fragmentKey 검증 → utils.validate_key                    |
| **설정 중복**            | config 파일/환경 변수 중앙화                      | REVALIDATE_SECRET (Secrets/Vars 통합)                    |
| **템플릿 중복**          | Templater/partials 사용                           | 보고서 헤더/푸터 (Trinity Score 표시)                     |
| **검증 로직**            | validator 함수/데코레이터 재사용                  | Pydantic custom validator (strict mode)                  |
| **데이터 구조**          | 모델/인터페이스 재사용                            | Request/Response 모델 (API 공통 필드)                     |
| **테스트 코드**          | fixture/헬퍼 함수                                 | pytest fixture (TestClient)                               |
| **에러 처리**            | 중앙화된 에러 핸들러                              | HTTPException 커스텀 클래스 (401/400)                     |
| **로깅**                 | 로거 인스턴스 단일화                              | get_logger() 모든 모듈 사용                               |
| **API 라우터**           | 공통 prefix/middleware 재사용                     | /api/revalidate guard (Ticket 5A)                        |
| **유틸 함수**            | utils 모듈 집중                                   | date.now() / slug 생성 함수                               |

**축소 기준**:
- 상세 설명/주의점 병합 → 핵심 예시 중심
- 행 수 확장 (10개), 컬럼 3개로 간결화
- 왕국 적용 예시 강화 (대시보드/MCP 중심)

---

## 왕국 적용 예시 코드

### Next.js Edge Route (현재 구현)

**fragmentKey 검증 로직 중복 제거** (DRY 적용):

**현재 구현**: `packages/dashboard/src/app/api/revalidate/route.ts`

```typescript
// 중복 제거 전 (가정)
const KEY_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;

// DRY 적용: utils/validation.ts로 추출
export function validateFragmentKey(key: string): boolean {
  const KEY_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;
  return KEY_RE.test(key);
}
```

### FastAPI 백엔드 (참고용)

**Pydantic 모델 중복 제거** (DRY 적용):

```python
from pydantic import BaseModel, ConfigDict

class BaseAPIRequest(BaseModel):
    """공통 요청 모델 (DRY 적용)"""
    model_config = ConfigDict(strict=True)

class RevalidateRequest(BaseAPIRequest):  # 중복 제거
    fragmentKey: str
    pageSlug: str | None = None
```

**FastAPI 엔드포인트 재사용**:

```python
from fastapi import Depends, Header, HTTPException

def get_revalidate_secret(x_revalidate_secret: str = Header(...)):
    """Secret 검증 재사용 (DRY)"""
    if x_revalidate_secret != os.getenv("REVALIDATE_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid secret")

@app.post("/revalidate")
async def revalidate(
    request: RevalidateRequest,
    secret: str = Depends(get_revalidate_secret)
):
    # 검증 로직 재사용
    ...
```

> **주의**: 위 FastAPI 예시는 참고용입니다. 현재 revalidate API는 Next.js Edge route로 구현되어 있습니다.

---

## 다음 단계 (왕국 확장)

- **즉시**: 왕국 코드베이스 DRY 점검 (중복 로직 검색)
- **단기**: Ticket 32 – DRY 위배 모듈 리팩터링
- **중기**: Oxc linter로 DRY 위배 자동 감지

---

## 참고 자료

- **원저자**: Andy Hunt & Dave Thomas, "The Pragmatic Programmer" (1999)
- **왕국 적용**: `packages/dashboard/src/app/api/revalidate/route.ts` (현재 구현)
- **SSOT 원칙**: `docs/reports/SSOT_REPORTING_GUIDELINES.md`

---

**SSOT 원칙 준수**: 팩트 기반 (원저자 정의 참조), 과장 표현 제거, 실제 구현 상태 반영

