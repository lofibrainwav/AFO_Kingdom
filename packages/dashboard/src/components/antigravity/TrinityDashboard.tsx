"use client";

import { AlertTriangle, Crown, Heart, Infinity, Palette, RefreshCw, Shield, TrendingUp } from 'lucide-react';
import { useEffect, useState } from 'react';

import { useVerdictStream } from '../../lib/useVerdictStream';
import TrinityRingChart from './TrinityRingChart';
import VerdictLogModal from './VerdictLogModal';



interface TrinityScore {
  truth_score: number;
  goodness_score: number;
  beauty_score: number;
  serenity_score: number;
  eternity_score: number;
  overall_score: number;
  auto_run_eligible: boolean;
  eligibility_reason: string;
}

interface QualityMetrics {
  total_issues: number;
  syntax_ok: boolean;
  test_coverage: number;
  has_ci: boolean;
  has_tests: boolean;
  has_docs: boolean;
}

interface TrinityReport {
  summary: {
    issues_before: number;
    issues_after: number;
    issues_fixed: number;
    improvement_rate: number;
    syntax_ok: boolean;
  };
  verification: {
    trinity_score: TrinityScore;
  };
  quality_metrics?: QualityMetrics;
}

export default function TrinityDashboard() {
  const [report, setReport] = useState<TrinityReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Ring→Log 딥링크 모달 상태
  const [selectedPillar, setSelectedPillar] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // 왕국의 신경계: SSE 스트리밍으로 실시간 verdict 수신
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8010";
  const { connected, events, error: streamError } = useVerdictStream(apiBase);

  useEffect(() => {
    fetchTrinityReport();
  }, []);

  // SSE 이벤트로 실시간 점수 업데이트
  useEffect(() => {
    if (events.length > 0 && report) {
      const latestEvent = events[0];
      // SSE 이벤트로 Trinity 점수 실시간 업데이트
      setReport(prevReport => {
        if (!prevReport) return prevReport;
        return {
          ...prevReport,
          verification: {
            ...prevReport.verification,
            trinity_score: {
              ...prevReport.verification.trinity_score,
              truth_score: latestEvent.risk_score || prevReport.verification.trinity_score.truth_score,
              goodness_score: latestEvent.trinity_score || prevReport.verification.trinity_score.goodness_score,
              auto_run_eligible: !latestEvent.veto_triggered,
            }
          }
        };
      });
    }
  }, [events, report]);

  // Ring→Log 딥링크 핸들러 + URL query 연동
  const handlePillarClick = (pillar: string) => {
    setSelectedPillar(pillar);
    setIsModalOpen(true);
    // URL query에 pillar 정보 추가 (브라우저 뒤로가기/새로고침 지원)
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      url.searchParams.set('pillar', pillar);
      window.history.replaceState({}, '', url.toString());
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPillar(null);
    // 모달 닫을 때 URL query 제거
    if (typeof window !== 'undefined') {
      const url = new URL(window.location.href);
      url.searchParams.delete('pillar');
      window.history.replaceState({}, '', url.toString());
    }
  };

  const fetchTrinityReport = async () => {
    try {
      setLoading(true);
      // 실제로는 API에서 데이터를 가져옴
      // const response = await fetch('/api/antigravity/metrics');
      // const data = await response.json();

      // 임시 데이터 (실제로는 API 연동)
      const mockData: TrinityReport = {
        summary: {
          issues_before: 1831,
          issues_after: 2107,
          issues_fixed: 1456,
          improvement_rate: -15.1,
          syntax_ok: true,
        },
        verification: {
          trinity_score: {
            truth_score: 85.0,
            goodness_score: 88.0,
            beauty_score: 87.0,
            serenity_score: 86.0,
            eternity_score: 84.0,
            overall_score: 86.5,
            auto_run_eligible: false,
            eligibility_reason: "Trinity Score 86.5 < 90.0",
          },
        },
        quality_metrics: {
          total_issues: 2107,
          syntax_ok: true,
          test_coverage: 65.2,
          has_ci: true,
          has_tests: true,
          has_docs: true,
        },
      };

      setReport(mockData);
      setError(null);
    } catch (err) {
      setError('Trinity 리포트를 불러오는데 실패했습니다.');
      console.error('Failed to fetch Trinity report:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-emerald-400';
    if (score >= 80) return 'text-yellow-400';
    if (score >= 70) return 'text-orange-400';
    return 'text-red-400';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 90) return 'bg-emerald-500/20 border-emerald-500/50';
    if (score >= 80) return 'bg-yellow-500/20 border-yellow-500/50';
    if (score >= 70) return 'bg-orange-500/20 border-orange-500/50';
    return 'bg-red-500/20 border-red-500/50';
  };

  const getStatusIcon = (score: number) => {
    if (score >= 90) return <Crown className="w-5 h-5 text-emerald-400" />;
    if (score >= 80) return <Shield className="w-5 h-5 text-yellow-400" />;
    if (score >= 70) return <Palette className="w-5 h-5 text-orange-400" />;
    return <AlertTriangle className="w-5 h-5 text-red-400" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="w-6 h-6 animate-spin text-emerald-400" />
          <span className="text-gray-400">Trinity Score 계산 중...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <p className="text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!report) return null;

  const { summary, verification, quality_metrics } = report;
  const trinityScore = verification.trinity_score;

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center">
            <Crown className="w-8 h-8 text-emerald-400 mr-3" />
            Trinity Quality Dashboard
          </h2>
          <p className="text-gray-400 mt-1">
            AFO 왕국의 5대 기둥 기반 코드 품질 모니터링
          </p>
        </div>
        <button
          onClick={fetchTrinityReport}
          className="flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          <span>새로고침</span>
        </button>
      </div>

      {/* Trinity Breakdown Ring Chart - 모바일 최소 모드 지원 */}
      <div className="bg-gray-800/50 p-4 md:p-6 rounded-lg border border-gray-700">
        <h3 className="text-base md:text-lg font-semibold text-white mb-4 text-center">
          Trinity Score Breakdown - 헌법 v1.0 기준
        </h3>
        {/* 모바일에서는 간소화된 Ring Chart */}
        <div className="block md:hidden mb-4">
          <div className="grid grid-cols-5 gap-2 mb-4">
            {[
              { key: 'truth', label: '眞', score: trinityScore.truth_score, color: 'text-blue-400' },
              { key: 'goodness', label: '善', score: trinityScore.goodness_score, color: 'text-green-400' },
              { key: 'beauty', label: '美', score: trinityScore.beauty_score, color: 'text-purple-400' },
              { key: 'serenity', label: '孝', score: trinityScore.serenity_score, color: 'text-pink-400' },
              { key: 'eternity', label: '永', score: trinityScore.eternity_score, color: 'text-cyan-400' },
            ].map((pillar) => (
              <button
                key={pillar.key}
                onClick={() => handlePillarClick(pillar.key)}
                className="bg-gray-700/50 p-2 rounded-lg border border-gray-600 hover:bg-gray-600/50 transition-colors"
              >
                <div className={`text-lg font-bold ${pillar.color}`}>{pillar.score}</div>
                <div className="text-xs text-gray-400">{pillar.label}</div>
              </button>
            ))}
          </div>
        </div>
        {/* 데스크톱에서는 풀 Ring Chart */}
        <div className="hidden md:block">
          <TrinityRingChart
            truthScore={trinityScore.truth_score}
            goodnessScore={trinityScore.goodness_score}
            beautyScore={trinityScore.beauty_score}
            serenityScore={trinityScore.serenity_score}
            eternityScore={trinityScore.eternity_score}
            vetoTriggered={!trinityScore.auto_run_eligible}
            vetoPillars={[]} // TODO: Chancellor Graph에서 veto 정보 전달받기
            onPillarClick={handlePillarClick}
          />
        </div>
      </div>

      {/* Overall Score */}
      <div className={`p-6 rounded-lg border ${getScoreBgColor(trinityScore.overall_score)}`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getStatusIcon(trinityScore.overall_score)}
            <div>
              <h3 className="text-lg font-semibold text-white">Overall Trinity Score</h3>
              <p className="text-gray-400 text-sm">5대 기둥 통합 점수 (眞0.35 + 善0.35 + 美0.20 + 孝0.08 + 永0.02)</p>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-3xl font-bold ${getScoreColor(trinityScore.overall_score)}`}>
              {trinityScore.overall_score}/100
            </div>
            <div className="flex items-center space-x-2 mt-1">
              <div className={`w-2 h-2 rounded-full ${trinityScore.auto_run_eligible ? 'bg-emerald-400' : 'bg-yellow-400'}`}></div>
              <span className="text-xs text-gray-400">
                {trinityScore.auto_run_eligible ? 'Auto-run Eligible' : 'Manual Review Required'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 5대 기둥 점수 */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <Crown className="w-5 h-5 text-blue-400" />
            <span className="text-gray-400 text-sm">眞 Truth</span>
          </div>
          <div className={`text-2xl font-bold ${getScoreColor(trinityScore.truth_score)}`}>
            {trinityScore.truth_score}
          </div>
          <div className="text-xs text-gray-500 mt-1">타입 정확성</div>
        </div>

        <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <Shield className="w-5 h-5 text-green-400" />
            <span className="text-gray-400 text-sm">善 Goodness</span>
          </div>
          <div className={`text-2xl font-bold ${getScoreColor(trinityScore.goodness_score)}`}>
            {trinityScore.goodness_score}
          </div>
          <div className="text-xs text-gray-500 mt-1">안전성</div>
        </div>

        <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <Palette className="w-5 h-5 text-purple-400" />
            <span className="text-gray-400 text-sm">美 Beauty</span>
          </div>
          <div className={`text-2xl font-bold ${getScoreColor(trinityScore.beauty_score)}`}>
            {trinityScore.beauty_score}
          </div>
          <div className="text-xs text-gray-500 mt-1">코드 품질</div>
        </div>

        <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <Heart className="w-5 h-5 text-pink-400" />
            <span className="text-gray-400 text-sm">孝 Serenity</span>
          </div>
          <div className={`text-2xl font-bold ${getScoreColor(trinityScore.serenity_score)}`}>
            {trinityScore.serenity_score}
          </div>
          <div className="text-xs text-gray-500 mt-1">유지보수성</div>
        </div>

        <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
          <div className="flex items-center space-x-2 mb-2">
            <Infinity className="w-5 h-5 text-cyan-400" />
            <span className="text-gray-400 text-sm">永 Eternity</span>
          </div>
          <div className={`text-2xl font-bold ${getScoreColor(trinityScore.eternity_score)}`}>
            {trinityScore.eternity_score}
          </div>
          <div className="text-xs text-gray-500 mt-1">확장성</div>
        </div>
      </div>

      {/* 개선 현황 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800/50 p-6 rounded-lg border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 text-emerald-400 mr-2" />
            코드 개선 현황
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">수정 전 이슈</span>
              <span className="text-red-400 font-semibold">{summary.issues_before}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">수정 후 이슈</span>
              <span className="text-yellow-400 font-semibold">{summary.issues_after}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">자동 수정</span>
              <span className="text-emerald-400 font-semibold">{summary.issues_fixed}</span>
            </div>
            <div className="flex justify-between items-center border-t border-gray-700 pt-2">
              <span className="text-gray-400">개선율</span>
              <span className={`font-semibold ${summary.improvement_rate >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {summary.improvement_rate >= 0 ? '+' : ''}{summary.improvement_rate}%
              </span>
            </div>
          </div>
        </div>

        <div className="bg-gray-800/50 p-6 rounded-lg border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Shield className="w-5 h-5 text-blue-400 mr-2" />
            품질 메트릭
          </h3>
          {quality_metrics && (
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Syntax 상태</span>
                <span className={`font-semibold ${quality_metrics.syntax_ok ? 'text-emerald-400' : 'text-red-400'}`}>
                  {quality_metrics.syntax_ok ? '✅ 정상' : '❌ 오류'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">테스트 커버리지</span>
                <span className={`font-semibold ${quality_metrics.test_coverage >= 80 ? 'text-emerald-400' : 'text-yellow-400'}`}>
                  {quality_metrics.test_coverage}%
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">CI/CD</span>
                <span className={`font-semibold ${quality_metrics.has_ci ? 'text-emerald-400' : 'text-red-400'}`}>
                  {quality_metrics.has_ci ? '✅ 활성' : '❌ 없음'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">문서화</span>
                <span className={`font-semibold ${quality_metrics.has_docs ? 'text-emerald-400' : 'text-red-400'}`}>
                  {quality_metrics.has_docs ? '✅ 완전' : '❌ 불충분'}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 자동화 상태 */}
      <div className={`p-4 rounded-lg border ${trinityScore.auto_run_eligible ? 'bg-emerald-500/10 border-emerald-500/50' : 'bg-yellow-500/10 border-yellow-500/50'}`}>
        <div className="flex items-center space-x-3">
          <div className={`w-3 h-3 rounded-full ${trinityScore.auto_run_eligible ? 'bg-emerald-400' : 'bg-yellow-400'}`}></div>
          <div>
            <h4 className="text-white font-semibold">
              {trinityScore.auto_run_eligible ? '🚀 자동 승인 가능' : '⏳ 수동 검토 필요'}
            </h4>
            <p className="text-gray-400 text-sm">
              {trinityScore.eligibility_reason}
            </p>
          </div>
        </div>
      </div>

      {/* Ring→Log 딥링크 모달 */}
      <VerdictLogModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        pillar={selectedPillar || ''}
        verdictEvents={events}
      />
    </div>
  );
}
