"use client";

/**
 * Budget Prediction Widget (Prophet 기반)
 *
 * Phase 14: Julie CPA 미래 예측 위젯
 *
 * 眞 (Truth): Prophet 데이터 기반 정밀 예측
 * 美 (Beauty): 직관적인 차트 + 카드 UI
 * 孝 (Serenity): 형님 안심을 위한 명확한 결과
 */

import React, { useState, useEffect, useCallback } from "react";
import {
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  RefreshCw,
  Sparkles,
  Calendar,
  Shield,
} from "lucide-react";
import { logError } from "@/lib/logger";

interface Prediction {
  date: string;
  month: string;
  predicted: number;
  lower: number;
  upper: number;
  trend: number;
}

interface ForecastResult {
  engine: string;
  periods: number;
  predictions: Prediction[];
  summary: {
    total: number;
    average: number;
    confidence: number;
  };
  message: string;
  advice: string;
  kingdom_status: "healthy" | "monitoring";
  last_updated: string;
}

import { API_BASE_URL } from "@/lib/constants";
const API_BASE = API_BASE_URL;

export const BudgetPredictionWidget: React.FC = () => {
  const [periods, setPeriods] = useState(3);
  const [result, setResult] = useState<ForecastResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch forecast
  const fetchForecast = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/api/julie/budget/forecast?periods=${periods}`);

      if (!response.ok) throw new Error("API Error");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("예측 실패 - 서버 상태를 확인하세요");
      logError("Budget prediction failed", {
        error: err instanceof Error ? err.message : "Unknown error",
      });
    } finally {
      setLoading(false);
    }
  }, [periods]);

  // Auto-fetch on mount
  useEffect(() => {
    fetchForecast();
  }, [fetchForecast]); // Added fetchForecast dependency

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Get confidence color
  const getConfidenceColor = (conf: number) => {
    if (conf >= 80) return "text-emerald-400";
    if (conf >= 60) return "text-amber-400";
    return "text-rose-400";
  };

  // Get bar width for mini chart
  const getBarWidth = (value: number, max: number) => {
    return Math.min(100, (value / max) * 100);
  };

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl border border-emerald-500/30 shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-6 text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-white/20 rounded-xl">
              <TrendingUp className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold">Julie CPA Prophet 예측</h2>
              <p className="text-emerald-100 text-sm">미래 지출 자동 예측</p>
            </div>
          </div>
          <button
            onClick={fetchForecast}
            disabled={loading}
            className="p-2 bg-white/10 hover:bg-white/20 rounded-xl transition-colors"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Period Selector */}
        <div>
          <label className="block text-xs font-bold text-slate-400 uppercase mb-2">예측 기간</label>
          <div className="grid grid-cols-4 gap-2">
            {[1, 3, 6, 12].map((p) => (
              <button
                key={p}
                onClick={() => setPeriods(p)}
                className={`py-2 px-3 rounded-xl text-sm font-bold transition-all ${
                  periods === p
                    ? "bg-emerald-600 text-white"
                    : "bg-white/10 text-slate-300 hover:bg-white/20"
                }`}
              >
                {p}개월
              </button>
            ))}
          </div>
        </div>

        {/* Fetch Button */}
        <button
          onClick={fetchForecast}
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-2xl font-bold flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-emerald-500/30 transition-all disabled:opacity-50"
        >
          {loading ? (
            <RefreshCw className="w-5 h-5 animate-spin" />
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              예측 실행
            </>
          )}
        </button>

        {/* Error */}
        {error && (
          <div className="p-4 bg-rose-500/20 border border-rose-500/30 rounded-xl text-rose-300 text-sm flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            {error}
          </div>
        )}

        {/* Results */}
        {result && !error && (
          <div className="space-y-4">
            {/* Hero Stats */}
            <div className="bg-gradient-to-r from-emerald-600/20 to-teal-600/20 rounded-2xl p-6 border border-emerald-500/30">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="text-sm text-emerald-300 mb-1">
                    향후 {result.periods}개월 예상 지출
                  </div>
                  <div className="text-4xl font-black text-white">
                    {formatCurrency(result.summary.total)}
                  </div>
                </div>
                <div
                  className={`flex items-center gap-2 px-3 py-1 rounded-lg ${
                    result.kingdom_status === "healthy"
                      ? "bg-emerald-500/20 text-emerald-400"
                      : "bg-amber-500/20 text-amber-400"
                  }`}
                >
                  {result.kingdom_status === "healthy" ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    <AlertTriangle className="w-4 h-4" />
                  )}
                  <span className="text-sm font-bold">
                    {result.kingdom_status === "healthy" ? "Healthy" : "Monitoring"}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-black/20 rounded-xl p-3">
                  <div className="text-xs text-slate-400 uppercase">월 평균</div>
                  <div className="text-lg font-bold text-white">
                    {formatCurrency(result.summary.average)}
                  </div>
                </div>
                <div className="bg-black/20 rounded-xl p-3">
                  <div className="text-xs text-slate-400 uppercase">신뢰도</div>
                  <div
                    className={`text-lg font-bold ${getConfidenceColor(result.summary.confidence)}`}
                  >
                    {result.summary.confidence.toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>

            {/* Mini Chart */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <div className="flex items-center gap-2 mb-4 text-slate-300">
                <Calendar className="w-4 h-4 text-emerald-400" />
                <span className="text-sm font-bold">월별 예측</span>
                <span className="text-xs text-slate-500 ml-auto">{result.engine}</span>
              </div>

              <div className="space-y-3">
                {result.predictions.map((pred) => {
                  const maxValue = Math.max(...result.predictions.map((p) => p.upper));
                  return (
                    <div key={pred.month} className="space-y-1">
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-400">{pred.month}</span>
                        <span className="text-white font-bold">
                          {formatCurrency(pred.predicted)}
                        </span>
                      </div>
                      <div className="h-3 bg-slate-700 rounded-full overflow-hidden relative">
                        {/* Lower bound */}
                        <div
                          className="absolute h-full bg-emerald-900/50 rounded-full"
                          style={{ width: `${getBarWidth(pred.upper, maxValue)}%` }}
                        />
                        {/* Predicted */}
                        <div
                          className="absolute h-full bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full"
                          style={{ width: `${getBarWidth(pred.predicted, maxValue)}%` }}
                        />
                      </div>
                      <div className="flex justify-between text-xs text-slate-500">
                        <span>{formatCurrency(pred.lower)}</span>
                        <span>{formatCurrency(pred.upper)}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Advice */}
            <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-600/30">
              <div className="flex items-center gap-2 mb-2 text-amber-400">
                <Shield className="w-4 h-4" />
                <span className="text-sm font-bold">Julie's Advice</span>
              </div>
              <p className="text-slate-300 text-sm">{result.advice}</p>
            </div>

            {/* Message */}
            <div className="text-center p-3 bg-black/20 rounded-xl">
              <p className="text-emerald-300 text-sm italic">{result.message}</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="px-6 py-3 bg-black/30 text-center">
        <p className="text-white/50 text-xs italic">
          "Prophet가 왕국 지출 미래를 보여줘요 – 형님 안심하세요 ✨"
        </p>
      </div>
    </div>
  );
};

export default BudgetPredictionWidget;
