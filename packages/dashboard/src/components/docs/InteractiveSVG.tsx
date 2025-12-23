"use client";

import { ReactNode, useState, useCallback } from "react";
import { motion } from "framer-motion";

interface InteractiveSVGProps {
  /**
   * SVG 내용 (JSX 또는 HTML 문자열)
   */
  children: ReactNode;
  /**
   * 클릭 핸들러 (선택사항)
   */
  onClick?: (event: React.MouseEvent<SVGSVGElement>) => void;
  /**
   * 호버 효과 (기본값: true)
   */
  hover?: boolean;
  /**
   * 클래스명 (선택사항)
   */
  className?: string;
  /**
   * 너비 (선택사항)
   */
  width?: number | string;
  /**
   * 높이 (선택사항)
   */
  height?: number | string;
}

/**
 * 인터랙티브 SVG 래퍼 컴포넌트
 * 
 * 클릭 이벤트와 호버 효과를 지원하는 SVG 컨테이너
 * 
 * @example
 * ```tsx
 * <InteractiveSVG
 *   onClick={(e) => console.log('클릭됨')}
 *   hover
 * >
 *   <svg>...</svg>
 * </InteractiveSVG>
 * ```
 */
export function InteractiveSVG({
  children,
  onClick,
  hover = true,
  className = "",
  width,
  height,
}: InteractiveSVGProps) {
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseEnter = useCallback(() => {
    if (hover) setIsHovered(true);
  }, [hover]);

  const handleMouseLeave = useCallback(() => {
    if (hover) setIsHovered(false);
  }, [hover]);

  return (
    <motion.div
      className={`interactive-svg-container ${className}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      animate={{
        scale: isHovered ? 1.02 : 1,
      }}
      transition={{ duration: 0.2 }}
    >
      <svg
        onClick={onClick}
        width={width}
        height={height}
        className="w-full h-auto"
        style={{ cursor: onClick ? "pointer" : "default" }}
      >
        {children}
      </svg>
    </motion.div>
  );
}

