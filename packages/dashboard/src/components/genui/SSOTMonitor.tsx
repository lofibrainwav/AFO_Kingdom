/**
 * SSOTMonitor.tsx
 * 
 * SSOT (Single Source of Truth) 모니터 컴포넌트
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useMemo, useCallback } from "react";
import { useApi } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/common";
import { REFRESH_INTERVALS } from "@/lib/constants";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface SSOTData {
  status: string;
  health: string;
  trinity: {
    truth: number;
    goodness: number;
    beauty: number;
    serenity: number;
    eternity: number;
    total: number;
  };
  risk: number;
  services: { online: number; total: number };
  git: { clean: boolean };
  timestamp: string;
}

function SSOTMonitorContent() {
  const { data: ssot, loading } = useApi<SSOTData>("/api/ssot-status", {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  // Memoize pillar scores
  const pillarScores = useMemo(() => {
    if (!ssot) return null;
    return {
      眞: ssot.trinity.truth,
      善: ssot.trinity.goodness,
      美: ssot.trinity.beauty,
      孝: ssot.trinity.serenity,
      永: ssot.trinity.eternity,
    };
  }, [ssot]);

  // Memoize formatted values
  const formattedData = useMemo(() => {
    if (!ssot) return null;
    return {
      totalScore: (ssot.trinity.total * 100).toFixed(1),
      healthStatus:
        ssot.health === "excellent" ? "✅ 眞善美孝永 정렬 완료" : `⚠️ ${ssot.health}`,
      timestamp: new Date(ssot.timestamp).toLocaleString(),
      servicesStatus: `${ssot.services.online}/${ssot.services.total} SERVICES ONLINE`,
    };
  }, [ssot]);

  // Memoize health color
  const getHealthColor = useCallback((health: string) => {
    return health === "excellent" ? "text-emerald-400" : "text-yellow-400";
  }, []);

  if (loading || !ssot || !pillarScores || !formattedData) {
    return (
      <div
        className="glass-card p-6 max-w-md mx-auto bg-black/40 rounded-3xl border border-white/10"
        role="status"
        aria-live="polite"
        aria-label="Loading SSOT status"
      >
        <LoadingSpinner size="sm" text="SSOT 점검 중... 곧 정렬 완료돼요 ✨" />
      </div>
    );
  }

  return (
    <div
      className="glass-card p-6 max-w-md mx-auto bg-gradient-to-br from-cyan-900/20 to-emerald-900/20 rounded-3xl border border-cyan-500/30 shadow-xl backdrop-blur-md"
      role="region"
      aria-labelledby="ssot-monitor-title"
    >
      <h3
        id="ssot-monitor-title"
        className="text-xl font-bold text-cyan-400 mb-4 text-center tracking-widest font-mono"
      >
        왕국 SSOT 상태
      </h3>

      <div
        className="flex justify-center items-end gap-2 mb-4"
        role="status"
        aria-live="polite"
        aria-label={`Total SSOT score: ${formattedData.totalScore} out of 100`}
      >
        <span className="text-5xl font-black text-emerald-400 drop-shadow-[0_0_10px_rgba(52,211,153,0.5)]">
          {formattedData.totalScore}
        </span>
        <span className="text-xl text-emerald-600 font-bold mb-2">/100</span>
      </div>

      <div
        className="bg-black/30 rounded-xl p-3 mb-6 grid grid-cols-5 gap-1 text-center"
        role="list"
        aria-label="Pillar scores"
      >
        {Object.entries(pillarScores).map(([key, val]) => (
          <div
            key={key}
            className="flex flex-col"
            role="listitem"
            aria-label={`${key} pillar: ${(val * 100).toFixed(0)}%`}
          >
            <span className="text-xs text-white/50">{key}</span>
            <span className="text-sm font-bold text-white">{(val * 100).toFixed(0)}</span>
          </div>
        ))}
      </div>

      <p
        className={`text-center text-white/90 mb-2 font-medium bg-emerald-500/10 py-2 rounded-lg border border-emerald-500/20 ${getHealthColor(
          ssot.health
        )}`}
        role="status"
        aria-live="polite"
      >
        {formattedData.healthStatus}
      </p>

      <p
        className="text-[10px] text-white/40 text-center italic font-mono uppercase"
        aria-label={`Last update: ${formattedData.timestamp}, ${formattedData.servicesStatus}`}
      >
        Last Update: {formattedData.timestamp} <br />
        <span className="text-cyan-500/60">● {formattedData.servicesStatus}</span>
      </p>
    </div>
  );
}

export function SSOTMonitor() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("SSOTMonitor error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-6 max-w-md mx-auto bg-black/40 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">SSOT 모니터를 불러올 수 없습니다.</p>
        </div>
      }
    >
      <SSOTMonitorContent />
    </ErrorBoundary>
  );
}

export default SSOTMonitor;
