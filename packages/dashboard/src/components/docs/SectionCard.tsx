"use client";

import { ReactNode } from "react";
import { motion } from "framer-motion";

interface SectionCardProps {
  /**
   * 섹션 제목
   */
  title: string;
  /**
   * 섹션 내용
   */
  children: ReactNode;
  /**
   * 섹션 ID (선택사항)
   */
  id?: string;
  /**
   * 배지 (선택사항)
   */
  badge?: string;
  /**
   * 클래스명 (선택사항)
   */
  className?: string;
  /**
   * Glassmorphism 효과 (기본값: true)
   */
  glass?: boolean;
}

/**
 * 섹션 카드 컴포넌트
 * 
 * Glassmorphism 스타일의 섹션 카드
 * 
 * @example
 * ```tsx
 * <SectionCard
 *   title="시스템 아키텍처"
 *   badge="핵심"
 * >
 *   <p>아키텍처 설명...</p>
 * </SectionCard>
 * ```
 */
export function SectionCard({
  title,
  children,
  id,
  badge,
  className = "",
  glass = true,
}: SectionCardProps) {
  return (
    <motion.section
      id={id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`section-card ${className}`}
    >
      <div
        className={`rounded-3xl border ${
          glass
            ? "bg-white/30 backdrop-blur-sm border-white/40 shadow-inner"
            : "bg-white border-slate-200 shadow-sm"
        } p-6 md:p-8`}
      >
        {/* 헤더 */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-700">{title}</h2>
          {badge && (
            <span className="px-3 py-1 text-xs font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-700 rounded-full border border-indigo-500/30">
              {badge}
            </span>
          )}
        </div>

        {/* 내용 */}
        <div className="text-slate-600">{children}</div>
      </div>
    </motion.section>
  );
}

