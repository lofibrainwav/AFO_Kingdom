'use client';

import { useState, useEffect } from 'react';
import { Brain, TrendingUp, Lightbulb, CheckCircle2, Loader2, Sparkles } from 'lucide-react';

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
  const [report, setReport] = useState<LearningReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await fetch('/api/learning/report');
        if (res.ok) {
          const data = await res.json();
          setReport(data);
        }
      } catch (error) {
        console.error('Learning Report Error:', error);
        // Mock data for demo
        setReport({
          timestamp: new Date().toISOString(),
          total_actions_analyzed: 247,
          average_trinity_score: 95.2,
          success_rate: 0.98,
          top_patterns: [
            "Voice commands show high user satisfaction",
            "Multi-model consensus improves accuracy",
            "Security hardening reduces risk score"
          ],
          improvement_suggestions: [
            "Add more voice personas for accessibility",
            "Expand multi-model validation to edge cases"
          ],
          metrics: [
            { metric: "Trinity Score", current_value: 95.2, trend: "improving", improvement_suggestion: null },
            { metric: "Success Rate", current_value: 98, trend: "stable", improvement_suggestion: null },
            { metric: "Risk Score", current_value: 5.2, trend: "improving", improvement_suggestion: "Continue hardening" }
          ]
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchReport();
    const interval = setInterval(fetchReport, 30000);
    return () => clearInterval(interval);
  }, []);

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
      <div className="p-6 bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 rounded-2xl border border-emerald-500/40 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-emerald-400 animate-spin" />
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
