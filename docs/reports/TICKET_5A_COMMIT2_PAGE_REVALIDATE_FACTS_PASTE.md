# Ticket 5A Commit 2 — Page Revalidate Example (FACTS/PASTE)

**As-of**: 2025-12-24  
**Status**: 예시 (제안)  
**SSOT 원칙 준수**: 팩트 기반, 복붙 가능한 최종본

---

## FACTS (검증됨)

* Next.js App Router에서 `revalidatePath()`는 **Server Functions / Route Handlers**에서 호출 가능하고, **Route Handler에서 호출하면 "다음 방문 시" 재검증**이 일어나는 방식이다. ([Next.js][1])
* `revalidatePath(path)`의 `path`는 **1024자 이하** 등 제약이 있다. ([Next.js][1])
* (왕국 SSOT 정책) **쿼리 파라미터 금지**, **헤더 인증 + JSON body**로만 트리거한다. *(이건 내부 정책이므로 FACTS가 아니라 "규칙")*

---

## PASTE (최종 붙여넣기 버전)

> 파일 경로 예시: `packages/dashboard/src/app/api/revalidate-page/route.ts`  
> **주의:** Commit 1(Edge)와 분리해서 **nodejs runtime**으로 두는 게 가장 안전함(페이지 revalidate는 `next/cache` 호출이 핵심이므로).

```ts
import { revalidatePath } from "next/cache";
import type { NextRequest } from "next/server";

export const runtime = "nodejs";

function json(status: number, body: Record<string, unknown>) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function methodNotAllowed() {
  return json(405, { ok: false, error: "method_not_allowed" });
}

function getSecret(req: NextRequest) {
  return req.headers.get("x-revalidate-secret") ?? "";
}

function isValidPath(path: string) {
  // Next 문서 제약(1024) 준수 + 내부 정책(절대경로만) + 범위 제한(예: /docs 아래만)
  if (!path) return false;
  if (path.length > 1024) return false;
  if (!path.startsWith("/")) return false;
  if (!path.startsWith("/docs")) return false;
  if (path.includes("..")) return false;
  if (path.includes("\\") || path.includes("\0")) return false;
  return true;
}

export async function POST(req: NextRequest) {
  const expected = process.env.REVALIDATE_SECRET ?? "";
  if (!expected) return json(500, { ok: false, error: "missing_server_secret" });

  const provided = getSecret(req);
  if (!provided) return json(401, { ok: false, error: "missing_secret" });
  if (provided !== expected) return json(401, { ok: false, error: "invalid_secret" });

  const ct = req.headers.get("content-type") ?? "";
  if (!ct.toLowerCase().includes("application/json")) {
    return json(415, { ok: false, error: "content_type_must_be_json" });
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return json(400, { ok: false, error: "invalid_json" });
  }

  const pagePath = (body as any)?.pagePath;
  const type = (body as any)?.type;

  if (typeof pagePath !== "string") {
    return json(400, { ok: false, error: "missing_pagePath" });
  }
  if (!isValidPath(pagePath)) {
    return json(400, { ok: false, error: "invalid_pagePath" });
  }

  // dynamic segment 패턴이면 type('page'|'layout') 필요 (Next 문서)
  if (typeof type !== "undefined" && type !== "page" && type !== "layout") {
    return json(400, { ok: false, error: "invalid_type" });
  }

  try {
    if (type) revalidatePath(pagePath, type);
    else revalidatePath(pagePath);

    return json(200, { ok: true, revalidated: true, pagePath, type: type ?? null, now: Date.now() });
  } catch (e: any) {
    return json(500, { ok: false, error: "revalidate_failed", message: String(e?.message ?? e) });
  }
}

// Explicitly block other methods (CI/보안 명확화)
export async function GET() { return methodNotAllowed(); }
export async function PUT() { return methodNotAllowed(); }
export async function PATCH() { return methodNotAllowed(); }
export async function DELETE() { return methodNotAllowed(); }
```

### curl (복붙용)

```bash
export REVALIDATE_URL="https://<your-domain>/api/revalidate-page"
export REVALIDATE_SECRET="(배포 환경과 동일한 값)"

curl -i -X POST "$REVALIDATE_URL" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -H "content-type: application/json" \
  -d '{"pagePath":"/docs/hello","type":"page"}'
```

---

**참고 자료**:
- [Next.js: revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)

