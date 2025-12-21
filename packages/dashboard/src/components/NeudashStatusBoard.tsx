"use client";

import React, { useEffect, useState } from 'react';
import useSWR from 'swr';

// API Fetcher
const fetcher = (url: string) => fetch(url).then((res) => res.json());

interface KingdomStatus {
    heartbeat: number;
    dependency_count: number;
    total_dependencies: number;
    verified_dependencies: string[];
    pillars: Array<{ name: string; score: number }>;
    scholars: Array<{ name: string; role: string; status: string }>;
    entropy: number;
    timestamp: string;
}

export default function NeudashStatusBoard() {
  const [mounted, setMounted] = useState(false);

  // Fetch Real Data
  const { data, error, isLoading } = useSWR<KingdomStatus>(
    `${process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010'}/api/system/kingdom-status`,
    fetcher,
    { refreshInterval: 5000 } // Real-time pulse
  );

  useEffect(() => {
    setMounted(true);
  }, []);

  // Fallback / Loading State
  if (error) return <div className="p-8 text-center text-red-500">Failed to load Kingdom Status. Backend might be offline.</div>;
  if (isLoading || !data) return <div className="p-8 text-center text-neu-text">Connecting to AFO Core...</div>;

  const { verified_dependencies, pillars, scholars, heartbeat, dependency_count, total_dependencies, entropy } = data;

  return (
    <div className="flex min-h-screen bg-platinum text-neu-text font-sans selection:bg-neu-primary selection:text-white">
      
      {/* Sidebar (Desktop) */}
      <aside className="hidden lg:flex w-64 flex-col p-8 gap-8 fixed h-full overflow-y-auto">
        <div className="text-2xl font-bold text-neu-primary flex items-center gap-2">
            <span>💠</span> AFO BOARD
        </div>
        
        <nav className="flex flex-col gap-4">
            <div className="neu-btn active justify-start">Status Report</div>
            <div className="neu-btn justify-start bg-transparent shadow-none hover:shadow-[6px_6px_12px_var(--shadow-dark),-6px_-6px_12px_var(--shadow-light)]">Chancellor Rules</div>
            <div className="neu-btn justify-start bg-transparent shadow-none hover:shadow-[6px_6px_12px_var(--shadow-dark),-6px_-6px_12px_var(--shadow-light)]">Trinity Metrics</div>
            <div className="neu-btn justify-start bg-transparent shadow-none hover:shadow-[6px_6px_12px_var(--shadow-dark),-6px_-6px_12px_var(--shadow-light)]">Logs</div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-4 lg:p-8 lg:ml-64">
        
        {/* Header */}
        <header className="flex justify-between items-center mb-12">
            <div>
                <div className="text-neu-light text-sm font-medium mb-1">Kingdom / Overview / Deep Research</div>
                <h1 className="text-3xl font-bold tracking-tight text-neu-text">Status Report 2025</h1>
            </div>
            <div className="neu-icon-box w-12 h-12 text-lg">
                👑
            </div>
        </header>

        {/* KPI Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {/* Health */}
            <div className="neu-card flex flex-col items-center text-center">
                <div className="text-neu-light font-semibold text-sm mb-2 uppercase tracking-wide">System Heartbeat</div>
                <div className="text-5xl font-extrabold text-neu-text mb-4">{heartbeat}%</div>
                <div className="neu-pill text-emerald-500">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span> OPERATIONAL
                </div>
            </div>

            {/* Dependencies */}
            <div className="neu-card flex flex-col items-center text-center">
                <div className="text-neu-light font-semibold text-sm mb-2 uppercase tracking-wide">Dependency Core</div>
                <div className="text-5xl font-extrabold text-neu-text mb-4">{dependency_count}<span className="text-2xl text-neu-light">/{total_dependencies}</span></div>
                <div className="neu-pill text-neu-primary">
                    <span className="w-2 h-2 rounded-full bg-neu-primary shadow-[0_0_8px_rgba(90,103,216,0.8)]"></span> VERIFIED
                </div>
            </div>

            {/* Entropy */}
            <div className="neu-card flex flex-col items-center text-center">
                <div className="text-neu-light font-semibold text-sm mb-2 uppercase tracking-wide">Entropy Level</div>
                <div className="text-5xl font-extrabold text-neu-text mb-4">{entropy}%</div>
                <div className="neu-pill text-amber-500">
                    <span className="w-2 h-2 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></span> OPTIMIZED
                </div>
            </div>
        </div>

        {/* 2-Col Layout: Scholars & Pillars */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-12">
            
            {/* Scholars */}
            <div className="neu-card">
                <h3 className="text-xl font-bold text-neu-text mb-8">Active Scholars</h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
                    {scholars.map((scholar) => (
                        <div key={scholar.name} className="flex flex-col items-center text-center">
                            <div className="neu-icon-box w-20 h-20 text-4xl mb-4">
                                {scholar.name === "Jaryong" ? "🐉" : 
                                 scholar.name === "Bangtong" ? "🐥" : 
                                 scholar.name === "Yeongdeok" ? "🛡️" : "🏛️"}
                            </div>
                            <div className="font-bold text-neu-text">{scholar.name}</div>
                            <div className="text-xs text-neu-light mt-1 uppercase font-semibold">{scholar.role}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Trinity Pillars */}
            <div className="neu-card">
                <h3 className="text-xl font-bold text-neu-text mb-8">Trinity Pillars</h3>
                <div className="space-y-6">
                    {pillars.map((pillar) => {
                         // Map colors based on name for gradient
                         let color = "from-gray-400 to-gray-500";
                         if (pillar.name.includes("Truth")) color = "from-blue-400 to-blue-500";
                         if (pillar.name.includes("Good")) color = "from-emerald-400 to-teal-400";
                         if (pillar.name.includes("Beauty")) color = "from-pink-400 to-purple-400";
                         if (pillar.name.includes("Serenity")) color = "from-amber-300 to-amber-500";
                         if (pillar.name.includes("Eternity")) color = "from-indigo-400 to-indigo-600";
                         
                         return (
                            <div key={pillar.name} className="flex items-center gap-4">
                                <div className="w-24 font-bold text-neu-text">{pillar.name}</div>
                                <div className="flex-1 h-4 rounded-full bg-platinum shadow-[inset_6px_6px_12px_var(--shadow-dark),inset_-6px_-6px_12px_var(--shadow-light)] overflow-hidden">
                                    <div 
                                        className={`h-full rounded-full bg-gradient-to-r ${color} transition-all duration-1000 ease-out`}
                                        style={{ width: mounted ? `${pillar.score}%` : '0%' }}
                                    ></div>
                                </div>
                                <div className="text-xs font-mono text-neu-light">{pillar.score}%</div>
                            </div>
                         );
                    })}
                </div>
            </div>
        </div>

        {/* Dependency Matrix */}
        <div className="mb-12">
            <h3 className="text-xl font-bold text-neu-text mb-6 flex items-center gap-3">
                Framework Matrix 
                <span className="text-xs px-3 py-1 rounded-full bg-platinum shadow-[inset_4px_4px_8px_var(--shadow-dark),inset_-4px_-4px_8px_var(--shadow-light)] font-mono">
                    {verified_dependencies.length} Active
                </span>
            </h3>
            
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
                {verified_dependencies.map((dep) => (
                    <div key={dep} className="group p-4 rounded-2xl bg-platinum shadow-[6px_6px_12px_var(--shadow-dark),-6px_-6px_12px_var(--shadow-light)] hover:-translate-y-1 transition-transform border border-white/40 flex items-center gap-3 text-sm font-semibold text-neu-text">
                        <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] group-hover:scale-125 transition-transform"></span>
                        {dep}
                    </div>
                ))}
            </div>
        </div>

        <footer className="text-center text-neu-light text-sm pt-8 border-t border-black/5">
            Neudash 2025 • AFO Chancellor System • All Rights Reserved
        </footer>

      </main>
    </div>
  );
}
