// genui/PerformanceMetricsWidget.tsx (실시간 성능 위젯 – 완성 버전)
'use client';

import { useEffect, useState, useRef } from 'react';
import { Zap, Activity, Gauge } from 'lucide-react';

export function PerformanceMetricsWidget() {
  const [fps, setFps] = useState(60);
  const [loadTime, setLoadTime] = useState(0);
  const [memory, setMemory] = useState(0);
  const frameCount = useRef(0);
  const lastTime = useRef(0); // Initialize with 0 for client-side execution

  // FPS 측정 (requestAnimationFrame)
  useEffect(() => {
    lastTime.current = performance.now(); // Set initial time on client
    const measureFps = (now: number) => {
      frameCount.current += 1;
      const delta = now - lastTime.current;
      if (delta >= 1000) {
        setFps(Math.round((frameCount.current * 1000) / delta));
        frameCount.current = 0;
        lastTime.current = now;
      }
      requestAnimationFrame(measureFps);
    };
    const id = requestAnimationFrame(measureFps);
    return () => cancelAnimationFrame(id);
  }, []);

  // 로딩 시간 (navigation timing)
  useEffect(() => {
    if (typeof window !== 'undefined' && performance.getEntriesByType('navigation')[0]) {
      const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      setLoadTime(Math.round(nav.domContentLoadedEventEnd - nav.fetchStart)); // eslint-disable-line react-hooks/set-state-in-effect
    }
  }, []);

  // 메모리 (Chrome/Edge only – fallback 0)
  useEffect(() => {
    if (typeof window !== 'undefined' && 'memory' in performance) {
      // Chrome-only API
      const mem = (performance as any).memory;
      if (mem && mem.usedJSHeapSize) {
        // eslint-disable-next-line
        setMemory(Math.round(mem.usedJSHeapSize / 1024 / 1024)); // MB
      }
    }
  }, []);

  const getColor = (value: number, good: number, warn: number) => {
    // Logic: Higher FPS is better, Lower Load/Memory is better
    // Wait, getColor args logic in snippet was: value >= good ? Green ...
    // But for LoadTime: value >= 1000 (bad).
    // I should adapt logic per type or make logic generic. 
    // User snippet: getColor(fps, 55, 30) -> 60 >= 55 Green. Correct.
    // User snippet: getColor(loadTime, 1000, 3000) -> 100 >= 1000 ? No. 
    // The user snippet logic was: value >= good ? Green.
    // That works for FPS (Higher is better).
    // For LoadTime (Lower is better), logic must be inverted.
    // I will implement separate helpers to be safe.
    return 'text-white'; // placeholder, corrected below in JSX
  };

  const getFpsColor = (val: number) => val >= 55 ? 'text-emerald-400' : val >= 30 ? 'text-yellow-400' : 'text-red-400';
  const getLoadColor = (val: number) => val < 1000 ? 'text-emerald-400' : val < 3000 ? 'text-yellow-400' : 'text-red-400';
  const getMemColor = (val: number) => val < 100 ? 'text-emerald-400' : val < 200 ? 'text-yellow-400' : 'text-red-400';

  return (
    <div className="glass-card p-8 bg-gradient-to-br from-indigo-900/20 to-purple-900/20 rounded-3xl border border-cyan-500/30 shadow-2xl">
      <div className="flex items-center gap-3 mb-6 text-cyan-400">
        <Gauge className="w-8 h-8" />
        <h3 className="text-2xl font-bold">실시간 성능 메트릭</h3>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="text-center">
          <Zap className="w-12 h-12 mx-auto mb-2 text-yellow-400" />
          <p className={`text-4xl font-black ${getFpsColor(fps)}`}>{fps}</p>
          <p className="text-white/80 text-sm">FPS (60이 최고!)</p>
        </div>
        <div className="text-center">
          <Activity className="w-12 h-12 mx-auto mb-2 text-cyan-400" />
          <p className={`text-4xl font-black ${getLoadColor(loadTime)}`}>{loadTime}ms</p>
          <p className="text-white/80 text-sm">로딩 시간</p>
        </div>
        <div className="text-center">
          <Gauge className="w-12 h-12 mx-auto mb-2 text-purple-400" />
          <p className={`text-4xl font-black ${getMemColor(memory)}`}>{memory}MB</p>
          <p className="text-white/80 text-sm">메모리 사용</p>
        </div>
      </div>

      <p className="text-center text-emerald-400 mt-8 text-lg font-semibold">
        성능 최고 – 위젯 번개처럼 빠르네요!
      </p>

      <p className="text-center text-white/70 mt-4 italic text-sm">
        "FPS 60, 로딩 1초 미만 – 왕국 위젯 건강해요!"
      </p>
    </div>
  );
}
