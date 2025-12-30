"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
    AlertTriangle,
    CheckCircle2,
    Clock,
    Cpu,
    Heart,
    Shield,
    Terminal,
    TrendingUp,
    Zap
} from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { ROYAL_CONSTANTS } from "../../config/royal_constants";
import { createEventSource } from "@/lib/sse";

interface RoyalOpsCenterProps {
  trinityScore: number;
  healthData?: any;
}

/**
 * Royal Ops Center (Genesis v1.1 - Optimized)
 * The central command interface for the AFO Kingdom.
 * Integrates Kingdom Health, Chancellor Stream, and Grok Insights with high-fidelity motion.
 */
export default function RoyalOpsCenter({ trinityScore, healthData }: RoyalOpsCenterProps) {
  // API_BASE is not used in SSE connection (proxy is used), but kept for future API calls
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || ROYAL_CONSTANTS.LINKS.API_DEFAULT;

  const [logs, setLogs] = useState<string[]>([]);
  const [currentTime, setCurrentTime] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  
  // API_BASE is not used in SSE connection (proxy is used), but kept for future API calls

  // Real-time Clock
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // SSE Log Stream Integration
  const handleLogMessage = useCallback((event: MessageEvent) => {
    if (!event.data) return;
    try {
        const data = JSON.parse(event.data);
        const logMsg = data.message || event.data;
        
        setLogs((prev) => {
          const newLogs = [...prev, logMsg];
          if (newLogs.length > 50) return newLogs.slice(newLogs.length - 50);
          return newLogs;
        });
    } catch (e) {
        // Fallback for non-json logs
        setLogs((prev) => {
          const newLogs = [...prev, event.data];
          if (newLogs.length > 50) return newLogs.slice(newLogs.length - 50);
          return newLogs;
        });
    }
  }, []);

  useEffect(() => {
    // SSOT: Use Next.js proxy for SSE to avoid CORS issues
    // Canonical path: /api/logs/stream (AGENTS.md SSOT)
    console.log("[Chancellor Stream] Connecting to Chancellor Stream via SSOT proxy");

    const eventSource = createEventSource("/api/logs/stream");

    eventSource.onopen = () => {
      console.log("[Chancellor Stream] Chancellor Stream Connected");
      setLogs(prev => [...prev, "🏰 [Chancellor] Stream Connected - Real-time Thoughts Active"]);
    };

    eventSource.onmessage = (event) => {
      handleLogMessage(event);
    };

    eventSource.onerror = (err) => {
      // Don't log full error object to avoid "{}" in console
      console.error("[Chancellor Stream] Connection error. Reconnecting...");
      setLogs(prev => [...prev, "⚠️ [Chancellor] Connection Lost - Attempting Reconnect"]);
    };

    // Send initial connection test
    setTimeout(() => {
      console.log("[Chancellor Stream] Chancellor Stream initialized");
      setLogs(prev => [...prev, "🔄 [Chancellor] Real-time Thought Stream Active"]);
    }, 1000);

    return () => {
      console.log("[Chancellor Stream] Closing Chancellor Stream connection");
      eventSource.close();
    };
  }, [handleLogMessage]);

  const handleHeal = async () => {
    try {
        setLogs(prev => [...prev, "[COMMAND] Initiating Heal Protocol..."]);
        const res = await fetch(`${API_BASE}/api/system/heal`, { method: "POST" });
        const data = await res.json();
        
        if (res.ok) {
             setLogs(prev => [...prev, `[SYSTEM] ${data.message}`]);
        } else {
             setLogs(prev => [...prev, `[ERROR] ${data.detail || "Heal failed"}`]);
        }
    } catch (e) {
        setLogs(prev => [...prev, `[CRITICAL] Heal request failed: ${e}`]);
    }
  };

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  // Helper to determine Pillar status color
  const getPillarColor = (score: number) => {
    if (score >= 90) return "bg-emerald-500";
    if (score >= 80) return "bg-blue-500";
    if (score >= 70) return "bg-amber-500";
    return "bg-red-500";
  };

  // Safe Trinity Breakdown Access
  const breakdown = healthData?.trinity_breakdown || {};
  const pillars = [
    { name: "眞 Truth", status: (breakdown.truth || 0) * 100, color: "bg-blue-500" },
    { name: "善 Goodness", status: (breakdown.goodness || 0) * 100, color: "bg-emerald-500" },
    { name: "美 Beauty", status: (breakdown.beauty || 0) * 100, color: "bg-purple-500" },
    { name: "孝 Serenity", status: (breakdown.filial_serenity || 0) * 100, color: "bg-indigo-500" },
    { name: "永 Eternity", status: (breakdown.eternity || 0) * 100, color: "bg-amber-500" },
  ];

  // Docker / System Status Check
  const postgresStatus = healthData?.organs?.["肝_PostgreSQL"]?.status === "healthy";
  const redisStatus = healthData?.organs?.["心_Redis"]?.status === "healthy";
  const systemOptimal = postgresStatus && redisStatus;

  // Animation Variants
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="w-full bg-black/40 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 flex flex-col gap-6 text-white shadow-2xl relative overflow-hidden"
    >
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/10 rounded-full blur-[80px] pointer-events-none" />

      {/* Header */}
      <motion.div variants={itemVariants} className="flex items-center justify-between border-b border-white/10 pb-4 relative z-10">
        <div className="flex items-center gap-4">
            <div className="p-2.5 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-xl border border-white/10 shadow-inner">
                <Cpu className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                    Royal Ops Center
                </h1>
                <p className="text-[10px] text-white/40 font-mono tracking-[0.2em] uppercase">AFO Kingdom • Genesis Node</p>
            </div>
        </div>
        <div className="flex items-center gap-6 text-sm font-mono text-white/50">
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border ${systemOptimal ? 'border-emerald-500/30' : 'border-amber-500/30'}`}>
                <div className={`w-2 h-2 rounded-full ${systemOptimal ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 'bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]'} animate-pulse`} />
                <span className={systemOptimal ? "text-emerald-400/80" : "text-amber-400/80"}>
                  {systemOptimal ? "SYSTEM OPTIMAL" : "SYSTEM DEGRADED"}
                </span>
            </div>
            <div className="flex items-center gap-2">
                 <Clock className="w-4 h-4" />
                 <span>{currentTime}</span>
            </div>
        </div>
      </motion.div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10">
        
        {/* Left: Kingdom HUD */}
        <div className="lg:col-span-3 flex flex-col gap-4">
            
            {/* Trinity Score Card */}
            <motion.div variants={itemVariants} className="flex-1 bg-gradient-to-br from-white/10 to-transparent rounded-2xl p-5 border border-white/10 flex flex-col justify-center items-center relative overflow-hidden hover:border-indigo-500/30 transition-colors group">
                <div className="absolute inset-0 bg-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                
                <h3 className="text-xs text-indigo-200/50 mb-3 font-medium uppercase tracking-wider">Trinity Score</h3>
                <div className="relative">
                    <svg className="w-32 h-32 transform -rotate-90">
                        <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="6" fill="transparent" className="text-white/5" />
                        <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="6" fill="transparent" className="text-indigo-500" strokeDasharray={377} strokeDashoffset={377 - (377 * trinityScore) / 100} strokeLinecap="round" />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-bold text-white tracking-tighter">{trinityScore}</span>
                        <span className="text-[10px] text-white/40">%</span>
                    </div>
                </div>
                
                <div className="mt-4 flex items-center gap-2 text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-full border border-emerald-500/20">
                    <TrendingUp className="w-3 h-3" />
                    Target: 99.0%
                </div>
            </motion.div>

            {/* Pillars Status */}
            <motion.div variants={itemVariants} className="bg-white/5 rounded-2xl p-5 border border-white/10 backdrop-blur-sm">
                <h3 className="text-[10px] text-white/40 mb-4 font-bold uppercase tracking-widest flex items-center gap-2">
                    <Shield className="w-3 h-3" />
                    Pillar Harmony
                </h3>
                <div className="space-y-3">
                    {pillars.map(pillar => (
                        <div key={pillar.name} className="group">
                            <div className="flex items-center justify-between text-xs mb-1">
                                <span className="text-white/70 group-hover:text-white transition-colors">{pillar.name}</span>
                                <span className="text-white/30">{pillar.status.toFixed(1)}%</span>
                            </div>
                            <div className="h-1 bg-white/10 rounded-full overflow-hidden">
                                <motion.div 
                                    initial={{ width: 0 }}
                                    animate={{ width: `${pillar.status}%` }}
                                    transition={{ duration: 1, delay: 0.5 }}
                                    className={`h-full ${pillar.color}`} 
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </motion.div>

        </div>

        {/* Center: Chancellor Stream */}
        <motion.div variants={itemVariants} className="lg:col-span-5 bg-black/60 rounded-2xl border border-white/10 flex flex-col overflow-hidden shadow-inner h-[500px]">
            <div className="p-3 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-medium text-white/60 uppercase tracking-wider">
                    <Terminal className="w-3 h-3 text-indigo-400" />
                    Chancellor Stream
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-[10px] text-green-500/80 font-mono">LIVE</span>
                </div>
            </div>
            <div 
                ref={scrollRef}
                className="flex-1 p-4 font-mono text-xs text-white/70 space-y-2 overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent"
            >
                <AnimatePresence initial={false}>
                    {logs.map((log, i) => (
                        <motion.div 
                            key={i} 
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="border-l-2 border-transparent hover:border-indigo-500/50 pl-2 py-0.5 hover:bg-white/5 cursor-default transition-colors group"
                        >
                            <span className="text-indigo-400/40 mr-2 text-[10px] group-hover:text-indigo-400 transition-colors">[{new Date().toLocaleTimeString()}]</span>
                            <span className="text-white/80 group-hover:text-white transition-colors">{log}</span>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </motion.div>

        {/* Right: Grok Insight */}
        <div className="lg:col-span-4 flex flex-col gap-4">
            
            {/* Insight Card */}
            <motion.div variants={itemVariants} className="flex-1 bg-gradient-to-br from-indigo-900/40 via-purple-900/20 to-transparent rounded-2xl p-6 border border-white/10 relative overflow-hidden group hover:border-indigo-500/50 transition-all duration-300">
                <div className="absolute top-0 right-0 p-3 opacity-20 group-hover:opacity-40 transition-opacity duration-500">
                    <Zap className="w-32 h-32 text-indigo-300 rotate-12 -mr-8 -mt-8" />
                </div>
                
                <div className="flex items-center gap-2 mb-6">
                    <div className="p-1.5 bg-white text-black rounded-lg shadow-[0_0_15px_rgba(255,255,255,0.3)]">
                        <svg viewBox="0 0 24 24" className="w-4 h-4" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </div>
                    <span className="font-bold tracking-wide text-lg text-white">Grok Insight</span>
                </div>

                <div className="space-y-6 relative z-10">
                    <div>
                        <h4 className="text-[10px] text-indigo-300/70 uppercase tracking-widest mb-2 font-bold">Strategic Observation</h4>
                        <p className="text-lg leading-relaxed font-light text-white/90 drop-shadow-sm">
                            "System stability is {systemOptimal ? 'optimal' : 'at risk'}. {systemOptimal ? 'Serenity protocols active.' : 'PostgreSQL connectivity failure detected.'}"
                        </p>
                    </div>

                    <div className="pt-6 border-t border-white/10">
                         <div className="flex items-center gap-3 mb-3">
                             <h4 className="text-[10px] text-white/40 uppercase tracking-widest">Active Protocols</h4>
                        </div>
                        <ul className="space-y-2 text-sm text-white/70">
                            {[
                                "Sequential Thinking",
                                "Context7 Analysis",
                                systemOptimal ? "Growth Mode" : "Recovery Mode"
                            ].map((action, i) => (
                                <li key={i} className="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 cursor-pointer transition-all hover:translate-x-1 group/item">
                                    <CheckCircle2 className="w-4 h-4 text-emerald-500/50 group-hover/item:text-emerald-400" />
                                    <span className="group-hover/item:text-white">{action}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </motion.div>

            {/* Quick Actions */}
            <motion.div variants={itemVariants} className="bg-white/5 rounded-2xl p-4 border border-white/10 flex gap-3 backdrop-blur-md">
                <button 
                  onClick={handleHeal}
                  className="flex-1 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-all shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/40 flex items-center justify-center gap-2 active:scale-95"
                >
                    <Heart className="w-4 h-4" />
                    Heal
                </button>
                <button className="flex-1 py-3 rounded-xl bg-white/5 hover:bg-white/10 text-white text-sm font-medium transition-all border border-white/5 hover:border-white/20 flex items-center justify-center gap-2 active:scale-95">
                    <AlertTriangle className="w-4 h-4 text-amber-400" />
                </button>
            </motion.div>

        </div>
      </div>
    </motion.div>
  );
}