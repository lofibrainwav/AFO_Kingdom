"use client";

import { useState } from "react";
import { useApi } from "@/hooks/useApi";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import type { GitTreeAnalysis, Phase } from "@/types/common";
import { PHASE_COLORS, PHASE_ICONS, REFRESH_INTERVALS } from "@/lib/constants";
import Link from "next/link";

export default function GitTreeDocsPage() {
  const [expandedPhase, setExpandedPhase] = useState<Phase | null>(null);

  const {
    data: analysis,
    loading,
    error,
    refetch,
  } = useApi<GitTreeAnalysis>("/api/git-tree", {
    refetchInterval: REFRESH_INTERVALS.SLOW, // 5분마다 자동 업데이트
  });

  if (loading && !analysis) {
    return (
      <div className="min-h-screen bg-[#e0e5ec] p-8">
        <div className="max-w-7xl mx-auto">
          <LoadingSpinner size="lg" text="Git 트리 분석 중..." fullScreen />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#e0e5ec] p-8">
        <div className="max-w-7xl mx-auto">
          <ErrorMessage message={error.message} onRetry={refetch} retryText="다시 시도" />
        </div>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  const phaseOrder = [
    "Phase 0: Genesis",
    "Phase 1: Awakening",
    "Phase 2: Harmony",
    "Phase 3: Expansion",
    "Phase 4: Eternal",
    "Maintenance",
    "Features",
    "Other",
  ];

  return (
    <div className="min-h-screen bg-[#e0e5ec] p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold text-slate-700 mb-2">🌳 Git 트리 Phase 분석</h1>
              <p className="text-slate-500">Phase 0부터 차근차근 분석한 Git 트리 히스토리</p>
            </div>
            <Link
              href="/docs"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors"
            >
              ← 문서 목록
            </Link>
          </div>
          <div className="mt-4 flex items-center gap-4 text-sm text-slate-500">
            <span>총 커밋: {analysis.total_commits}개</span>
            <span>•</span>
            <span>
              기간: {analysis.first_commit?.date} ~ {analysis.latest_commit?.date}
            </span>
            <span>•</span>
            <span>분석 시간: {new Date(analysis.analyzed_at).toLocaleString("ko-KR")}</span>
            <button
              onClick={refetch}
              className="ml-auto px-3 py-1 bg-slate-200/50 hover:bg-slate-300/50 rounded text-slate-700 text-sm transition-colors"
            >
              🔄 새로고침
            </button>
          </div>
        </div>

        {/* Phase Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {phaseOrder.map((phaseName) => {
            const phase = analysis.phases[phaseName];
            if (!phase) return null;

            const colorClass = PHASE_COLORS[phaseName] || "from-gray-500 to-slate-500";
            const icon = PHASE_ICONS[phaseName] || "📦";

            return (
              <div
                key={phaseName}
                className={`bg-gradient-to-br ${colorClass} rounded-xl p-6 shadow-lg cursor-pointer transform transition-all hover:scale-105`}
                onClick={() =>
                  setExpandedPhase(expandedPhase === phaseName ? null : (phaseName as Phase))
                }
              >
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span>{icon}</span>
                    <span className="text-lg">{phaseName}</span>
                  </h2>
                  <span className="text-white/80 text-sm">{phase.count}개</span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-white/90 text-sm">
                    <span>비율</span>
                    <span>{phase.percentage.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div
                      className="bg-white rounded-full h-2 transition-all"
                      style={{ width: `${phase.percentage}%` }}
                    ></div>
                  </div>
                  <div className="text-white/80 text-xs mt-2">
                    {phase.start_date} ~ {phase.end_date}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Expanded Phase Details */}
        {expandedPhase && analysis.phases[expandedPhase as Phase] && (
          <div className="bg-white/30 backdrop-blur-sm rounded-xl p-6 mb-8 border border-white/40">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-slate-700 flex items-center gap-2">
                <span>{PHASE_ICONS[expandedPhase]}</span>
                <span>{expandedPhase}</span>
              </h2>
              <button
                onClick={() => setExpandedPhase(null)}
                className="text-slate-400 hover:text-slate-700"
              >
                ✕
              </button>
            </div>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {analysis.phases[expandedPhase as Phase].commits.map((commit, idx) => (
                <div
                  key={`${commit.hash}-${idx}`}
                  className="bg-slate-100/50 rounded-lg p-4 border border-slate-200 hover:border-purple-500 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-mono text-purple-600 text-sm">{commit.hash}</span>
                        <span className="text-slate-500 text-xs">[{commit.date}]</span>
                      </div>
                      <p className="text-slate-700 text-sm">{commit.message}</p>
                      <p className="text-slate-500 text-xs mt-1">{commit.author}</p>
                    </div>
                  </div>
                </div>
              ))}
              {analysis.phases[expandedPhase as Phase].count > 20 && (
                <div className="text-center text-slate-400 text-sm py-2">
                  ... 외 {analysis.phases[expandedPhase as Phase].count - 20}개 커밋
                </div>
              )}
            </div>
          </div>
        )}

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white/30 backdrop-blur-sm rounded-xl p-6 border border-white/40">
            <h3 className="text-slate-500 text-sm mb-2">첫 커밋</h3>
            {analysis.first_commit && (
              <div>
                <p className="text-slate-700 font-mono text-sm mb-1">
                  {analysis.first_commit.hash}
                </p>
                <p className="text-slate-600 text-sm">{analysis.first_commit.message}</p>
                <p className="text-slate-500 text-xs mt-1">{analysis.first_commit.date}</p>
              </div>
            )}
          </div>
          <div className="bg-white/30 backdrop-blur-sm rounded-xl p-6 border border-white/40">
            <h3 className="text-slate-500 text-sm mb-2">최근 커밋</h3>
            {analysis.latest_commit && (
              <div>
                <p className="text-slate-700 font-mono text-sm mb-1">
                  {analysis.latest_commit.hash}
                </p>
                <p className="text-slate-600 text-sm">{analysis.latest_commit.message}</p>
                <p className="text-slate-500 text-xs mt-1">{analysis.latest_commit.date}</p>
              </div>
            )}
          </div>
          <div className="bg-white/30 backdrop-blur-sm rounded-xl p-6 border border-white/40">
            <h3 className="text-slate-500 text-sm mb-2">Phase 통계</h3>
            <p className="text-slate-700 text-2xl font-bold mb-1">
              {Object.keys(analysis.phases).length}
            </p>
            <p className="text-slate-500 text-sm">활성 Phase</p>
          </div>
        </div>
      </div>
    </div>
  );
}
