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

```typescript
import { NextRequest, NextResponse } from "next/server";
import { revalidatePath } from "next/cache";

export const runtime = "edge";

const HEADER = "x-revalidate-secret";
const FRAGMENT_KEY_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;
const PAGE_SLUG_RE = /^[A-Za-z0-9][A-Za-z0-9/_-]{0,255}$/;

type Body = {
  fragmentKey?: unknown;
  pageSlug?: unknown; // 선택
};

export async function POST(req: NextRequest) {
  // Query Parameter 금지
  if (req.nextUrl.searchParams.size > 0) {
    return NextResponse.json(
      { ok: false, error: "query_params_not_allowed" },
      { status: 400 }
    );
  }

  // 헤더 인증
  const expected = process.env.REVALIDATE_SECRET;
  const provided = req.headers.get(HEADER);
  if (!expected || !provided || provided !== expected) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  // JSON 파싱
  let body: Body;
  try {
    body = (await req.json()) as Body;
  } catch {
    return NextResponse.json({ ok: false, error: "invalid_json" }, { status: 400 });
  }

  const fragmentKey = body.fragmentKey;
  const pageSlug = body.pageSlug;

  // fragmentKey 검증 (필수)
  if (typeof fragmentKey !== "string" || !FRAGMENT_KEY_RE.test(fragmentKey)) {
    return NextResponse.json(
      { ok: false, error: "invalid_fragmentKey" },
      { status: 400 }
    );
  }

  const fragmentPath = `/fragments/${fragmentKey}.html`;

  // pageSlug 검증 (선택)
  let pagePath: string | null = null;
  if (typeof pageSlug === "string" && pageSlug.trim().length > 0) {
    const normalized = pageSlug.trim().replace(/^\/+/, "");
    if (!PAGE_SLUG_RE.test(normalized)) {
      return NextResponse.json(
        { ok: false, error: "invalid_pageSlug" },
        { status: 400 }
      );
    }
    // 설계 기준: /docs/[slug]
    pagePath = `/docs/${normalized}`;
  }

  // revalidate
  revalidatePath(fragmentPath);
  if (pagePath) revalidatePath(pagePath);

  return NextResponse.json({
    ok: true,
    revalidated: pagePath ? [fragmentPath, pagePath] : [fragmentPath],
  });
}

export async function GET() {
  return NextResponse.json({ ok: false, error: "method_not_allowed" }, { status: 405 });
}
```

---

## 📋 커밋 메시지 (예시)

```txt
feat(dashboard): extend revalidate API to optionally revalidate pages (edge, header-auth)
```

---

## ✅ 테스트 curl (예시)

### 1) Fragment만 (기본)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"home-hero"}'
```

### 2) Fragment + Page (선택)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"home-hero","pageSlug":"home"}'
```

### 3) pageSlug 불량 (400)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"home-hero","pageSlug":"../evil"}'
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

