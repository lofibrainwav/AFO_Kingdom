"use client";

import { useMemo } from "react";
import { useChancellorStore } from "@/state/chancellorStore";
import { usePillarConfig } from "@/hooks/usePillarConfig";

type Node = { name: string; role: string };

export function CouncilOrbits() {
  const score = useChancellorStore((s) => s.trinityScore);
  const active = useChancellorStore((s) => s.activePillar);
  const connected = useChancellorStore((s) => s.connected);

  const { config } = usePillarConfig();
  const nodes = useMemo(() => {
    if (!config?.pillars) return [];
    // Transform API pillars to Council nodes + add Guardians (Julie, Yeongdeok) if not present
    // For now, we just map the pillars directly as they are the core council
    return config.pillars.map((p) => ({
      name: p.role.split(" - ")[0], // Extract Name "제갈량" from "제갈량 - 기술적 확실성"
      role: p.id === "truth" ? "Truth" : p.id === "goodness" ? "Goodness" : p.id === "beauty" ? "Beauty" : "Guardian",
    }));
  }, [config]);

  // Fallback if loading or empty
  const displayNodes = nodes.length > 0 ? nodes : [
    { name: "Zhuge Liang", role: "Truth" },
    { name: "Sima Yi", role: "Goodness" },
    { name: "Zhou Yu", role: "Beauty" },
    { name: "Julie", role: "Guardian" },
    { name: "Yeongdeok", role: "Guardian" },
  ];

  return (
    <div className="relative mx-auto mt-6 h-[320px] w-full max-w-2xl">
      <div className="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/15 bg-white/5 backdrop-blur-xl" />
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
        <div className="text-sm opacity-80">{connected ? "SSE Connected" : "SSE Disconnected"}</div>
        <div className="mt-1 text-2xl font-semibold">{score ?? "—"}</div>
        <div className="mt-1 text-xs opacity-70">{active ?? "active_pillar: —"}</div>
      </div>

      <div className="absolute inset-0 rounded-full border border-white/10" />
      <div className="orbit absolute inset-0">
        {displayNodes.map((n, i) => (
          <div key={n.name} className="node" style={{ ["--i" as any]: i }}>
            <div className="rounded-2xl border border-white/15 bg-white/5 px-3 py-2 backdrop-blur-md">
              <div className="text-sm font-medium">{n.name}</div>
              <div className="text-xs opacity-70">{n.role}</div>
            </div>
          </div>
        ))}
      </div>

      <style jsx>{`
        .orbit {
          position: absolute;
          inset: 0;
          animation: spin 18s linear infinite;
        }
        .node {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: rotate(calc(var(--i) * 72deg)) translateX(140px) rotate(calc(var(--i) * -72deg));
          transform-origin: center;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
