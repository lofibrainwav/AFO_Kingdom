/**
 * 공통 에러 메시지 컴포넌트
 * AFO Kingdom Dashboard - Unified Error Component
 */

import { AlertTriangle, RefreshCw } from 'lucide-react';
import type { ErrorProps } from '@/types/common';

export function ErrorMessage({
  message,
  onRetry,
  retryText = '다시 시도',
  className = '',
}: ErrorProps) {
  return (
    <div
      className={`bg-red-900/20 border border-red-500/50 rounded-lg p-6 ${className}`}
    >
      <div className="flex items-start gap-4">
        <AlertTriangle className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="text-red-300 text-lg font-semibold mb-2">오류 발생</h3>
          <p className="text-red-400 text-sm">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-white text-sm font-medium flex items-center gap-2 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              {retryText}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

