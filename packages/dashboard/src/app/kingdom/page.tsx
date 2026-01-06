"use client";

import React, { useState } from 'react';
import { PalaceArchitecture } from '../../components/genui/PalaceArchitecture';
import { CommandOverlay } from '../../components/genui/CommandOverlay';
import { StrategistCard } from '../../components/genui/StrategistCard';
import KingdomParticles from '../../components/genui/KingdomParticles';
import { EvolutionMonitor } from '../../components/EvolutionMonitor';
import { AllianceObserver } from '../../components/AllianceObserver';
import { X } from 'lucide-react';

export default function KingdomPage() {
    const [isCommandOpen, setIsCommandOpen] = useState(false);
    const [isEvolutionOpen, setIsEvolutionOpen] = useState(false);
    const [isAllianceOpen, setIsAllianceOpen] = useState(false);

    // 🟢 6-SANCTUARY (Bio-Kingdom Map)
    // 1. Heart (Central)
    // 2. Brain (Top)
    // 3. Gallbladder/Gate (Bottom)
    // 4. Skills/Armory (Top Left)
    // 5. Lungs/Observatory (Top Right)
    // 6. Stomach/Warehouse (Bottom Right)

    // TODO: Connect to Real Context7 Data
    // currently using static Risk/Trinity Scores for Concept Demo
    
    return (
        <div className="relative w-full h-screen bg-[#0a0a0a] text-white overflow-hidden font-sans selection:bg-[#d4af37] selection:text-black">
            
            {/* 🌌 LAYER 0: Ambient Background (Parchment + Dark Void) */}
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/dark-matter.png')] opacity-40 z-0"></div>
            <div className="absolute inset-0 bg-gradient-to-b from-black via-[#1a1510] to-black opacity-90 z-0"></div>
            <KingdomParticles isActive={true} mode="harmony" />

            {/* 🏰 LAYER 1: GAME MAP (Hexagonal Grid) */}
            {/* Centered Absolute Container */}
            <div className="absolute inset-0 flex items-center justify-center z-10 perspective-[1000px]">
                <div className="relative w-[1200px] h-[900px] transform md:scale-90 lg:scale-100 transition-transform duration-1000">
                    
                    {/* 1. HEART (Center): Chancellor Hall */}
                    <PalaceArchitecture 
                        type="Royal" 
                        x={0} y={0} 
                        scale={1.3} 
                        isActive={true} 
                        label="Chancellor Hall"
                        organLabel="HEART (Decision)"
                        riskLevel={22}
                        trinityScore={98}
                        onClick={() => setIsCommandOpen(true)}
                    />

                    {/* 2. BRAIN (Top): Royal Library */}
                    <PalaceArchitecture 
                        type="Sanctuary" 
                        x={0} y={-380} 
                        scale={0.95} 
                        isActive={true} 
                        label="Royal Library"
                        organLabel="BRAIN (Memory)"
                        riskLevel={10} 
                        onClick={() => setIsEvolutionOpen(true)}
                    />

                    {/* 3. SHIELD (Bottom): Iron Gate */}
                    <PalaceArchitecture 
                        type="Gate" 
                        x={0} y={380} 
                        scale={1.05} 
                        isActive={true} 
                        label="Iron Gate"
                        organLabel="GALL (Shield)"
                        riskLevel={45} 
                    />

                    {/* 4. SKILLS (Top-Left): Imperial Armory */}
                    <PalaceArchitecture 
                        type="Barracks" 
                        x={-420} y={-180} 
                        scale={0.9} 
                        isActive={true} 
                        label="Imperial Armory"
                        organLabel="SKILLS (Action)"
                        riskLevel={15}
                    />

                    {/* 5. LUNGS (Top-Right): Heavenly Observatory */}
                    <PalaceArchitecture 
                        type="Observatory"  
                        x={420} y={-180} 
                        scale={0.9} 
                        isActive={true} 
                        label="Heavenly Obs."
                        organLabel="LUNGS (Monitor)"
                        riskLevel={5} 
                        onClick={() => setIsAllianceOpen(true)}
                    />

                    {/* 6. STOMACH (Bottom-Right): Alchemical Warehouse */}
                    <PalaceArchitecture 
                        type="Warehouse" 
                        x={420} y={180} 
                        scale={0.9} 
                        isActive={true} 
                        label="Alchemy Depot"
                        organLabel="STOMACH (LLM)"
                        riskLevel={2} 
                    />

                     {/* DECORATIVE: Connecting Lines (Golden Paths) */}
                     {/* SVG Overlay for Connections */}
                     <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30 drop-shadow-glow">
                        <defs>
                            <linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#d4af37" stopOpacity="0" />
                                <stop offset="50%" stopColor="#d4af37" stopOpacity="1" />
                                <stop offset="100%" stopColor="#d4af37" stopOpacity="0" />
                            </linearGradient>
                        </defs>
                        {/* Center to Top */}
                        <path d="M 600 450 L 600 70" stroke="url(#gold-grad)" strokeWidth="2" strokeDasharray="5,5" />
                        {/* Center to Bottom */}
                        <path d="M 600 450 L 600 830" stroke="url(#gold-grad)" strokeWidth="2" strokeDasharray="5,5" />
                        {/* Center to TopLeft */}
                        <path d="M 600 450 L 180 270" stroke="url(#gold-grad)" strokeWidth="2" strokeDasharray="5,5" />
                        {/* Center to TopRight */}
                        <path d="M 600 450 L 1020 270" stroke="url(#gold-grad)" strokeWidth="2" strokeDasharray="5,5" />
                         {/* Center to BottomRight (Warehouse is roughly at 1020, 630) */}
                         <path d="M 600 450 L 1020 630" stroke="url(#gold-grad)" strokeWidth="2" strokeDasharray="5,5" />
                     </svg>

                </div>
            </div>

            {/* 🎮 LAYER 2: GAME HUD (Overlay) */}
            <div className="absolute inset-0 z-50 pointer-events-none flex flex-col justify-between p-6">
                
                {/* TOP HUD: Resources & Title */}
                <div className="flex justify-between items-start pointer-events-auto">
                    {/* User Profile / Status */}
                    <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-full border-2 border-[#d4af37] bg-[url('/assets/commander_avatar.png')] bg-cover bg-center shadow-lg bg-gray-800"></div>
                        <div className="flex flex-col">
                            <h2 className="text-xl font-display font-bold text-[#f5e6d3] tracking-widest uppercase">Commander</h2>
                            <span className="text-xs text-[#d4af37] font-serif">Level 99 • Grand Strategist</span>
                            {/* Resource Bar */}
                            <div className="flex gap-4 mt-2 bg-black/60 px-3 py-1 rounded-md border border-white/10 backdrop-blur-md">
                                <div className="flex items-center gap-1 text-emerald-400 text-xs font-bold">
                                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span> 98% Vitality
                                </div>
                                <div className="flex items-center gap-1 text-cyan-400 text-xs font-bold">
                                    <span className="w-2 h-2 rounded-full bg-cyan-500"></span> 24ms Ping
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* MAIN TITLE BADGE */}
                    <div className="relative mt-2">
                        <div className="bg-[#2d1b0e] border-2 border-[#d4af37] px-8 py-2 transform skew-x-[-10deg] shadow-[0_0_20px_rgba(212,175,55,0.4)]">
                            <div className="transform skew-x-[10deg] text-center">
                                <h1 className="text-2xl font-serif font-bold text-[#f5e6d3] tracking-[0.3em] uppercase">AFO Kingdom</h1>
                                <div className="text-[10px] text-[#d4af37] tracking-widest uppercase mt-0.5">Tactical Command Center</div>
                            </div>
                        </div>
                    </div>

                    {/* System Clock / Menu */}
                    <div className="flex flex-col items-end gap-2">
                         <div className="text-4xl font-mono font-bold text-[#f5e6d3] opacity-80">09:41</div>
                         <button className="bg-[#2d1b0e] border border-[#d4af37]/50 text-[#d4af37] px-4 py-1 text-xs uppercase tracking-widest hover:bg-[#d4af37] hover:text-[#2d1b0e] transition-colors">
                             System Menu
                         </button>
                    </div>
                </div>

                {/* BOTTOM HUD: Strategists & Mini-Map */}
                <div className="flex items-end justify-between pointer-events-auto">
                    
                    {/* Left: Chat / Log (Minimised) */}
                    <div className="w-64 h-32 bg-black/60 border border-white/10 rounded-tr-3xl backdrop-blur-md p-4 hidden md:block">
                        <h3 className="text-xs font-bold text-gray-400 mb-2 uppercase tracking-wider">System Log</h3>
                        <div className="space-y-1 text-[10px] font-mono text-gray-300 opacity-80">
                            <p>&gt; <span className="text-emerald-400">System</span> initialized...</p>
                            <p>&gt; <span className="text-emerald-400">Assets</span> loaded (Uigwe_Pack_v1)</p>
                            <p>&gt; <span className="text-amber-400">Alert</span> Gallbladder Load 45%</p>
                        </div>
                    </div>

                    {/* CENTER: Strategist Deck */}
                    <div className="flex items-end gap-4 pb-4">
                        <div className="transform translate-y-4 hover:translate-y-0 transition-transform duration-300">
                             <StrategistCard name="Zhuge Liang" role="Truth (Arch)" influence={95} iconName="book" color="emerald" />
                        </div>
                        <div className="transform translate-y-4 hover:translate-y-0 transition-transform duration-300 mb-8">
                             <StrategistCard name="Sima Yi" role="Goodness (Risk)" influence={88} iconName="shield" color="slate" />
                        </div>
                        <div className="transform translate-y-4 hover:translate-y-0 transition-transform duration-300">
                             <StrategistCard name="Zhou Yu" role="Beauty (UX)" influence={92} iconName="aperture" color="cyan" />
                        </div>
                    </div>

                    {/* Right: Mini-Map / Actions */}
                    <div className="flex flex-col gap-2">
                        {/* Action Buttons */}
                         <div className="grid grid-cols-2 gap-2 mb-2">
                             <button className="w-12 h-12 bg-[#2d1b0e] border border-[#d4af37] flex items-center justify-center hover:bg-[#d4af37] hover:text-black transition-colors rounded">
                                 <span className="text-xl">⚔️</span>
                             </button>
                             <button className="w-12 h-12 bg-[#2d1b0e] border border-[#d4af37] flex items-center justify-center hover:bg-[#d4af37] hover:text-black transition-colors rounded">
                                 <span className="text-xl">🛡️</span>
                             </button>
                         </div>
                         {/* Mini Map (Static Placeholder) */}
                        <div className="w-48 h-48 bg-black/80 border-2 border-[#d4af37] rounded-tl-3xl overflow-hidden relative shadow-lg">
                            <div className="absolute inset-0 bg-[url('/assets/concept_game_ui_joseon_1767584678385.png')] bg-cover bg-center opacity-70"></div>
                            <div className="absolute inset-0 border-4 border-[#d4af37]/30 rounded-tl-3xl pointer-events-none"></div>
                        </div>
                    </div>

                </div>
            </div>

            {/* OVERLAYS */}
            <CommandOverlay isOpen={isCommandOpen} onClose={() => setIsCommandOpen(false)} />

            {isEvolutionOpen && (
                <div className="fixed inset-0 z-[300] flex items-center justify-center p-8 bg-black/80 backdrop-blur-md animate-in fade-in duration-500">
                    <div className="relative w-full max-w-4xl shadow-[0_0_50px_rgba(79,70,229,0.3)] rounded-2xl overflow-hidden">
                        <button 
                            onClick={() => setIsEvolutionOpen(false)}
                            className="absolute top-4 right-4 z-[310] p-2 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white rounded-full transition-colors"
                        >
                            <X className="w-5 h-5" />
                        </button>
                        <EvolutionMonitor />
                    </div>
                </div>
            )}

            {isAllianceOpen && (
                <div className="fixed inset-0 z-[300] flex items-center justify-center p-8 bg-black/80 backdrop-blur-md animate-in fade-in duration-500">
                    <div className="relative w-full max-w-2xl shadow-[0_0_50px_rgba(59,130,246,0.3)] rounded-2xl overflow-hidden">
                        <button 
                            onClick={() => setIsAllianceOpen(false)}
                            className="absolute top-4 right-4 z-[310] p-2 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white rounded-full transition-colors"
                        >
                            <X className="w-5 h-5" />
                        </button>
                        <AllianceObserver />
                    </div>
                </div>
            )}

        </div>
    );
}
