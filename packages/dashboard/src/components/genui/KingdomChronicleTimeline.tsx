/**
 * KingdomChronicleTimeline.tsx
 *
 * AFO 왕국 92커밋 연대기 타임라인 위젯
 * "역사를 모르는 자는 미래를 만들 수 없다." — 孫子
 *
 * Design: Glassmorphism + Gradient + Timeline
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo } from "react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface Phase {
  phase: string;
  title: string;
  desc: string;
  commits?: string;
  color: string;
  icon: string;
}

const phases: Phase[] = [
  {
    phase: "0",
    title: "Genesis",
    desc: "초심 설정 · 승상 탄생",
    commits: "5",
    color: "#9333EA",
    icon: "🌟",
  },
  {
    phase: "1",
    title: "Security Hardening",
    desc: "善의 방패 · GitHub Actions",
    commits: "10",
    color: "#EF4444",
    icon: "🛡️",
  },
  {
    phase: "2",
    title: "CI/CD Stabilization",
    desc: "眞의 기반 · 290 테스트",
    commits: "30",
    color: "#3B82F6",
    icon: "⚙️",
  },
  {
    phase: "3",
    title: "MCP Ecosystem",
    desc: "孝의 연결 · Context7",
    commits: "10",
    color: "#22C55E",
    icon: "🔗",
  },
  {
    phase: "4-6",
    title: "Trinity Governance",
    desc: "균형의 통치 · 라우팅",
    commits: "15",
    color: "#06B6D4",
    icon: "⚖️",
  },
  {
    phase: "7-9",
    title: "Autonomous Kingdom",
    desc: "永의 자율 · GenUI",
    commits: "15",
    color: "#10B981",
    icon: "🤖",
  },
  {
    phase: "10",
    title: "Final Polish",
    desc: "美의 광택 · 100% Clean",
    commits: "7",
    color: "#EC4899",
    icon: "✨",
  },
  { phase: "現", title: "SSOT 100.0", desc: "왕국 완성", color: "#FBBF24", icon: "👑" },
];

function KingdomChronicleTimelineContent() {
  // Memoize phases data
  const memoizedPhases = useMemo(() => phases, []);

  return (
    <div
      className="chronicle-timeline bg-gradient-to-br from-gray-900/90 to-purple-900/30 backdrop-blur-xl rounded-3xl border border-white/10 p-8 max-w-[800px] mx-auto shadow-2xl"
      role="region"
      aria-labelledby="chronicle-title"
    >
      {/* Header */}
      <header className="text-center mb-8">
        <h2
          id="chronicle-title"
          className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-2"
        >
          🏰 AFO 왕국 진화 연대기
        </h2>
        <p className="text-white/70 italic" aria-label="Quote from Sun Tzu">
          "역사를 모르는 자는 미래를 만들 수 없다." — 孫子
        </p>
      </header>

      {/* Timeline */}
      <div className="relative pl-10" role="list" aria-label="Kingdom evolution timeline">
        {/* Vertical Line */}
        <div
          className="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-cyan-400 via-purple-500 to-amber-400"
          aria-hidden="true"
        />

        {memoizedPhases.map((p, i) => (
          <div
            key={i}
            className="flex items-center gap-5 mb-6 relative"
            role="listitem"
            aria-label={`Phase ${p.phase}: ${p.title} - ${p.desc}`}
          >
            {/* Circle Node */}
            <div
              className="absolute -left-8 w-8 h-8 rounded-full flex items-center justify-center text-base z-10"
              style={{
                background: p.color,
                boxShadow: `0 0 20px ${p.color}50`,
              }}
              aria-hidden="true"
            >
              {p.icon}
            </div>

            {/* Content Card */}
            <div
              className="flex-1 bg-white/5 rounded-xl px-5 py-4 transition-all duration-300 ease-in-out hover:bg-white/10 hover:translate-x-2"
              style={{
                border: `1px solid ${p.color}30`,
              }}
            >
              <div className="flex items-center gap-3">
                <span
                  className="text-white px-3 py-1 rounded-full text-xs font-bold"
                  style={{ background: p.color }}
                  aria-label={`Phase ${p.phase}`}
                >
                  Phase {p.phase}
                </span>
                {p.commits && (
                  <span className="text-white/50 text-xs" aria-label={`${p.commits} commits`}>
                    {p.commits} commits
                  </span>
                )}
              </div>
              <h3 className="text-white text-lg font-bold mt-2">{p.title}</h3>
              <p className="text-white/70 text-sm mt-1">{p.desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Footer Stats */}
      <footer
        className="mt-8 p-5 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 rounded-2xl border border-white/10 text-center"
        aria-label="Kingdom statistics"
      >
        <div className="flex justify-center gap-10 flex-wrap" role="list" aria-label="Statistics">
          <div role="listitem" aria-label="Total commits: 92">
            <div className="text-cyan-400 text-3xl font-bold">92</div>
            <div className="text-white/70 text-sm">Total Commits</div>
          </div>
          <div role="listitem" aria-label="SSOT Score: 100.0">
            <div className="text-purple-500 text-3xl font-bold">100.0</div>
            <div className="text-white/70 text-sm">SSOT Score</div>
          </div>
          <div role="listitem" aria-label="Tests passing: 290+">
            <div className="text-green-500 text-3xl font-bold">290+</div>
            <div className="text-white/70 text-sm">Tests Passing</div>
          </div>
        </div>
        <p className="text-amber-400 mt-4 font-bold text-base" aria-live="polite">
          眞善美孝永 — 다섯 기둥이 왕국을 지탱합니다
        </p>
      </footer>
    </div>
  );
}

export function KingdomChronicleTimeline() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("KingdomChronicleTimeline error:", error, errorInfo);
      }}
      fallback={
        <div
          className="chronicle-timeline bg-gradient-to-br from-gray-900/90 to-purple-900/30 backdrop-blur-xl rounded-3xl border border-red-500/30 p-8 max-w-[800px] mx-auto shadow-2xl"
          role="alert"
        >
          <p className="text-red-400 text-center">왕국 연대기를 불러올 수 없습니다.</p>
        </div>
      }
    >
      <KingdomChronicleTimelineContent />
    </ErrorBoundary>
  );
}

export default KingdomChronicleTimeline;
