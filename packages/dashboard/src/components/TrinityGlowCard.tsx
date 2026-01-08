"use client";

import { useEffect, useState, useCallback, useMemo } from "react";

// Breakdown Interface - now supports null for loading states
export interface TrinityBreakdown {
  truth: number | null;
  goodness: number | null;
  beauty: number | null;
  filial_serenity: number | null;
  eternity: number | null;
  iccls_score?: number | null;  // ICCLS: Inter-Component Consistency Level Score
  sentiment_score?: number | null;  // Optional sentiment 0.0-1.0
}

interface TrinityGlowCardProps {
  trinityScore: number | null; // 0.0 - 1.0, null = loading
  riskScore: number | null; // 0.0 - 1.0, null = loading
  breakdown?: TrinityBreakdown;
  children?: React.ReactNode;
}

/**
 * TrinityGlowCard - Phase 7 Sensory Integration
 *
 * Displays a pulsing glow based on Trinity/Risk scores:
 * - Trinity ≥ 0.9: Bright green pulse (Safe)
 * - Trinity 0.7-0.9: Yellow steady glow (Caution)
 * - Trinity < 0.7: Red warning pulse (Alert)
 * - High Risk: Dark red aura overlay
 */
export function TrinityGlowCard({
  trinityScore,
  riskScore,
  breakdown,
  children,
}: TrinityGlowCardProps) {
  const [pulseScale, setPulseScale] = useState(1);

  // Animate pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setPulseScale((prev) => (prev === 1 ? 1.02 : 1));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Memoize glow color getter
  const getGlowColor = useCallback((): string => {
    if (trinityScore === null) return "#6b7280"; // Gray for loading
    if (trinityScore >= 0.9) return "#22c55e"; // Green
    if (trinityScore >= 0.7) return "#eab308"; // Yellow
    return "#ef4444"; // Red
  }, [trinityScore]);

  // Memoize calculated values
  const glowColor = useMemo(() => getGlowColor(), [getGlowColor]);
  const glowStrength = useMemo(
    () => (trinityScore !== null ? Math.round(trinityScore * 30) : 5),
    [trinityScore]
  );
  const riskOverlay = useMemo(
    () => (riskScore !== null && riskScore > 0.1 ? riskScore * 0.3 : 0),
    [riskScore]
  );

  return (
    <div
      className="relative p-6 rounded-2xl bg-black/80 min-h-[200px] flex flex-col justify-between transition-all duration-1000 ease-in-out"
      style={{
        boxShadow: `0 0 ${glowStrength}px ${glowColor}, 0 0 ${glowStrength * 2}px ${glowColor}`,
        transform: `scale(${pulseScale})`,
      }}
      role="region"
      aria-label={`Trinity Score: ${trinityScore !== null ? `${(trinityScore * 100).toFixed(0)}%` : "Loading"}, Risk Score: ${riskScore !== null ? `${(riskScore * 100).toFixed(0)}%` : "Loading"}`}
    >
      {/* Risk Overlay */}
      {riskScore !== null && riskScore > 0.1 && (
        <div
          className="absolute inset-0 rounded-2xl pointer-events-none"
          style={{
            background: `rgba(239, 68, 68, ${riskOverlay})`,
          }}
        />
      )}

      {/* Content */}
      <div className="relative z-10">{children}</div>

      {/* Breakdown Display */}
      {breakdown && (
        <div className="flex justify-between mt-4 border-t border-white/10 pt-2 text-xs text-gray-300">
          <div title="Truth (35%)" className="text-center">
            <div className="text-blue-500">眞</div>
            <div>{breakdown.truth !== null ? (breakdown.truth * 100).toFixed(0) : "--"}</div>
          </div>
          <div title="Goodness (35%)" className="text-center">
            <div className="text-green-500">善</div>
            <div>{breakdown.goodness !== null ? (breakdown.goodness * 100).toFixed(0) : "--"}</div>
          </div>
          <div title="Beauty (20%)" className="text-center">
            <div className="text-pink-500">美</div>
            <div>{breakdown.beauty !== null ? (breakdown.beauty * 100).toFixed(0) : "--"}</div>
          </div>
          <div title="Serenity (8%)" className="text-center">
            <div className="text-purple-500">孝</div>
            <div>
              {breakdown.filial_serenity !== null
                ? (breakdown.filial_serenity * 100).toFixed(0)
                : "--"}
            </div>
          </div>
          <div title="Eternity (2%)" className="text-center">
            <div className="text-amber-500">永</div>
            <div>{breakdown.eternity !== null ? (breakdown.eternity * 100).toFixed(0) : "--"}</div>
          </div>
        </div>
      )}

      {/* ICCLS + Sentiment Status */}
      {(breakdown?.iccls_score !== undefined || breakdown?.sentiment_score !== undefined) && (
        <div className="flex justify-between mt-2 text-xs border-t border-white/10 pt-2">
          {breakdown.iccls_score !== undefined && breakdown.iccls_score !== null && (
            <div className={`flex items-center gap-1 ${breakdown.iccls_score > 0.3 ? 'text-red-400' : 'text-green-400'}`}>
              <span>🔗</span>
              <span>ICCLS: {(breakdown.iccls_score * 100).toFixed(1)}%</span>
            </div>
          )}
          {breakdown.sentiment_score !== undefined && breakdown.sentiment_score !== null && (
            <div className="flex items-center gap-1">
              <span>{breakdown.sentiment_score > 0.6 ? '🟢' : breakdown.sentiment_score > 0.4 ? '🟡' : '🔴'}</span>
              <span>Sentiment: {(breakdown.sentiment_score * 100).toFixed(0)}%</span>
            </div>
          )}
        </div>
      )}

      {/* Score Display (Summary) */}
      {!breakdown && (
        <div className="flex justify-between mt-4 font-mono text-sm">
          <span className="font-semibold" style={{ color: glowColor }}>
            ⚖️ {trinityScore !== null ? `${(trinityScore * 100).toFixed(0)}%` : "Loading..."}
          </span>
          {riskScore !== null && riskScore > 0.1 && (
            <span className="text-red-500 font-semibold">
              ⚠️ Risk: {(riskScore * 100).toFixed(0)}%
            </span>
          )}
        </div>
      )}
    </div>
  );
}

export default TrinityGlowCard;
