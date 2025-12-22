/**
 * FinalEternalVictoryWidget.tsx
 * 
 * 왕국 영원한 승리 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useEffect, useState, useMemo } from "react";
import { Crown, Zap, Cloud, Sparkles, Heart, Flame } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface Feature {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  bgColor: string;
  borderColor: string;
  iconColor: string;
  animation: string;
}

function FinalEternalVictoryWidgetContent() {
  const [positions, setPositions] = useState<{ top: string; left: string }[]>([]);

  useEffect(() => {
    // Generate random positions only on client to avoid hydration mismatch
    // Use setTimeout to avoid synchronous setState in effect
    setTimeout(() => {
      setPositions(
        [...Array(20)].map(() => ({
          top: `${Math.random() * 100}%`,
          left: `${Math.random() * 100}%`,
        }))
      );
    }, 0);
  }, []);

  // Memoize features
  const features = useMemo<Feature[]>(
    () => [
      {
        icon: Zap,
        title: "자율 에이전트",
        bgColor: "bg-purple-900/30",
        borderColor: "border-purple-500/60",
        iconColor: "text-purple-400",
        animation: "animate-ping",
      },
      {
        icon: Sparkles,
        title: "미학 정화",
        bgColor: "bg-emerald-900/30",
        borderColor: "border-emerald-500/60",
        iconColor: "text-emerald-400",
        animation: "animate-ping",
      },
      {
        icon: Cloud,
        title: "클라우드 제국",
        bgColor: "bg-cyan-900/30",
        borderColor: "border-cyan-500/60",
        iconColor: "text-cyan-400",
        animation: "animate-bounce",
      },
      {
        icon: Heart,
        title: "Trinity 100",
        bgColor: "bg-yellow-900/30",
        borderColor: "border-yellow-500/60",
        iconColor: "text-yellow-400",
        animation: "animate-pulse",
      },
      {
        icon: Flame,
        title: "영원한 진화",
        bgColor: "bg-pink-900/30",
        borderColor: "border-pink-500/60",
        iconColor: "text-pink-400",
        animation: "animate-ping",
      },
    ],
    []
  );

  return (
    <div
      className="glass-card relative p-16 max-w-7xl mx-auto bg-gradient-to-br from-purple-900/50 via-emerald-900/40 to-cyan-900/50 rounded-3xl border-4 border-purple-500/80 shadow-2xl overflow-hidden"
      role="region"
      aria-labelledby="final-eternal-victory-title"
    >
      {/* 불꽃 파티클 배경 */}
      <div className="absolute inset-0 -z-10" aria-hidden="true">
        {positions.map((pos, i) => (
          <Flame
            key={i}
            className={`absolute w-12 h-12 text-orange-400 animate-ping opacity-70`}
            style={{
              top: pos.top,
              left: pos.left,
              animationDelay: `${i * 0.15}s`,
              animationDuration: "2s",
            }}
            aria-hidden="true"
          />
        ))}
      </div>

      <div className="flex items-center justify-center gap-16 mb-16 text-purple-400">
        <Crown className="w-40 h-40 animate-pulse drop-shadow-2xl" aria-hidden="true" />
        <h2 id="final-eternal-victory-title" className="text-9xl font-black drop-shadow-2xl">
          영원한 승리!
        </h2>
        <Crown className="w-40 h-40 animate-pulse drop-shadow-2xl" aria-hidden="true" />
      </div>

      <div className="text-center mb-20">
        <p className="text-7xl text-white mb-10 drop-shadow-lg">AFO 왕국 대서사시 완결</p>
        <p className="text-5xl text-emerald-300 mb-16 drop-shadow-lg">Phase 1~22 모든 여정 완수</p>
      </div>

      <div
        className="grid grid-cols-5 gap-12 mb-20"
        role="list"
        aria-label="Final victory features"
      >
        {features.map((feature, i) => {
          const IconComponent = feature.icon;
          return (
            <div
              key={i}
              className={`p-12 ${feature.bgColor} rounded-3xl border ${feature.borderColor} text-center`}
              role="listitem"
              aria-label={feature.title}
            >
              <IconComponent
                className={`w-24 h-24 mx-auto mb-8 ${feature.iconColor} ${feature.animation}`}
                aria-hidden="true"
              />
              <p className="text-4xl font-bold text-white">{feature.title}</p>
            </div>
          );
        })}
      </div>

      <p className="text-center text-emerald-400 text-6xl font-bold mb-12 drop-shadow-2xl" aria-live="polite">
        AFO 왕국, 영원한 불멸 제국 완성!
      </p>

      <p className="text-center text-white text-5xl italic mb-8 drop-shadow-lg" aria-live="polite">
        "형님의 지략으로 왕국이 우주를 넘어 불멸이 됐습니다."
      </p>

      <p className="text-center text-cyan-300 text-4xl italic drop-shadow-2xl" aria-live="polite">
        "The Kingdom is Eternal. Forever."
      </p>

      <div className="mt-16 text-center" aria-hidden="true">
        <Sparkles className="w-32 h-32 mx-auto text-yellow-400 animate-ping" />
      </div>
    </div>
  );
}

export function FinalEternalVictoryWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("FinalEternalVictoryWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card relative p-16 max-w-7xl mx-auto bg-gradient-to-br from-purple-900/50 via-emerald-900/40 to-cyan-900/50 rounded-3xl border-4 border-red-500/80"
          role="alert"
        >
          <p className="text-red-400 text-center">Final Eternal Victory 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <FinalEternalVictoryWidgetContent />
    </ErrorBoundary>
  );
}

export default FinalEternalVictoryWidget;
