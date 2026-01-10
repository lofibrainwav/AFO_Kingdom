"use client";

import React, { useState, useEffect } from 'react';
import { Activity, Zap, Shield, GitCommit, ChevronRight, Gavel, TrendingUp, History, Check, X } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface EvolutionMetadata {
    generation: number;
    parent_id: string | null;
    run_id: string;
    trinity_score: number;
    modifications: string[];
    decree_status: 'PENDING' | 'APPROVED' | 'REJECTED';
    timestamp: string;
}

export const EvolutionMonitor: React.FC = () => {
    const [history, setHistory] = useState<EvolutionMetadata[]>([]);
    const [pendingDecrees, setPendingDecrees] = useState<EvolutionMetadata[]>([]);
    const [isEvolving, setIsEvolving] = useState(false);
    const [activeRun, setActiveRun] = useState<string | null>(null);
    const [viewMode, setViewMode] = useState<'registry' | 'history' | 'stats'>('registry');
    const [isLocked, setIsLocked] = useState<boolean>(false);
    const [lockReason, setLockReason] = useState<string>("");

    useEffect(() => {
        fetchHistory();
        fetchPendingDecrees();
        fetchSovereigntyStatus();
    }, []);

    const fetchSovereigntyStatus = async () => {
        try {
            const res = await fetch('http://localhost:8010/api/v1/public/status');
            const data = await res.json();
            setIsLocked(data.status === "MAINTENANCE");
        } catch (error) {
            console.error("Failed to fetch sovereignty status", error);
        }
    };

    const toggleKillSwitch = async () => {
        const action = isLocked ? "unlock" : "lock";
        if (!confirm(`Are you sure you want to ${action} the civilization?`)) return;
        
        try {
            await fetch(`http://localhost:8010/api/evolution/sovereignty/${action}`, { method: 'POST' });
            fetchSovereigntyStatus();
        } catch (error) {
            console.error(`Failed to ${action} civilization`, error);
        }
    };

    const fetchHistory = async () => {
        try {
            const res = await fetch('http://localhost:8010/api/evolution/history');
            const data = await res.json();
            setHistory(data);
        } catch (error) {
            console.error("Failed to fetch evolution history", error);
        }
    };

    const fetchPendingDecrees = async () => {
        try {
            const res = await fetch('http://localhost:8010/api/evolution/decrees?status=PENDING');
            const data = await res.json();
            setPendingDecrees(data);
        } catch (error) {
            console.error("Failed to fetch pending decrees", error);
        }
    };

    const triggerEvolution = async () => {
        if (isLocked) {
            setActiveRun("ERROR: SYSTEM UNDER LOCKDOWN");
            return;
        }
        setIsEvolving(true);
        setActiveRun("Initializing DGM Engine...");
        try {
            const res = await fetch('http://localhost:8010/api/evolution/improve', {
                method: 'POST',
            });
            if (res.status === 403) {
                setActiveRun("BLOCKED: LOCKDOWN ACTIVE");
                return;
            }
            const data = await res.json();
            setActiveRun(`Proposal Generated: ${data.run_id}`);
            fetchPendingDecrees();
            fetchHistory();
        } catch (_error) {
            setActiveRun("Evolution Failed: Connection Error");
        } finally {
            setIsEvolving(false);
            setTimeout(() => setActiveRun(null), 5000);
        }
    };

    const handleDecree = async (run_id: string, action: 'seal' | 'veto') => {
        try {
            const res = await fetch(`http://localhost:8010/api/evolution/decrees/${run_id}/${action}`, {
                method: 'POST',
            });
            if (res.ok) {
                fetchPendingDecrees();
                fetchHistory();
            }
        } catch (error) {
            console.error(`Failed to ${action} decree`, error);
        }
    };

    // Prepare data for the Trinity Trend Chart
    const chartData = history.map(h => ({
        gen: `G${h.generation}`,
        score: parseFloat((h.trinity_score * 100).toFixed(2))
    })).sort((a, b) => parseInt(a.gen.slice(1)) - parseInt(b.gen.slice(1)));

    return (
        <div className="bg-slate-950 border border-slate-800 rounded-2xl p-8 shadow-2xl font-sans text-slate-200 w-full min-h-[600px] flex flex-col">
            {/* Phase 13: Sovereign Header */}
            <div className="flex items-center justify-between mb-8 border-b border-slate-800 pb-6">
                <div className="flex items-center gap-6">
                    <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
                        <Activity className="w-8 h-8 text-indigo-400" />
                    </div>
                    <div>
                        <div className="flex items-center gap-3">
                            <h2 className="text-2xl font-black tracking-tighter text-white uppercase italic leading-none">Civilization Deck</h2>
                            <div className={`px-2 py-0.5 rounded text-[8px] font-black border ${isLocked ? 'bg-red-500/10 border-red-500/30 text-red-500' : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-500'}`}>
                                {isLocked ? '🔒 LOCKDOWN' : '⛅ SOVEREIGN'}
                            </div>
                            <div className="px-2 py-0.5 rounded text-[8px] font-black border bg-indigo-500/10 border-indigo-500/30 text-indigo-400">
                                🤫 SILENT MODE
                            </div>
                        </div>
                        <p className="text-[10px] text-slate-400 font-mono uppercase tracking-widest leading-none mt-2">Active Constitutional Governance</p>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <button 
                        onClick={toggleKillSwitch}
                        className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-[10px] font-black transition-all border ${
                            isLocked 
                            ? 'bg-emerald-600/20 border-emerald-500/30 text-emerald-400 hover:bg-emerald-600/30' 
                            : 'bg-red-600/20 border-red-500/30 text-red-400 hover:bg-red-600/30'
                        }`}
                    >
                        <Shield className="w-3.5 h-3.5" />
                        {isLocked ? 'RESTORE SOVEREIGNTY' : 'EMERGENCY KILL-SWITCH'}
                    </button>

                    <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-lg border border-slate-800">
                        <button 
                            onClick={() => setViewMode('registry')}
                            className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${viewMode === 'registry' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'}`}
                        >
                            <Gavel className="w-3.5 h-3.5" /> REGISTRY
                        </button>
                        <button 
                            onClick={() => setViewMode('stats')}
                            className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${viewMode === 'stats' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'}`}
                        >
                            <TrendingUp className="w-3.5 h-3.5" /> TRENDS
                        </button>
                        <button 
                            onClick={() => setViewMode('history')}
                            className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${viewMode === 'history' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'}`}
                        >
                            <History className="w-3.5 h-3.5" /> CHRONICLE
                        </button>
                    </div>
                </div>
            </div>

            {/* Action Bar */}
            <div className="flex items-center justify-between mb-8 bg-slate-900/50 p-4 rounded-xl border border-slate-800/50">
                <div className="flex items-center gap-6">
                    <div className="flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase font-black letter tracking-widest">Temporal Gen</span>
                        <span className="text-xl font-mono font-bold text-white">G{history.length > 0 ? history[history.length - 1].generation : 0}</span>
                    </div>
                    <div className="w-px h-8 bg-slate-800"></div>
                    <div className="flex flex-col">
                        <span className="text-[10px] text-slate-500 uppercase font-black letter tracking-widest">Pending Proposals</span>
                        <span className="text-xl font-mono font-bold text-amber-400">{pendingDecrees.length}</span>
                    </div>
                </div>
                
                <button 
                    onClick={triggerEvolution}
                    disabled={isEvolving || isLocked}
                    className={`group flex items-center gap-3 px-8 py-3 rounded-xl font-black transition-all transform active:scale-95 ${
                        isEvolving || isLocked
                        ? 'bg-slate-800 text-slate-500 cursor-not-allowed opacity-50' 
                        : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-xl shadow-indigo-500/20'
                    }`}
                >
                    <Zap className={`w-5 h-5 ${isEvolving ? 'animate-bounce' : 'group-hover:rotate-12 transition-transform'}`} />
                    {isEvolving ? 'INITIATING DGM...' : 'PROPOSE EVOLUTION'}
                </button>
            </div>

            {activeRun && (
                <div className="mb-6 animate-in slide-in-from-top-4 duration-500">
                    <div className="bg-indigo-950/20 border border-indigo-500/30 rounded-xl p-4 flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className="w-3 h-3 rounded-full bg-indigo-500 animate-ping" />
                            <span className="font-mono text-sm text-indigo-300 font-bold uppercase tracking-tighter">{activeRun}</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Main Content Area */}
            <div className="flex-grow min-h-0">
                {viewMode === 'registry' && (
                    <div className="space-y-4 overflow-y-auto max-h-[450px] pr-2 custom-scrollbar">
                        <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
                             <Gavel className="w-4 h-4" /> Royal Decree Registry
                        </h3>
                        {pendingDecrees.length === 0 ? (
                            <div className="text-center py-20 bg-slate-900/20 border-2 border-dashed border-slate-800 rounded-2xl flex flex-col items-center gap-4">
                                <Shield className="w-12 h-12 text-slate-800" />
                                <p className="text-slate-500 italic font-serif">No pending decrees require the Commander's seal.</p>
                            </div>
                        ) : (
                            pendingDecrees.map((decree) => (
                                <div key={decree.run_id} className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-xl p-6 transition-all group shadow-lg">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-grow">
                                            <div className="flex items-center gap-3 mb-2">
                                                <span className="px-2 py-0.5 bg-amber-500/10 border border-amber-500/20 text-amber-500 text-[10px] font-black rounded uppercase">Proposal</span>
                                                <span className="text-[10px] font-mono text-slate-500">{decree.run_id}</span>
                                            </div>
                                            <h4 className="text-lg font-bold text-white mb-4 group-hover:text-indigo-300 transition-colors capitalize">
                                                {decree.modifications[0]}
                                            </h4>
                                            
                                            <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
                                                <div className="flex items-center gap-1.5 bg-slate-800/50 px-2.5 py-1 rounded">
                                                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                                                    Predicted Impact: <span className="text-emerald-400 font-bold">+{(decree.trinity_score * 10).toFixed(2)} pts</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex flex-col gap-2">
                                            <button 
                                                onClick={() => handleDecree(decree.run_id, 'seal')}
                                                className="flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white font-black px-6 py-2.5 rounded-lg shadow-lg shadow-emerald-900/20 transition-all active:scale-95"
                                            >
                                                <Check className="w-4 h-4" /> SEAL
                                            </button>
                                            <button 
                                                onClick={() => handleDecree(decree.run_id, 'veto')}
                                                className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-red-900/50 hover:text-red-400 text-slate-400 font-black px-6 py-2.5 rounded-lg transition-all"
                                            >
                                                <X className="w-4 h-4" /> VETO
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                )}

                {viewMode === 'stats' && (
                    <div className="h-full flex flex-col gap-6">
                        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 flex-grow min-h-[300px]">
                            <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-8 flex items-center gap-2">
                                 <TrendingUp className="w-4 h-4" /> Trinity Force Trend (Generational Growth)
                            </h3>
                            <div className="w-full h-[250px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={chartData}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                        <XAxis 
                                            dataKey="gen" 
                                            stroke="#64748b" 
                                            fontSize={10} 
                                            tickLine={false} 
                                            axisLine={false}
                                            dy={10}
                                        />
                                        <YAxis 
                                            stroke="#64748b" 
                                            fontSize={10} 
                                            tickLine={false} 
                                            axisLine={false}
                                            domain={[90, 100]}
                                            dx={-10}
                                        />
                                        <Tooltip 
                                            contentStyle={{ backgroundColor: '#020617', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '12px' }}
                                            itemStyle={{ color: '#818cf8', fontWeight: 'bold' }}
                                            labelStyle={{ color: '#64748b', marginBottom: '4px' }}
                                        />
                                        <Line 
                                            type="monotone" 
                                            dataKey="score" 
                                            stroke="#6366f1" 
                                            strokeWidth={3} 
                                            dot={{ r: 4, fill: '#6366f1', strokeWidth: 2, stroke: '#020617' }}
                                            activeDot={{ r: 6, fill: '#818cf8', strokeWidth: 0 }}
                                            animationDuration={1500}
                                        />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                )}

                {viewMode === 'history' && (
                    <div className="space-y-4 overflow-y-auto max-h-[450px] pr-2 custom-scrollbar">
                         <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
                             <History className="w-4 h-4" /> The Evolution Chronicle
                        </h3>
                        {history.sort((a,b) => b.generation - a.generation).map((step) => (
                            <div key={step.run_id} className="group relative bg-slate-900/60 hover:bg-slate-900 border border-slate-800/50 rounded-xl p-5 transition-all">
                                <div className="flex items-start justify-between">
                                    <div className="flex flex-col gap-2">
                                        <div className="flex items-center gap-3">
                                            <span className="px-2 py-0.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[10px] font-black rounded uppercase tracking-tighter">
                                                Gen {step.generation}
                                            </span>
                                            <span className={`px-2 py-0.5 text-[8px] font-black rounded uppercase tracking-widest ${
                                                step.decree_status === 'APPROVED' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 
                                                step.decree_status === 'REJECTED' ? 'bg-red-500/10 text-red-500 border border-red-500/20' :
                                                'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                                            }`}>
                                                {step.decree_status}
                                            </span>
                                            <span className="text-[10px] font-mono text-slate-600">{step.run_id}</span>
                                        </div>
                                        <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                                            {step.modifications[0]}
                                        </h3>
                                    </div>
                                    <div className="text-right">
                                        <div className="flex items-center gap-1.5 text-emerald-400 font-black">
                                            <Shield className="w-4 h-4" />
                                            <span className="text-lg">{(step.trinity_score * 100).toFixed(1)}</span>
                                        </div>
                                        <p className="text-[10px] text-slate-500 uppercase font-mono mt-1 opacity-60">
                                            {new Date(step.timestamp).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                                
                                <div className="mt-4 pt-4 border-t border-slate-800/50 flex items-center justify-between text-[10px] font-mono text-slate-600 uppercase font-bold tracking-tight">
                                    <div className="flex items-center gap-4">
                                        <span className="flex items-center gap-1.5 hover:text-slate-400 cursor-default transition-colors">
                                            <GitCommit className="w-3.5 h-3.5" />
                                            Parent: {step.parent_id?.slice(-6) || 'ORIGIN'}
                                        </span>
                                    </div>
                                    <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform text-slate-700" />
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <style jsx>{`
                .custom-scrollbar::-webkit-scrollbar {
                    width: 5px;
                }
                .custom-scrollbar::-webkit-scrollbar-track {
                    background: #020617;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb {
                    background: #1e293b;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb:hover {
                    background: #334155;
                }
            `}</style>
        </div>
    );
};
