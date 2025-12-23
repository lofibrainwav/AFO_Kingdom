"use client";

import { useEffect, ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";

interface ModalProps {
  /**
   * 모달 표시 여부
   */
  isOpen: boolean;
  /**
   * 모달 닫기 함수
   */
  onClose: () => void;
  /**
   * 모달 제목
   */
  title?: string;
  /**
   * 모달 내용
   */
  children: ReactNode;
  /**
   * 모달 크기 (sm, md, lg, xl)
   */
  size?: "sm" | "md" | "lg" | "xl";
  /**
   * 배경 클릭 시 닫기 여부
   */
  closeOnBackdropClick?: boolean;
}

/**
 * 범용 모달 컴포넌트
 * 
 * @example
 * ```tsx
 * <Modal
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   title="모달 제목"
 *   size="lg"
 * >
 *   <p>모달 내용</p>
 * </Modal>
 * ```
 */
export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
  closeOnBackdropClick = true,
}: ModalProps) {
  // ESC 키로 닫기
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-2xl",
    lg: "max-w-4xl",
    xl: "max-w-6xl",
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeOnBackdropClick ? onClose : undefined}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              onClick={(e) => e.stopPropagation()}
              className={`w-full ${sizeClasses[size]} bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl border border-white/40 pointer-events-auto max-h-[90vh] overflow-hidden flex flex-col`}
            >
              {/* Header */}
              {title && (
                <div className="flex items-center justify-between p-6 border-b border-slate-200/50">
                  <h2 className="text-2xl font-bold text-slate-700">{title}</h2>
                  <button
                    onClick={onClose}
                    className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                    aria-label="닫기"
                  >
                    <X className="w-5 h-5 text-slate-600" />
                  </button>
                </div>
              )}

              {/* Content */}
              <div className="flex-1 overflow-y-auto p-6">{children}</div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}

