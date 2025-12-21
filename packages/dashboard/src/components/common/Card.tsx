/**
 * 공통 카드 컴포넌트
 * AFO Kingdom Dashboard - Unified Card Component
 */

import type { CardProps } from '@/types/common';

export function Card({
  title,
  subtitle,
  icon,
  gradient = 'from-gray-800/50 to-gray-900/50',
  border = 'border-gray-700',
  className = '',
  children,
}: CardProps) {
  return (
    <div
      className={`bg-gradient-to-br ${gradient} backdrop-blur-sm rounded-xl p-6 border ${border} shadow-lg ${className}`}
    >
      {(title || subtitle || icon) && (
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            {icon && <div className="text-2xl">{icon}</div>}
            <div>
              {title && (
                <h3 className="text-xl font-bold text-white">{title}</h3>
              )}
              {subtitle && (
                <p className="text-gray-400 text-sm mt-1">{subtitle}</p>
              )}
            </div>
          </div>
        </div>
      )}
      {children}
    </div>
  );
}

