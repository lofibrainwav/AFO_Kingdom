/**
 * JulieCPAWidget.tsx
 *
 * 수호자 Julie CPA - 왕국의 금고를 지키는 재무 수호자
 * Phase 12: Complete Awakening
 *
 * "금고가 튼튼해야 왕국이 번영한다"
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

interface Transaction {
  id: string;
  merchant: string;
  amount: number;
  date: string;
  category: string;
}

interface RiskAlert {
  level: "info" | "warning" | "critical";
  message: string;
}

interface FinanceDashboard {
  financial_health_score: number;
  monthly_spending: number;
  budget_remaining: number;
  recent_transactions: Transaction[];
  risk_alerts: RiskAlert[];
  advice: string;
}

function JulieCPAWidgetContent() {
  const { data, loading, error, refetch } = useApi<FinanceDashboard>("/api/finance/dashboard", {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  // Memoize color getters
  const getHealthColor = useCallback((score: number) => {
    if (score >= 80) return "#22C55E"; // Green
    if (score >= 60) return "#FBBF24"; // Yellow
    if (score >= 40) return "#F97316"; // Orange
    return "#EF4444"; // Red
  }, []);

  const getAlertColor = useCallback((level: string) => {
    switch (level) {
      case "critical":
        return "#EF4444";
      case "warning":
        return "#FBBF24";
      default:
        return "#3B82F6";
    }
  }, []);

  // Memoize currency formatter
  const formatCurrency = useCallback((amount: number) => {
    return new Intl.NumberFormat("ko-KR", {
      style: "currency",
      currency: "KRW",
      maximumFractionDigits: 0,
    }).format(amount);
  }, []);

  // Memoize formatted values
  const formattedData = useMemo(() => {
    if (!data) return null;
    return {
      healthColor: getHealthColor(data.financial_health_score),
      healthPercentage: data.financial_health_score,
      healthStatus:
        data.financial_health_score >= 80
          ? "✅ 안정"
          : data.financial_health_score >= 60
            ? "⚠️ 주의"
            : "🚨 위험",
      monthlySpending: formatCurrency(data.monthly_spending),
      budgetRemaining: formatCurrency(data.budget_remaining),
      recentTransactions: data.recent_transactions.slice(0, 3),
    };
  }, [data, getHealthColor, formatCurrency]);

  // Memoize risk alerts with colors
  const riskAlertsWithColors = useMemo(() => {
    if (!data?.risk_alerts) return [];
    return data.risk_alerts.map((alert) => ({
      ...alert,
      color: getAlertColor(alert.level),
      icon: alert.level === "critical" ? "🚨" : alert.level === "warning" ? "⚠️" : "ℹ️",
    }));
  }, [data, getAlertColor]);

  if (loading) {
    return (
      <div
        className="bg-gradient-to-br from-gray-900/90 to-blue-900/20 backdrop-blur-xl rounded-2xl border border-white/10 p-8"
        role="status"
        aria-live="polite"
        aria-label="Loading finance data"
      >
        <LoadingSpinner size="md" text="재무 데이터 로딩 중..." />
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="bg-gradient-to-br from-gray-900/90 to-blue-900/20 backdrop-blur-xl rounded-2xl border border-white/10 p-8"
        role="alert"
        aria-live="assertive"
      >
        <ErrorMessage
          message={error.message || "재무 데이터를 불러올 수 없습니다."}
          onRetry={refetch}
        />
      </div>
    );
  }

  if (!data || !formattedData) {
    return null;
  }

  return (
    <div
      className="bg-gradient-to-br from-gray-900/95 to-blue-500/15 backdrop-blur-xl rounded-3xl border border-white/10 p-7 shadow-2xl"
      role="region"
      aria-labelledby="julie-cpa-title"
    >
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-4xl" aria-hidden="true">
            💰
          </span>
          <div>
            <h2 id="julie-cpa-title" className="text-xl font-bold text-white m-0">
              Julie CPA
            </h2>
            <p className="text-white/60 text-xs m-0">수호자 시대 · Phase 12</p>
          </div>
        </div>
        <div
          className="rounded-xl px-4 py-2"
          style={{
            background: `${formattedData.healthColor}20`,
            border: `1px solid ${formattedData.healthColor}50`,
          }}
          role="status"
          aria-label={`Financial health status: ${formattedData.healthStatus}, Score: ${formattedData.healthPercentage}%`}
        >
          <span className="font-bold text-sm" style={{ color: formattedData.healthColor }}>
            {formattedData.healthStatus}
          </span>
        </div>
      </header>

      {/* Health Score Gauge */}
      <section aria-label="Financial health score">
        <div className="bg-black/30 rounded-2xl p-5 mb-5">
          <div className="flex justify-between items-center mb-3">
            <span className="text-white/80 text-sm">재무 건강도</span>
            <span
              className="text-3xl font-bold"
              style={{ color: formattedData.healthColor }}
              aria-live="polite"
            >
              {formattedData.healthPercentage}%
            </span>
          </div>
          <div
            className="w-full h-3 bg-white/10 rounded-full overflow-hidden"
            role="progressbar"
            aria-valuenow={formattedData.healthPercentage}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Financial health score: ${formattedData.healthPercentage}%`}
          >
            <div
              className="h-full rounded-full transition-all duration-500 ease-out"
              style={{
                width: `${formattedData.healthPercentage}%`,
                background: `linear-gradient(90deg, ${formattedData.healthColor}, ${formattedData.healthColor}80)`,
              }}
            />
          </div>
        </div>
      </section>

      {/* Stats Grid */}
      <section aria-label="Financial statistics">
        <div className="grid grid-cols-2 gap-4 mb-5" role="list">
          <div
            className="bg-blue-500/10 rounded-xl p-4 border border-blue-500/20"
            role="listitem"
            aria-label={`Monthly spending: ${formattedData.monthlySpending}`}
          >
            <div className="text-white/60 text-xs mb-1">월간 지출</div>
            <div className="text-blue-500 text-lg font-bold">
              {formattedData.monthlySpending}
            </div>
          </div>
          <div
            className="bg-green-500/10 rounded-xl p-4 border border-green-500/20"
            role="listitem"
            aria-label={`Remaining budget: ${formattedData.budgetRemaining}`}
          >
            <div className="text-white/60 text-xs mb-1">잔여 예산</div>
            <div className="text-green-500 text-lg font-bold">
              {formattedData.budgetRemaining}
            </div>
          </div>
        </div>
      </section>

      {/* Risk Alerts */}
      {riskAlertsWithColors.length > 0 && (
        <section aria-label="Risk alerts">
          <div className="mb-5">
            <div className="text-white/80 text-sm mb-3 font-semibold">🛡️ 리스크 알림</div>
            <div role="list" aria-label="Risk alerts list">
              {riskAlertsWithColors.map((alert, i) => (
                <div
                  key={i}
                  className="rounded-lg p-3 mb-2 flex items-center gap-2.5"
                  style={{
                    background: `${alert.color}15`,
                    border: `1px solid ${alert.color}30`,
                  }}
                  role="listitem"
                  aria-label={`${alert.level} alert: ${alert.message}`}
                >
                  <span className="text-base" aria-hidden="true">
                    {alert.icon}
                  </span>
                  <span className="text-white/90 text-[13px]">{alert.message}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Recent Transactions */}
      <section aria-label="Recent transactions">
        <div className="mb-5">
          <div className="text-white/80 text-sm mb-3 font-semibold">📊 최근 거래</div>
          <div role="list" aria-label="Recent transactions list">
            {formattedData.recentTransactions.map((tx) => (
              <div
                key={tx.id}
                className="flex justify-between items-center py-2.5 border-b border-white/5"
                role="listitem"
                aria-label={`Transaction: ${tx.merchant}, ${tx.category}, ${formatCurrency(tx.amount)}`}
              >
                <div>
                  <div className="text-white text-sm">{tx.merchant}</div>
                  <div className="text-white/50 text-[11px]">
                    {tx.category} · {tx.date}
                  </div>
                </div>
                <div className="text-orange-500 font-semibold text-sm">
                  -{formatCurrency(tx.amount)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Advice */}
      <section aria-label="AI advice">
        <div className="bg-gradient-to-br from-purple-500/15 to-blue-500/15 rounded-xl p-4 border border-purple-500/20">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-base" aria-hidden="true">
              🤖
            </span>
            <span className="text-purple-400 text-xs font-semibold">Julie's Advice</span>
          </div>
          <p className="text-white/85 text-[13px] leading-relaxed m-0" aria-live="polite">
            {data.advice}
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-4 text-center text-white/40 text-[11px]" aria-label="Footer">
        眞善美孝永 · Julie CPA Phase 12 Active
      </footer>
    </div>
  );
}

export function JulieCPAWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("JulieCPAWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="bg-gradient-to-br from-gray-900/90 to-blue-900/20 backdrop-blur-xl rounded-2xl border border-white/10 p-8"
          role="alert"
        >
          <ErrorMessage message="Julie CPA 위젯을 불러올 수 없습니다." />
        </div>
      }
    >
      <JulieCPAWidgetContent />
    </ErrorBoundary>
  );
}

export default JulieCPAWidget;
