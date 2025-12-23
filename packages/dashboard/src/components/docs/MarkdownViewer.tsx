"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";

interface MarkdownViewerProps {
  /**
   * Markdown 내용
   */
  content: string;
  /**
   * 클래스명 (선택사항)
   */
  className?: string;
  /**
   * 로딩 상태 (선택사항)
   */
  loading?: boolean;
}

/**
 * Markdown 뷰어 컴포넌트
 * 
 * 간단한 Markdown 렌더링 (향후 react-markdown 또는 remark로 확장 가능)
 * 
 * @example
 * ```tsx
 * <MarkdownViewer
 *   content="# 제목\n\n내용..."
 * />
 * ```
 */
export function MarkdownViewer({
  content,
  className = "",
  loading = false,
}: MarkdownViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [renderedContent, setRenderedContent] = useState<string>("");

  useEffect(() => {
    if (loading || !content) {
      setRenderedContent("");
      return;
    }

    // 간단한 Markdown 변환 (향후 라이브러리로 교체 가능)
    let html = content
      // 헤딩
      .replace(/^### (.*$)/gim, "<h3 class='text-xl font-bold text-slate-700 mt-6 mb-3'>$1</h3>")
      .replace(/^## (.*$)/gim, "<h2 class='text-2xl font-bold text-slate-700 mt-8 mb-4'>$1</h2>")
      .replace(/^# (.*$)/gim, "<h1 class='text-3xl font-bold text-slate-700 mt-10 mb-5'>$1</h1>")
      // 강조
      .replace(/\*\*(.*?)\*\*/gim, "<strong class='font-bold text-slate-700'>$1</strong>")
      .replace(/\*(.*?)\*/gim, "<em class='italic text-slate-600'>$1</em>")
      // 코드
      .replace(/`([^`]+)`/gim, "<code class='bg-slate-100 px-1.5 py-0.5 rounded text-sm font-mono text-slate-700'>$1</code>")
      // 링크
      .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, "<a href='$2' class='text-indigo-600 hover:text-indigo-800 underline' target='_blank' rel='noopener noreferrer'>$1</a>")
      // 리스트
      .replace(/^\* (.*$)/gim, "<li class='ml-4 mb-1'>$1</li>")
      .replace(/^- (.*$)/gim, "<li class='ml-4 mb-1'>$1</li>")
      // 줄바꿈
      .replace(/\n\n/gim, "</p><p class='mb-4 text-slate-600 leading-relaxed'>")
      .replace(/\n/gim, "<br />");

    // 리스트 래핑
    html = html.replace(/(<li.*<\/li>)/gim, "<ul class='list-disc ml-6 mb-4'>$1</ul>");

    // 문단 래핑
    if (!html.startsWith("<")) {
      html = `<p class='mb-4 text-slate-600 leading-relaxed'>${html}</p>`;
    }

    setRenderedContent(html);
  }, [content, loading]);

  if (loading) {
    return (
      <div className={`markdown-viewer loading ${className}`}>
        <div className="flex items-center justify-center p-8">
          <div className="animate-pulse text-slate-400">로딩 중...</div>
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

