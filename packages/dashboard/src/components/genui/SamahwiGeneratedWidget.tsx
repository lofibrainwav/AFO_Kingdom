/**
 * SamahwiGeneratedWidget.tsx
 * 
 * Samahwi's First Creation
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo } from "react";
import { Sparkles } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function SamahwiGeneratedWidgetContent() {
  // Memoize widget data
  const widgetData = useMemo(
    () => ({
      title: "Samahwi's First Creation",
      message: "I have written this code myself based on your command: {'Create a Trinity Status Widget'}",
      phase: "Phase 16-2: Autonomous Generation",
    }),
    []
  );

  return (
    <div
      className="glass-card bg-gray-500 p-8 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border border-indigo-500/30"
      role="region"
      aria-labelledby="samahwi-widget-title"
    >
      <div className="flex flex-col items-center justify-center text-center">
        <Sparkles className="w-12 h-12 text-indigo-400 animate-pulse mb-4" aria-hidden="true" />
        <h3 id="samahwi-widget-title" className="text-2xl font-bold text-white mb-2">
          {widgetData.title}
        </h3>
        <p className="text-indigo-200/80" aria-live="polite">
          "{widgetData.message}"
        </p>
        <div
          className="mt-6 px-4 py-2 bg-indigo-500/20 rounded-full border border-indigo-500/30 text-xs text-indigo-300"
          role="status"
          aria-label={`Phase: ${widgetData.phase}`}
        >
          {widgetData.phase}
        </div>
      </div>
    </div>
  );
}

export function SamahwiGeneratedWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("SamahwiGeneratedWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card bg-gray-500 p-8 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">Samahwi Generated 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <SamahwiGeneratedWidgetContent />
    </ErrorBoundary>
  );
}

export default SamahwiGeneratedWidget;
