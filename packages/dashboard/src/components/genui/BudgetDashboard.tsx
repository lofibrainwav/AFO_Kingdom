/**
 * BudgetDashboard.tsx
 *
 * Phase 12 Extension: 실시간 예산 대시보드
 * "금고 안전! Julie CPA가 왕국 부를 지켜요" 🛡️💰
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo, useCallback } from "react";
import { useApi } from "@/hooks/useApi";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { REFRESH_INTERVALS } from "@/lib/constants";
import ErrorBoundary from "@/components/common/ErrorBoundary";

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
  risk_level: "safe" | "warning" | "critical";
  summary: string;
  timestamp: string;
}

function BudgetDashboardContent() {
  const { data, loading, error, refetch } = useApi<BudgetData>("/api/julie/budget", {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  // Memoize currency formatter
  const formatCurrency = useCallback((amount: number) => {
    return new Intl.NumberFormat("ko-KR", {
      style: "currency",
      currency: "KRW",
      maximumFractionDigits: 0,
    }).format(amount);
  }, []);

  // Memoize risk color getter
  const getRiskColor = useCallback((level: string) => {
    switch (level) {
      case "safe":
        return "#22C55E";
      case "warning":
        return "#FBBF24";
      case "critical":
        return "#EF4444";
      default:
        return "#6B7280";
    }
  }, []);

  // Memoize utilization color getter
  const getUtilizationColor = useCallback((rate: number) => {
    if (rate < 60) return "#22C55E";
    if (rate < 80) return "#FBBF24";
    return "#EF4444";
  }, []);

  // Memoize budgets with calculated rates
  const budgetsWithRates = useMemo(() => {
    if (!data || !data.budgets) return [];
    return data.budgets.map((budget) => ({
      ...budget,
      rate: (budget.spent / budget.allocated) * 100,
    }));
  }, [data]);

  // Memoize formatted currency values
  const formattedTotals = useMemo(() => {
    if (!data) return null;
    return {
      allocated: formatCurrency(data.total_allocated),
      spent: formatCurrency(data.total_spent),
      remaining: formatCurrency(data.total_remaining),
    };
  }, [data, formatCurrency]);

  // Memoize risk color for current data
  const currentRiskColor = useMemo(() => {
    if (!data) return "#6B7280";
    return getRiskColor(data.risk_level);
  }, [data, getRiskColor]);

  // Memoize utilization color for current data
  const currentUtilizationColor = useMemo(() => {
    if (!data) return "#6B7280";
    return getUtilizationColor(data.utilization_rate);
  }, [data, getUtilizationColor]);

  if (loading) {
    return (
      <div
        className="bg-gradient-to-br from-gray-900/90 to-green-500/10 backdrop-blur-xl rounded-2xl p-8"
        role="status"
        aria-live="polite"
        aria-label="Loading budget data"
      >
        <LoadingSpinner size="md" text="예산 데이터 로딩 중..." />
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="bg-gradient-to-br from-gray-900/90 to-red-500/20 backdrop-blur-xl rounded-2xl p-8"
        role="alert"
        aria-live="assertive"
      >
        <ErrorMessage
          message={error.message || "예산 데이터를 불러올 수 없습니다."}
          onRetry={refetch}
        />
      </div>
    );
  }

  if (!data) return null;

  return (
    <div
      className="bg-gradient-to-br from-gray-900/95 to-green-500/10 backdrop-blur-xl rounded-3xl border border-white/10 p-7 shadow-2xl"
      role="region"
      aria-labelledby="budget-dashboard-title"
    >
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-4xl" aria-hidden="true">
            📊
          </span>
          <div>
            <h2 id="budget-dashboard-title" className="text-xl font-bold text-white m-0">
              예산 대시보드
            </h2>
            <p className="text-white/60 text-xs m-0">Phase 12 · Julie CPA 확장</p>
          </div>
        </div>
        <div
          className="rounded-xl px-4 py-2"
          style={{
            background: `${currentRiskColor}20`,
            border: `1px solid ${currentRiskColor}50`,
          }}
          role="status"
          aria-label={`Risk level: ${data.risk_level}, Score: ${data.risk_score}`}
        >
          <span className="font-bold text-sm" style={{ color: currentRiskColor }}>
            Risk: {data.risk_score}
          </span>
        </div>
      </header>

      {/* Summary Stats */}
      <section aria-label="Budget summary statistics">
        <div className="grid grid-cols-3 gap-4 mb-6" role="list">
          <div
            className="bg-green-500/10 rounded-xl p-4 text-center"
            role="listitem"
            aria-label={`Total allocated budget: ${formattedTotals?.allocated}`}
          >
            <div className="text-white/60 text-xs mb-1">총 예산</div>
            <div className="text-green-500 text-lg font-bold">
              {formattedTotals?.allocated}
            </div>
          </div>
          <div
            className="bg-amber-500/10 rounded-xl p-4 text-center"
            role="listitem"
            aria-label={`Total spent: ${formattedTotals?.spent}`}
          >
            <div className="text-white/60 text-xs mb-1">지출</div>
            <div className="text-amber-400 text-lg font-bold">{formattedTotals?.spent}</div>
          </div>
          <div
            className="bg-blue-500/10 rounded-xl p-4 text-center"
            role="listitem"
            aria-label={`Remaining budget: ${formattedTotals?.remaining}`}
          >
            <div className="text-white/60 text-xs mb-1">잔여</div>
            <div className="text-blue-500 text-lg font-bold">{formattedTotals?.remaining}</div>
          </div>
        </div>
      </section>

      {/* Utilization Bar */}
      <section aria-label="Budget utilization">
        <div className="mb-6">
          <div className="flex justify-between mb-2">
            <span className="text-white/80 text-sm">예산 사용률</span>
            <span
              className="font-bold"
              style={{ color: currentUtilizationColor }}
              aria-label={`Utilization rate: ${data.utilization_rate}%`}
            >
              {data.utilization_rate}%
            </span>
          </div>
          <div
            className="w-full h-3 bg-white/10 rounded-full overflow-hidden"
            role="progressbar"
            aria-valuenow={data.utilization_rate}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Budget utilization: ${data.utilization_rate}%`}
          >
            <div
              className="h-full rounded-full transition-all duration-500 ease-out"
              style={{
                width: `${Math.min(data.utilization_rate, 100)}%`,
                background: `linear-gradient(90deg, ${currentUtilizationColor}, ${currentUtilizationColor}80)`,
              }}
            />
          </div>
        </div>
      </section>

      {/* Category Breakdown */}
      <section aria-label="Category breakdown">
        <div className="mb-5">
          <div className="text-white/80 text-sm mb-3 font-semibold">
            📋 카테고리별 현황
          </div>
          <div role="list" aria-label="Budget categories">
            {budgetsWithRates.map((budget) => {
              const categoryColor = getUtilizationColor(budget.rate);
              return (
                <div
                  key={budget.id}
                  className="flex items-center justify-between p-3 mb-2 bg-white/5 rounded-lg"
                  role="listitem"
                  aria-label={`${budget.category}: ${formatCurrency(budget.remaining)} remaining, ${budget.rate.toFixed(0)}% used`}
                >
                  <div className="flex-1">
                    <div className="text-white text-sm mb-1">{budget.category}</div>
                    <div
                      className="w-full h-1 bg-white/10 rounded"
                      role="progressbar"
                      aria-valuenow={budget.rate}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-label={`${budget.category} utilization: ${budget.rate.toFixed(0)}%`}
                    >
                      <div
                        className="h-full rounded"
                        style={{
                          width: `${Math.min(budget.rate, 100)}%`,
                          background: categoryColor,
                        }}
                      />
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-sm font-semibold" style={{ color: categoryColor }}>
                      {formatCurrency(budget.remaining)}
                    </div>
                    <div className="text-white/50 text-[11px]">{budget.rate.toFixed(0)}% 사용</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Julie Summary */}
      <section aria-label="Summary">
        <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-xl p-4 text-center">
          <p
            className="text-sm font-semibold m-0"
            style={{ color: currentRiskColor }}
            aria-live="polite"
          >
            {data.summary}
          </p>
        </div>
      </section>
    </div>
  );
}

export function BudgetDashboard() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("BudgetDashboard error:", error, errorInfo);
      }}
      fallback={
        <div
          className="bg-gradient-to-br from-gray-900/90 to-red-500/20 backdrop-blur-xl rounded-2xl p-8"
          role="alert"
        >
          <ErrorMessage message="예산 대시보드를 불러올 수 없습니다." />
        </div>
      }
    >
      <BudgetDashboardContent />
    </ErrorBoundary>
  );
}

export default BudgetDashboard;
