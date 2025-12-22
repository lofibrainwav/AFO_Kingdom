/**
 * 공통 로딩 스피너 컴포넌트
 * AFO Kingdom Dashboard - Unified Loading Component
 */

import type { LoadingProps } from "@/types/common";

const SIZE_CLASSES = {
  sm: "w-4 h-4",
  md: "w-8 h-8",
  lg: "w-16 h-16",
};

export function LoadingSpinner({
  size = "md",
  text,
  fullScreen = false,
  className = "",
}: LoadingProps) {
  const sizeClass = SIZE_CLASSES[size];
  const textSizeClass = size === "sm" ? "text-sm" : size === "md" ? "text-base" : "text-lg";

  const spinner = (
    <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
      <div
        className={`${sizeClass} border-4 border-gray-300 border-t-purple-500 rounded-full animate-spin`}
      />
      {text && <p className={`text-gray-300 ${textSizeClass} font-medium`}>{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
        {spinner}
      </div>
    );
  }

  return spinner;
}
