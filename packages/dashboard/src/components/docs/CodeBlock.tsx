"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { motion } from "framer-motion";

interface CodeBlockProps {
  /**
   * 코드 내용
   */
  code: string;
  /**
   * 언어 (선택사항)
   * @example "typescript", "python", "bash"
   */
  language?: string;
  /**
   * 파일명 (선택사항)
   */
  filename?: string;
  /**
   * 복사 버튼 표시 여부 (기본값: true)
   */
  showCopy?: boolean;
  /**
   * 클래스명 (선택사항)
   */
  className?: string;
}

/**
 * 코드 블록 컴포넌트
 * 
 * 간단한 코드 하이라이팅과 복사 기능 제공
 * 향후 react-syntax-highlighter 또는 shiki로 확장 가능
 * 
 * @example
 * ```tsx
 * <CodeBlock
 *   code="const x = 1;"
 *   language="typescript"
 *   filename="example.ts"
 * />
 * ```
 */
export function CodeBlock({
  code,
  language,
  filename,
  showCopy = true,
  className = "",
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("복사 실패:", err);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`relative ${className}`}
    >
      {/* 헤더 */}
      {(filename || language) && (
        <div className="flex items-center justify-between px-4 py-2 bg-slate-800 rounded-t-lg border-b border-slate-700">
          <div className="flex items-center gap-2">
            {filename && (
              <span className="text-xs font-mono text-slate-300">
                {filename}
              </span>
            )}
            {language && (
              <span className="text-xs px-2 py-0.5 bg-slate-700 rounded text-slate-400">
                {language}
              </span>
            )}
          </div>
          {showCopy && (
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 px-2 py-1 text-xs text-slate-400 hover:text-slate-200 transition-colors"
              aria-label="코드 복사"
            >
              {copied ? (
                <>
                  <Check className="w-3 h-3" />
                  <span>복사됨</span>
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" />
                  <span>복사</span>
                </>
              )}
            </button>
          )}
        </div>
      )}

      {/* 코드 블록 */}
      <div className="relative">
        <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm font-mono leading-relaxed">
          <code>{code}</code>
        </pre>

        {/* 복사 버튼 (헤더 없을 때) */}
        {showCopy && !filename && !language && (
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 p-2 bg-slate-800 hover:bg-slate-700 rounded text-slate-400 hover:text-slate-200 transition-colors"
            aria-label="코드 복사"
          >
            {copied ? (
              <Check className="w-4 h-4" />
            ) : (
              <Copy className="w-4 h-4" />
            )}
          </button>
        )}
      </div>
    </motion.div>
  );
}

