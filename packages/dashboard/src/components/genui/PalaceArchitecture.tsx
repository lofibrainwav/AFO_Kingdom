"use client";

import React from "react";

interface PalaceArchitectureProps {
  type: string;
  x: number;
  y: number;
  scale?: number;
  isActive?: boolean;
  label?: string;
  organLabel?: string;
  riskLevel?: number;
  trinityScore?: number;
  onClick?: () => void;
}

export function PalaceArchitecture({
  type,
  x,
  y,
  scale = 1,
  isActive = false,
  label = "",
  organLabel = "",
  riskLevel = 0,
  trinityScore,
  onClick,
}: PalaceArchitectureProps) {
  const getRiskColor = () => {
    if (riskLevel < 20) return "border-emerald-500/60 bg-emerald-900/20";
    if (riskLevel < 50) return "border-amber-500/60 bg-amber-900/20";
    return "border-red-500/60 bg-red-900/20";
  };

  return (
    <div
      className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-500 hover:scale-110 ${
        isActive ? "animate-pulse" : ""
      }`}
      style={{
        left: `calc(50% + ${x}px)`,
        top: `calc(50% + ${y}px)`,
        transform: `translate(-50%, -50%) scale(${scale})`,
      }}
      onClick={onClick}
    >
      <div
        className={`relative w-32 h-32 rounded-lg border-2 ${getRiskColor()} backdrop-blur-md shadow-lg hover:shadow-xl`}
      >
        <div className="absolute inset-0 flex flex-col items-center justify-center p-2">
          <span className="text-3xl mb-1">
            {type === "Royal" && "🏛️"}
            {type === "Sanctuary" && "📚"}
            {type === "Gate" && "🛡️"}
            {type === "Barracks" && "⚔️"}
            {type === "Observatory" && "🔭"}
            {type === "Warehouse" && "🧪"}
          </span>
          <span className="text-xs font-bold text-[#f5e6d3] text-center">
            {label}
          </span>
          <span className="text-[10px] text-[#d4af37] opacity-80">
            {organLabel}
          </span>
          {trinityScore && (
            <span className="text-[10px] text-emerald-400 font-mono">
              Trinity: {trinityScore}%
            </span>
          )}
          <span className="text-[10px] text-gray-400 font-mono">
            Risk: {riskLevel}%
          </span>
        </div>
      </div>
    </div>
  );
}
