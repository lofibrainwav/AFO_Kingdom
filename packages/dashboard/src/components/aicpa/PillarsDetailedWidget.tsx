import React, { useState, useEffect, useCallback, useMemo } from "react";
import { Shield, Zap, Heart, Clock, Search } from "lucide-react";
import { logError } from "@/lib/logger";

interface PillarDetail {
  name: string;
  key: string;
  score: number;
  weight: string;
  detail: string;
}

interface SSOTData {
  pillars_detailed: PillarDetail[];
  trinity_score: number;
}

const ICONS: Record<string, React.ReactNode> = {
  truth: <Search className="w-6 h-6" />,
  goodness: <Shield className="w-6 h-6" />,
  beauty: <Heart className="w-6 h-6" />,
  serenity: <Zap className="w-6 h-6" />,
  eternity: <Clock className="w-6 h-6" />,
};

export function PillarsDetailedWidget() {
  const [data, setData] = useState<SSOTData | null>(null);
  const [loading, setLoading] = useState(true);

  // Memoize fetch function
  const fetchPillarsData = useCallback(async () => {
    try {
      const res = await fetch("/api/ssot-status");
      if (!res.ok) throw new Error("Failed to fetch pillars data");
      const json = await res.json();
      setData(json);
    } catch (err) {
      logError("Failed to fetch pillars data", {
        error: err instanceof Error ? err.message : "Unknown error",
      });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPillarsData();
  }, [fetchPillarsData]);

  // Memoize pillars list
  const pillarsList = useMemo(() => {
    if (!data?.pillars_detailed) return [];
    return data.pillars_detailed;
  }, [data?.pillars_detailed]);

  if (loading || !data)
    return (
      <div className="glass-card p-8 animate-pulse">
        <div className="h-8 bg-white/10 rounded w-1/3 mb-6 mx-auto"></div>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-32 bg-white/5 rounded-xl"></div>
          ))}
        </div>
      </div>
    );

  return (
    <div className="glass-card p-8 mt-8 border-t border-white/10">
      <h3 className="text-2xl font-bold text-center mb-8 flex items-center justify-center gap-2">
        <span className="text-cyan-400">5 Pillars of AFO</span>
        <span className="px-2 py-0.5 rounded text-xs bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
          Live Metrics
        </span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4" role="list" aria-label="5 Pillars of AFO">
        {pillarsList.map((p) => (
          <div
            key={p.key}
            className="group relative p-5 bg-gradient-to-b from-white/5 to-transparent rounded-2xl border border-white/5 hover:border-cyan-500/30 transition-all hover:bg-white/10"
            role="listitem"
            aria-label={`${p.name}: ${p.score.toFixed(1)} (${p.weight})`}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-3 text-cyan-400 opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-transform origin-left">
              {ICONS[p.key]}
              <span className="text-xs font-mono text-white/30">{p.weight}</span>
            </div>

            {/* Score */}
            <div className="mb-3">
              <p className="text-3xl font-black text-white group-hover:text-cyan-200 transition-colors">
                {p.score.toFixed(1)}
              </p>
              <p className="text-sm font-bold text-white/60">{p.name}</p>
            </div>

            {/* Detail */}
            <div className="pt-3 border-t border-white/5">
              <p className="text-xs text-indigo-200/70 leading-relaxed font-medium">
                {p.detail.split("•").map((line, i) => (
                  <span key={i} className="block mb-1 last:mb-0">
                    • {line.trim()}
                  </span>
                ))}
              </p>
            </div>

            {/* Hover Glow */}
            <div className="absolute inset-0 bg-cyan-500/5 opacity-0 group-hover:opacity-100 rounded-2xl pointer-events-none transition-opacity"></div>
          </div>
        ))}
      </div>

      <div className="mt-8 text-center">
        <p className="text-emerald-400 text-lg font-bold flex items-center justify-center gap-2">
          Status: <span className="text-white">Kingdom Trinity Optimal • Compass True North</span>
        </p>
      </div>
    </div>
  );
}
