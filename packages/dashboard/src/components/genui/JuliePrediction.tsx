/**
 * JuliePrediction.tsx
 *
 * Phase 12-4: Predictive Guardian - Julie CPA의 미래 예측
 * "Julie가 미래를 봐요 – 다음 달 예상 지출 알려줄게요 ✨"
 */
'use client';

import React from 'react';
import { useApi } from '@/hooks/useApi';
import { LoadingSpinner } from '@/components/common';
import { REFRESH_INTERVALS } from '@/lib/constants';

interface HistoryPoint {
  month: string;
  spent: number;
}

interface PredictionData {
  current_month_spending: number;
  next_month_predicted: number;
  difference: number;
  difference_percent: number;
  confidence: number;
  confidence_note: string;
  trend: 'increasing' | 'decreasing' | 'stable';
  trend_slope: number;
  risk_level: 'safe' | 'warning' | 'info';
  advice: string;
  history: HistoryPoint[];
  summary: string;
}

export function JuliePrediction() {
  const {
    data,
    loading,
  } = useApi<PredictionData>('/api/julie/budget/prediction', {
    refetchInterval: REFRESH_INTERVALS.SLOW, // 5분마다 자동 업데이트
  });

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return '📈';
      case 'decreasing': return '📉';
      default: return '📊';
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'increasing': return '#FBBF24';
      case 'decreasing': return '#22C55E';
      default: return '#3B82F6';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#22C55E';
    if (confidence >= 0.5) return '#FBBF24';
    return '#EF4444';
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-gray-900/90 to-green-500/10 rounded-2xl p-8">
        <LoadingSpinner size="md" text="미래 예측 중..." />
      </div>
    );
  }

  if (!data) return null;

  const maxSpent = Math.max(...data.history.map(h => h.spent), data.next_month_predicted);

  return (
    <div className="bg-gradient-to-br from-gray-900/95 to-green-500/15 backdrop-blur-xl rounded-3xl border border-green-500/20 p-7 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-4xl">🔮</span>
          <div>
            <h2 className="text-xl font-bold text-white m-0">
              Julie CPA의 미래 예측
            </h2>
            <p className="text-white/60 text-xs m-0">
              Phase 12-4 · Predictive Guardian
            </p>
          </div>
        </div>
        <div className="bg-green-500/20 border border-green-500/40 rounded-xl px-4 py-2">
          <span className="font-bold text-sm" style={{ color: getTrendColor(data.trend) }}>
            {getTrendIcon(data.trend)} {data.trend === 'increasing' ? '증가 추세' : data.trend === 'decreasing' ? '감소 추세' : '안정 추세'}
          </span>
        </div>
      </div>

      {/* Main Prediction */}
      <div className="bg-black/30 rounded-2xl p-6 mb-5 text-center">
        <p className="text-white/60 text-sm mb-2">
          다음 달 예상 지출
        </p>
        <div className="text-4xl font-bold text-green-500 mb-2">
          {formatCurrency(data.next_month_predicted)}
        </div>
        <div className={`inline-block rounded-full px-3.5 py-1.5 text-sm font-semibold ${
          data.difference > 0 
            ? 'bg-amber-500/20 text-amber-400' 
            : 'bg-green-500/20 text-green-500'
        }`}>
          {data.difference > 0 ? '↑' : '↓'} {Math.abs(data.difference_percent)}% vs 현재
        </div>
      </div>

      {/* Confidence Meter */}
      <div className="mb-5">
        <div className="flex justify-between mb-2">
          <span className="text-white/80 text-sm">예측 신뢰도</span>
          <span className="font-bold" style={{ color: getConfidenceColor(data.confidence) }}>
            {(data.confidence * 100).toFixed(0)}% {data.confidence_note}
          </span>
        </div>
        <div className="w-full h-2 bg-white/10 rounded overflow-hidden">
          <div 
            className="h-full rounded transition-all duration-500 ease-out"
            style={{
              width: `${data.confidence * 100}%`,
              background: `linear-gradient(90deg, ${getConfidenceColor(data.confidence)}, ${getConfidenceColor(data.confidence)}80)`,
            }}
          />
        </div>
      </div>

      {/* Mini Chart (Simple Bar Chart) */}
      <div className="mb-5">
        <div className="text-white/80 text-sm mb-3 font-semibold">
          📊 지출 추이 (6개월)
        </div>
        <div className="flex items-end gap-2 h-20">
          {data.history.map((point, i) => {
            const height = (point.spent / maxSpent) * 100;
            return (
              <div key={i} className="flex-1 flex flex-col items-center">
                <div 
                  className="w-full bg-gradient-to-t from-blue-500 to-blue-400 rounded-t min-h-2"
                  style={{ height: `${height}%` }}
                />
                <span className="text-white/50 text-[10px] mt-1">
                  {point.month.split('-')[1]}월
                </span>
              </div>
            );
          })}
          {/* Prediction Bar */}
          <div className="flex-1 flex flex-col items-center">
            <div 
              className="w-full bg-gradient-to-t from-green-500 to-green-400 rounded-t min-h-2 border-2 border-dashed border-white/30"
              style={{ height: `${(data.next_month_predicted / maxSpent) * 100}%` }}
            />
            <span className="text-green-500 text-[10px] mt-1 font-bold">
              예측
            </span>
          </div>
        </div>
      </div>

      {/* Advice */}
      <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-xl p-4">
        <p className="text-sm m-0 leading-relaxed" style={{ color: getTrendColor(data.trend) }}>
          {data.advice}
        </p>
      </div>
    </div>
  );
}

export default JuliePrediction;
