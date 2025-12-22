/**
 * JuliePrediction.tsx
 *
 * Phase 12-4: Predictive Guardian - Julie CPA의 미래 예측
 * "Julie가 미래를 봐요 – 다음 달 예상 지출 알려줄게요 ✨"
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo, useCallback } from "react";
import { useApi } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/common";
import { REFRESH_INTERVALS } from "@/lib/constants";
import ErrorBoundary from "@/components/common/ErrorBoundary";

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
  trend: "increasing" | "decreasing" | "stable";
  trend_slope: number;
  risk_level: "safe" | "warning" | "info";
  advice: string;
  history: HistoryPoint[];
  summary: string;
}

function JuliePredictionContent() {
  const { data, loading } = useApi<PredictionData>("/api/julie/budget/prediction", {
    refetchInterval: REFRESH_INTERVALS.SLOW, // 5분마다 자동 업데이트
  });

  // Memoize currency formatter
  const formatCurrency = useCallback((amount: number) => {
    return new Intl.NumberFormat("ko-KR", {
      style: "currency",
      currency: "KRW",
      maximumFractionDigits: 0,
    }).format(amount);
  }, []);

  // Memoize trend getters
  const getTrendIcon = useCallback((trend: string) => {
    switch (trend) {
      case "increasing":
        return "📈";
      case "decreasing":
        return "📉";
      default:
        return "📊";
    }
  }, []);

  const getTrendColor = useCallback((trend: string) => {
    switch (trend) {
      case "increasing":
        return "#FBBF24";
      case "decreasing":
        return "#22C55E";
      default:
        return "#3B82F6";
    }
  }, []);

  const getConfidenceColor = useCallback((confidence: number) => {
    if (confidence >= 0.8) return "#22C55E";
    if (confidence >= 0.5) return "#FBBF24";
    return "#EF4444";
  }, []);

  // Memoize formatted values
  const formattedData = useMemo(() => {
    if (!data) return null;
    return {
      currentSpending: formatCurrency(data.current_month_spending),
      nextPredicted: formatCurrency(data.next_month_predicted),
      difference: formatCurrency(Math.abs(data.difference)),
      differencePercent: Math.abs(data.difference_percent).toFixed(1),
      confidencePercent: (data.confidence * 100).toFixed(0),
      trendIcon: getTrendIcon(data.trend),
      trendColor: getTrendColor(data.trend),
      confidenceColor: getConfidenceColor(data.confidence),
    };
  }, [data, formatCurrency, getTrendIcon, getTrendColor, getConfidenceColor]);

  if (loading) {
    return (
      <div
        className="bg-gradient-to-br from-gray-900/90 to-green-500/10 rounded-2xl p-8"
        role="status"
        aria-live="polite"
        aria-label="Loading prediction"
      >
        <LoadingSpinner size="md" text="미래 예측 중..." />
      </div>
    );
  }

  if (!data || !formattedData) return null;

  return (
    <div
      className="bg-gradient-to-br from-gray-900/95 to-green-500/15 backdrop-blur-xl rounded-3xl border border-green-500/20 p-7 shadow-2xl"
      role="region"
      aria-labelledby="julie-prediction-title"
    >
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <span className="text-4xl" aria-hidden="true">
            🔮
          </span>
          <div>
            <h2 id="julie-prediction-title" className="text-xl font-bold text-white m-0">
              Julie CPA의 미래 예측
            </h2>
            <p className="text-white/60 text-xs m-0">Phase 12-4 · Predictive Guardian</p>
          </div>
        </div>
        <div
          className="rounded-xl px-4 py-2"
          style={{
            background: `${formattedData.trendColor}20`,
            border: `1px solid ${formattedData.trendColor}50`,
          }}
          role="status"
          aria-label={`Trend: ${data.trend}`}
        >
          <span className="text-2xl" aria-hidden="true">
            {formattedData.trendIcon}
          </span>
        </div>
      </header>

      {/* Prediction Stats */}
      <section aria-label="Prediction statistics">
        <div className="grid grid-cols-2 gap-4 mb-6" role="list">
          <div
            className="bg-blue-500/10 rounded-xl p-4 border border-blue-500/20"
            role="listitem"
            aria-label={`Current month spending: ${formattedData.currentSpending}`}
          >
            <div className="text-white/60 text-xs mb-1">이번 달 지출</div>
            <div className="text-blue-500 text-lg font-bold">{formattedData.currentSpending}</div>
          </div>
          <div
            className="bg-green-500/10 rounded-xl p-4 border border-green-500/20"
            role="listitem"
            aria-label={`Next month predicted: ${formattedData.nextPredicted}`}
          >
            <div className="text-white/60 text-xs mb-1">다음 달 예상</div>
            <div className="text-green-500 text-lg font-bold">{formattedData.nextPredicted}</div>
          </div>
        </div>
      </section>

      {/* Difference */}
      <section aria-label="Difference analysis">
        <div className="bg-black/30 rounded-2xl p-5 mb-5">
          <div className="flex justify-between items-center mb-3">
            <span className="text-white/80 text-sm">예상 차이</span>
            <span
              className="text-2xl font-bold"
              style={{ color: formattedData.trendColor }}
              aria-live="polite"
            >
              {data.difference > 0 ? "+" : "-"}
              {formattedData.difference} ({formattedData.differencePercent}%)
            </span>
          </div>
        </div>
      </section>

      {/* Confidence */}
      <section aria-label="Prediction confidence">
        <div className="mb-5">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white/80 text-sm">예측 신뢰도</span>
            <span
              className="font-bold"
              style={{ color: formattedData.confidenceColor }}
              aria-label={`Confidence: ${formattedData.confidencePercent}%`}
            >
              {formattedData.confidencePercent}% {data.confidence_note}
            </span>
          </div>
          <div
            className="w-full h-3 bg-white/10 rounded-full overflow-hidden"
            role="progressbar"
            aria-valuenow={data.confidence * 100}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Prediction confidence: ${formattedData.confidencePercent}%`}
          >
            <div
              className="h-full rounded-full transition-all duration-500 ease-out"
              style={{
                width: `${data.confidence * 100}%`,
                background: `linear-gradient(90deg, ${formattedData.confidenceColor}, ${formattedData.confidenceColor}80)`,
              }}
            />
          </div>
        </div>
      </section>

      {/* Advice */}
      <section aria-label="Advice">
        <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-xl p-4 border border-green-500/20">
          <p className="text-sm text-white/85 leading-relaxed m-0" aria-live="polite">
            {data.advice}
          </p>
        </div>
      </section>

      {/* Summary */}
      <footer className="mt-4 text-center text-white/40 text-[11px]" aria-label="Summary">
        {data.summary}
      </footer>
    </div>
  );
}

export function JuliePrediction() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("JuliePrediction error:", error, errorInfo);
      }}
      fallback={
        <div
          className="bg-gradient-to-br from-gray-900/90 to-green-500/10 rounded-2xl p-8"
          role="alert"
        >
          <p className="text-red-400 text-center">Julie 예측 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <JuliePredictionContent />
    </ErrorBoundary>
  );
}

export default JuliePrediction;
