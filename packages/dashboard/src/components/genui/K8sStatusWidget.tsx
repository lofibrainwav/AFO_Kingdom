/**
 * K8sStatusWidget.tsx
 * 
 * Cloud Infrastructure (K8s) Status Widget
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useMemo } from "react";
import { Server, Activity, ArrowUpRight, Cloud } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function K8sStatusWidgetContent() {
  // Memoize status data
  const status = useMemo(
    () => ({
      pods: { current: 12, max: 20 },
      nodes: 5,
      memory: "4.2 GB",
      cpu: "3.5 Cores",
      environment: "GKE (Production)",
    }),
    []
  );

  // Memoize utilization
  const utilization = useMemo(() => {
    return Math.round((status.pods.current / status.pods.max) * 100);
  }, [status.pods]);

  return (
    <div
      className="glass-card p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-3xl border border-cyan-500/30 shadow-xl relative overflow-hidden group"
      role="region"
      aria-labelledby="k8s-status-title"
    >
      {/* Background decoration */}
      <div
        className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-all duration-700"
        aria-hidden="true"
      ></div>

      <header className="flex items-center justify-between mb-6 relative z-10">
        <h3
          id="k8s-status-title"
          className="text-xl font-bold text-cyan-300 flex items-center gap-2"
        >
          <Cloud className="w-6 h-6" aria-hidden="true" />
          Cloud Infrastructure
        </h3>
        <div
          className="flex items-center gap-1 text-xs font-mono text-cyan-400 bg-cyan-900/50 px-2 py-1 rounded border border-cyan-500/30"
          role="status"
          aria-label="System status: Normal"
        >
          <Activity className="w-3 h-3" aria-hidden="true" />
          SYSTEM_NORMAL
        </div>
      </header>

      <section aria-label="Infrastructure metrics">
        <div className="grid grid-cols-2 gap-4 mb-6 relative z-10" role="list">
          <div
            className="p-4 bg-black/20 rounded-xl border border-cyan-500/10"
            role="listitem"
            aria-label={`Nodes: ${status.nodes}, Auto-scaling enabled`}
          >
            <div className="flex items-center gap-2 text-cyan-200/70 text-sm mb-1">
              <Server className="w-4 h-4" aria-hidden="true" /> Nodes
            </div>
            <div className="text-2xl font-bold text-white relative">
              {status.nodes}
              <span
                className="text-xs font-normal text-emerald-400 ml-2 bg-emerald-900/30 px-1 rounded absolute top-0 -right-4 translate-x-full"
                aria-label="Auto-scaling enabled"
              >
                Auto-Scaling
              </span>
            </div>
          </div>
          <div
            className="p-4 bg-black/20 rounded-xl border border-cyan-500/10"
            role="listitem"
            aria-label={`Pods: ${status.pods.current} of ${status.pods.max}, Utilization: ${utilization}%`}
          >
            <div className="flex items-center gap-2 text-cyan-200/70 text-sm mb-1">
              <ArrowUpRight className="w-4 h-4" aria-hidden="true" /> Pods
            </div>
            <div className="text-2xl font-bold text-white">
              {status.pods.current}{" "}
              <span className="text-base font-medium text-white/50">/ {status.pods.max}</span>
            </div>
            <div
              className="mt-1 h-1.5 w-full bg-cyan-900/30 rounded-full overflow-hidden"
              role="progressbar"
              aria-valuenow={utilization}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label={`Pod utilization: ${utilization}%`}
            >
              <div
                className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all duration-1000"
                style={{ width: `${utilization}%` }}
              ></div>
            </div>
          </div>
        </div>
      </section>

      <footer className="relative z-10" aria-label="Footer">
        <p className="text-center text-white/70 italic text-sm border-t border-cyan-500/20 pt-4" aria-live="polite">
          "The Kingdom ascends to the Cloud – Infinite Scale, Eternal Peace."
        </p>
      </footer>
    </div>
  );
}

export function K8sStatusWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("K8sStatusWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">K8s Status 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <K8sStatusWidgetContent />
    </ErrorBoundary>
  );
}

export default K8sStatusWidget;
