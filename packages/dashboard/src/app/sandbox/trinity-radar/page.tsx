"use client";

import { useState } from "react";
import { TrinityGlowCard, TrinityBreakdown } from "@/components/TrinityGlowCard";
import { TrinityRadar } from "@/components/TrinityRadar";

/**
 * TrinityRadar Demo Page - 眞善美孝永 시각화 검증
 *
 * 사용법: npm run dev → http://localhost:3000/sandbox/trinity-radar
 */
export default function TrinityRadarDemoPage() {
  const [showRadar, setShowRadar] = useState(true);

  const breakdown: TrinityBreakdown = {
    truth: 0.92,
    goodness: 0.88,
    beauty: 0.75,
    filial_serenity: 0.90,
    eternity: 0.85,
    iccls_score: 0.15,
    sentiment_score: 0.75,
  };

  const trinityScore =
    (breakdown.truth ?? 0) * 0.35 +
    (breakdown.goodness ?? 0) * 0.35 +
    (breakdown.beauty ?? 0) * 0.20 +
    (breakdown.filial_serenity ?? 0) * 0.08 +
    (breakdown.eternity ?? 0) * 0.02;

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <h1 className="text-3xl font-bold text-white mb-8 text-center">
        🏰 TrinityRadar 검증 페이지
      </h1>

      <div className="max-w-4xl mx-auto space-y-8">
        {/* Controls */}
        <div className="flex justify-center gap-4">
          <button
            onClick={() => setShowRadar(!showRadar)}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              showRadar
                ? "bg-green-600 text-white"
                : "bg-gray-700 text-gray-300"
            }`}
          >
            {showRadar ? "🎯 Radar ON" : "🎯 Radar OFF"}
          </button>
        </div>

        {/* Side by Side Comparison */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* TrinityGlowCard with showRadar */}
          <div>
            <h2 className="text-xl text-white mb-4 text-center">
              TrinityGlowCard (showRadar={showRadar ? "true" : "false"})
            </h2>
            <TrinityGlowCard
              trinityScore={trinityScore}
              riskScore={0.05}
              breakdown={breakdown}
              showRadar={showRadar}
            >
              <div className="text-white text-center">
                <h3 className="text-lg font-bold">👑 AFO Kingdom Status</h3>
                <p className="text-sm text-gray-400">
                  眞善美孝永 Balance Monitor
                </p>
              </div>
            </TrinityGlowCard>
          </div>

          {/* Standalone TrinityRadar */}
          <div>
            <h2 className="text-xl text-white mb-4 text-center">
              Standalone TrinityRadar
            </h2>
            <div className="flex justify-center">
              <TrinityRadar breakdown={breakdown} size={300} />
            </div>
          </div>
        </div>

        {/* Data Display */}
        <div className="bg-black/50 rounded-xl p-6 text-white">
          <h3 className="text-lg font-bold mb-4">📊 Current Data</h3>
          <pre className="text-xs overflow-auto">
            {JSON.stringify(breakdown, null, 2)}
          </pre>
          <div className="mt-4 flex gap-4 text-sm">
            <span>Trinity Score: {(trinityScore * 100).toFixed(1)}%</span>
            <span>ICCLS: {((breakdown.iccls_score ?? 0) * 100).toFixed(1)}%</span>
            <span>Sentiment: {((breakdown.sentiment_score ?? 0) * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
