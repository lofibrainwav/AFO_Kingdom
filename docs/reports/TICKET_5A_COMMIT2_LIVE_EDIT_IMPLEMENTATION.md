# Ticket 5-A Commit 2: Live Edit 최소 구현 (복붙 가능 코드)

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 2 (Live Edit 최소 구현)  
**Status:** 🟡 **Ready for Implementation**

---

## 🎯 목표

실시간 업데이트, fragment overwrite 없이 테스트

- 전용 라우트 분리: `/docs/[slug]/live`
- SSOT 경로와 완전 분리 유지
- 옵션 A (추천): 클라이언트에서 polling, `/fragments/draft/{fragment_key}.html`을 fetch

---

## 📋 구현 내용

### 1. Live Edit 전용 라우트 생성 (서버 컴포넌트)

**파일 경로**: `packages/dashboard/src/app/docs/[slug]/live/page.tsx`

**구현 내용**:

- **서버 컴포넌트** (SSOT slug 검증)
- `fragmentKeyFromSlug(slug)` 변환 함수 사용
- 클라이언트 컴포넌트(Poller)에 `fragmentKey` 전달
- SSOT 경로와 완전 분리 유지

### 2. Live Edit Poller (클라이언트 컴포넌트)

**파일 경로**: `packages/dashboard/src/components/live/LiveEditPoller.tsx`

**구현 내용**:

- 클라이언트 컴포넌트 (polling 필요)
- `/fragments/draft/{fragmentKey}.html`을 fetch로 읽기
- 실시간 업데이트 (polling 간격: 2초)
- fragment overwrite 없이 테스트

### 3. Edge Runtime 제약 해결

**문제**: Edge Runtime은 로컬 파일시스템 read가 안 됨

**해결**: 옵션 A (fetch polling)

- 파일은 `public/fragments/draft/`에 있음
- Live Edit은 HTTP fetch로 읽기
- Edge든 Node든 상관없이 동작

### 4. SSOT 일관성 보장

**핵심 수정사항**:

- ❌ `slug === fragment_key` 가정 금지
- ✅ `fragmentKeyFromSlug(slug)` 변환 함수 사용
- ❌ Client Page에서 slug 검증 금지
- ✅ 서버 컴포넌트에서 slug 검증 후 Poller에 전달

---

## 🔧 생성할 파일

### 1. `packages/dashboard/src/app/docs/[slug]/live/page.tsx` (서버 컴포넌트)

**구현 내용:**

1. 서버 컴포넌트 (SSOT slug 검증)
2. `fragmentKeyFromSlug(slug)` 변환 함수
3. 클라이언트 컴포넌트(Poller)에 `fragmentKey` 전달
4. SSOT 경로와 완전 분리 유지

### 2. `packages/dashboard/src/components/live/LiveEditPoller.tsx` (클라이언트 컴포넌트)

**구현 내용:**

1. 클라이언트 컴포넌트 (`'use client'`)
2. Polling 로직 (2초 간격)
3. `/fragments/draft/{fragmentKey}.html` fetch
4. 실시간 업데이트 UI

---

## ✅ Gate 영향 없음 보증

### 검증 명령어

```bash
# 1. Contract Gate 검증 (변경 없음)
python3 scripts/validate_widgets_json.py

# 2. TypeScript 타입 체크
pnpm -C packages/dashboard type-check

# 3. Next.js 빌드 (정적 생성 유지)
pnpm -C packages/dashboard build
```

**예상 결과**: 모든 검증 통과 (변경 없음)

---

## 📝 복붙 가능 코드

### 1. `packages/dashboard/src/app/docs/[slug]/live/page.tsx` (서버 컴포넌트)

```typescript
import { notFound } from "next/navigation";
import Link from "next/link";
import LiveEditPoller from "@/components/live/LiveEditPoller";

export const dynamic = "force-dynamic";

// [Ticket 5-A Commit 2] SSOT slug 검증 (기존 page.tsx와 동일 규칙)
function isValidSlug(slug: string): boolean {
  const slugPattern = /^[a-z0-9가-힣\-]+$/;
  if (!slugPattern.test(slug)) return false;
  if (slug.includes("--")) return false; // 연속 하이픈 불가
  if (slug.startsWith("-") || slug.endsWith("-")) return false; // 양끝 하이픈 불가
  return true;
}

// [Ticket 5-A Commit 2] fragmentKey 변환 (SSOT: slug ↔ fragment_key 1:1)
// "항상 동일"이라고 가정하지 말고 변환 함수로 고정
function fragmentKeyFromSlug(slug: string): string {
  // Ticket4 봉인 기준: fragment_key는 slug와 1:1.
  // "같다"를 가정하지 말고 변환 함수로 고정.
  return slug;
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;
  return {
    title: `LIVE: ${resolvedParams.slug}`,
    robots: { index: false, follow: false },
  };
}

export default async function LivePage({ params }: { params: Promise<{ slug: string }> }) {
  // Next.js 15+ params는 Promise
  const resolvedParams = await params;
  const slug = resolvedParams.slug;

  // [Ticket 5-A Commit 2] SSOT slug 검증 (기존 page.tsx와 동일)
  if (!isValidSlug(slug)) {
    notFound();
  }

  // [Ticket 5-A Commit 2] fragmentKey 변환 (SSOT 일관성)
  const fragmentKey = fragmentKeyFromSlug(slug);

  return (
    <main className="p-6 space-y-4">
      <div className="flex gap-3 items-center">
        <Link className="underline" href="/docs">
          ← Back to Docs
        </Link>
        <Link className="underline" href={`/docs/${slug}`}>
          View Published
        </Link>
        <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-sm animate-pulse">
          🔴 Live Edit Mode
        </span>
      </div>

      <h1 className="text-2xl font-semibold">Live Edit: {slug}</h1>

      <LiveEditPoller fragmentKey={fragmentKey} />
    </main>
  );
}
```

