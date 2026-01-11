"use client";

import * as React from "react";

export type PillarScores = {
  truth: number;
  goodness: number;
  beauty: number;
  serenity: number;
  eternity: number;
};

export type KingdomBuilding = {
  id: string;
  name: string;        // 표시명 (한글/한자 느낌)
  subtitle: string;    // 설명(시스템 매핑)
  x: number;           // 0~100 (%)
  y: number;           // 0~100 (%)
  kind:
    | "Royal"
    | "Sanctuary"
    | "Barracks"
    | "Gate"
    | "Observatory"
    | "Warehouse"
    | "Forge";
  scores?: Partial<PillarScores>;
};

type Props = {
  buildings: KingdomBuilding[];
  selectedId?: string | null;
  onSelect?: (id: string) => void;
  className?: string;
};

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}

function scoreLabel(s?: Partial<PillarScores>) {
  if (!s) return null;
  const t = typeof s.truth === "number" ? clamp(s.truth, 0, 100) : null;
  const g = typeof s.goodness === "number" ? clamp(s.goodness, 0, 100) : null;
  const b = typeof s.beauty === "number" ? clamp(s.beauty, 0, 100) : null;
  if (t === null && g === null && b === null) return null;
  return `眞 ${t ?? "-"} · 善 ${g ?? "-"} · 美 ${b ?? "-"}`;
}

function kindBadge(kind: KingdomBuilding["kind"]) {
  const map: Record<KingdomBuilding["kind"], string> = {
    Royal: "ROYAL",
    Sanctuary: "SANCTUARY",
    Barracks: "BARRACKS",
    Gate: "GATE",
    Observatory: "OBSERVATORY",
    Warehouse: "TREASURY",
    Forge: "FORGE",
  };
  return map[kind] ?? "BUILDING";
}

export function KingdomMap({
  buildings,
  selectedId,
  onSelect,
  className,
}: Props) {
  return (
    <section className={className}>
      <div className="relative w-full overflow-hidden rounded-2xl border border-black/10 shadow-sm bg-[#f5eee0]">
        {/* Background: Premium Joseon Map Asset (Explicit Image Tag) */}
        <img
          src="/assets/joseon_map_bg.png"
          alt="Joseon Kingdom Map"
          className="absolute inset-0 w-full h-full object-cover pointer-events-none"
          style={{
            filter: "sepia(0.2) contrast(1.1) brightness(0.95)",
            zIndex: 0,
          }}
        />
        
        {/* Subtle overlay to enhance parchment texture */}
        <div
          className="absolute inset-0 pointer-events-none opacity-40 mix-blend-multiply"
          style={{
            background: `
              radial-gradient(circle at 50% 50%, transparent 60%, rgba(0,0,0,0.1) 100%),
              url('https://www.transparenttextures.com/patterns/parchment.png')
            `,
            zIndex: 1,
          }}
        />

        {/* Frame / HUD Overlay */}
        <div className="relative p-3 sm:p-4 min-h-[500px]">
          <div className="mb-3 flex items-baseline justify-between gap-3 relative z-10 bg-white/50 backdrop-blur-sm p-3 rounded-lg border border-black/5">
            <div>
              <div className="text-xs uppercase tracking-[0.2em] font-bold text-black/50">Palace Command View</div>
              <div className="text-xl font-black bg-gradient-to-br from-slate-900 to-slate-700 bg-clip-text text-transparent">RTK8 · AFO Kingdom Map</div>
            </div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-black/40 hidden sm:block">
              클릭: 건물 선택 · Hover: 실시간 眞善美 스탯
            </div>
          </div>

          {/* Building Canvas */}
          <div className="relative w-full h-full min-h-[400px]">
            {buildings.map((b) => {
              const isSelected = selectedId === b.id;
              return (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => onSelect?.(b.id)}
                  className={[
                    "group absolute -translate-x-1/2 -translate-y-1/2",
                    "rounded-xl border px-3 py-2 text-left shadow-md transition-all duration-300",
                    "focus:outline-none focus:ring-2",
                    isSelected
                      ? "bg-white/95 border-amber-600/50 ring-amber-500/20 scale-110 shadow-amber-900/10 z-30"
                      : "bg-white/80 border-black/10 hover:bg-white/95 hover:border-black/20 z-20",
                  ].join(" ")}
                  style={{
                    left: `${clamp(b.x, 0, 100)}%`,
                    top: `${clamp(b.y, 0, 100)}%`,
                    backdropFilter: "blur(4px)",
                  }}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="text-[9px] font-black tracking-widest text-black/30 uppercase leading-none mb-1">
                        {kindBadge(b.kind)}
                      </div>
                      <div className="text-sm font-bold text-slate-900 leading-tight">{b.name}</div>
                      <div className="text-[10px] font-medium text-slate-500 leading-tight opacity-70">{b.subtitle}</div>
                    </div>

                    <div className="h-8 w-8 rounded-lg border border-black/5 bg-black/5 flex items-center justify-center text-lg shadow-inner">
                        {b.kind === "Royal" && "🏛️"}
                        {b.kind === "Sanctuary" && "📚"}
                        {b.kind === "Barracks" && "⚔️"}
                        {b.kind === "Gate" && "🛡️"}
                        {b.kind === "Observatory" && "🔭"}
                        {b.kind === "Warehouse" && "🧪"}
                        {b.kind === "Forge" && "🔨"}
                    </div>
                  </div>

                  {/* Enhanced Hover Stats */}
                  <div className="pointer-events-none absolute left-1/2 bottom-full z-40 mb-3 w-56 -translate-x-1/2 rounded-xl border border-black/10 bg-white/98 p-3 text-xs shadow-2xl opacity-0 scale-95 transition-all duration-300 group-hover:opacity-100 group-hover:scale-100 backdrop-blur-md">
                    <div className="font-black text-slate-900 border-b border-black/5 pb-1 mb-2 flex justify-between">
                        <span>{b.name}</span>
                        <span className="text-[9px] text-amber-600">LIVE</span>
                    </div>
                    <div className="font-mono text-black/80 font-bold bg-slate-50 p-1.5 rounded-lg border border-black/5">
                        {scoreLabel(b.scores) ?? "Pillar scores: -"} 
                    </div>
                    <div className="mt-2 text-[9px] uppercase tracking-widest font-black text-black/30 text-center">
                      Detailed Metrics in Sidebar
                    </div>
                    <div className="absolute -bottom-1 left-1/2 w-2 h-2 bg-white border-b border-r border-black/10 -translate-x-1/2 rotate-45" />
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}

export default KingdomMap;
