'use client';

import { motion } from 'framer-motion';
import { useMemo, useRef } from 'react';

interface MarkdownViewerProps {
  content: string;
  className?: string;
  loading?: boolean;
}

export function MarkdownViewer({
  content,
  className = '',
  loading = false,
}: MarkdownViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  const renderedContent = useMemo(() => {
    if (loading || !content) {
      return '';
    }

    let html = content
      .replace(/^### (.*$)/gim, '<h3 class=\"text-xl font-bold text-slate-700 mt-6 mb-3\">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class=\"text-2xl font-bold text-slate-700 mt-8 mb-4\">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class=\"text-3xl font-bold text-slate-700 mt-10 mb-5\">$1</h1>')
      .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong class=\"font-bold text-slate-700\">$1</strong>')
      .replace(/\\*(.*?)\\*/gim, '<em class=\"italic text-slate-600\">$1</em>')
      .replace(/`([^`]+)`/gim, '<code class=\"bg-slate-100 px-1.5 py-0.5 rounded text-sm font-mono text-slate-700\">$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" class="text-indigo-600 hover:text-indigo-800 underline" target="_blank" rel="noopener noreferrer">$1</a>')
      .replace(/^\\* (.*$)/gim, '<li class=\"ml-4 mb-1\">$1</li>')
      .replace(/^- (.*$)/gim, '<li class=\"ml-4 mb-1\">$1</li>')
      .replace(/\\n\\n/gim, '</p><p class=\"mb-4 text-slate-600 leading-relaxed\">')
      .replace(/\\n/gim, '<br />');

    html = html.replace(/(<li.*<\/li>)/gim, '<ul class="list-disc ml-6 mb-4">$1</ul>');

    if (!html.startsWith('<')) {
      html = `<p class=\"mb-4 text-slate-600 leading-relaxed\">${html}</p>`;
    }

    return html;
  }, [content, loading]);

  if (loading) {
    return (
      <div className={`markdown-viewer loading ${className}`}>
        <div className='flex items-center justify-center p-8'>
          <div className='animate-pulse text-slate-400'>로딩 중...</div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      ref={containerRef}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className={`markdown-viewer prose prose-slate max-w-none ${className}`}
      dangerouslySetInnerHTML={{ __html: renderedContent }}
    />
  );
}
