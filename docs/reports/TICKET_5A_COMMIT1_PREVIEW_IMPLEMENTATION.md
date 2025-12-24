# Ticket 5-A Commit 1: Preview 모드 구현 (복붙 가능 코드)

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 1 (Preview 모드)  
**Status:** 🟡 **Ready for Implementation**

---

## 🎯 목표

쿼리 파라미터 `?preview=true` 기반 Preview 모드 구현
- Draft/Publish 분리
- 기존 fragment 유지 (overwrite 없음)
- Gate 영향 없음 (읽기 경로만 확장)

---

## 📋 구현 내용

### 1. Preview 모드 체크 (쿼리 파라미터)

```typescript
// [Ticket 5-A Commit 1] Preview 모드 체크
const searchParams = await getSearchParams(); // Next.js 15+ searchParams
const isPreview = searchParams.get('preview') === 'true';
```

### 2. Draft Fragment 읽기 (Preview 모드일 때)

```typescript
// [Ticket 5-A Commit 1] Draft fragment 경로
const draftFragmentPath = join(
  process.cwd(),
  "packages/dashboard/public/fragments/draft",
  `${fragmentKey}.html`
);

// Preview 모드일 때 Draft fragment 우선 읽기
const fragmentContent = isPreview
  ? await getFragmentContent(draftFragmentPath) || await getFragmentContent(fragmentKey)
  : await getFragmentContent(fragmentKey);
```

### 3. 기존 Fragment 유지 (overwrite 없음)

- 기존 `public/fragments/{fragment_key}.html` 유지
- Draft는 별도 경로: `public/fragments/draft/{fragment_key}.html`
- Preview 모드가 아니면 기존 fragment 그대로 사용

---

## 🔧 수정할 파일

### `packages/dashboard/src/app/docs/[slug]/page.tsx`

**변경 내용:**
1. `getSearchParams()` import 추가
2. Preview 모드 체크 로직 추가
3. Draft fragment 읽기 로직 추가
4. 기존 fragment 유지 (overwrite 없음)

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

### 전체 파일 (수정 후)

