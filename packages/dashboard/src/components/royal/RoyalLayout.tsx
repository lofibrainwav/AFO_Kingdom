"use client";

import useSWR from "swr";
import { useState } from 'react';
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X } from 'lucide-react';
import TrinityGlow from "./TrinityGlow";
import ChancellorStream from "./ChancellorStream";
import OrgansMonitor from "./OrgansMonitor";
import SkillDeck from "./SkillDeck";
import { GraphRAGQuery } from "../GraphRAGQuery";
import { RoyalPhilosophy } from "./RoyalPhilosophy";
import { RoyalArchitecture } from "./RoyalArchitecture";
import { RoyalLibrary } from './RoyalLibrary';
import { SystemStatusWidget } from './widgets/SystemStatusWidget';
import { GitWidget } from './widgets/GitWidget';
import { RoyalTreasuryCard } from '../genui/RoyalTreasuryCard';
import { JulieTaxWidget } from '../genui/JulieTaxWidget';

import { ROYAL_CONSTANTS } from '../../config/royal_constants';
// ... existing imports

// Basic SWR fetcher
const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function RoyalLayout() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || ROYAL_CONSTANTS.LINKS.API_DEFAULT;
  const { data, error, isLoading } = useSWR(
    `${API_BASE}/api/system/kingdom-status`,
    fetcher,
    { refreshInterval: 2000 }
  );

  return (
    <div className="relative min-h-screen w-full bg-[#e0e5ec] text-slate-700 font-sans selection:bg-indigo-500/30 overflow-hidden">
      {/* 1. Nervous System (Background & Audio) */}
      <TrinityGlow score={data?.trinity_score || 85} />

      {/* Main Content Container with Glass Effect */}
      <div className="relative z-10 max-w-7xl mx-auto p-6 md:p-10 lg:p-12 space-y-12 h-screen overflow-y-auto scrollbar-hide">
        
        {/* Header Section */}
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
            <a
              href="/docs"
              className="px-4 py-2 bg-slate-200/50 rounded-lg text-slate-700 hover:bg-slate-300/50 transition-colors text-sm font-medium"
            >
              📐 문서
            </a>
            <div className="text-right">
               <div className="text-xs text-slate-400 font-mono">{ROYAL_CONSTANTS.TRINITY_SCORE_LABEL}</div>
               <div className="text-3xl font-bold text-slate-600">
                 {data?.trinity_score || "..."}<span className="text-lg text-slate-400">/100</span>
               </div>
            </div>
          </div>
        </header>

        {/* 2. Organs Monitor (Top Dashboard) */}
        <section>
          <div className="flex items-center gap-4 mb-6">
            <h2 className="text-xl font-bold text-slate-600">{ROYAL_CONSTANTS.SECTIONS.ORGANS}</h2>
            <div className="h-[1px] flex-1 bg-slate-300"/>
          </div>
          <OrgansMonitor organs={data?.organs} />
        </section>

        {/* 3. Neural Stream & Skills (Split View) */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[500px]">
          {/* Genesis Widgets (Vibe Coding Verification) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <SystemStatusWidget />
              <GitWidget />
              <RoyalTreasuryCard />
              <JulieTaxWidget />
          </div>

          {/* Left: Chancellor Stream */}
          <div className="flex flex-col h-full">
            <div className="flex items-center gap-4 mb-4">
              <h2 className="text-xl font-bold text-slate-600">{ROYAL_CONSTANTS.SECTIONS.CHANCELLOR}</h2>
              <div className="h-[1px] flex-1 bg-slate-300"/>
            </div>
            <div className="flex-1">
              <ChancellorStream />
            </div>
          </div>

          {/* Right: Skills Deck */}
          <div className="flex flex-col h-full">
            <div className="flex items-center gap-4 mb-4">
               <h2 className="text-xl font-bold text-slate-600">{ROYAL_CONSTANTS.SECTIONS.SKILLS}</h2>
               <div className="h-[1px] flex-1 bg-slate-300"/>
            </div>
            <div className="flex-1 neu-card bg-slate-200/30 rounded-3xl border border-white/40 shadow-inner flex flex-col justify-center relative">
               <div className="absolute inset-0 bg-white/20 backdrop-blur-sm rounded-3xl -z-10"/>
               <SkillDeck />
               <p className="text-center text-xs text-slate-400 mt-4">{ROYAL_CONSTANTS.MESSAGES.SKILL_HINT}</p>
            </div>
          </div>

        </section>

        {/* 4. GraphRAG Brain (Advanced Intelligence) - REMOVED STATIC SECTION */}
        {/* <GraphRAGQuery /> moved to Modal */}

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
