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

