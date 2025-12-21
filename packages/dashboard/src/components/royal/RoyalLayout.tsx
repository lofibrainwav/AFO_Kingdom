"use client";

import useSWR from "swr";
import { motion } from "framer-motion";
import TrinityGlow from "./TrinityGlow";
import ChancellorStream from "./ChancellorStream";
import OrgansMonitor from "./OrgansMonitor";
import SkillDeck from "./SkillDeck";

const fetcher = (url: string) =>
  fetch(url).then((res) => {
    if (!res.ok) throw new Error("Backend Offline");
    return res.json();
  });

export default function RoyalLayout() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";
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
              PROJECT GENESIS
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-2 text-slate-500 font-light tracking-widest text-sm uppercase"
            >
              Digital Royal Palace v1.0 • AFO Kingdom
            </motion.p>
          </div>
          <div className="text-right">
             <div className="text-xs text-slate-400 font-mono">TRINITY SCORE</div>
             <div className="text-3xl font-bold text-slate-600">
               {data?.trinity_score || "..."}<span className="text-lg text-slate-400">/100</span>
             </div>
          </div>
        </header>

        {/* 2. Organs Monitor (Top Dashboard) */}
        <section>
          <div className="flex items-center gap-4 mb-6">
            <h2 className="text-xl font-bold text-slate-600">11-ORGANS VITALITY</h2>
            <div className="h-[1px] flex-1 bg-slate-300"/>
          </div>
          <OrgansMonitor organs={data?.organs} />
        </section>

        {/* 3. Neural Stream & Skills (Split View) */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[500px]">
          
          {/* Left: Chancellor Stream */}
          <div className="flex flex-col h-full">
            <div className="flex items-center gap-4 mb-4">
              <h2 className="text-xl font-bold text-slate-600">CHANCELLOR TOT</h2>
              <div className="h-[1px] flex-1 bg-slate-300"/>
            </div>
            <div className="flex-1">
              <ChancellorStream />
            </div>
          </div>

          {/* Right: Skills Deck */}
          <div className="flex flex-col h-full">
            <div className="flex items-center gap-4 mb-4">
               <h2 className="text-xl font-bold text-slate-600">ROYAL SKILL DECK</h2>
               <div className="h-[1px] flex-1 bg-slate-300"/>
            </div>
            <div className="flex-1neu-card bg-slate-200/30 rounded-3xl border border-white/40 shadow-inner flex flex-col justify-center relative">
               <div className="absolute inset-0 bg-white/20 backdrop-blur-sm rounded-3xl -z-10"/>
               <SkillDeck />
               <p className="text-center text-xs text-slate-400 mt-4">SWIPE TO EXPLORE • TAP TO SIMULATE</p>
            </div>
          </div>

        </section>

      </div>
    </div>
  );
}
