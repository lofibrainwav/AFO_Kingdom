'use client';

import React, { useState, useEffect, useCallback } from 'react';
import FinancialHealthDial from '@/components/julie/FinancialHealthDial';
import TransactionLedger from '@/components/julie/TransactionLedger';
import ApprovalQueue from '@/components/julie/ApprovalQueue';
import { Briefcase, Building2, Coins, AlertTriangle, RefreshCw } from 'lucide-react';

interface CPADashboardProps {
    // GenUI: Props for Flexibility
}

export default function CPADashboard({}: CPADashboardProps) {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    // Mock Fallback Data (GenUI Safe Mode)
    const mockData = {
        financial_health_score: 85,
        monthly_spending: 0,
        budget_remaining: 0,
        recent_transactions: [],
        risk_alerts: [],
        advice: "Loading Royal Strategies..."
    };

    const fetchData = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            // GenUI: Connect to Backend (Vault Integrated) via Proxy
            // Port 8011 is targeted via next.config.ts proxy
            const res = await fetch('/api/proxy/api/julie/dashboard');
            if (!res.ok) throw new Error(`Failed to fetch dashboard data: ${res.statusText}`);
            const jsonData = await res.json();
            setData(jsonData);
        } catch (err) {
            console.error("GenUI Fetch Error:", err);
            setError("Backend Sync Failed (Using Cached Royal Data)");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const displayData = data || mockData;

    return (
        <div className="min-h-screen bg-[#050505] text-white p-6 relative font-sans">
            {/* GenUI Aesthetic Layer */}
             <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none"></div>

            <div className="max-w-7xl mx-auto relative z-10">
                {/* Header Section */}
                <div className="flex justify-between items-center mb-8 bg-[#0A0F1C]/80 backdrop-blur-md p-4 rounded-2xl border border-gray-800 shadow-xl">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-amber-500/10 rounded-xl flex items-center justify-center border border-amber-500/20">
                            <Building2 className="w-6 h-6 text-amber-500" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-gray-100 tracking-tight">AICPA Julie's Office</h1>
                            <div className="flex items-center gap-2">
                                <p className="text-xs text-gray-500 uppercase tracking-widest">Royal Finance Department</p>
                                {loading && <span className="text-xs text-amber-500 animate-pulse">• Syncing...</span>}
                            </div>
                            <p className="text-xs text-emerald-400 mt-1 italic opacity-90">"{displayData.advice}"</p>
                        </div>
                    </div>
                     <button 
                        onClick={fetchData}
                        disabled={loading}
                        className={`p-2 bg-gray-800 rounded-lg hover:bg-gray-700 text-xs text-gray-400 border border-gray-700 transition-all ${loading ? 'opacity-50 cursor-not-allowed' : 'hover:text-white'}`}
                        title="Force Sync with Royal Vault"
                    >
                        <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                    </button>
                </div>

                {/* Risk Alerts (GenUI Addition) */}
                {displayData.risk_alerts && displayData.risk_alerts.length > 0 && (
                    <div className="mb-6 grid gap-2">
                        {displayData.risk_alerts.map((alert: any, i: number) => (
                            <div key={i} className={`p-3 rounded-lg border ${alert.level === 'warning' ? 'bg-red-500/5 border-red-500/20 text-red-300' : 'bg-blue-500/5 border-blue-500/20 text-blue-300'} flex items-center gap-3 shadow-sm`}>
                                <AlertTriangle className="w-4 h-4" />
                                <span className="text-sm font-medium">{alert.message}</span>
                            </div>
                        ))}
                    </div>
                )}


                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {/* Left Column: Metrics */}
                    <div className="lg:col-span-1 space-y-6">
                        <FinancialHealthDial 
                            score={displayData.financial_health_score} 
                            trend={displayData.financial_health_score > 80 ? "up" : "down"}
                            risk_level={displayData.financial_health_score > 80 ? "low" : "medium"}
                        />
                        
                        <div className="bg-[#0A0F1C] border border-gray-800 rounded-2xl p-6 space-y-4 shadow-lg">
                            <div>
                                <div className="text-xs text-gray-500 mb-1 font-medium">Monthly Spending</div>
                                <div className="text-xl font-mono text-white tracking-wider">₩ {displayData.monthly_spending?.toLocaleString()}</div>
                            </div>
                             <div>
                                <div className="text-xs text-gray-500 mb-1 font-medium">Budget Remaining</div>
                                <div className="text-xl font-mono text-emerald-400 tracking-wider">₩ {displayData.budget_remaining?.toLocaleString()}</div>
                            </div>
                        </div>

                        {/* Approvals (Mock for now as backend endpoint might verify in future) */}
                         <div className="bg-[#0A0F1C] border border-gray-800 rounded-2xl p-4 shadow-lg">
                            <h3 className="text-sm font-bold text-gray-400 mb-3 border-b border-gray-800 pb-2">Pending Approvals</h3>
                            <div className="space-y-2">
                                <div className="p-3 bg-gray-900/50 rounded-lg border border-gray-800 text-xs hover:border-gray-700 transition-colors cursor-pointer">
                                    <div className="flex justify-between text-gray-300 font-bold mb-1">GPU Server</div>
                                    <div className="text-right text-gray-500 font-mono">₩ 1.2M</div>
                                </div>
                            </div>
                         </div>
                    </div>

                    {/* Right Column: Ledger */}
                    <div className="lg:col-span-3">
                        <TransactionLedger transactions={displayData.recent_transactions || []} />
                    </div>
                </div>
            </div>
            {error && (
                <div className="fixed bottom-4 right-4 bg-red-900/80 text-white px-4 py-2 rounded-lg text-xs backdrop-blur-sm border border-red-700/50">
                    {error}
                </div>
            )}
        </div>
    );
}
