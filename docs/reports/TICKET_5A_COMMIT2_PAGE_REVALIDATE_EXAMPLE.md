# Ticket 5-A Commit 2: Page Revalidate 확장 (예시/준비)

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 2 (Page Revalidate 확장)  
**Status:** 🟡 **Example/Ready (Not Implemented)**

---

## 📋 팩트 (현재 상태)

- **Commit 1**: Fragment만 revalidate (구현 완료 ✅)
- **Commit 2**: Fragment + Page 동시 revalidate (선택 기능, 미구현 🟡)
- **목적**: Page도 선택적으로 revalidate 가능하도록 확장

---

## 📝 예시 코드 (붙여넣기용) — 오타/보안/타입 안전 버전

**파일**: `packages/dashboard/src/app/api/revalidate/route.ts` (Commit 1을 수정하는 예시)

> **주의**: 아래 코드는 **예시/준비 단계**입니다. 실제 구현 전 검토 필요.

### FACTS

- Commit 2는 **"예시/준비 단계(미구현)"**로 문서에만 존재해야 함.
- Commit 1의 보안 원칙 유지: **헤더 인증 / Query 금지 / fragmentKey 검증 / GET 차단**
- Commit 2에서 추가되는 건 **pageSlug(선택)** 뿐.

### PASTE (최종 붙여넣기 버전)

```typescript
import { NextResponse } from "next/server";
import { revalidatePath } from "next/cache";

export const runtime = "edge";

const FRAGMENT_KEY_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;
const PAGE_SLUG_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;

function methodNotAllowed() {
  return NextResponse.json({ error: "Method Not Allowed" }, { status: 405 });
}

export async function POST(request: Request) {
  // Query parameter 금지 (보안)
  const url = new URL(request.url);
  if (url.search && url.search.length > 0) {
    return NextResponse.json({ error: "Query parameters are not allowed" }, { status: 400 });
  }

  // 헤더 인증
  const secret = request.headers.get("x-revalidate-secret");
  if (!secret || secret !== process.env.REVALIDATE_SECRET) {
    return NextResponse.json({ error: "Invalid secret" }, { status: 401 });
  }

  // JSON 파싱 안전 처리
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const fragmentKey = (body as any)?.fragmentKey;
  const pageSlug = (body as any)?.pageSlug;

  // fragmentKey 검증 (필수)
  if (typeof fragmentKey !== "string" || !FRAGMENT_KEY_RE.test(fragmentKey)) {
    return NextResponse.json({ error: "Invalid fragmentKey" }, { status: 400 });
  }

  // pageSlug 검증 (선택)
  if (pageSlug !== undefined) {
    if (typeof pageSlug !== "string" || !PAGE_SLUG_RE.test(pageSlug)) {
      return NextResponse.json({ error: "Invalid pageSlug" }, { status: 400 });
    }
  }

  const paths: string[] = [];
  const fragmentPath = `/fragments/${fragmentKey}.html`;
  revalidatePath(fragmentPath);
  paths.push(fragmentPath);

  if (typeof pageSlug === "string" && pageSlug.length > 0) {
    const pagePath = `/docs/${pageSlug}`;
    revalidatePath(pagePath);
    paths.push(pagePath);
  }

  return NextResponse.json({ revalidated: true, paths });
}

export function GET() { return methodNotAllowed(); }
export function PUT() { return methodNotAllowed(); }
export function PATCH() { return methodNotAllowed(); }
export function DELETE() { return methodNotAllowed(); }
```

---

## 📋 커밋 메시지 (예시)

```txt
feat(dashboard): extend revalidate API to optionally revalidate pages (edge, header-auth)
```

---

## ✅ 테스트 curl (예시) — 전부 Content-Type 포함

### 1) 성공 (fragment만)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

### 2) 성공 (fragment + page)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero","pageSlug":"home"}'
```

### 3) 헤더 없음 (401)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

### 4) fragmentKey 불량 (400)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"../evil"}'
```

### 5) Query 금지 (400)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate?x=1" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

---

## 🔒 SSOT 일관성 보장

### ✅ 유지할 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   - slug 검증 (Contract Gate와 동일)
   - fragment_key 필수 (빌드 타임 검증)
   - 렌더링 우선순위 (React → Fragment → 404)

2. **Gate 검증**
   - 빌드 타임 검증 유지
   - Contract Gate 유지
   - fragment_key 검증 유지

3. **기존 Fragment**
   - `public/fragments/{fragment_key}.html` 유지
   - fragment overwrite 없음

### ✅ 확장 가능한 것 (읽기 경로만)

1. **Page Revalidate**
   - 선택적 pageSlug 파라미터
   - Fragment + Page 동시 revalidate

---

## ⚠️ 주의사항

- **정규식 오타 금지**: `/^[A-Za-z0-9].../` (공백 없음)
- **Content-Type 필수**: curl 예시에 `-H "content-type: application/json"` 포함
- **상태 명확화**: Commit 2는 **예시/준비 단계** (미구현)

---

**Status:** 🟡 **Example/Ready (Not Implemented)**  
**Next Action:** 필요 시 구현 시작


