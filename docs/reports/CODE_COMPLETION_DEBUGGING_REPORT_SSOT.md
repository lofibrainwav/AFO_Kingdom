# 코드 완성 및 디버깅 보고서 (2025 왕국 Next.js Edge Route 적용 버전)

**As-of**: 2025-12-24  
**Status**: 완료됨 (디버깅 통과, PASTE-ready)  
**SSOT 원칙 준수**: 팩트 기반 (실제 구현 상태 반영), Gate/Contract 유지

---

## 완료 요약 (팩트 기반)

### 현재 구현 상태

- **구현 완료**: Next.js Edge route로 구현됨 (Ticket 5A Commit 1)
  - **경로**: `packages/dashboard/src/app/api/revalidate/route.ts`
  - **Runtime**: Edge Runtime (`export const runtime = "edge"`)
  - **인증**: `x-revalidate-secret` 헤더 필수
  - **검증**: fragmentKey 정규식 검증 (`/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/`)
  - **동작**: `revalidatePath("/fragments/{fragmentKey}.html")` 호출

### 디버깅 결과

- ✅ 타입 안전성 확인 (TypeScript strict mode)
- ✅ 런타임 검증 (정규식 패턴 매칭)
- ✅ 에러 처리 (400/401/405 명확)
- ✅ 보안 (Query Parameter 금지, 헤더 인증)

### 테스트 결과

- ✅ 로컬 curl 성공 (200/400/401 구분)
- ✅ Edge Runtime 동작 확인
- ✅ SSOT Gate 통과

---

## 현재 구현 코드 (PASTE-ready, 주석 포함)

### Next.js Edge Route (실제 구현)

**파일 경로**: `packages/dashboard/src/app/api/revalidate/route.ts`

```typescript
import { NextRequest, NextResponse } from "next/server";
import { revalidatePath } from "next/cache";

export const runtime = "edge";

const HEADER = "x-revalidate-secret";
const KEY_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;

export async function POST(req: NextRequest) {
  // Query parameter 금지 (보안)
  if (req.nextUrl.searchParams.size > 0) {
    return NextResponse.json({ ok: false, error: "query_params_not_allowed" }, { status: 400 });
  }

  // 헤더 인증
  const expected = process.env.REVALIDATE_SECRET;
  const provided = req.headers.get(HEADER);

  if (!expected || !provided || provided !== expected) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  // JSON 파싱 안전 처리
  let json: unknown;
  try {
    json = await req.json();
  } catch {
    return NextResponse.json({ ok: false, error: "invalid_json" }, { status: 400 });
  }

  // fragmentKey 검증 (SSOT 일치)
  const fragmentKey = (json as { fragmentKey?: unknown })?.fragmentKey;
  if (typeof fragmentKey !== "string" || !KEY_RE.test(fragmentKey)) {
    return NextResponse.json({ ok: false, error: "invalid_fragmentKey" }, { status: 400 });
  }

  // revalidatePath 호출
  const path = `/fragments/${fragmentKey}.html`;
  revalidatePath(path);

  return NextResponse.json({ ok: true, revalidated: [path] });
}

export async function GET() {
  return NextResponse.json({ ok: false, error: "method_not_allowed" }, { status: 405 });
}
```

---

## 테스트 curl (복붙 가능)

### 1) 성공 케이스 (200 OK)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"home-hero"}'
```

**예상 응답:**
```json
{
  "ok": true,
  "revalidated": ["/fragments/home-hero.html"]
}
```

**HTTP 상태 코드**: `200 OK`

---

### 2) 인증 실패 (401 Unauthorized)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

**예상 응답:**
```json
{
  "ok": false,
  "error": "unauthorized"
}
```

**HTTP 상태 코드**: `401 Unauthorized`

---

### 3) 입력값 실패 (400 Bad Request)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"../evil"}'
```

**예상 응답:**
```json
{
  "ok": false,
  "error": "invalid_fragmentKey"
}
```

**HTTP 상태 코드**: `400 Bad Request`

---

### 4) Query Parameter 금지 (400 Bad Request)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate?fragmentKey=home-hero" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"home-hero"}'
```

**예상 응답:**
```json
{
  "ok": false,
  "error": "query_params_not_allowed"
}
```

**HTTP 상태 코드**: `400 Bad Request`

---

### 5) GET 메서드 차단 (405 Method Not Allowed)

```bash
curl -i -X GET "http://localhost:3000/api/revalidate"
```

**예상 응답:**
```json
{
  "ok": false,
  "error": "method_not_allowed"
}
```

**HTTP 상태 코드**: `405 Method Not Allowed`

---

## 디버깅 결과 (팩트 기반)

### ✅ 통과 항목

1. **타입 안전성**: TypeScript strict mode 통과
2. **런타임 검증**: 정규식 패턴 매칭 정상 동작
3. **에러 처리**: 400/401/405 명확한 응답
4. **보안**: Query Parameter 금지, 헤더 인증 정상
5. **SSOT Gate**: Contract Gate 통과 (fragmentKey 검증 규칙 일치)

### ⚠️ 주의 사항

- **FastAPI 백엔드**: 별도 revalidate 엔드포인트 없음 (현재 아키텍처와 불일치)
- **현재 구현**: Next.js Edge route로만 구현됨
- **확장 가능성**: 필요 시 FastAPI 백엔드에 별도 구현 가능 (현재는 불필요)

---

## 다음 단계 (왕국 확장)

- **즉시**: 현재 구현 상태 유지 (Next.js Edge route)
- **단기**: Ticket 33 – Pydantic 모델 전체 strict mode 적용 (FastAPI 백엔드)
- **중기**: Oxc linter 통합 (런타임 + 정적 검증)

---

## 참고 자료

- **현재 구현**: `packages/dashboard/src/app/api/revalidate/route.ts`
- **Ticket 5A**: `docs/reports/TICKET_5A_COMMIT1_REVALIDATE_API_IMPLEMENTATION.md`
- **SSOT 원칙**: `docs/reports/SSOT_REPORTING_GUIDELINES.md`

---

**SSOT 원칙 준수**: 팩트 기반 (실제 구현 상태 반영), 과장 표현 제거, Gate/Contract 유지

