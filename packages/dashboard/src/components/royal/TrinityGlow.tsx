"use client";

import { useMemo } from "react";
import { useChancellorStore } from "@/state/chancellorStore";

function glowFor(score: number | null) {
  if (score === null) return { a: 0.18, b: 0.10 };
  if (score >= 95) return { a: 0.28, b: 0.14 };
  if (score >= 90) return { a: 0.22, b: 0.12 };
  return { a: 0.16, b: 0.09 };
}

export function TrinityGlow() {
  const score = useChancellorStore((s) => s.trinityScore);

  const style = useMemo(() => {
    const g = glowFor(score);
    return {
      background:
        "radial-gradient(1200px 700px at 20% 10%, rgba(0,255,180," +
        g.a +
        "), transparent 60%), " +
        "radial-gradient(900px 600px at 80% 20%, rgba(255,215,0," +
        g.b +
        "), transparent 55%), " +
        "radial-gradient(700px 500px at 50% 90%, rgba(120,120,255,0.10), transparent 60%)",
      filter: "blur(0px)",
      animation: "trinityPulse 6s ease-in-out infinite",
    } as const;
  }, [score]);

  return (
    <div className="pointer-events-none absolute inset-0">
      <div className="absolute inset-0 opacity-90" style={style} />
      <style jsx global>{`
        @keyframes trinityPulse {
          0% { opacity: 0.70; transform: scale(1.00); }
          50% { opacity: 1.00; transform: scale(1.02); }
          100% { opacity: 0.70; transform: scale(1.00); }
        }
      `}</style>
    </div>
  );
}
