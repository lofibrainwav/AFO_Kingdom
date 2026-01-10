"use client";

import React from "react";
import { Book, Shield, Aperture, LucideIcon } from "lucide-react";

interface StrategistCardProps {
  name: string;
  role: string;
  influence: number;
  iconName: "book" | "shield" | "aperture";
  color: "emerald" | "slate" | "cyan";
}

const iconMap: Record<string, LucideIcon> = {
  book: Book,
  shield: Shield,
  aperture: Aperture,
};

const colorMap: Record<string, string> = {
  emerald:
    "border-emerald-500/60 bg-emerald-900/30 text-emerald-400 hover:border-emerald-400",
  slate:
    "border-slate-500/60 bg-slate-900/30 text-slate-400 hover:border-slate-400",
  cyan: "border-cyan-500/60 bg-cyan-900/30 text-cyan-400 hover:border-cyan-400",
};

export function StrategistCard({
  name,
  role,
  influence,
  iconName,
  color,
}: StrategistCardProps) {
  const Icon = iconMap[iconName] || Book;
  const colorClasses = colorMap[color] || colorMap.slate;

  return (
    <div
      className={`w-28 h-36 rounded-lg border-2 ${colorClasses} backdrop-blur-md p-3 cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-lg`}
    >
      <div className="flex flex-col items-center justify-between h-full">
        <Icon className="w-8 h-8 opacity-80" />
        <div className="text-center">
          <h4 className="text-xs font-bold text-[#f5e6d3] truncate w-full">
            {name}
          </h4>
          <span className="text-[10px] opacity-70">{role}</span>
        </div>
        <div className="w-full bg-black/40 rounded-full h-1.5">
          <div
            className="h-full rounded-full bg-current opacity-80"
            style={{ width: `${influence}%` }}
          />
        </div>
        <span className="text-[10px] font-mono">{influence}%</span>
      </div>
    </div>
  );
}
