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
