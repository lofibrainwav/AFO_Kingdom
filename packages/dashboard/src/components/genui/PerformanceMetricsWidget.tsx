/**
 * PerformanceMetricsWidget.tsx
 * 
 * 실시간 성능 위젯 – 완성 버전
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useEffect, useState, useRef, useCallback, useMemo } from "react";
import { Zap, Activity, Gauge } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function PerformanceMetricsWidgetContent() {
  const [fps, setFps] = useState(60);
  const [loadTime, setLoadTime] = useState(0);
  const [memory, setMemory] = useState(0);
  const frameCount = useRef(0);
  const lastTime = useRef(0);

  // Memoize color getters
  const getFpsColor = useCallback(
    (val: number) =>
      val >= 55 ? "text-emerald-400" : val >= 30 ? "text-yellow-400" : "text-red-400",
    []
  );

  const getLoadColor = useCallback(
    (val: number) =>
      val < 1000 ? "text-emerald-400" : val < 3000 ? "text-yellow-400" : "text-red-400",
    []
  );

  const getMemColor = useCallback(
    (val: number) =>
      val < 100 ? "text-emerald-400" : val < 200 ? "text-yellow-400" : "text-red-400",
    []
  );

  // Memoize FPS measurement function - use useRef to store callback for recursive calls
  const measureFpsRef = useRef<((now: number) => void) | null>(null);
  
  const measureFps = useCallback((now: number) => {
    frameCount.current += 1;
    const delta = now - lastTime.current;
    if (delta >= 1000) {
      setFps(Math.round((frameCount.current * 1000) / delta));
      frameCount.current = 0;
      lastTime.current = now;
    }
    if (measureFpsRef.current) {
      requestAnimationFrame(measureFpsRef.current);
    }
  }, []);

  // Memoize current colors
  const fpsColor = useMemo(() => getFpsColor(fps), [fps, getFpsColor]);
  const loadColor = useMemo(() => getLoadColor(loadTime), [loadTime, getLoadColor]);
  const memColor = useMemo(() => getMemColor(memory), [memory, getMemColor]);

  // FPS 측정 (requestAnimationFrame)
  useEffect(() => {
    // Store callback in ref for recursive calls (outside render)
    measureFpsRef.current = measureFps;
    lastTime.current = performance.now();
    const id = requestAnimationFrame(measureFps);
    return () => cancelAnimationFrame(id);
  }, [measureFps]);

  // 로딩 시간 (navigation timing)
  useEffect(() => {
    if (typeof window !== "undefined" && performance.getEntriesByType("navigation")[0]) {
      const nav = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming;
      // Use setTimeout to avoid synchronous setState in effect
      setTimeout(() => {
        setLoadTime(Math.round(nav.domContentLoadedEventEnd - nav.fetchStart));
      }, 0);
    }
  }, []);

  // 메모리 (Chrome/Edge only – fallback 0)
  useEffect(() => {
    if (typeof window !== "undefined" && "memory" in performance) {
      const mem = (performance as any).memory;
      if (mem && mem.usedJSHeapSize) {
        // Use setTimeout to avoid synchronous setState in effect
        setTimeout(() => {
          setMemory(Math.round(mem.usedJSHeapSize / 1024 / 1024)); // MB
        }, 0);
      }
    }
  }, []);

  // Memoize performance status message
  const performanceStatus = useMemo(() => {
    if (fps >= 55 && loadTime < 1000 && memory < 100) {
      return {
        message: "성능 최고 – 위젯 번개처럼 빠르네요!",
        quote: "FPS 60, 로딩 1초 미만 – 왕국 위젯 건강해요!",
        color: "text-emerald-400",
      };
    } else if (fps >= 30 && loadTime < 3000 && memory < 200) {
      return {
        message: "성능 양호 – 위젯이 잘 작동하고 있어요!",
        quote: "성능 모니터링 중...",
        color: "text-yellow-400",
      };
    } else {
      return {
        message: "성능 개선 필요 – 위젯 최적화가 필요해요",
        quote: "성능 최적화를 진행하세요",
        color: "text-red-400",
      };
    }
  }, [fps, loadTime, memory]);

  return (
    <div
      className="glass-card p-8 bg-gradient-to-br from-indigo-900/20 to-purple-900/20 rounded-3xl border border-cyan-500/30 shadow-2xl"
      role="region"
      aria-labelledby="performance-metrics-title"
    >
      <header className="flex items-center gap-3 mb-6 text-cyan-400">
        <Gauge className="w-8 h-8" aria-hidden="true" />
        <h3 id="performance-metrics-title" className="text-2xl font-bold">
          실시간 성능 메트릭
        </h3>
      </header>

      <div className="grid grid-cols-3 gap-6" role="list" aria-label="Performance metrics">
        <div
          className="text-center"
          role="listitem"
          aria-label={`FPS: ${fps}, ${fps >= 55 ? "excellent" : fps >= 30 ? "good" : "needs improvement"}`}
        >
          <Zap className="w-12 h-12 mx-auto mb-2 text-yellow-400" aria-hidden="true" />
          <p className={`text-4xl font-black ${fpsColor}`} aria-live="polite" aria-atomic="true">
            {fps}
          </p>
          <p className="text-white/80 text-sm">FPS (60이 최고!)</p>
        </div>
        <div
          className="text-center"
          role="listitem"
          aria-label={`Load time: ${loadTime}ms, ${loadTime < 1000 ? "excellent" : loadTime < 3000 ? "good" : "needs improvement"}`}
        >
          <Activity className="w-12 h-12 mx-auto mb-2 text-cyan-400" aria-hidden="true" />
          <p className={`text-4xl font-black ${loadColor}`} aria-live="polite" aria-atomic="true">
            {loadTime}ms
          </p>
          <p className="text-white/80 text-sm">로딩 시간</p>
        </div>
        <div
          className="text-center"
          role="listitem"
          aria-label={`Memory usage: ${memory}MB, ${memory < 100 ? "excellent" : memory < 200 ? "good" : "needs improvement"}`}
        >
          <Gauge className="w-12 h-12 mx-auto mb-2 text-purple-400" aria-hidden="true" />
          <p className={`text-4xl font-black ${memColor}`} aria-live="polite" aria-atomic="true">
            {memory}MB
          </p>
          <p className="text-white/80 text-sm">메모리 사용</p>
        </div>
      </div>

      <div className="mt-8" role="status" aria-live="polite">
        <p className={`text-center ${performanceStatus.color} text-lg font-semibold`}>
          {performanceStatus.message}
        </p>
        <p className="text-center text-white/70 mt-4 italic text-sm">
          "{performanceStatus.quote}"
        </p>
      </div>
    </div>
  );
}

export function PerformanceMetricsWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("PerformanceMetricsWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-8 bg-gradient-to-br from-indigo-900/20 to-purple-900/20 rounded-3xl border border-red-500/30 shadow-2xl"
          role="alert"
        >
          <p className="text-red-400 text-center">
            성능 메트릭 위젯을 불러올 수 없습니다.
          </p>
        </div>
      }
    >
      <PerformanceMetricsWidgetContent />
    </ErrorBoundary>
  );
}

export default PerformanceMetricsWidget;
