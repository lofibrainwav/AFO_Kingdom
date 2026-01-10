"use client";

import DOMPurify from "isomorphic-dompurify";
import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";

interface MermaidDiagramProps {
  /**
   * Mermaid 다이어그램 코드
   * @example "graph TD\n    A[Start] --> B[End]"
   */
  code: string;
  /**
   * 다이어그램 제목 (선택사항)
   */
  title?: string;
  /**
   * 클래스명 (선택사항)
   */
  className?: string;
  /**
   * 지연 로딩 여부 (기본값: true)
   */
  lazy?: boolean;
}

/**
 * Mermaid 다이어그램 렌더링 컴포넌트
 * 
 * SSR/하이드레이션 불일치를 방지하기 위해 클라이언트 전용으로 구현
 * Intersection Observer를 사용한 지연 로딩 지원
 * 
 * @example
 * ```tsx
 * <MermaidDiagram
 *   code="graph TD\n    A[Start] --> B[End]"
 *   title="시스템 플로우"
 * />
 * ```
 */
export function MermaidDiagram({
  code,
  title,
  className = "",
  lazy = true,
}: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(!lazy);
  const [isRendered, setIsRendered] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Intersection Observer for lazy loading
  useEffect(() => {
    if (!lazy || isVisible) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
            observer.disconnect();
          }
        });
      },
      { rootMargin: "50px" }
    );

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, [lazy, isVisible]);

  // Mermaid 렌더링
  useEffect(() => {
    if (!isVisible || isRendered || !containerRef.current) return;

    const renderMermaid = async () => {
      try {
        // 동적 임포트로 Mermaid 로드
        const mermaid = (await import("mermaid")).default;

        // Mermaid 초기화 (Phase 15 Security Seal: securityLevel "strict")
        mermaid.initialize({
          startOnLoad: false,
          theme: "default",
          securityLevel: "strict", // XSS 방지: loose → strict
          flowchart: {
            useMaxWidth: true,
            htmlLabels: false, // XSS 방지: HTML 레이블 비활성화
          },
        });

        // 고유 ID 생성
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
        const element = containerRef.current;
        if (!element) return;

        // XSS 방지: 코드 새니타이징 후 컨테이너 준비
        const sanitizedCode = DOMPurify.sanitize(code, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
        element.innerHTML = `<div class="mermaid" id="${id}">${sanitizedCode}</div>`;

        // 렌더링
        await mermaid.run({
          nodes: [element.querySelector(`#${id}`)!],
        });

        setIsRendered(true);
        setError(null);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Mermaid 렌더링 실패";
        setError(errorMessage);
        console.error("Mermaid 렌더링 오류:", err);
      }
    };

    renderMermaid();
  }, [isVisible, code, isRendered]);

  return (
    <motion.div
      ref={containerRef}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: isVisible ? 1 : 0.3, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`mermaid-container ${className}`}
    >
      {title && (
        <div className="mb-4">
          <h3 className="text-lg font-bold text-slate-700">{title}</h3>
        </div>
      )}

      {error ? (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">
            다이어그램 렌더링 실패: {error}
          </p>
          <pre className="mt-2 text-xs text-red-500 overflow-x-auto">
            {code}
          </pre>
        </div>
      ) : !isVisible ? (
        <div className="p-8 bg-slate-100 rounded-lg text-center">
          <p className="text-sm text-slate-500">다이어그램 로딩 중...</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg p-4 border border-slate-200 overflow-x-auto">
          {/* Mermaid가 여기에 렌더링됨 */}
        </div>
      )}
    </motion.div>
  );
}

