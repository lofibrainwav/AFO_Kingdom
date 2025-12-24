import { notFound } from "next/navigation";
import { readFile } from "fs/promises";
import { join } from "path";
import type { Metadata } from "next";
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

// [Ticket 3] fragment 파일 읽기 (경로 직접 지정)
async function getFragmentContent(fragmentPath: string): Promise<string | null> {
  try {
    const content = await readFile(fragmentPath, "utf-8");
    return content;
  } catch {
    return null;
  }
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

  // [Ticket 5-A Commit 1] Preview 모드 체크 (쿼리 파라미터)
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const isPreview = resolvedSearchParams.preview === 'true';

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
  // 정책: draft 없으면 publish로 fallback (Preview UX 부드러움)
  const publishFragmentPath = join(process.cwd(), "packages/dashboard/public/fragments", `${fragmentKey}.html`);
  const draftFragmentPath = join(process.cwd(), "packages/dashboard/public/fragments/draft", `${fragmentKey}.html`);
  
  let fragmentContent: string | null = null;
  
  if (isPreview) {
    // Preview 모드: Draft 우선, 없으면 Publish로 fallback (정책 A안)
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
      <div className="flex gap-3 items-center">
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