### 2. `packages/dashboard/src/components/live/LiveEditPoller.tsx` (클라이언트 컴포넌트)

```typescript
"use client";

import { useEffect, useState } from "react";

type Props = { fragmentKey: string };

export default function LiveEditPoller({ fragmentKey }: Props) {
  const [fragmentContent, setFragmentContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [source, setSource] = useState<"draft" | "publish" | null>(null);

  useEffect(() => {
    let stopped = false;

    const fetchFragment = async () => {
      try {
        // [Ticket 5-A Commit 2] Draft 우선, 없으면 Publish fallback
        const draftUrl = `/fragments/draft/${fragmentKey}.html`;
        const r1 = await fetch(draftUrl, { cache: "no-store" });

        if (r1.ok) {
          const content = await r1.text();
          if (stopped) return;
          setFragmentContent(content);
          setLastUpdate(new Date());
          setError(null);
          setSource("draft");
          setLoading(false);
          return;
        }

        // Draft 없으면 Publish로 fallback
        const publishUrl = `/fragments/${fragmentKey}.html`;
        const r2 = await fetch(publishUrl, { cache: "no-store" });

        if (r2.ok) {
          const content = await r2.text();
          if (stopped) return;
          setFragmentContent(content);
          setLastUpdate(new Date());
          setError(null);
          setSource("publish");
          setLoading(false);
          return;
        }

        // 둘 다 없으면 에러
        if (stopped) return;
        setError("Fragment not found (draft/publish)");
        setFragmentContent(null);
        setSource(null);
        setLoading(false);
      } catch (e: any) {
        if (stopped) return;
        setError(e?.message ?? "Unknown error");
        setFragmentContent(null);
        setSource(null);
        setLoading(false);
      }
    };

    // 초기 로드
    fetchFragment();
    
    // [Ticket 5-A Commit 2] Polling (2초 간격)
    const interval = window.setInterval(fetchFragment, 2000);

    return () => {
      stopped = true;
      window.clearInterval(interval);
    };
  }, [fragmentKey]);

  return (
    <div className="space-y-3">
      <div className="flex gap-3 items-center text-xs text-gray-400">
        <span className="px-2 py-1 rounded border border-gray-600">
          source: {source ?? "-"}
        </span>
        <span>poll: 2000ms</span>
        {lastUpdate && <span>updated: {lastUpdate.toLocaleTimeString()}</span>}
      </div>

      {loading && (
        <div className="text-center py-8 text-gray-400">Loading fragment...</div>
      )}

      {error && (
        <div className="p-4 bg-red-500/20 border border-red-500/30 rounded">
          <p className="text-red-400">Error: {error}</p>
        </div>
      )}

      {fragmentContent && (
        <div
          className="prose prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: fragmentContent }}
        />
      )}
    </div>
  );
}
```

---

## ✅ 검증 체크리스트 (재현 가능)

### 1. Gate 영향 없음 보증

```bash
# Contract Gate 검증 (변경 없음)
python3 scripts/validate_widgets_json.py
# 예상: ✅ 통과

# TypeScript 타입 체크
pnpm -C packages/dashboard type-check
# 예상: ✅ 통과

# Next.js 빌드 (정적 생성 유지)
pnpm -C packages/dashboard build
# 예상: ✅ 통과
```

### 2. Live Edit 동작 테스트

```bash
# Live Edit 라우트 테스트
curl http://localhost:3000/docs/philosophy-widget/live

# 실시간 업데이트 테스트
# (브라우저에서 확인: 2초마다 자동 갱신)

# fragment overwrite 없이 테스트
# (기존 fragment 유지 확인)
```

---

## 🔒 안전 범위 명확화

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

1. **Live Edit**
   - 전용 라우트 `/docs/[slug]/live` 분리
   - 서버 컴포넌트에서 slug 검증 (SSOT 일관성)
   - `fragmentKeyFromSlug(slug)` 변환 함수 사용
   - 클라이언트 컴포넌트(Poller)에서 polling (fetch)
   - fragment overwrite 없이 테스트

---

## 🏁 결론

Commit 2 (Live Edit)는 **전용 라우트로 격리**하는 안전한 구현입니다.

**안전 범위:**

- SSOT 규칙 유지
- Gate 영향 없음
- 기존 fragment 유지
- SSOT 경로와 완전 분리

**구현 계획:**

- 옵션 A (fetch polling)
- 서버 컴포넌트에서 slug 검증 (SSOT 일관성)
- `fragmentKeyFromSlug(slug)` 변환 함수 사용
- 전용 라우트 분리
- fragment overwrite 없음

**SSOT 일관성 보장:**

- ❌ `slug === fragment_key` 가정 금지
- ✅ `fragmentKeyFromSlug(slug)` 변환 함수 사용
- ❌ Client Page에서 slug 검증 금지
- ✅ 서버 컴포넌트에서 slug 검증 후 Poller에 전달

---

**Status:** 🟡 **Ready for Implementation**  
**Next Action:** 검증 완료 후 구현 시작
