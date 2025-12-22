/**
 * PrometheusWidget.tsx
 * 
 * Prometheus 모니터링 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useMemo } from "react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function PrometheusWidgetContent() {
  // Memoize placeholder message
  const placeholderMessage = useMemo(
    () => ({
      title: "📊 Grafana Dashboard Loading...",
      subtitle: "Connecting to Prometheus Datasource...",
      quote: "Prometheus가 왕국 모든 맥박 실시간 모니터링 – 문제 생기기 전에 알림 와요!",
    }),
    []
  );

  return (
    <div
      className="glass-card p-8 bg-gradient-to-br from-gray-900/50 to-slate-900/50 rounded-3xl border border-gray-500/30"
      role="region"
      aria-labelledby="prometheus-title"
    >
      <h3 id="prometheus-title" className="text-2xl font-bold text-orange-400 mb-6">
        왕국 관측소 (Prometheus)
      </h3>
      <div
        className="bg-black/40 rounded-xl p-4 min-h-[400px] flex items-center justify-center border border-white/10"
        role="status"
        aria-live="polite"
        aria-label="Prometheus monitoring dashboard"
      >
        {/* Placeholder for Grafana Iframe or Chart.js */}
        <div className="text-center">
          <p className="text-2xl text-white/50 mb-2">{placeholderMessage.title}</p>
          <p className="text-sm text-white/30">{placeholderMessage.subtitle}</p>
        </div>
      </div>
      <p className="text-white/90 mt-6 italic text-center" aria-live="polite">
        "{placeholderMessage.quote}"
      </p>
    </div>
  );
}

export function PrometheusWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("PrometheusWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-8 bg-gradient-to-br from-gray-900/50 to-slate-900/50 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">Prometheus 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <PrometheusWidgetContent />
    </ErrorBoundary>
  );
}

export default PrometheusWidget;
