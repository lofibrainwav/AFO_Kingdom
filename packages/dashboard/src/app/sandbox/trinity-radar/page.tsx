"use client";

import { TrinityGlowCard } from "@/components/TrinityGlowCard";
import { TrinityRadar } from "@/components/TrinityRadar";
import { useTrinityData } from "@/hooks/useTrinityData";

/**
 * TrinityRadar Demo Page - 眞善美孝永 시각화 검증
 *
 * 실시간 API 데이터 연결 (/api/health → useTrinityData)
 *
 * 사용법: npm run dev → http://localhost:3000/sandbox/trinity-radar
 */
export default function TrinityRadarDemoPage() {
  // 실시간 데이터 가져오기 (15초 간격 갱신)
  const { trinityScore, riskScore, breakdown, loading, error, lastUpdated } =
    useTrinityData(15000);

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <h1 className="text-3xl font-bold text-white mb-2 text-center">
        🏰 TrinityRadar (실시간 API 연결)
      </h1>

      {/* Status Badge */}
      <div className="flex justify-center gap-4 mb-8">
        {loading ? (
          <span className="px-3 py-1 bg-yellow-600 text-white rounded-full text-sm">
            ⏳ Loading...
          </span>
        ) : error ? (
          <span className="px-3 py-1 bg-orange-600 text-white rounded-full text-sm">
            ⚠️ {error}
          </span>
        ) : (
          <span className="px-3 py-1 bg-green-600 text-white rounded-full text-sm">
            🟢 Live Data
          </span>
        )}
        {lastUpdated && (
          <span className="text-gray-400 text-sm">
            Last: {lastUpdated.toLocaleTimeString()}
          </span>
        )}
      </div>

      <div className="max-w-4xl mx-auto space-y-8">
        {/* Side by Side Comparison */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* TrinityGlowCard with showRadar */}
          <div>
            <h2 className="text-xl text-white mb-4 text-center">
              TrinityGlowCard (showRadar=true)
            </h2>
            <TrinityGlowCard
              trinityScore={trinityScore}
              riskScore={riskScore}
              breakdown={breakdown}
              showRadar={true}
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
          <h3 className="text-lg font-bold mb-4">📊 Live Data (from /api/health)</h3>
          <pre className="text-xs overflow-auto bg-black/30 p-4 rounded">
            {JSON.stringify(breakdown, null, 2)}
          </pre>
          <div className="mt-4 flex flex-wrap gap-4 text-sm">
            <span className="px-2 py-1 bg-blue-900 rounded">
              Trinity: {trinityScore !== null ? `${(trinityScore * 100).toFixed(1)}%` : "--"}
            </span>
            <span className="px-2 py-1 bg-red-900 rounded">
              Risk: {riskScore !== null ? `${(riskScore * 100).toFixed(1)}%` : "--"}
            </span>
            <span className="px-2 py-1 bg-green-900 rounded">
              ICCLS: {breakdown.iccls_score !== null && breakdown.iccls_score !== undefined ? `${(breakdown.iccls_score * 100).toFixed(1)}%` : "--"}
            </span>
            <span className="px-2 py-1 bg-purple-900 rounded">
              Sentiment: {breakdown.sentiment_score !== null && breakdown.sentiment_score !== undefined ? `${(breakdown.sentiment_score * 100).toFixed(0)}%` : "--"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
