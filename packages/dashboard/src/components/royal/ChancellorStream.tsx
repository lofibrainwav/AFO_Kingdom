"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect, useRef, useCallback, useMemo } from "react";

// Mock log generator if SSE is silent
const _MOCK_LOGS = [
  "[System] Trinity Core initialized...",
  "[Chancellor] Monitoring 11-Organs...",
  "[Zhuge Liang] Architecture analysis: 100% (Truth)",
  "[Sima Yi] Risk Assessment: 0% (Goodness)",
  "[Zhou Yu] UI Rendering: 60fps (Beauty)",
  "[System] Heartbeat: 60bpm - Stable",
  "[Chancellor] Awaiting Commander's Input...",
  "[GenUI] Project Genesis: Active",
  "[Network] Graph Protocol: Synced",
];

export default function ChancellorStream() {
  const [logs, setLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";

  // Memoize log update handler
  const handleLogMessage = useCallback((event: MessageEvent) => {
    if (!event.data) return;
    setLogs((prev) => {
      // Keep last 50 logs to prevent memory overflow
      const newLogs = [...prev, event.data];
      if (newLogs.length > 50) return newLogs.slice(newLogs.length - 50);
      return newLogs;
    });
  }, []);

  // Memoize error handler
  const handleError = useCallback((err: Event) => {
    console.error("EventSource failed:", err);
  }, []);

  useEffect(() => {
    // SSE Connection to Backend Log Stream
    const eventSource = new EventSource(`${API_BASE}/api/system/logs/stream`);

    eventSource.onmessage = handleLogMessage;
    eventSource.onerror = handleError;

    return () => {
      eventSource.close();
    };
  }, [API_BASE, handleLogMessage, handleError]);

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  // Memoize animation config
  const animationConfig = useMemo(
    () => ({
      rotateX: [0, 2, 0],
      rotateY: [0, 2, -2, 0],
    }),
    []
  );

  const transitionConfig = useMemo(
    () => ({
      duration: 20,
      repeat: Infinity,
      ease: "easeInOut" as const,
    }),
    []
  );

  return (
    <motion.div
      className="neu-card h-96 relative overflow-hidden flex flex-col"
      animate={animationConfig}
      transition={transitionConfig}
      style={{ perspective: 1000 }}
      role="region"
      aria-label="Chancellor neural stream"
    >
      <div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-slate-200/90 to-transparent z-10 p-4 border-b border-white/20 backdrop-blur-sm flex justify-between items-center">
        <h3 className="text-slate-600 font-bold text-sm tracking-wider flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          CHANCELLOR NEURAL STREAM
        </h3>
        <span className="text-[10px] text-slate-400 font-mono">LIVE FEED</span>
      </div>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 pt-16 font-mono text-xs text-slate-600 space-y-2 scrollbar-hide"
        role="log"
        aria-live="polite"
        aria-label="System logs"
      >
        <AnimatePresence>
          {logs.map((log, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }}
              className="border-l-2 border-slate-300 pl-3 py-1 hover:bg-white/30 rounded transition-colors"
              role="listitem"
              aria-label={`Log ${i + 1}: ${log}`}
            >
              <span className="text-slate-400 mr-2">[{new Date().toLocaleTimeString()}]</span>
              {log}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Footer / Input Placeholder for Human-in-the-loop */}
      <div className="p-3 bg-white/30 border-t border-white/40">
        <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-indigo-500"
            animate={{ width: ["0%", "100%"] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
        </div>
        <p className="text-[10px] text-center text-slate-400 mt-1">PROCESSING THOUGHT GRAPH...</p>
      </div>
    </motion.div>
  );
}
