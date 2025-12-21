'use client';

import { Brain, TrendingUp, Lightbulb, CheckCircle2, Sparkles } from 'lucide-react';
import { useApi } from '@/hooks/useApi';
import { LoadingSpinner } from '@/components/common';
import { REFRESH_INTERVALS } from '@/lib/constants';

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

export function SelfImprovementWidget() {
  const {
    data: report,
    loading: isLoading,
  } = useApi<LearningReport>('/api/learning/report', {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'improving': return 'text-green-400';
      case 'stable': return 'text-blue-400';
      case 'declining': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving': return '↗';
      case 'stable': return '→';
      case 'declining': return '↘';
      default: return '→';
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 rounded-2xl border border-emerald-500/40">
        <LoadingSpinner size="md" text="학습 리포트 분석 중..." />
      </div>
    );
  }

  if (!report) return null;

  return (
    <div className="p-6 bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 rounded-2xl border border-emerald-500/40 backdrop-blur-xl shadow-2xl">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <Brain className="w-8 h-8 text-emerald-400 animate-pulse" />
        <h3 className="text-2xl font-bold text-white">사마휘의 자율 학습</h3>
        <Sparkles className="w-5 h-5 text-yellow-400 animate-ping" />
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-black/30 rounded-xl border border-white/10 text-center">
          <p className="text-3xl font-bold text-emerald-400">{report.total_actions_analyzed}</p>
          <p className="text-sm text-gray-400">분석된 행동</p>
        </div>
        <div className="p-4 bg-black/30 rounded-xl border border-white/10 text-center">
          <p className="text-3xl font-bold text-cyan-400">{report.average_trinity_score.toFixed(1)}</p>
          <p className="text-sm text-gray-400">평균 Trinity</p>
        </div>
        <div className="p-4 bg-black/30 rounded-xl border border-white/10 text-center">
          <p className="text-3xl font-bold text-green-400">{(report.success_rate * 100).toFixed(0)}%</p>
          <p className="text-sm text-gray-400">성공률</p>
        </div>
      </div>

      {/* Metrics */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
          <TrendingUp className="w-4 h-4" /> 핵심 지표
        </h4>
        <div className="space-y-2">
          {report.metrics.map((m, i) => (
            <div key={i} className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
              <span className="text-white">{m.metric}</span>
              <div className="flex items-center gap-2">
                <span className="font-medium text-white">{m.current_value.toFixed(1)}</span>
                <span className={`text-lg ${getTrendColor(m.trend)}`}>{getTrendIcon(m.trend)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Patterns */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> 발견된 패턴
        </h4>
        <ul className="space-y-2">
          {report.top_patterns.map((p, i) => (
            <li key={i} className="text-sm text-emerald-300 flex items-start gap-2">
              <span className="text-emerald-500">•</span>
              {p}
            </li>
          ))}
        </ul>
      </div>

      {/* Suggestions */}
      <div>
        <h4 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
          <Lightbulb className="w-4 h-4" /> 개선 제안
        </h4>
        <ul className="space-y-2">
          {report.improvement_suggestions.map((s, i) => (
            <li key={i} className="text-sm text-yellow-300 flex items-start gap-2">
              <span className="text-yellow-500">💡</span>
              {s}
            </li>
          ))}
        </ul>
      </div>

      {/* Footer */}
      <div className="mt-4 pt-4 border-t border-white/10 text-xs text-gray-500 text-center">
        마지막 분석: {new Date(report.timestamp).toLocaleString('ko-KR')}
      </div>
    </div>
  );
}
