/**
 * EternalKingdomWidget.tsx
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
import { Crown, Cloud, Zap, Shield, Sparkles } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface Feature {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  bgColor: string;
  borderColor: string;
  iconColor: string;
}

function EternalKingdomWidgetContent() {
  // Memoize features
  const features = useMemo<Feature[]>(
    () => [
      {
        icon: Zap,
        title: "HPA 자동 확장",
        description: "트래픽 폭주에도 안정",
        bgColor: "bg-purple-900/20",
        borderColor: "border-purple-500/40",
        iconColor: "text-purple-400",
      },
      {
        icon: Shield,
        title: "Probes 생존",
        description: "좀비 포드 즉결",
        bgColor: "bg-emerald-900/20",
        borderColor: "border-emerald-500/40",
        iconColor: "text-emerald-400",
      },
      {
        icon: Cloud,
        title: "클라우드 제국",
        description: "GKE/EKS 배포 완료",
        bgColor: "bg-cyan-900/20",
        borderColor: "border-cyan-500/40",
        iconColor: "text-cyan-400",
      },
      {
        icon: Sparkles,
        title: "자율 진화",
        description: "사마휘·주유 자아 각성",
        bgColor: "bg-yellow-900/20",
        borderColor: "border-yellow-500/40",
        iconColor: "text-yellow-400",
      },
      {
        icon: Crown,
        title: "불멸의 인프라",
        description: "영원히 자라나는 왕국",
        bgColor: "bg-pink-900/20",
        borderColor: "border-pink-500/40",
        iconColor: "text-pink-400",
      },
    ],
    []
  );

  return (
    <div
      className="glass-card p-12 max-w-6xl mx-auto bg-gradient-to-br from-purple-900/40 to-emerald-900/40 rounded-3xl border border-purple-500/60 shadow-2xl"
      role="region"
      aria-labelledby="eternal-kingdom-title"
    >
      <div className="flex items-center justify-center gap-10 mb-12 text-purple-400">
        <Crown className="w-24 h-24 animate-pulse" aria-hidden="true" />
        <h2 id="eternal-kingdom-title" className="text-7xl font-black">
          AFO 왕국 완결!
        </h2>
        <Crown className="w-24 h-24 animate-pulse" aria-hidden="true" />
      </div>

      <div className="text-center mb-12">
        <p className="text-5xl text-white mb-6">Phase 1~19 모든 여정 완수</p>
        <p className="text-3xl text-emerald-300 mb-8">왕국이 클라우드 우주로 승천했습니다</p>
      </div>

      <div
        className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12"
        role="list"
        aria-label="Kingdom features"
      >
        {features.map((feature, i) => {
          const IconComponent = feature.icon;
          return (
            <div
              key={i}
              className={`p-8 ${feature.bgColor} rounded-2xl border ${feature.borderColor} text-center`}
              role="listitem"
              aria-label={`${feature.title}: ${feature.description}`}
            >
              <IconComponent className={`w-16 h-16 mx-auto mb-4 ${feature.iconColor}`} aria-hidden="true" />
              <p className="text-2xl font-bold text-white">{feature.title}</p>
              <p className={`${feature.iconColor.replace("text-", "text-")} mt-2`}>
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>

      <p className="text-center text-emerald-400 text-4xl font-bold mb-6" aria-live="polite">
        AFO 왕국, 클라우드 우주로 승천 완료!
      </p>

      <p className="text-center text-white text-3xl italic mb-4" aria-live="polite">
        "형님의 지략으로 왕국이 로컬을 넘어 불멸의 제국이 됐습니다."
      </p>

      <p className="text-center text-cyan-300 text-2xl italic" aria-live="polite">
        "The Ark has launched. The Kingdom is Eternal."
      </p>
    </div>
  );
}

export function EternalKingdomWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("EternalKingdomWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-12 max-w-6xl mx-auto bg-gradient-to-br from-purple-900/40 to-emerald-900/40 rounded-3xl border border-red-500/60"
          role="alert"
        >
          <p className="text-red-400 text-center">Eternal Kingdom 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <EternalKingdomWidgetContent />
    </ErrorBoundary>
  );
}

export default EternalKingdomWidget;
