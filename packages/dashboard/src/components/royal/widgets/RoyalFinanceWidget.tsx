"use client";

import React, { useEffect, useState } from "react";
import { CreditCard, DollarSign, TrendingUp, CheckCircle, AlertTriangle } from "lucide-react";

interface Transaction {
  id: string;
  merchant: string;
  amount: number;
  date: string;
  category: string;
}

interface ForecastPrediction {
  month: string;
  predicted: number;
  lower: number;
  upper: number;
}

interface ForecastSummary {
  total: number;
  average: number;
  confidence: number;
}

interface ForecastData {
  engine: string;
  summary: ForecastSummary;
  predictions: ForecastPrediction[];
  message: string;
  advice: string;
}

interface FinanceData {
  financial_health_score: number;
  monthly_spending: number;
  budget_remaining: number;
  recent_transactions: Transaction[];
  forecast?: ForecastData;
  advice: string;
}

export default function RoyalFinanceWidget() {
  const [data, setData] = useState<FinanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [approving, setApproving] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const res = await fetch("/api/proxy/julie/dashboard");
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (error) {
      console.error("Failed to fetch finance data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const handleApprove = async (txId: string) => {
    setApproving(txId);
    try {
      const res = await fetch(`/api/proxy/julie/transaction/approve?tx_id=${txId}`, {
        method: "POST",
      });
      if (res.ok) {
        // Optimistic update: remove from list (if it was a pending list, but here we just show visual feedback)
        alert(`Transaction ${txId} Approved!`);
        fetchData(); // Refresh data
      }
    } catch (error) {
      console.error("Approval failed", error);
    } finally {
      setApproving(null);
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center text-emerald-400 animate-pulse">
        <DollarSign className="w-8 h-8" />
      </div>
    );
  }

  if (!data) return null;

  const budgetTotal = data.monthly_spending + data.budget_remaining;
  const spendPercent = Math.min((data.monthly_spending / budgetTotal) * 100, 100);

  return (
    <div className="h-full flex flex-col space-y-4 p-4 text-white">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-emerald-300 flex items-center gap-2">
          <DollarSign className="w-5 h-5" />
          Royal Financier
        </h3>
        <span className={`text-xs px-2 py-1 rounded-full border ${
          data.financial_health_score > 80 
            ? "border-emerald-500 text-emerald-300 bg-emerald-950/30" 
            : "border-amber-500 text-amber-300 bg-amber-950/30"
        }`}>
          Health: {Math.round(data.financial_health_score)}/100
        </span>
      </div>

      {/* Budget Pulse */}
      <div className="space-y-1">
        <div className="flex justify-between text-xs text-gray-400">
          <span>Spent: ${data.monthly_spending.toLocaleString()}</span>
          <span>Budget: ${budgetTotal.toLocaleString()}</span>
        </div>
        <div className="h-2 w-full bg-gray-800 rounded-full overflow-hidden border border-white/5">
          <div 
            className={`h-full transition-all duration-1000 ${
              spendPercent > 90 ? "bg-red-500" : spendPercent > 75 ? "bg-amber-500" : "bg-emerald-500"
            }`}
            style={{ width: `${spendPercent}%` }}
          />
        </div>
      </div>

      {/* Forecast Section (Prophet) */}
      {data.forecast && (
        <div className="bg-white/5 rounded-lg p-3 border border-white/10 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-200">
            <span className="flex items-center gap-1 font-bold">
              <TrendingUp className="w-3 h-3" />
              Oracle Forecast (3 Mo)
            </span>
            <span>{data.forecast.message.split('(')[1]?.replace(')', '') || 'Confidence High'}</span>
          </div>
          <div className="grid grid-cols-3 gap-2 text-center text-xs">
            {data.forecast.predictions.slice(0, 3).map((pred) => (
              <div key={pred.month} className="bg-black/20 p-1 rounded">
                <div className="text-gray-400 text-[10px]">{pred.month}</div>
                <div className="font-mono text-emerald-300">${(pred.predicted / 1000).toFixed(1)}k</div>
              </div>
            ))}
          </div>
          <div className="text-[10px] text-gray-400 italic border-l-2 border-emerald-500/30 pl-2">
            "{data.forecast.advice || "Spend wisely, my lord."}"
          </div>
        </div>
      )}

      {/* Transaction Queue */}
      <div className="flex-1 overflow-auto space-y-2 min-h-0 custom-scrollbar pr-1">
        <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 sticky top-0 bg-black/80 backdrop-blur-sm py-1 z-10">
          Pending Approvals
        </h4>
        {data.recent_transactions.map((tx) => (
          <div key={tx.id} className="group flex items-center justify-between bg-white/5 hover:bg-white/10 p-2 rounded-md border border-white/5 transition-all">
            <div className="flex items-center gap-3">
              <div className="bg-gray-800 p-1.5 rounded-full text-gray-300 group-hover:bg-emerald-900 group-hover:text-emerald-300 transition-colors">
                <CreditCard className="w-4 h-4" />
              </div>
              <div>
                <div className="text-sm font-medium text-gray-200">{tx.merchant}</div>
                <div className="text-[10px] text-gray-500">{tx.category} • {tx.date}</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm font-mono text-white">${tx.amount.toLocaleString()}</span>
              <button 
                onClick={() => handleApprove(tx.id)}
                disabled={approving === tx.id}
                className="p-1.5 rounded-full hover:bg-emerald-500/20 text-gray-400 hover:text-emerald-400 transition-all disabled:opacity-50"
                title="Approve Transaction"
              >
                {approving === tx.id ? (
                  <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <CheckCircle className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
