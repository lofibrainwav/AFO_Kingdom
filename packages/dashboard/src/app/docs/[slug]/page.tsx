import generated from '@/generated/widgets.generated.json';
import DOMPurify from 'isomorphic-dompurify';
import { readFile } from 'fs/promises';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { join } from 'path';

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

function isValidSlug(slug: string): boolean {
  const slugPattern = /^[a-z0-9가-힣\-]+$/;
  if (!slugPattern.test(slug)) return false;
  if (slug.includes('--')) return false; 
  if (slug.startsWith('-') || slug.endsWith('-')) return false; 
  return true;
}

export async function generateStaticParams() {
  const payload = generated as unknown as Payload;
  const widgets = payload.widgets || [];

  const validSlugs = widgets
    .map((w) => w.id)
    .filter((slug) => isValidSlug(slug));

  return validSlugs.map((slug) => ({
    slug,
  }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const resolvedParams = await params;
  const slug = resolvedParams.slug;

  const payload = generated as unknown as Payload;
  const w = (payload.widgets || []).find((x) => x.id === slug);

  if (!w) {
    return {
      title: 'Not Found',
    };
  }

  return {
    title: `${w.title} | AFO Kingdom Docs`,
    description: w.fragment_key || `Documentation for ${w.title}`,
  };
}

async function getFragmentContent(fragmentPath: string): Promise<string | null> {
  try {
    const content = await readFile(fragmentPath, 'utf-8');
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
  const resolvedParams = await params;
  const slug = resolvedParams.slug;

  const resolvedSearchParams = searchParams ? await searchParams : {};
  const isPreview = resolvedSearchParams.preview === 'true';

  if (!isValidSlug(slug)) {
    return notFound();
  }

  const payload = generated as unknown as Payload;
  const w = (payload.widgets || []).find((x) => x.id === slug);
  if (!w) return notFound();

  const { getWidget } = await import('@/widgets/registry');
  const widgetEntry = getWidget(slug);
  
  const fragmentKey = w.fragment_key || w.html_section_id || w.sourceId || w.id;

  const publishFragmentPath = join(process.cwd(), 'packages/dashboard/public/fragments', `${fragmentKey}.html`);
  const draftFragmentPath = join(process.cwd(), 'packages/dashboard/public/fragments/draft', `${fragmentKey}.html`);
  
  let fragmentContent: string | null = null;
  
  if (isPreview) {
    fragmentContent = await getFragmentContent(draftFragmentPath) || await getFragmentContent(publishFragmentPath);
  } else {
    fragmentContent = await getFragmentContent(publishFragmentPath);
  }

  if (!fragmentContent) {
    return notFound();
  }

  return (
    <div className='p-6 space-y-4'>
      <div className='flex gap-3 items-center'>
        <Link className='underline' href='/docs'>Back</Link>
        {isPreview && (
          <span className='px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded text-sm'>
            Preview Mode
          </span>
        )}
        <Link className='underline' href={`/legacy/kingdom_dashboard.html#${w.sourceId || ''}`}>
          Open in Legacy
        </Link>
      </div>

      <h1 className='text-2xl font-semibold'>{w.title}</h1>
      
      <div
        className='prose prose-invert max-w-none'
        dangerouslySetInnerHTML={{
          // XSS 방지: DOMPurify로 새니타이징 (Phase 15 Security Seal)
          __html: DOMPurify.sanitize(fragmentContent, { USE_PROFILES: { html: true } }),
        }}
      />
    </div>
  );
}
