/**
 * JulieCPAWidget.tsx
 *
 * 수호자 Julie CPA - 왕국의 금고를 지키는 재무 수호자
 * Phase 12: Complete Awakening
 *
 * "금고가 튼튼해야 왕국이 번영한다"
 */
'use client';

import React from 'react';

interface Transaction {
  id: string;
  merchant: string;
  amount: number;
  date: string;
  category: string;
}

interface RiskAlert {
  level: 'info' | 'warning' | 'critical';
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

import { useApi } from '@/hooks/useApi';
import { LoadingSpinner, ErrorMessage } from '@/components/common';
import { backendApi } from '@/lib/api-client';
import { REFRESH_INTERVALS } from '@/lib/constants';

export function JulieCPAWidget() {
  const {
    data,
    loading,
    error,
    refetch,
  } = useApi<FinanceDashboard>('/api/finance/dashboard', {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  const getHealthColor = (score: number) => {
    if (score >= 80) return '#22C55E'; // Green
    if (score >= 60) return '#FBBF24'; // Yellow
    if (score >= 40) return '#F97316'; // Orange
    return '#EF4444'; // Red
  };

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'critical': return '#EF4444';
      case 'warning': return '#FBBF24';
      default: return '#3B82F6';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-gray-900/90 to-blue-900/20 backdrop-blur-xl rounded-2xl border border-white/10 p-8">
        <LoadingSpinner size="md" text="재무 데이터 로딩 중..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-br from-gray-900/90 to-blue-900/20 backdrop-blur-xl rounded-2xl border border-white/10 p-8">
        <ErrorMessage
          message={error.message || '재무 데이터를 불러올 수 없습니다.'}
          onRetry={refetch}
        />
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const healthColor = getHealthColor(data.financial_health_score);
  const healthPercentage = data.financial_health_score;

  return (
    <div className="bg-gradient-to-br from-gray-900/95 to-blue-500/15 backdrop-blur-xl rounded-3xl border border-white/10 p-7 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-4xl">💰</span>
          <div>
            <h2 className="text-xl font-bold text-white m-0">
              Julie CPA
            </h2>
            <p className="text-white/60 text-xs m-0">
              수호자 시대 · Phase 12
            </p>
          </div>
        </div>
        <div
          className="rounded-xl px-4 py-2"
          style={{
            background: `${healthColor}20`,
            border: `1px solid ${healthColor}50`,
          }}
        >
          <span className="font-bold text-sm" style={{ color: healthColor }}>
            {healthPercentage >= 80 ? '✅ 안정' : healthPercentage >= 60 ? '⚠️ 주의' : '🚨 위험'}
          </span>
        </div>
      </div>

      {/* Health Score Gauge */}
      <div className="bg-black/30 rounded-2xl p-5 mb-5">
        <div className="flex justify-between items-center mb-3">
          <span className="text-white/80 text-sm">재무 건강도</span>
          <span className="text-3xl font-bold" style={{ color: healthColor }}>
            {data.financial_health_score}%
          </span>
        </div>
        <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden">
          <div 
            className="h-full rounded-full transition-all duration-500 ease-out"
            style={{
              width: `${healthPercentage}%`,
              background: `linear-gradient(90deg, ${healthColor}, ${healthColor}80)`,
            }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-5">
        <div className="bg-blue-500/10 rounded-xl p-4 border border-blue-500/20">
          <div className="text-white/60 text-xs mb-1">
            월간 지출
          </div>
          <div className="text-blue-500 text-lg font-bold">
            {formatCurrency(data.monthly_spending)}
          </div>
        </div>
        <div className="bg-green-500/10 rounded-xl p-4 border border-green-500/20">
          <div className="text-white/60 text-xs mb-1">
            잔여 예산
          </div>
          <div className="text-green-500 text-lg font-bold">
            {formatCurrency(data.budget_remaining)}
          </div>
        </div>
      </div>

      {/* Risk Alerts */}
      {data.risk_alerts.length > 0 && (
        <div className="mb-5">
          <div className="text-white/80 text-sm mb-3 font-semibold">
            🛡️ 리스크 알림
          </div>
          {data.risk_alerts.map((alert, i) => (
            <div
              key={i}
              className="rounded-lg p-3 mb-2 flex items-center gap-2.5"
              style={{
                background: `${getAlertColor(alert.level)}15`,
                border: `1px solid ${getAlertColor(alert.level)}30`,
              }}
            >
              <span className="text-base">
                {alert.level === 'critical' ? '🚨' : alert.level === 'warning' ? '⚠️' : 'ℹ️'}
              </span>
              <span className="text-white/90 text-[13px]">
                {alert.message}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Recent Transactions */}
      <div className="mb-5">
        <div className="text-white/80 text-sm mb-3 font-semibold">
          📊 최근 거래
        </div>
        {data.recent_transactions.slice(0, 3).map((tx) => (
          <div
            key={tx.id}
            className="flex justify-between items-center py-2.5 border-b border-white/5"
          >
            <div>
              <div className="text-white text-sm">{tx.merchant}</div>
              <div className="text-white/50 text-[11px]">{tx.category} · {tx.date}</div>
            </div>
            <div className="text-orange-500 font-semibold text-sm">
              -{formatCurrency(tx.amount)}
            </div>
          </div>
        ))}
      </div>

      {/* AI Advice */}
      <div className="bg-gradient-to-br from-purple-500/15 to-blue-500/15 rounded-xl p-4 border border-purple-500/20">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-base">🤖</span>
          <span className="text-purple-400 text-xs font-semibold">Julie's Advice</span>
        </div>
        <p className="text-white/85 text-[13px] leading-relaxed m-0">
          {data.advice}
        </p>
      </div>

      {/* Footer */}
      <div className="mt-4 text-center text-white/40 text-[11px]">
        眞善美孝永 · Julie CPA Phase 12 Active
      </div>
    </div>
  );
}

export default JulieCPAWidget;
