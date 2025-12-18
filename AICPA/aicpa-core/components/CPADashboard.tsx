// AICPA/aicpa-core/components/CPADashboard.tsx
import React, { useEffect, useState } from 'react';
import { Shield, TrendingUp, AlertTriangle, CheckCircle, DollarSign, Activity } from 'lucide-react';
import { JulieService, JulieStatusResponse } from '../services/julieService';

export const CPADashboard: React.FC = () => {
    const [status, setStatus] = useState<JulieStatusResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const data = await JulieService.getStatus();
            setStatus(data);
            setLoading(false);
        };
        fetchData();
        // Poll every 10 seconds for real-time updates (like SSE simulation)
        const interval = setInterval(fetchData, 10000);
        return () => clearInterval(interval);
    }, []);

    if (loading && !status) {
        return <div className="p-8 text-center text-slate-500 animate-pulse">Connecting to Julie CPA Engine...</div>;
    }

    if (!status) return null;

    // Parse advice into lines if it's a single string
    const adviceLines = status.advice.split('\n').map(s => s.trim()).filter(s => s.length > 0);

    return (
        <div className="max-w-6xl mx-auto space-y-8 animate-fade-in p-2">
            
            {/* Header / Engine Status */}
            <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-emerald-100 text-emerald-700 rounded-xl">
                            <Shield size={24} />
                        </div>
                        <h1 className="text-2xl font-bold text-slate-900">Julie CPA AutoMate</h1>
                    </div>
                    <p className="text-slate-500">Your Personal AI CFO for Los Angeles, CA</p>
                </div>
                <div className="flex items-center gap-4">
                     <div className={`px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2 ${status.status.includes('활성화') ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'}`}>
                        <Activity size={16} />
                        {status.status}
                     </div>
                     <div className="px-4 py-2 bg-blue-50 text-blue-700 rounded-full text-sm font-bold flex items-center gap-2">
                        <CheckCircle size={16} />
                        Mock TXs: {status.dry_run_tx_count}
                     </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                
                {/* Left Column: Financial Health & Budget */}
                <div className="space-y-8">
                    {/* Budget Card (Mock Visualization based on Backend State) */}
                    <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-8 opacity-5">
                            <DollarSign size={120} />
                        </div>
                        <h2 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
                            <TrendingUp size={20} className="text-amber-500"/> 
                            Monthly Burn Rate (USD)
                        </h2>
                        
                        <div className="space-y-6 relative z-10">
                            <div>
                                <div className="flex justify-between text-sm font-medium mb-2">
                                    <span className="text-slate-500">Current Spend</span>
                                    <span className="text-rose-600 font-bold">$4,200.00</span>
                                </div>
                                <div className="h-4 bg-slate-100 rounded-full overflow-hidden">
                                    <div className="h-full bg-rose-500 w-[100%] rounded-full relative">
                                        <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                                    </div>
                                </div>
                                <p className="text-xs text-rose-500 mt-2 font-medium">⚠️ 20% Over Budget ($3,500 Limit)</p>
                            </div>
                            
                            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                                <h3 className="text-sm font-bold text-slate-700 mb-2">Category Breakdown (Top 3)</h3>
                                <div className="space-y-2">
                                    <div className="flex justify-between text-xs">
                                        <span>Dining (Restaurants)</span>
                                        <span className="font-mono">$1,850</span>
                                    </div>
                                    <div className="flex justify-between text-xs">
                                        <span>Rent/Utilities</span>
                                        <span className="font-mono">$1,200</span>
                                    </div>
                                    <div className="flex justify-between text-xs">
                                        <span>Shopping</span>
                                        <span className="font-mono">$800</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Risk Alerts */}
                    <div className="bg-white rounded-3xl p-8 border border-red-100 shadow-sm shadow-red-50">
                        <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <AlertTriangle size={20} className="text-rose-500"/> 
                            Risk Alerts
                        </h2>
                        <div className="space-y-3">
                            {status.alerts.length > 0 ? (
                                status.alerts.map((alert, idx) => (
                                    <div key={idx} className="p-4 bg-rose-50 border border-rose-100 rounded-xl text-rose-700 text-sm font-medium flex items-start gap-3">
                                        <AlertTriangle size={16} className="mt-0.5 shrink-0" />
                                        {alert}
                                    </div>
                                ))
                            ) : (
                                <div className="p-4 bg-emerald-50 text-emerald-700 rounded-xl text-sm font-medium">
                                    ✅ No active risks detected.
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Column: Personalized Advice */}
                <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-8 text-white shadow-xl flex flex-col">
                    <h2 className="text-lg font-bold mb-6 flex items-center gap-2 text-amber-300">
                        <Shield size={20}/>
                        Julie's Strategic Advice
                    </h2>
                    
                    <div className="flex-1 space-y-4">
                         {adviceLines.map((line, idx) => (
                             <div key={idx} className="p-5 bg-white/10 rounded-2xl backdrop-blur-sm border border-white/5 hover:bg-white/15 transition-colors">
                                 <p className="text-sm leading-relaxed font-medium text-slate-100">
                                     {line}
                                 </p>
                             </div>
                         ))}
                    </div>

                    <div className="mt-8 pt-6 border-t border-white/10 flex justify-between items-center text-xs text-slate-400">
                        <span>Powered by Soul Engine (Vault Secured)</span>
                        <span>v1.0.0</span>
                    </div>
                </div>

            </div>
        </div>
    );
};
