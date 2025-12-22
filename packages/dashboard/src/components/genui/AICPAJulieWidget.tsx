'use client';

import React, { useEffect, useState } from 'react';
import { Shield, TrendingUp, AlertTriangle, CreditCard, PieChart } from 'lucide-react';
import { logError } from '@/lib/logger';

interface Transaction {
  id: string;
  merchant: string;
  amount: number;
  date: string;
  category: string;
}

interface FinanceData {
  financial_health_score: number;
  monthly_spending: number;
  budget_remaining: number;
  recent_transactions: Transaction[];
  risk_alerts: { level: 'warning' | 'info'; message: string }[];
  advice: string;
}

export function AICPAJulieWidget() {
  const [data, setData] = useState<FinanceData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/finance/dashboard')
      .then(res => res.json())
      .then(setData)
      .catch((err) => logError('Failed to fetch AICPA Julie data', { error: err instanceof Error ? err.message : 'Unknown error' }))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="w-full h-64 flex items-center justify-center text-gold-400 animate-pulse bg-black/40 rounded-xl border border-white/10">
        <Shield className="w-8 h-8 mr-2" />
        <span className="font-mono">Connecting to Royal Ledger...</span>
      </div>
    );
  }


  return (
    <div className="w-full bg-black/40 backdrop-blur-md border border-white/10 rounded-2xl p-6 shadow-2xl overflow-hidden relative">
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-600 via-yellow-400 to-yellow-600 opacity-50" />
      
      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-yellow-900/20 rounded-xl border border-yellow-500/30">
            <Shield className="w-6 h-6 text-yellow-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-wide">Julie CPA</h2>
            <p className="text-xs text-yellow-500/60 font-mono uppercase tracking-widest">Royal Financial Guardian</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-white font-mono">
            {data.financial_health_score}
          </div>
          <div className="text-xs text-white/40 uppercase tracking-wider">Health Score</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Left Column: Metrics */}
        <div className="space-y-4">
          <div className="bg-white/5 rounded-xl p-4 border border-white/5 hover:border-white/10 transition-colors">
            <div className="text-xs text-white/40 mb-1 flex items-center gap-2">
              <CreditCard className="w-3 h-3" /> Monthly Spending
            </div>
            <div className="text-lg font-mono text-white">
              ₩{data.monthly_spending.toLocaleString()}
            </div>
            <div className="text-xs text-white/20 mt-1">Target: ₩3,000,000</div>
          </div>

          <div className="bg-white/5 rounded-xl p-4 border border-white/5 hover:border-white/10 transition-colors">
            <div className="text-xs text-white/40 mb-1 flex items-center gap-2">
              <PieChart className="w-3 h-3" /> Budget Remaining
            </div>
            <div className="text-lg font-mono text-emerald-400">
              ₩{data.budget_remaining.toLocaleString()}
            </div>
          </div>
         
         {/* Strategic Advice (AI) */}
         <div className="bg-gradient-to-br from-indigo-900/20 to-purple-900/20 rounded-xl p-4 border border-indigo-500/20">
            <div className="text-xs text-indigo-300 mb-2 flex items-center gap-2 font-bold uppercase tracking-wider">
               <TrendingUp className="w-3 h-3" /> Strategic Counsel
            </div>
            <p className="text-sm text-indigo-100 italic">
              "{data.advice}"
            </p>
         </div>

        </div>

        {/* Middle Column: Transactions */}
        <div className="md:col-span-2 bg-black/20 rounded-xl border border-white/5 p-4 flex flex-col h-[300px]">
          <h3 className="text-xs font-bold text-white/60 uppercase tracking-wider mb-4 flex justify-between items-center">
            <span>Recent Transactions</span>
            <span className="text-[10px] bg-white/10 px-2 py-1 rounded text-white/40">LIVE SYNC</span>
          </h3>
          
          <div className="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
            {data.recent_transactions.map((tx) => (
              <div key={tx.id} className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/5 hover:bg-white/10 transition-colors group">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-white/40 group-hover:text-white/80 transition-colors">
                     {tx.category === 'Food' ? '☕' : tx.category === 'Infrastructure' ? '☁️' : '💳'}
                  </div>
                  <div>
                    <div className="text-sm text-white font-medium">{tx.merchant}</div>
                    <div className="text-xs text-white/30">{tx.date} • {tx.category}</div>
                  </div>
                </div>
                <div className="text-sm font-mono text-white/80">
                  -₩{tx.amount.toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Footer: Alerts */}
      {data.risk_alerts.length > 0 && (
          <div className="mt-6 flex gap-3 overflow-x-auto pb-2">
             {data.risk_alerts.map((alert, i) => (
                 <div key={i} className={`flex-shrink-0 px-3 py-2 rounded-lg border text-xs flex items-center gap-2 ${
                     alert.level === 'warning' 
                     ? 'bg-red-500/10 border-red-500/20 text-red-200' 
                     : 'bg-blue-500/10 border-blue-500/20 text-blue-200'
                 }`}>
                     <AlertTriangle className="w-3 h-3" />
                     {alert.message}
                 </div>
             ))}
          </div>
      )}
    </div>
  );
}
