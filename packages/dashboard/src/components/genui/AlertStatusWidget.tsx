/**
 * AlertStatusWidget.tsx
 * 
 * Alertmanager 상태 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useMemo } from "react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function AlertStatusWidgetContent() {
  // Memoize alert data
  const alertData = useMemo(
    () => ({
      activeAlerts: 0,
      status: "모든 시스템 정상 – 왕국 안전!",
      sampleAlerts: [
        "High CPU Usage (Critical)",
        "OOM Risk (Warning)",
        "API Latency (Warning)",
        "Risk Score High (Warning)",
      ],
      quote: "문제 생기면 Slack/PagerDuty로 즉시 알림 – 형님 평온 지킴!",
    }),
    []
  );

  return (
    <div
      className="glass-card p-8 bg-gradient-to-br from-red-900/30 to-orange-900/30 rounded-3xl border border-red-500/30"
      role="region"
      aria-labelledby="alert-status-title"
    >
      <h3 id="alert-status-title" className="text-2xl font-bold text-red-400 mb-6">
        Alertmanager 상태
      </h3>
      <div className="flex items-center gap-4 mb-4" role="status" aria-live="polite">
        <div
          className="w-4 h-4 rounded-full bg-emerald-500 animate-pulse"
          aria-hidden="true"
        ></div>
        <p className="text-emerald-400 text-xl">
          현재 활성 알림: {alertData.activeAlerts}
        </p>
      </div>
      <p className="text-white/90 mb-6" aria-live="polite">
        {alertData.status}
      </p>
      <div
        className="space-y-2 text-sm text-white/60 bg-black/20 p-4 rounded-xl"
        role="list"
        aria-label="Sample alerts"
      >
        {alertData.sampleAlerts.map((alert, i) => (
          <p key={i} role="listitem">
            • {alert}
          </p>
        ))}
      </div>
      <p className="text-white/70 mt-6 italic text-center text-sm" aria-live="polite">
        "{alertData.quote}"
      </p>
    </div>
  );
}

export function AlertStatusWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("AlertStatusWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-8 bg-gradient-to-br from-red-900/30 to-orange-900/30 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">Alert Status 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <AlertStatusWidgetContent />
    </ErrorBoundary>
  );
}

export default AlertStatusWidget;
