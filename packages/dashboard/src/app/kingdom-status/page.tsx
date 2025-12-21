'use client';

import { useApi } from '@/hooks/useApi';
import { LoadingSpinner, ErrorMessage } from '@/components/common';
import { REFRESH_INTERVALS } from '@/lib/constants';

interface KingdomStatus {
  git: {
    totalCommits: number;
    todayCommits: number;
    head: string;
    branch: string;
    synced: boolean;
  };
  trinity: {
    total: number;
    truth: number;
    goodness: number;
    beauty: number;
    serenity: number;
    eternity: number;
  };
  trackedFiles: number;
  timeline: Array<{ num: number; hash: string; msg: string }>;
  generatedAt: string;
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between py-2.5 border-b border-white/10">
      <span className="text-gray-300">{label}</span>
      <span className="font-bold text-green-400">{value}</span>
    </div>
  );
}

export default function KingdomStatusPage() {
  const {
    data: status,
    loading,
    error,
    refetch,
  } = useApi<KingdomStatus>('/api/kingdom-status', {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading Kingdom Status..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
        <ErrorMessage message={error.message} onRetry={refetch} />
      </div>
    );
  }

  if (!status) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white p-10 font-sans">
      <h1 className="text-center text-5xl mb-2.5 bg-gradient-to-r from-[#FFD700] to-[#FFA500] bg-clip-text text-transparent">
        👑 AFO Kingdom Status
      </h1>
      <p className="text-center text-gray-400 mb-10">
        Generated: {new Date(status.generatedAt).toLocaleString()} | {status.git.totalCommits} Commits
      </p>

      {/* Trinity Score */}
      <div className="text-center py-10 px-10 bg-gradient-to-br from-[rgba(255,215,0,0.1)] to-[rgba(255,165,0,0.1)] rounded-[30px] mb-7.5">
        <div className="text-[5rem] font-bold text-[#FFD700]">
          {status.trinity.total}
        </div>
        <div className="text-gray-400 text-xl">Trinity Score (眞善美孝永)</div>
        <div className="flex justify-center gap-7.5 mt-5 flex-wrap">
          <div className="text-center">
            <div className="text-2xl">眞 {status.trinity.truth}</div>
            <div className="text-gray-400">Truth 35%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl">善 {status.trinity.goodness}</div>
            <div className="text-gray-400">Goodness 35%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl">美 {status.trinity.beauty}</div>
            <div className="text-gray-400">Beauty 20%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl">孝 {status.trinity.serenity}</div>
            <div className="text-gray-400">Serenity 8%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl">永 {status.trinity.eternity}</div>
            <div className="text-gray-400">Eternity 2%</div>
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-5">
        {/* Git Status Card */}
        <div className="bg-white/5 backdrop-blur-[10px] rounded-[20px] p-6 border border-white/10">
          <h2 className="text-xl mb-3.75 text-[#FFD700]">📊 Git Status</h2>
          <Stat label="Total Commits" value={status.git.totalCommits.toString()} />
          <Stat label="Today's Commits" value={status.git.todayCommits.toString()} />
          <Stat label="HEAD" value={status.git.head} />
          <Stat label="Branch" value={status.git.branch} />
          <Stat label="Synced" value={status.git.synced ? '✅ Synced' : '⚠️ Changes'} />
        </div>

        {/* Timeline Card */}
        <div className="bg-white/5 backdrop-blur-[10px] rounded-[20px] p-6 border border-white/10">
          <h2 className="text-xl mb-3.75 text-[#FFD700]">🌳 Recent Commits</h2>
          {status.timeline.slice(0, 5).map((commit) => (
            <div key={commit.hash} className="flex gap-2.5 py-2 border-b border-white/10">
              <span className="text-blue-400 font-mono">{commit.hash}</span>
              <span className="text-gray-200">{commit.msg}</span>
            </div>
          ))}
        </div>
      </div>

      <p className="text-center mt-10 text-gray-500">
        승상 (Seungsang) | AFO Kingdom | 眞善美孝永
      </p>
    </div>
  );
}
