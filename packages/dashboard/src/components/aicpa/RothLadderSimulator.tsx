'use client';

/**
 * Roth Ladder Simulator Widget
 *
 * 정밀 Roth Ladder 시뮬레이션
 * Bracket 기반 세금 계산 + 복리 성장 + 미래 절세 예측
 *
 * 眞 (Truth): 2025 OBBBA bracket 정확 반영
 * 美 (Beauty): 직관적인 슬라이더 UI
 * 永 (Eternity): 장기 부의 증식 전략
 */

import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  DollarSign,
  Calendar,
  Sparkles,
  RefreshCw,
  Shield,
  ChevronRight
} from 'lucide-react';
import { logError } from '@/lib/logger';

interface RothResult {
  strategy: string;
  total_converted: number;
  total_tax_paid: number;
  estimated_savings: number;
  summary: string;
  years: Array<{
    year: number;
    conversion_amount: number;
    tax_paid: number;
    remaining_ira: number;
    marginal_rate: number;
  }>;
}

import { API_BASE_URL } from '@/lib/constants';
const API_BASE = API_BASE_URL;

export const RothLadderSimulator: React.FC = () => {
  // Form State
  const [iraBalance, setIraBalance] = useState(600000);
  const [currentIncome, setCurrentIncome] = useState(180000);
  const [filingStatus, setFilingStatus] = useState('mfj');
  const [years, setYears] = useState(4);

  // Result State
  const [result, setResult] = useState<RothResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Simulate
  const runSimulation = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/api/aicpa/roth-ladder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ira_balance: iraBalance,
          filing_status: filingStatus,
          current_income: currentIncome,
          years: years,
        }),
      });

      if (!response.ok) throw new Error('API Error');

      const data = await response.json();
      setResult(data.strategy);
    } catch (e) {
      setError('시뮬레이션 실패 - 서버 상태를 확인하세요');
      logError('[RothLadder] Error', { error: e instanceof Error ? e.message : 'Unknown error' });
    } finally {
      setLoading(false);
    }
  };

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="bg-gradient-to-br from-purple-900/20 to-emerald-900/20 backdrop-blur-xl rounded-3xl border border-purple-500/30 shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-emerald-600 p-6 text-white">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-white/20 rounded-xl">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Roth Ladder 시뮬레이터</h2>
            <p className="text-purple-100 text-sm">OBBBA 기간 최적 전환 전략</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Filing Status */}
        <div>
          <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Filing Status</label>
          <div className="grid grid-cols-2 gap-2">
            {[
              { value: 'single', label: 'Single' },
              { value: 'mfj', label: 'Married (MFJ)' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => setFilingStatus(opt.value)}
                className={`py-2 px-3 rounded-xl text-sm font-bold transition-all ${
                  filingStatus === opt.value
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* IRA Balance Slider */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-400 uppercase flex items-center gap-1">
              <DollarSign className="w-3 h-3" /> Traditional IRA Balance
            </label>
            <span className="text-lg font-bold text-white">{formatCurrency(iraBalance)}</span>
          </div>
          <input
            type="range"
            min={100000}
            max={2000000}
            step={10000}
            value={iraBalance}
            onChange={(e) => setIraBalance(parseInt(e.target.value))}
            className="w-full h-2 bg-white/20 rounded-full appearance-none cursor-pointer accent-purple-500"
          />
          <div className="flex justify-between text-xs text-slate-500 mt-1">
            <span>$100k</span>
            <span>$2M</span>
          </div>
        </div>

        {/* Current Income Slider */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-400 uppercase">Current Income</label>
            <span className="text-lg font-bold text-white">{formatCurrency(currentIncome)}</span>
          </div>
          <input
            type="range"
            min={50000}
            max={400000}
            step={5000}
            value={currentIncome}
            onChange={(e) => setCurrentIncome(parseInt(e.target.value))}
            className="w-full h-2 bg-white/20 rounded-full appearance-none cursor-pointer accent-emerald-500"
          />
        </div>

        {/* Conversion Years */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-400 uppercase flex items-center gap-1">
              <Calendar className="w-3 h-3" /> Conversion Years
            </label>
            <span className="text-lg font-bold text-amber-400">{years} years</span>
          </div>
          <input
            type="range"
            min={2}
            max={10}
            step={1}
            value={years}
            onChange={(e) => setYears(parseInt(e.target.value))}
            className="w-full h-2 bg-white/20 rounded-full appearance-none cursor-pointer accent-amber-500"
          />
          <div className="flex justify-between text-xs text-slate-500 mt-1">
            <span>2 yrs</span>
            <span className="text-amber-400 font-bold">OBBBA: 4 yrs</span>
            <span>10 yrs</span>
          </div>
        </div>

        {/* Simulate Button */}
        <button
          onClick={runSimulation}
          disabled={loading}
          className="w-full py-4 bg-gradient-to-r from-purple-600 to-emerald-600 text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-purple-500/30 transition-all disabled:opacity-50"
        >
          {loading ? (
            <RefreshCw className="w-5 h-5 animate-spin" />
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Run Roth Ladder Simulation
            </>
          )}
        </button>

        {/* Error */}
        {error && (
          <div className="p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300 text-sm">
            {error}
          </div>
        )}

        {/* Results */}
        {result && !error && (
          <div className="space-y-4 pt-4">
            {/* Savings Hero */}
            <div className="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-2xl p-6 text-white text-center relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2" />
              <div className="relative z-10">
                <div className="text-emerald-100 text-sm mb-1">Estimated Tax Savings</div>
                <div className="text-4xl font-black">{formatCurrency(result.estimated_savings)}</div>
                <div className="text-emerald-200 text-sm mt-2 flex items-center justify-center gap-1">
                  <Shield className="w-4 h-4" />
                  미래 tax-free 인출 가능
                </div>
              </div>
            </div>

            {/* Summary Stats */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                <div className="text-xs text-slate-400 uppercase">Total Converted</div>
                <div className="text-xl font-bold text-white">{formatCurrency(result.total_converted)}</div>
              </div>
              <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                <div className="text-xs text-slate-400 uppercase">Tax Paid (Ladder)</div>
                <div className="text-xl font-bold text-amber-400">{formatCurrency(result.total_tax_paid)}</div>
              </div>
            </div>

            {/* Year-by-Year Breakdown */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <div className="text-sm font-bold text-slate-300 mb-3 flex items-center gap-2">
                <Calendar className="w-4 h-4 text-purple-400" />
                Year-by-Year Conversion Plan
              </div>
              <div className="space-y-2">
                {result.years.map((yr, idx) => (
                  <div key={yr.year} className="flex items-center justify-between p-2 bg-white/5 rounded-lg">
                    <div className="flex items-center gap-3">
                      <span className="w-12 h-8 bg-purple-600/30 rounded flex items-center justify-center text-purple-300 text-sm font-bold">
                        {yr.year}
                      </span>
                      <ChevronRight className="w-4 h-4 text-slate-500" />
                      <span className="text-white font-medium">{formatCurrency(yr.conversion_amount)}</span>
                    </div>
                    <div className="text-right">
                      <div className="text-amber-400 text-sm font-bold">{formatCurrency(yr.tax_paid)} tax</div>
                      <div className="text-xs text-slate-500">{(yr.marginal_rate * 100).toFixed(0)}% bracket</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Summary */}
            <div className="p-4 bg-slate-900/50 rounded-xl text-center">
              <p className="text-slate-300 text-sm">{result.summary}</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="px-6 py-3 bg-black/30 text-center">
        <p className="text-white/50 text-xs italic">
          "Julie CPA가 최적 전략 제안해요 – 미래 tax-free 인출로 왕국 부 지키세요 ✨"
        </p>
      </div>
    </div>
  );
};

export default RothLadderSimulator;
