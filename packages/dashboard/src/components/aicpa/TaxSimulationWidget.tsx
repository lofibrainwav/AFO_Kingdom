'use client';

/**
 * AICPA Tax Simulation Widget
 *
 * 실시간 세금 시뮬레이션 위젯
 * 슬라이더 조작으로 세금 계산 결과 즉시 확인
 *
 * 眞 (Truth): 정확한 2025 OBBBA 세법 기반
 * 美 (Beauty): 직관적인 슬라이더 UI
 * 孝 (Serenity): Zero Friction - 마찰 없는 경험
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Calculator,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  RefreshCw,
  Sparkles
} from 'lucide-react';
import { logError } from '@/lib/logger';

interface TaxResult {
  filing_status: string;
  gross_income: number;
  taxable_income: number;
  federal_tax: number;
  effective_federal_rate: number;
  marginal_bracket: number;
  state_tax: number;
  total_tax: number;
  after_tax_income: number;
  sweet_spot_headroom: number;
  roth_conversion_recommendation: number;
  irmaa_warning: boolean;
  advice: string;
}

import { API_BASE_URL } from '@/lib/constants';
const API_BASE = API_BASE_URL;

export const TaxSimulationWidget: React.FC = () => {
  // Form State
  const [filingStatus, setFilingStatus] = useState('mfj');
  const [grossIncome, setGrossIncome] = useState(180000);
  const [iraBalance, setIraBalance] = useState(600000);
  const [rothConversion, setRothConversion] = useState(0);

  // Result State
  const [result, setResult] = useState<TaxResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Debounced API Call
  const simulateTax = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/api/aicpa/tax-simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filing_status: filingStatus,
          gross_income: grossIncome,
          ira_balance: iraBalance,
          roth_conversion: rothConversion,
          state: 'CA',
        }),
      });

      if (!response.ok) throw new Error('API Error');

      const data = await response.json();
      setResult(data.simulation);
    } catch (err) {
      setError('연결 실패 - 서버 상태를 확인하세요');
      logError('Tax simulation failed', { error: err instanceof Error ? err.message : 'Unknown error' });
    } finally {
      setLoading(false);
    }
  }, [filingStatus, grossIncome, iraBalance, rothConversion]);

  // Auto-simulate on mount
  useEffect(() => {
    simulateTax();
    }, [simulateTax]); // Added simulateTax dependency

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Calculate slider position for visual feedback
  const getProgressColor = (rate: number) => {
    if (rate <= 12) return 'bg-emerald-500';
    if (rate <= 22) return 'bg-amber-500';
    return 'bg-rose-500';
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 p-6 text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-emerald-500/20 rounded-xl">
              <Calculator className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <h2 className="text-xl font-bold">2025 OBBBA Tax Simulator</h2>
              <p className="text-slate-400 text-sm">Real-time calculation</p>
            </div>
          </div>
          <button
            onClick={simulateTax}
            disabled={loading}
            className="p-2 bg-white/10 hover:bg-white/20 rounded-xl transition-colors"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Filing Status */}
        <div>
          <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Filing Status</label>
          <div className="grid grid-cols-4 gap-2">
            {[
              { value: 'single', label: 'Single' },
              { value: 'mfj', label: 'MFJ' },
              { value: 'mfs', label: 'MFS' },
              { value: 'hoh', label: 'HOH' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => setFilingStatus(opt.value)}
                className={`py-2 px-3 rounded-xl text-sm font-bold transition-all ${
                  filingStatus === opt.value
                    ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/30'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Income Slider */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Gross Income</label>
            <span className="text-lg font-bold text-slate-800">{formatCurrency(grossIncome)}</span>
          </div>
          <input
            type="range"
            min={50000}
            max={500000}
            step={5000}
            value={grossIncome}
            onChange={(e) => setGrossIncome(parseInt(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-full appearance-none cursor-pointer slider-thumb"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>$50k</span>
            <span>$500k</span>
          </div>
        </div>

        {/* IRA Balance Slider */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Traditional IRA</label>
            <span className="text-lg font-bold text-slate-800">{formatCurrency(iraBalance)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={2000000}
            step={10000}
            value={iraBalance}
            onChange={(e) => setIraBalance(parseInt(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-full appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>$0</span>
            <span>$2M</span>
          </div>
        </div>

        {/* Roth Conversion Slider */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs font-bold text-slate-500 uppercase">Roth Conversion</label>
            <span className="text-lg font-bold text-emerald-600">{formatCurrency(rothConversion)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={Math.min(iraBalance, 200000)}
            step={5000}
            value={rothConversion}
            onChange={(e) => setRothConversion(parseInt(e.target.value))}
            className="w-full h-2 bg-emerald-100 rounded-full appearance-none cursor-pointer"
          />
        </div>

        {/* Simulate Button */}
        <button
          onClick={simulateTax}
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-2xl font-bold text-sm flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-emerald-500/30 transition-all disabled:opacity-50"
        >
          {loading ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <Sparkles className="w-4 h-4" />
          )}
          Calculate Tax
        </button>

        {/* Error State */}
        {error && (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-rose-700 text-sm">
            <AlertTriangle className="w-4 h-4 inline mr-2" />
            {error}
          </div>
        )}

        {/* Results */}
        {result && !error && (
          <div className="space-y-4 pt-4 border-t border-slate-100">
            {/* Tax Summary */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-50 rounded-2xl p-4">
                <div className="text-xs text-slate-500 uppercase mb-1">Federal Tax</div>
                <div className="text-xl font-bold text-slate-800">{formatCurrency(result.federal_tax)}</div>
                <div className="text-xs text-slate-400">{result.effective_federal_rate}% effective</div>
              </div>
              <div className="bg-slate-50 rounded-2xl p-4">
                <div className="text-xs text-slate-500 uppercase mb-1">CA State Tax</div>
                <div className="text-xl font-bold text-slate-800">{formatCurrency(result.state_tax)}</div>
              </div>
            </div>

            {/* Total Tax */}
            <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-4 text-white">
              <div className="flex justify-between items-center">
                <span className="text-slate-300">Total Tax</span>
                <span className="text-2xl font-bold">{formatCurrency(result.total_tax)}</span>
              </div>
              <div className="flex justify-between items-center mt-2 pt-2 border-t border-white/10">
                <span className="text-slate-400">After-Tax Income</span>
                <span className="text-lg font-bold text-emerald-400">{formatCurrency(result.after_tax_income)}</span>
              </div>
            </div>

            {/* Marginal Bracket Indicator */}
            <div className="bg-slate-50 rounded-2xl p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs text-slate-500 uppercase">Marginal Bracket</span>
                <span className={`text-sm font-bold px-2 py-1 rounded-lg ${
                  result.marginal_bracket <= 0.12
                    ? 'bg-emerald-100 text-emerald-700'
                    : result.marginal_bracket <= 0.22
                    ? 'bg-amber-100 text-amber-700'
                    : 'bg-rose-100 text-rose-700'
                }`}>
                  {(result.marginal_bracket * 100).toFixed(0)}%
                </span>
              </div>
              <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className={`h-full ${getProgressColor(result.marginal_bracket * 100)} transition-all`}
                  style={{ width: `${result.marginal_bracket * 100 * 2.7}%` }}
                />
              </div>
            </div>

            {/* Sweet Spot Analysis */}
            {result.sweet_spot_headroom > 0 && (
              <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-emerald-600 mt-0.5" />
                  <div>
                    <div className="font-bold text-emerald-800">OBBBA Sweet Spot Available!</div>
                    <div className="text-sm text-emerald-700 mt-1">
                      {formatCurrency(result.sweet_spot_headroom)} headroom in 12% bracket
                    </div>
                    {result.roth_conversion_recommendation > 0 && (
                      <div className="text-sm text-emerald-600 mt-2 flex items-center gap-1">
                        <TrendingUp className="w-4 h-4" />
                        Recommended Roth Conversion: {formatCurrency(result.roth_conversion_recommendation)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* IRMAA Warning */}
            {result.irmaa_warning && (
              <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />
                  <div>
                    <div className="font-bold text-amber-800">IRMAA Warning</div>
                    <div className="text-sm text-amber-700 mt-1">
                      Income may trigger Medicare premium surcharge. Consider income smoothing.
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Julie's Advice */}
            <div className="bg-slate-900 text-white rounded-2xl p-4">
              <div className="flex items-center gap-2 mb-2 text-amber-400">
                <Sparkles className="w-4 h-4" />
                <span className="text-sm font-bold">Julie CPA Advice</span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{result.advice}</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 text-xs text-slate-400 text-center">
        Powered by AFO AICPA Agent Army | 2025 OBBBA Tax Regulations
      </div>
    </div>
  );
};

export default TaxSimulationWidget;
