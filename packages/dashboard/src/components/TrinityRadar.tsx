"use client";

import { useMemo } from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { TrinityBreakdown } from "./TrinityGlowCard";

interface TrinityRadarProps {
  breakdown: TrinityBreakdown;
  size?: number;
  showLabels?: boolean;
  animated?: boolean;
}

/**
 * TrinityRadar - 眞善美孝永 5기둥 레이더 차트
 *
 * SSOT 가중치: 眞(35%) + 善(35%) + 美(20%) + 孝(8%) + 永(2%) = 100%
 *
 * 색상 스키마 (TrinityGlowCard와 일관성 유지):
 * - 眞 (Truth): blue-500
 * - 善 (Goodness): green-500
 * - 美 (Beauty): pink-500
 * - 孝 (Serenity): purple-500
 * - 永 (Eternity): amber-500
 */
export function TrinityRadar({
  breakdown,
  size = 300,
  showLabels = true,
  animated = true,
}: TrinityRadarProps) {
  // Transform breakdown to radar data format (3-Axis Friction Triangle)
  const radarData = useMemo(() => {
    return [
      {
        pillar: "眞",
        fullName: "Truth (35%)",
        value: breakdown.truth !== null ? breakdown.truth * 100 : 0,
        weight: 35,
        color: "#3b82f6", // blue-500
      },
      {
        pillar: "善",
        fullName: "Goodness (35%)",
        value: breakdown.goodness !== null ? breakdown.goodness * 100 : 0,
        weight: 35,
        color: "#22c55e", // green-500
      },
      {
        pillar: "美",
        fullName: "Beauty (30%)",
        value: breakdown.beauty !== null ? breakdown.beauty * 100 : 0,
        weight: 30,
        color: "#ec4899", // pink-500
      },
    ];
  }, [breakdown]);

  // Calculate weighted Trinity Score
  const trinityScore = useMemo(() => {
    const weighted = radarData.reduce((acc, item) => {
      return acc + (item.value / 100) * (item.weight / 100);
    }, 0);
    return weighted * 100;
  }, [radarData]);

  // Determine radar fill color based on Trinity Score
  const radarFillColor = useMemo(() => {
    if (trinityScore >= 90) return "#22c55e"; // green
    if (trinityScore >= 70) return "#eab308"; // yellow
    return "#ef4444"; // red
  }, [trinityScore]);

  // Check if data is loading (all values are 0)
  const isLoading = useMemo(() => {
    return radarData.every((item) => item.value === 0);
  }, [radarData]);

  if (isLoading) {
    return (
      <div
        className="flex items-center justify-center bg-black/60 rounded-xl"
        style={{ width: size, height: size }}
        role="img"
        aria-label="Trinity Radar loading"
      >
        <div className="text-gray-500 text-sm">Loading...</div>
      </div>
    );
  }

  return (
    <div
      className="relative bg-black/60 rounded-xl p-2"
      style={{ width: size, height: size }}
      role="img"
      aria-label={`Trinity Radar Chart - Score: ${trinityScore.toFixed(0)}%`}
    >
      {/* Trinity Score Badge */}
      <div
        className="absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-bold z-10"
        style={{
          backgroundColor: radarFillColor + "33",
          color: radarFillColor,
          border: `1px solid ${radarFillColor}`,
        }}
      >
        ⚖️ {trinityScore.toFixed(0)}%
      </div>

      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="70%">
          <PolarGrid stroke="#374151" strokeOpacity={0.5} />
          <PolarAngleAxis
            dataKey="pillar"
            tick={{
              fill: "#9ca3af",
              fontSize: showLabels ? 14 : 0,
              fontWeight: "bold",
            }}
            tickLine={false}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: "#6b7280", fontSize: 10 }}
            tickCount={5}
            axisLine={false}
          />
          <Radar
            name="Trinity Score"
            dataKey="value"
            stroke={radarFillColor}
            fill={radarFillColor}
            fillOpacity={0.4}
            strokeWidth={2}
            isAnimationActive={animated}
            animationDuration={1000}
          />
          <Tooltip
            content={({ payload }) => {
              if (!payload || payload.length === 0) return null;
              const data = payload[0].payload;
              return (
                <div className="bg-black/90 border border-white/20 rounded-lg p-2 text-xs">
                  <div className="font-bold" style={{ color: data.color }}>
                    {data.pillar} {data.fullName}
                  </div>
                  <div className="text-white">Score: {data.value.toFixed(1)}%</div>
                </div>
              );
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TrinityRadar;