```typescript
import { notFound } from "next/navigation";
import { readFile } from "fs/promises";
import { join } from "path";
import type { Metadata } from "next";
import { headers } from "next/headers";
import generated from "@/generated/widgets.generated.json";

type Payload = {
  widgets: Array<{
    id: string;
    title: string;
    fragment_key?: string | null;
    dataWidgetId?: string | null;
    sourceId?: string | null;
    html_section_id?: string | null;
  }>;
};

// [Ticket 4] slug 검증 (Contract Gate와 동일 규칙)
// SSOT: 허용 문자: a-z, 0-9, -, 가-힣
// 연속 하이픈(--), 양끝 하이픈(-foo / foo-) 불가
function isValidSlug(slug: string): boolean {
  const slugPattern = /^[a-z0-9가-힣\-]+$/;
  if (!slugPattern.test(slug)) return false;
  if (slug.includes("--")) return false; // 연속 하이픈 불가
  if (slug.startsWith("-") || slug.endsWith("-")) return false; // 양끝 하이픈 불가
  return true;
}

// [Ticket 4-A] 정적 생성: 모든 slug를 빌드 타임에 고정
export async function generateStaticParams() {
  const payload = generated as unknown as Payload;
  const widgets = payload.widgets || [];

  // 유효한 slug만 반환 (Contract Gate 규칙 준수)
  const validSlugs = widgets
    .map((w) => w.id)
    .filter((slug) => isValidSlug(slug));

  return validSlugs.map((slug) => ({
    slug,
  }));
}

// [Ticket 4-A] Metadata 자동 생성
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const resolvedParams = await params;
  const slug = resolvedParams.slug;

  const payload = generated as unknown as Payload;
  const w = (payload.widgets || []).find((x) => x.id === slug);

  if (!w) {
    return {
      title: "Not Found",
    };
  }

  return {
    title: `${w.title} | AFO Kingdom Docs`,
    description: w.fragment_key || `Documentation for ${w.title}`,
  };
}

// [Ticket 3] fragment 파일 읽기 (fallback: fragment_key ?? html_section_id ?? sourceId)
async function getFragmentContent(fragmentPath: string): Promise<string | null> {
  try {
    const content = await readFile(fragmentPath, "utf-8");
    return content;
  } catch {
    return null;
  }
}

// [Ticket 5-A Commit 1] Preview 모드 체크 (쿼리 파라미터)
async function getSearchParams(): Promise<URLSearchParams> {
  const headersList = await headers();
  const referer = headersList.get("referer") || "";
  const url = new URL(referer || "http://localhost");
  return url.searchParams;
}

export default async function DocWidgetPage({ 
  params,
  searchParams 
}: { 
  params: Promise<{ slug: string }>;
  searchParams?: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  // Next.js 15+ params는 Promise
  const resolvedParams = await params;
  const slug = resolvedParams.slug;

  // [Ticket 5-A Commit 1] Preview 모드 체크
  const resolvedSearchParams = searchParams ? await searchParams : new URLSearchParams();
  const isPreview = resolvedSearchParams.get('preview') === 'true';

  // 1. slug 검증
  if (!isValidSlug(slug)) {
    return notFound();
  }

  // 2. 위젯 찾기
  const payload = generated as unknown as Payload;
  const w = (payload.widgets || []).find((x) => x.id === slug);
  if (!w) return notFound();

  // 3. [Ticket 4-B] Override 우선순위 규칙 (SSOT)
  // 규칙 1: registry에 React 컴포넌트가 있으면 무조건 override
  // 규칙 2: 없으면 fragment 렌더
  // 규칙 3: 둘 다 없으면 404
  
  // Override 체크 (registry에서 React 컴포넌트 확인)
  const { getWidget } = await import("@/widgets/registry");
  const widgetEntry = getWidget(slug);
  
  // TODO: registry에 React 컴포넌트 저장 기능 추가 시 활성화
  // if (widgetEntry?.component) {
  //   return <widgetEntry.component />;
  // }

  // 4. fragment_key 결정 (fallback: fragment_key ?? html_section_id ?? sourceId)
  const fragmentKey = w.fragment_key || w.html_section_id || w.sourceId || w.id;

  // 5. [Ticket 5-A Commit 1] Fragment 파일 읽기 (Preview 모드 지원)
  // Preview 모드일 때 Draft fragment 우선 읽기, 없으면 기존 fragment 사용
  const publishFragmentPath = join(process.cwd(), "packages/dashboard/public/fragments", `${fragmentKey}.html`);
  const draftFragmentPath = join(process.cwd(), "packages/dashboard/public/fragments/draft", `${fragmentKey}.html`);
  
  let fragmentContent: string | null = null;
  
  if (isPreview) {
    // Preview 모드: Draft 우선, 없으면 Publish 사용
    fragmentContent = await getFragmentContent(draftFragmentPath) || await getFragmentContent(publishFragmentPath);
  } else {
    // 일반 모드: Publish만 사용
    fragmentContent = await getFragmentContent(publishFragmentPath);
  }

  // 6. Fragment 렌더 또는 404
  if (!fragmentContent) {
    return notFound();
  }

  return (
    <div className="p-6 space-y-4">
      <div className="flex gap-3">
        <a className="underline" href="/docs">Back</a>
        {isPreview && (
          <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded text-sm">
            Preview Mode
          </span>
        )}
        <a className="underline" href={`/legacy/kingdom_dashboard.html#${w.sourceId || ""}`}>
          Open in Legacy
        </a>
      </div>

      <h1 className="text-2xl font-semibold">{w.title}</h1>
      
      {/* [Ticket 3] Fragment 렌더 */}
      <div
        className="prose prose-invert max-w-none"
        dangerouslySetInnerHTML={{ __html: fragmentContent }}
      />
    </div>
  );
}
```

---

## ✅ 검증 체크리스트

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

### 2. Preview 모드 테스트

```bash
# Preview 모드 테스트
curl "http://localhost:3000/docs/philosophy-widget?preview=true"

# 일반 모드 테스트 (기존 fragment 유지)
curl "http://localhost:3000/docs/philosophy-widget"

# Draft fragment 없을 때 (Publish fragment 사용)
# (draft 폴더에 파일 없으면 자동으로 publish 사용)
```

---

## 🔒 안전 범위 명확화

### ✅ 유지할 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   * slug 검증 (Contract Gate와 동일)
   * fragment_key 필수 (빌드 타임 검증)
   * 렌더링 우선순위 (React → Fragment → 404)

2. **Gate 검증**
   * 빌드 타임 검증 유지
   * Contract Gate 유지
   * fragment_key 검증 유지

3. **기존 Fragment**
   * `public/fragments/{fragment_key}.html` 유지
   * fragment overwrite 없음

### ✅ 확장 가능한 것 (읽기 경로만)

1. **Preview 모드**
   * 쿼리 파라미터 `?preview=true` 체크
   * Draft fragment 읽기 (`public/fragments/draft/{fragment_key}.html`)
   * 기존 fragment 유지 (overwrite 없음)

---

## 🏁 결론

Commit 1 (Preview 모드)는 **읽기 경로만 확장**하는 안전한 구현입니다.

**안전 범위:**
* SSOT 규칙 유지
* Gate 영향 없음
* 기존 fragment 유지

**구현 계획:**
* 쿼리 파라미터 기반 Preview 모드
* Draft/Publish 분리
* 기존 fragment overwrite 없음

---

**Status:** 🟡 **Ready for Implementation**  
**Next Action:** 형님 승인 후 구현 시작

