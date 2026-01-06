"use client";

import { AnimatePresence, motion } from "framer-motion";
import { MessageCircle, X } from "lucide-react";
import { useMemo, useState } from "react";
import useSWR from "swr";
import { KingdomMessageBoard } from "../genui";
import RoyalOpsCenter from "../genui/RoyalOpsCenter";
import { GraphRAGQuery } from "../GraphRAGQuery";
import OrgansMonitor from "./OrgansMonitor";
import { RoyalArchitecture } from "./RoyalArchitecture";
import { RoyalLibrary } from "./RoyalLibrary";
import { RoyalPhilosophy } from "./RoyalPhilosophy";
import TrinityGlow from "./TrinityGlow";
import { GitWidget } from "./widgets/GitWidget";
import RoyalFinanceWidget from "./widgets/RoyalFinanceWidget";
import { SystemStatusWidget } from "./widgets/SystemStatusWidget";
import { RoyalCommandHierarchyCard } from "../../widgets/royal/RoyalCommandHierarchyCard";
import { FieldManualLawCard } from "../../widgets/royal/FieldManualLawCard";
import SSEHealthWidget from "../genui/SSEHealthWidget";

import { ROYAL_CONSTANTS } from "../../config/royal_constants";
import { TrinityEvidenceWidget } from "../genui/TrinityEvidenceWidget";
// ... existing imports

