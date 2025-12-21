'use client';

import { useState } from 'react';
import { useApi } from '@/hooks/useApi';
import { LoadingSpinner, ErrorMessage } from '@/components/common';
import type { GitTreeAnalysis, Phase } from '@/types/common';
import { PHASE_COLORS, PHASE_ICONS, REFRESH_INTERVALS } from '@/lib/constants';

export default function GitTreePage() {
  const [expandedPhase, setExpandedPhase] = useState<Phase | null>(null);

  const {
    data: analysis,
    loading,
    error,
    refetch,
  } = useApi<GitTreeAnalysis>('/api/git-tree', {
    refetchInterval: REFRESH_INTERVALS.SLOW, // 5분마다 자동 업데이트
  });

  if (loading && !analysis) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
        <div className="max-w-7xl mx-auto">
          <LoadingSpinner size="lg" text="Git 트리 분석 중..." fullScreen />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
        <div className="max-w-7xl mx-auto">
          <ErrorMessage
            message={error.message}
            onRetry={refetch}
            retryText="다시 시도"
          />
        </div>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  const phaseOrder = [
    'Phase 0: Genesis',
    'Phase 1: Awakening',
    'Phase 2: Harmony',
    'Phase 3: Expansion',
    'Phase 4: Eternal',
    'Maintenance',
    'Features',
    'Other',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            🌳 Git 트리 Phase 분석
          </h1>
          <p className="text-gray-300">
            Phase 0부터 차근차근 분석한 Git 트리 히스토리
          </p>
          <div className="mt-4 flex items-center gap-4 text-sm text-gray-400">
            <span>총 커밋: {analysis.total_commits}개</span>
            <span>•</span>
            <span>
              기간: {analysis.first_commit?.date} ~ {analysis.latest_commit?.date}
            </span>
            <span>•</span>
            <span>
              분석 시간: {new Date(analysis.analyzed_at).toLocaleString('ko-KR')}
            </span>
            <button
              onClick={refetch}
              className="ml-auto px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-white text-sm"
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

            const colorClass = PHASE_COLORS[phaseName] || 'from-gray-500 to-slate-500';
            const icon = PHASE_ICONS[phaseName] || '📦';

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
                  <span className="text-white/80 text-sm">
                    {phase.count}개
                  </span>
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
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                <span>{PHASE_ICONS[expandedPhase]}</span>
                <span>{expandedPhase}</span>
              </h2>
              <button
                onClick={() => setExpandedPhase(null)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {analysis.phases[expandedPhase as Phase].commits.map((commit, idx) => (
                <div
                  key={`${commit.hash}-${idx}`}
                  className="bg-gray-900/50 rounded-lg p-4 border border-gray-700 hover:border-purple-500 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-mono text-purple-400 text-sm">
                          {commit.hash}
                        </span>
                        <span className="text-gray-400 text-xs">
                          [{commit.date}]
                        </span>
                      </div>
                      <p className="text-white text-sm">{commit.message}</p>
                      <p className="text-gray-500 text-xs mt-1">
                        {commit.author}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              {analysis.phases[expandedPhase as Phase].count > 20 && (
                <div className="text-center text-gray-400 text-sm py-2">
                  ... 외 {analysis.phases[expandedPhase as Phase].count - 20}개 커밋
                </div>
              )}
            </div>
          </div>
        )}

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-2">첫 커밋</h3>
            {analysis.first_commit && (
              <div>
                <p className="text-white font-mono text-sm mb-1">
                  {analysis.first_commit.hash}
                </p>
                <p className="text-gray-300 text-sm">{analysis.first_commit.message}</p>
                <p className="text-gray-500 text-xs mt-1">{analysis.first_commit.date}</p>
              </div>
            )}
          </div>
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-2">최근 커밋</h3>
            {analysis.latest_commit && (
              <div>
                <p className="text-white font-mono text-sm mb-1">
                  {analysis.latest_commit.hash}
                </p>
                <p className="text-gray-300 text-sm">{analysis.latest_commit.message}</p>
                <p className="text-gray-500 text-xs mt-1">{analysis.latest_commit.date}</p>
              </div>
            )}
          </div>
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-2">Phase 통계</h3>
            <p className="text-white text-2xl font-bold mb-1">
              {Object.keys(analysis.phases).length}
            </p>
            <p className="text-gray-400 text-sm">활성 Phase</p>
          </div>
        </div>
      </div>
    </div>
  );
}

