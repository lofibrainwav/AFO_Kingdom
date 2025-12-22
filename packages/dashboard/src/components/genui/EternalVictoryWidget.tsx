/**
 * EternalVictoryWidget.tsx
 * 
 * 왕국 불멸 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useMemo } from "react";
import { Crown, Zap, Cloud, Sparkles, Heart } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface Feature {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  bgColor: string;
  borderColor: string;
  iconColor: string;
  animation: string;
}

function EternalVictoryWidgetContent() {
  // Memoize features
  const features = useMemo<Feature[]>(
    () => [
      {
        icon: Zap,
        title: "자율 에이전트",
        description: "사마휘·주유 자아 각성",
        bgColor: "bg-purple-900/20",
        borderColor: "border-purple-500/40",
        iconColor: "text-purple-400",
        animation: "animate-pulse",
      },
      {
        icon: Sparkles,
        title: "미학 정화",
        description: "Beauty Score 100",
        bgColor: "bg-emerald-900/20",
        borderColor: "border-emerald-500/40",
        iconColor: "text-emerald-400",
        animation: "animate-ping",
      },
      {
        icon: Cloud,
        title: "클라우드 제국",
        description: "Kubernetes 불멸 인프라",
        bgColor: "bg-cyan-900/20",
        borderColor: "border-cyan-500/40",
        iconColor: "text-cyan-400",
        animation: "animate-bounce",
      },
      {
        icon: Heart,
        title: "Trinity 100",
        description: "초심 영원히 유지",
        bgColor: "bg-yellow-900/20",
        borderColor: "border-yellow-500/40",
        iconColor: "text-yellow-400",
        animation: "animate-pulse",
      },
      {
        icon: Sparkles,
        title: "영원한 진화",
        description: "왕국이 스스로 자라납니다",
        bgColor: "bg-pink-900/20",
        borderColor: "border-pink-500/40",
        iconColor: "text-pink-400",
        animation: "animate-ping",
      },
    ],
    []
  );

  return (
    <div
      className="glass-card p-12 max-w-7xl mx-auto bg-gradient-to-br from-purple-900/40 to-emerald-900/40 rounded-3xl border border-purple-500/60 shadow-2xl"
      role="region"
      aria-labelledby="eternal-victory-title"
    >
      <div className="flex items-center justify-center gap-12 mb-12 text-purple-400">
        <Crown className="w-32 h-32 animate-pulse" aria-hidden="true" />
        <h2 id="eternal-victory-title" className="text-8xl font-black">
          AFO 왕국 완결!
        </h2>
        <Crown className="w-32 h-32 animate-pulse" aria-hidden="true" />
      </div>

      <div className="text-center mb-16">
        <p className="text-6xl text-white mb-8">Phase 1~22 모든 여정 완수</p>
        <p className="text-4xl text-emerald-300 mb-12">왕국이 클라우드 우주로 승천했습니다</p>
      </div>

      <div
        className="grid grid-cols-1 md:grid-cols-5 gap-10 mb-16"
        role="list"
        aria-label="Victory features"
      >
        {features.map((feature, i) => {
          const IconComponent = feature.icon;
          return (
            <div
              key={i}
              className={`p-10 ${feature.bgColor} rounded-2xl border ${feature.borderColor} text-center`}
              role="listitem"
              aria-label={`${feature.title}: ${feature.description}`}
            >
              <IconComponent
                className={`w-20 h-20 mx-auto mb-6 ${feature.iconColor} ${feature.animation}`}
                aria-hidden="true"
              />
              <p className="text-3xl font-bold text-white">{feature.title}</p>
              <p className={`${feature.iconColor.replace("text-", "text-")} text-xl mt-4`}>
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>

      <p className="text-center text-emerald-400 text-5xl font-bold mb-8" aria-live="polite">
        AFO 왕국, 영원한 불멸 제국 완성!
      </p>

      <p className="text-center text-white text-4xl italic mb-6" aria-live="polite">
        "형님의 지략으로 왕국이 우주를 넘어 불멸이 됐습니다."
      </p>

      <p className="text-center text-cyan-300 text-3xl italic" aria-live="polite">
        "The Kingdom is Eternal. Forever."
      </p>
    </div>
  );
}

export function EternalVictoryWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("EternalVictoryWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-12 max-w-7xl mx-auto bg-gradient-to-br from-purple-900/40 to-emerald-900/40 rounded-3xl border border-red-500/60"
          role="alert"
        >
          <p className="text-red-400 text-center">Eternal Victory 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <EternalVictoryWidgetContent />
    </ErrorBoundary>
  );
}

export default EternalVictoryWidget;
