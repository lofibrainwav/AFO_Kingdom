"use client";

import { useEffect } from "react";

interface PerformanceMetrics {
  pageLoadTime: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  timeToInteractive: number;
  bundleSize?: number;
}

/**
 * 성능 모니터링 훅
 * 
 * 페이지 로딩 시간, FCP, LCP, TTI 등을 측정합니다.
 */
export function usePerformanceMonitor(
  pageName: string,
  onMetrics?: (metrics: PerformanceMetrics) => void
) {
  useEffect(() => {
    if (typeof window === "undefined") return;

    const startTime = performance.now();

    // Performance Observer 설정
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      
      entries.forEach((entry) => {
        if (entry.entryType === "paint") {
          const paintEntry = entry as PerformancePaintTiming;
          if (paintEntry.name === "first-contentful-paint") {
            console.log(`[Performance] ${pageName} - FCP:`, paintEntry.startTime);
          }
        }
        
        if (entry.entryType === "largest-contentful-paint") {
          const lcpEntry = entry as PerformanceEntry & { renderTime: number };
          console.log(`[Performance] ${pageName} - LCP:`, lcpEntry.renderTime);
        }
      });
    });

    // 관찰 시작
    observer.observe({ entryTypes: ["paint", "largest-contentful-paint"] });

    // 페이지 로드 완료 시 메트릭 수집
    const handleLoad = () => {
      const loadTime = performance.now() - startTime;
      
      // Navigation Timing API
      const navigation = performance.getEntriesByType(
        "navigation"
      )[0] as PerformanceNavigationTiming;
      
      const metrics: PerformanceMetrics = {
        pageLoadTime: loadTime,
        firstContentfulPaint:
          navigation.domContentLoadedEventEnd - navigation.fetchStart,
        largestContentfulPaint: 0, // Performance Observer에서 업데이트
        timeToInteractive:
          navigation.domInteractive - navigation.fetchStart,
      };

      // 리소스 크기 계산
      const resources = performance.getEntriesByType(
        "resource"
      ) as PerformanceResourceTiming[];
      const totalSize = resources.reduce(
        (sum, resource) => sum + (resource.transferSize || 0),
        0
      );
      metrics.bundleSize = totalSize;

      console.log(`[Performance] ${pageName} Metrics:`, metrics);
      
      if (onMetrics) {
        onMetrics(metrics);
      }

      // API로 메트릭 전송 (선택사항)
      if (process.env.NODE_ENV === "production") {
        fetch("/api/performance/metrics", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            page: pageName,
            metrics,
            timestamp: new Date().toISOString(),
          }),
        }).catch((err) => console.error("Failed to send metrics:", err));
      }
    };

    window.addEventListener("load", handleLoad);

    return () => {
      observer.disconnect();
      window.removeEventListener("load", handleLoad);
    };
  }, [pageName, onMetrics]);
}

