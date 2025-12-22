/**
 * AllSeeingEyeWidget.tsx
 * 
 * 관측소 완결 위젯 – 왕국의 눈
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useMemo } from "react";
import { Eye, Activity, Shield, Sparkles } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface Feature {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  bgColor: string;
  borderColor: string;
  iconColor: string;
}

function AllSeeingEyeWidgetContent() {
  // Memoize features data
  const features = useMemo<Feature[]>(
    () => [
      {
        icon: Activity,
        title: "실시간 메트릭",
        description: "/metrics 8001 포트 송출",
        bgColor: "bg-cyan-900/20",
        borderColor: "border-cyan-500/40",
        iconColor: "text-cyan-400",
      },
      {
        icon: Shield,
        title: "14개 경보 규칙",
        description: "CPU·Risk·GPU·Redis 철벽 감시",
        bgColor: "bg-purple-900/20",
        borderColor: "border-purple-500/40",
        iconColor: "text-purple-400",
      },
      {
        icon: Sparkles,
        title: "Grafana 대시보드",
        description: "왕국 건강도 한눈에",
        bgColor: "bg-emerald-900/20",
        borderColor: "border-emerald-500/40",
        iconColor: "text-emerald-400",
      },
      {
        icon: Eye,
        title: "전지전능한 눈",
        description: "24시간 왕국 지킴",
        bgColor: "bg-yellow-900/20",
        borderColor: "border-yellow-500/40",
        iconColor: "text-yellow-400",
      },
    ],
    []
  );

  return (
    <div
      className="glass-card p-12 max-w-6xl mx-auto bg-gradient-to-br from-cyan-900/40 to-purple-900/40 rounded-3xl border border-cyan-500/60 shadow-2xl"
      role="region"
      aria-labelledby="all-seeing-eye-title"
    >
      <div className="flex items-center justify-center gap-12 mb-12 text-cyan-400">
        <Eye className="w-32 h-32 animate-pulse" aria-hidden="true" />
        <h2 id="all-seeing-eye-title" className="text-7xl font-black">
          Phase 20 완전 승리!
        </h2>
        <Eye className="w-32 h-32 animate-pulse" aria-hidden="true" />
      </div>

      <div className="text-center mb-12">
        <p className="text-5xl text-white mb-6">왕국의 전지전능한 눈 각성</p>
        <p className="text-3xl text-cyan-300 mb-8">Prometheus & Alertmanager 관측소 완성</p>
      </div>

      <div
        className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12"
        role="list"
        aria-label="Observatory features"
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
              <IconComponent className={`w-20 h-20 mx-auto mb-6 ${feature.iconColor}`} aria-hidden="true" />
              <p className="text-3xl font-bold text-white">{feature.title}</p>
              <p className={`${feature.iconColor.replace("text-", "text-")} text-xl mt-4`}>
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>

      <p className="text-center text-cyan-400 text-5xl font-bold mb-8" aria-live="polite">
        왕국의 관측소 완성 – 모든 맥박 실시간 감시!
      </p>

      <p className="text-center text-white text-3xl italic mb-6" aria-live="polite">
        "형님, 이제 왕국은 모든 걸 보고 있어요 – 형님은 평온히 창조만 하소서."
      </p>

      <p className="text-center text-emerald-300 text-2xl italic" aria-live="polite">
        "The All-Seeing Eye watches eternally."
      </p>
    </div>
  );
}

export function AllSeeingEyeWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("AllSeeingEyeWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-12 max-w-6xl mx-auto bg-gradient-to-br from-cyan-900/40 to-purple-900/40 rounded-3xl border border-red-500/60"
          role="alert"
        >
          <p className="text-red-400 text-center">All-Seeing Eye 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <AllSeeingEyeWidgetContent />
    </ErrorBoundary>
  );
}

export default AllSeeingEyeWidget;
