/**
 * BudgetDashboard.tsx
 *
 * Phase 12 Extension: 실시간 예산 대시보드
 * "금고 안전! Julie CPA가 왕국 부를 지켜요" 🛡️💰
 */
'use client';

import React from 'react';
import { useApi } from '@/hooks/useApi';
import { LoadingSpinner, ErrorMessage } from '@/components/common';
import { REFRESH_INTERVALS } from '@/lib/constants';

interface BudgetCategory {
  id: number;
  category: string;
  allocated: number;
  spent: number;
  remaining: number;
}

interface BudgetData {
  budgets: BudgetCategory[];
  total_allocated: number;
  total_spent: number;
  total_remaining: number;
  utilization_rate: number;
  risk_score: number;
  risk_level: 'safe' | 'warning' | 'critical';
  summary: string;
  timestamp: string;
}

export function BudgetDashboard() {
  const {
    data,
    loading,
    error,
    refetch,
  } = useApi<BudgetData>('/api/julie/budget', {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'safe': return '#22C55E';
      case 'warning': return '#FBBF24';
      case 'critical': return '#EF4444';
      default: return '#6B7280';
    }
  };

  const getUtilizationColor = (rate: number) => {
    if (rate < 60) return '#22C55E';
    if (rate < 80) return '#FBBF24';
    return '#EF4444';
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-gray-900/90 to-green-500/10 backdrop-blur-xl rounded-2xl p-8">
        <LoadingSpinner size="md" text="예산 데이터 로딩 중..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-br from-gray-900/90 to-red-500/20 backdrop-blur-xl rounded-2xl p-8">
        <ErrorMessage
          message={error.message || '예산 데이터를 불러올 수 없습니다.'}
          onRetry={refetch}
        />
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="bg-gradient-to-br from-gray-900/95 to-green-500/10 backdrop-blur-xl rounded-3xl border border-white/10 p-7 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-4xl">📊</span>
          <div>
            <h2 className="text-xl font-bold text-white m-0">
              예산 대시보드
            </h2>
            <p className="text-white/60 text-xs m-0">
              Phase 12 · Julie CPA 확장
            </p>
          </div>
        </div>
        <div
          className="rounded-xl px-4 py-2"
          style={{
            background: `${getRiskColor(data.risk_level)}20`,
            border: `1px solid ${getRiskColor(data.risk_level)}50`,
          }}
        >
          <span className="font-bold text-sm" style={{ color: getRiskColor(data.risk_level) }}>
            Risk: {data.risk_score}
          </span>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-green-500/10 rounded-xl p-4 text-center">
          <div className="text-white/60 text-xs mb-1">
            총 예산
          </div>
          <div className="text-green-500 text-lg font-bold">
            {formatCurrency(data.total_allocated)}
          </div>
        </div>
        <div className="bg-amber-500/10 rounded-xl p-4 text-center">
          <div className="text-white/60 text-xs mb-1">
            지출
          </div>
          <div className="text-amber-400 text-lg font-bold">
            {formatCurrency(data.total_spent)}
          </div>
        </div>
        <div className="bg-blue-500/10 rounded-xl p-4 text-center">
          <div className="text-white/60 text-xs mb-1">
            잔여
          </div>
          <div className="text-blue-500 text-lg font-bold">
            {formatCurrency(data.total_remaining)}
          </div>
        </div>
      </div>

      {/* Utilization Bar */}
      <div className="mb-6">
        <div className="flex justify-between mb-2">
          <span className="text-white/80 text-sm">예산 사용률</span>
          <span className="font-bold" style={{ color: getUtilizationColor(data.utilization_rate) }}>
            {data.utilization_rate}%
          </span>
        </div>
        <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden">
          <div 
            className="h-full rounded-full transition-all duration-500 ease-out"
            style={{
              width: `${Math.min(data.utilization_rate, 100)}%`,
              background: `linear-gradient(90deg, ${getUtilizationColor(data.utilization_rate)}, ${getUtilizationColor(data.utilization_rate)}80)`,
            }}
          />
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="mb-5">
        <div className="text-white/80 text-sm mb-3 font-semibold">
          📋 카테고리별 현황
        </div>
        {data.budgets.map((budget) => {
          const rate = (budget.spent / budget.allocated) * 100;
          return (
            <div
              key={budget.id}
              className="flex items-center justify-between p-3 mb-2 bg-white/5 rounded-lg"
            >
              <div className="flex-1">
                <div className="text-white text-sm mb-1">
                  {budget.category}
                </div>
                <div className="w-full h-1 bg-white/10 rounded">
                  <div 
                    className="h-full rounded"
                    style={{
                      width: `${Math.min(rate, 100)}%`,
                      background: getUtilizationColor(rate),
                    }}
                  />
                </div>
              </div>
              <div className="text-right ml-4">
                <div className="text-sm font-semibold" style={{ color: getUtilizationColor(rate) }}>
                  {formatCurrency(budget.remaining)}
                </div>
                <div className="text-white/50 text-[11px]">
                  {rate.toFixed(0)}% 사용
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Julie Summary */}
      <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-xl p-4 text-center">
        <p className="text-sm font-semibold m-0" style={{ color: getRiskColor(data.risk_level) }}>
          {data.summary}
        </p>
      </div>
    </div>
  );
}

export default BudgetDashboard;