// Memoize SWR fetcher
const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function RoyalLayout() {
  const [isChatOpen, setIsChatOpen] = useState(false);
    const {
    data,
    error: _error,
    isLoading: _isLoading,
  } = useSWR(`/api/kingdom-status`, fetcher, { refreshInterval: 2000 });


  // Memoize trinity score
  const trinityScore = useMemo(() => data?.trinity_score || 85, [data?.trinity_score]);

  return (
    <div className="relative min-h-screen w-full bg-[#e0e5ec] text-slate-700 font-sans selection:bg-indigo-500/30 overflow-hidden">
      {/* 1. Nervous System (Background & Audio) */}
      <TrinityGlow score={trinityScore} />

      {/* Main Content Container with Glass Effect */}
      <div className="relative z-10 max-w-7xl mx-auto p-6 md:p-10 lg:p-12 space-y-12 h-screen overflow-y-auto scrollbar-hide">
        {/* Header Section - PDF 6.1절 眞 적용: 시스템 상태 투명한 시각화 */}
        <header className="flex justify-between items-end pb-8 border-b border-slate-300/50">
          <div>
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-4xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-slate-600 to-slate-400 tracking-tighter"
            >
              {ROYAL_CONSTANTS.PROJECT_NAME}
            </motion.h1>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-2 text-slate-500 font-light tracking-widest text-sm uppercase"
            >
              {ROYAL_CONSTANTS.SUBTITLE}
            </motion.p>
          </div>
          <div className="flex items-end gap-6">
            {/* PDF 6.1절: 왕궁 현황판 - 메모리 상태 실시간 표시 */}
            <div className="text-right bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-white/10">
              <div className="text-xs text-slate-400 font-mono mb-1">
                🏰 메모리 현황 (Memory Status)
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="w-16 h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-400 to-blue-500 transition-all duration-500"
                    style={{ width: `${Math.min(100, ((data?.memory_usage || 0) / 24) * 100)}%` }}
                  />
                </div>
                <span className="text-slate-500 font-mono text-xs">
                  {data?.memory_usage || 0}GB / 24GB
                </span>
              </div>
            </div>

            <a
              href="http://localhost:8000/kingdom_dashboard.html"
              target="_blank"
              rel="noopener noreferrer"
              className="neu-btn px-4 py-2 text-sm font-bold text-slate-600 hover:text-indigo-600 flex items-center gap-2"
              title="Port 8000: 설계도 (Design Time)"
            >
              <span>🗺️ 왕국 설계도</span>
              <span className="text-[10px] bg-slate-200 px-1.5 py-0.5 rounded text-slate-500">:8000</span>
            </a>

            <div className="text-right">
              <div className="text-xs text-slate-400 font-mono">
                {ROYAL_CONSTANTS.TRINITY_SCORE_LABEL}
              </div>
              <div className="text-3xl font-bold text-slate-600" aria-live="polite" aria-atomic="true">
                {data?.trinity_score || "..."}
                <span className="text-lg text-slate-400">/100</span>
              </div>
            </div>
          </div>
        </header>

        {/* 2. Organs Monitor (Top Dashboard) */}
        <section>
          <div className="flex items-center gap-4 mb-6">
            <h2 className="text-xl font-bold text-slate-600">{ROYAL_CONSTANTS.SECTIONS.ORGANS}</h2>
            <div className="h-[1px] flex-1 bg-slate-300" />
          </div>
          <OrgansMonitor organs={data?.organs} />
        </section>

          {/* 3. Neural Stream & Skills (Unified Royal Ops Center) */}
          <section className="space-y-8">
            {/* Genesis Widgets Row 1: Quick Status (neu-card style, equal sizes) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <SystemStatusWidget />
              <GitWidget />
              <TrinityEvidenceWidget />
              <SSEHealthWidget />
            </div>

            {/* Use the Unified Royal Ops Center */}
            <RoyalOpsCenter trinityScore={trinityScore} healthData={data} />
          </section>

        {/* 4. Royal Decrees & Predictions (New Generation Section) */}
        <section className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          <div className="flex flex-col h-full">
            <div className="flex items-center gap-4 mb-4">
              <h2 className="text-xl font-bold text-slate-600">📜 왕명 (Royal Decrees)</h2>
              <div className="h-[1px] flex-1 bg-slate-300" />
            </div>
            <div className="flex-1 min-h-[500px]">
              <KingdomMessageBoard />
            </div>
          </div>

          <div className="flex flex-col h-full">
            <div className="flex items-center gap-4 mb-4">
              <h2 className="text-xl font-bold text-slate-600">🚀 미래 예측 (Prophet Predictions)</h2>
              <div className="h-[1px] flex-1 bg-slate-300" />
            </div>
            <div className="flex-1 bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 p-6 shadow-inner overflow-hidden">
               <RoyalFinanceWidget />
            </div>
          </div>
        </section>

        {/* 4.5 Royal Governance (Command & Law) */}
        <section className="space-y-8">
          <div className="flex items-center gap-4 mb-6">
            <h2 className="text-xl font-bold text-slate-600">👑 왕실 통치 (Royal Governance)</h2>
            <div className="h-[1px] flex-1 bg-slate-300" />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <RoyalCommandHierarchyCard />
            <FieldManualLawCard />
          </div>
        </section>

        {/* 5. Royal Philosophy (Foundations) */}
        <RoyalPhilosophy />

        {/* 6. System Architecture (Blueprints) */}
        <RoyalArchitecture />

        {/* 7. Royal Library & SSOT (Archives) */}
        <RoyalLibrary />
      </div>

      {/* FLOATING ACTION BUTTON (The Ear) */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsChatOpen(true)}
        aria-label="Open Chat"
        className="fixed bottom-8 right-8 z-[100] w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-700 rounded-full shadow-2xl flex items-center justify-center border-2 border-white/20 hover:shadow-indigo-500/50 transition-all cursor-pointer"
      >
        <MessageCircle className="w-8 h-8 text-white" />
      </motion.button>

      {/* CHAT MODAL (The Brain Interface) */}
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[110] flex items-center justify-center bg-black/60 backdrop-blur-md p-4"
            onClick={() => setIsChatOpen(false)} // Close on backdrop click
          >
            {/* Modal Content */}
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="relative w-full max-w-4xl"
              onClick={(e) => e.stopPropagation()} // Prevent close on content click
            >
              {/* Close Button */}
              <button
                onClick={() => setIsChatOpen(false)}
                aria-label="Close Chat"
                className="absolute -top-12 right-0 w-10 h-10 bg-white/10 rounded-full flex items-center justify-center text-white hover:bg-red-500/20 transition-colors shadow-lg backdrop-blur-sm"
              >
                <X className="w-6 h-6" />
              </button>

              <GraphRAGQuery />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}