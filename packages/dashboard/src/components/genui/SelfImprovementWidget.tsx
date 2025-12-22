/**
 * SelfImprovementWidget.tsx
 * 
 * 사마휘의 자율 학습 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { Brain, TrendingUp, Lightbulb, CheckCircle2, Sparkles } from "lucide-react";
import { useMemo, useCallback } from "react";
import { useApi } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/common";
import { REFRESH_INTERVALS } from "@/lib/constants";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface LearningMetric {
  metric: string;
  current_value: number;
  trend: string;
  improvement_suggestion: string | null;
}

interface LearningReport {
  timestamp: string;
  total_actions_analyzed: number;
  average_trinity_score: number;
  success_rate: number;
  top_patterns: string[];
  improvement_suggestions: string[];
  metrics: LearningMetric[];
}

function SelfImprovementWidgetContent() {
  const { data: report, loading: isLoading } = useApi<LearningReport>("/api/learning/report", {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  // Memoize trend getters
  const getTrendColor = useCallback((trend: string) => {
    switch (trend) {
      case "improving":
        return "text-green-400";
      case "stable":
        return "text-blue-400";
      case "declining":
        return "text-red-400";
      default:
        return "text-gray-400";
    }
  }, []);

  const getTrendIcon = useCallback((trend: string) => {
    switch (trend) {
      case "improving":
        return "↗";
      case "stable":
        return "→";
      case "declining":
        return "↘";
      default:
        return "→";
    }
  }, []);

  // Memoize formatted values
  const formattedData = useMemo(() => {
    if (!report) return null;
    return {
      averageTrinity: report.average_trinity_score.toFixed(1),
      successRate: (report.success_rate * 100).toFixed(0),
    };
  }, [report]);

  // Memoize metrics with colors
  const metricsWithStyles = useMemo(() => {
    if (!report?.metrics) return [];
    return report.metrics.map((metric) => ({
      ...metric,
      trendColor: getTrendColor(metric.trend),
      trendIcon: getTrendIcon(metric.trend),
    }));
  }, [report, getTrendColor, getTrendIcon]);

  if (isLoading) {
    return (
      <div
        className="p-6 bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 rounded-2xl border border-emerald-500/40"
        role="status"
        aria-live="polite"
        aria-label="Loading learning report"
      >
        <LoadingSpinner size="md" text="학습 리포트 분석 중..." />
      </div>
    );
  }

  if (!report || !formattedData) return null;

  return (
    <div
      className="p-6 bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 rounded-2xl border border-emerald-500/40 backdrop-blur-xl shadow-2xl"
      role="region"
      aria-labelledby="self-improvement-title"
    >
      {/* Header */}
      <header className="flex items-center gap-3 mb-6">
        <Brain className="w-8 h-8 text-emerald-400 animate-pulse" aria-hidden="true" />
        <h3 id="self-improvement-title" className="text-2xl font-bold text-white">
          사마휘의 자율 학습
        </h3>
        <Sparkles className="w-5 h-5 text-yellow-400 animate-ping" aria-hidden="true" />
      </header>

      {/* Summary Stats */}
      <section aria-label="Summary statistics">
        <div className="grid grid-cols-3 gap-4 mb-6" role="list">
          <div
            className="p-4 bg-black/30 rounded-xl border border-white/10 text-center"
            role="listitem"
            aria-label={`Total actions analyzed: ${report.total_actions_analyzed}`}
          >
            <p className="text-3xl font-bold text-emerald-400">{report.total_actions_analyzed}</p>
            <p className="text-sm text-gray-400">분석된 행동</p>
          </div>
          <div
            className="p-4 bg-black/30 rounded-xl border border-white/10 text-center"
            role="listitem"
            aria-label={`Average Trinity score: ${formattedData.averageTrinity}`}
          >
            <p className="text-3xl font-bold text-cyan-400">{formattedData.averageTrinity}</p>
            <p className="text-sm text-gray-400">평균 Trinity</p>
          </div>
          <div
            className="p-4 bg-black/30 rounded-xl border border-white/10 text-center"
            role="listitem"
            aria-label={`Success rate: ${formattedData.successRate}%`}
          >
            <p className="text-3xl font-bold text-green-400">{formattedData.successRate}%</p>
            <p className="text-sm text-gray-400">성공률</p>
          </div>
        </div>
      </section>

      {/* Metrics */}
      <section aria-label="Key metrics">
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" aria-hidden="true" /> 핵심 지표
          </h4>
          <div className="space-y-2" role="list" aria-label="Learning metrics">
            {metricsWithStyles.map((metric, i) => (
              <div
                key={i}
                className="flex items-center justify-between p-3 bg-black/20 rounded-lg border border-white/5"
                role="listitem"
                aria-label={`${metric.metric}: ${metric.current_value}, trend: ${metric.trend}`}
              >
                <div className="flex items-center gap-3">
                  <span className={`text-lg ${metric.trendColor}`} aria-label={`Trend: ${metric.trend}`}>
                    {metric.trendIcon}
                  </span>
                  <span className="text-white text-sm">{metric.metric}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-white font-bold">{metric.current_value}</span>
                  {metric.improvement_suggestion && (
                    <Lightbulb className="w-4 h-4 text-yellow-400" aria-label="Has improvement suggestion" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Top Patterns */}
      {report.top_patterns.length > 0 && (
        <section aria-label="Top patterns">
          <div className="mb-6">
            <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" aria-hidden="true" /> 주요 패턴
            </h4>
            <div className="space-y-2" role="list" aria-label="Top patterns list">
              {report.top_patterns.map((pattern, i) => (
                <div
                  key={i}
                  className="p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/20 text-sm text-emerald-200"
                  role="listitem"
                >
                  {pattern}
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Improvement Suggestions */}
      {report.improvement_suggestions.length > 0 && (
        <section aria-label="Improvement suggestions">
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
              <Lightbulb className="w-4 h-4" aria-hidden="true" /> 개선 제안
            </h4>
            <div className="space-y-2" role="list" aria-label="Improvement suggestions list">
              {report.improvement_suggestions.map((suggestion, i) => (
                <div
                  key={i}
                  className="p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20 text-sm text-yellow-200"
                  role="listitem"
                >
                  {suggestion}
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export function SelfImprovementWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("SelfImprovementWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="p-6 bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 rounded-2xl border border-red-500/40"
          role="alert"
        >
          <p className="text-red-400 text-center">자율 학습 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <SelfImprovementWidgetContent />
    </ErrorBoundary>
  );
}

export default SelfImprovementWidget;
