"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { Wifi, WifiOff, RefreshCw } from "lucide-react";
import { createEventSource } from "@/lib/sse";

// Connection status type
type ConnectionStatus = "connected" | "reconnecting" | "offline";

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
  const [status, setStatus] = useState<ConnectionStatus>("offline");
  const [lastMessageAt, setLastMessageAt] = useState<Date | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);
  const retryCountRef = useRef(0);
  const retryTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Calculate backoff delay (1s -> 2s -> 4s -> 8s -> max 10s)
  const getBackoffDelay = useCallback(() => {
    const delay = Math.min(1000 * Math.pow(2, retryCountRef.current), 10000);
    return delay;
  }, []);

  // Connect to SSE
  const connect = useCallback(() => {
    // React StrictMode guard: prevent duplicate connections in dev
    if (eventSourceRef.current) {
      console.log("[SSE] Connection already exists, skipping duplicate");
      return;
    }

    // Cleanup previous connection (safety check)
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    setStatus("reconnecting");
    const eventSource = createEventSource("/api/logs/stream");
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setStatus("connected");
      retryCountRef.current = 0; // Reset retry count on successful connection
    };

    eventSource.onmessage = (event) => {
      if (!event.data) return;
      setLastMessageAt(new Date());
      setLogs((prev) => {
        const newLogs = [...prev, event.data];
        if (newLogs.length > 50) return newLogs.slice(newLogs.length - 50);
        return newLogs;
      });
    };

    eventSource.onerror = () => {
      eventSource.close();
      eventSourceRef.current = null; // Clear ref for reconnection
      setStatus("offline");

      // Retry with exponential backoff
      const delay = getBackoffDelay();
      retryCountRef.current += 1;

      console.log(`[SSE] Reconnecting in ${delay}ms (attempt ${retryCountRef.current})`);
      retryTimeoutRef.current = setTimeout(connect, delay);
    };
  }, [getBackoffDelay]);

  useEffect(() => {
    connect();

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null; // Clear ref on cleanup
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
      }
    };
  }, [connect]);

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

  // Status badge component
  const StatusBadge = () => {
    const config = {
      connected: { icon: Wifi, color: "bg-emerald-500", text: "Connected" },
      reconnecting: { icon: RefreshCw, color: "bg-amber-500", text: "Reconnecting" },
      offline: { icon: WifiOff, color: "bg-red-500", text: "Offline" },
    }[status];

    const Icon = config.icon;

    return (
      <div className="flex items-center gap-1.5">
        <span className={`w-2 h-2 rounded-full ${config.color} ${status === "reconnecting" ? "animate-pulse" : ""}`} />
        <Icon className={`w-3 h-3 text-slate-500 ${status === "reconnecting" ? "animate-spin" : ""}`} />
        <span className="text-[10px] text-slate-400 font-mono">{config.text}</span>
      </div>
    );
  };

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
          <span className={`w-2 h-2 rounded-full ${status === "connected" ? "bg-emerald-500 animate-pulse" : "bg-slate-400"}`} />
          CHANCELLOR NEURAL STREAM
        </h3>
        <StatusBadge />
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

      {/* Footer with last message time */}
      <div className="p-3 bg-white/30 border-t border-white/40">
        <div className="flex justify-between items-center mb-1">
          <p className="text-[10px] text-slate-400">
            {lastMessageAt
              ? `Last message: ${lastMessageAt.toLocaleTimeString()}`
              : "Awaiting messages..."}
          </p>
          <p className="text-[10px] text-slate-400">{logs.length} logs</p>
        </div>
        <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
          <motion.div
            className={`h-full ${status === "connected" ? "bg-indigo-500" : "bg-slate-400"}`}
            animate={{ width: status === "connected" ? ["0%", "100%"] : "0%" }}
            transition={{ duration: 1.5, repeat: status === "connected" ? Infinity : 0 }}
          />
        </div>
      </div>
    </motion.div>
  );
}