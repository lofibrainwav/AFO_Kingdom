"use client";

import ErrorBoundary from "@/components/common/ErrorBoundary";
import { ArrowUpRight, Coins, TrendingUp, Zap } from "lucide-react";
import { useCallback, useMemo } from "react";

/**
 * RoyalTreasuryCard - Neumorphic Yellow/Amber Style
 * 
 * CSS Variables Used (from globals.css):
 * - --shadow-neu-flat: Neumorphic flat shadow
 * - --bg-platinum: #efeeee base background
 * 
 * Yellow/Amber Accent: #F59E0B (accent-warning)
 */

function RoyalTreasuryCardContent() {
  const treasuryData = useMemo(
    () => ({
      totalAssets: 4520000,
      tokens: 452000,
      growth: 12.5,
      manaReserves: 92,
    }),
    []
  );

  const formattedData = useMemo(() => ({
    totalAssets: new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(treasuryData.totalAssets),
    tokens: new Intl.NumberFormat("en-US").format(treasuryData.tokens),
    growth: `${treasuryData.growth > 0 ? "+" : ""}${treasuryData.growth}%`,
  }), [treasuryData]);

  const handleDeposit = useCallback(() => {
    console.log("Deposit action");
  }, []);

  const handleTransfer = useCallback(() => {
    console.log("Transfer action");
  }, []);

  return (
    <div
      className="neu-card min-h-[240px]"
      role="region"
      aria-labelledby="royal-treasury-title"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3
          id="royal-treasury-title"
          className="text-sm font-bold text-amber-700 flex items-center gap-2 uppercase tracking-wider"
        >
          <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center">
            <Coins className="w-4 h-4 text-amber-600" aria-hidden="true" />
          </div>
          Royal Treasury
        </h3>
        <span
          className="px-3 py-1 text-xs font-bold rounded-full bg-amber-100 text-amber-700 border border-amber-200"
          role="status"
        >
          Active
        </span>
      </div>

      {/* Main Balance */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Total Assets
          </span>
          <span className="text-xs font-bold text-emerald-600 flex items-center gap-1">
            <TrendingUp className="w-3 h-3" aria-hidden="true" />
            {formattedData.growth}
          </span>
        </div>
        <div className="text-3xl font-black text-slate-700 tracking-tight">
          {formattedData.totalAssets}
        </div>
        <p className="text-xs text-slate-400 font-medium mt-1">
          ≈ {formattedData.tokens} AFO Tokens
        </p>
      </div>

      {/* Mana Reserves - Neu Style Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs text-slate-600 mb-2">
          <span className="flex items-center gap-1 font-semibold">
            <Zap className="w-3 h-3 text-amber-500" aria-hidden="true" />
            Mana Reserves
          </span>
          <span className="font-bold text-amber-600">{treasuryData.manaReserves}%</span>
        </div>
        {/* Neumorphic Progress Bar */}
        <div
          className="h-3 w-full rounded-full overflow-hidden"
          style={{
            background: "var(--bg-platinum, #efeeee)",
            boxShadow: "inset 4px 4px 8px #d1d9e6, inset -4px -4px 8px #ffffff"
          }}
        >
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{
              width: `${treasuryData.manaReserves}%`,
              background: "linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%)",
              boxShadow: "2px 2px 4px rgba(245, 158, 11, 0.3)"
            }}
          />
        </div>
      </div>

      {/* Action Buttons - Neu Style */}
      <div className="grid grid-cols-2 gap-4">
        <button
          onClick={handleDeposit}
          className="neu-btn text-amber-700 font-bold text-sm py-3 px-4 rounded-xl hover:translate-y-[-2px] active:translate-y-0 transition-all"
          aria-label="Deposit funds"
          style={{
            background: "linear-gradient(145deg, #f5f7fa, #e8ecef)",
            boxShadow: "4px 4px 8px #d1d9e6, -4px -4px 8px #ffffff"
          }}
        >
          Deposit
        </button>
        <button
          onClick={handleTransfer}
          className="neu-btn text-amber-700 font-bold text-sm py-3 px-4 rounded-xl flex items-center justify-center gap-1 hover:translate-y-[-2px] active:translate-y-0 transition-all"
          aria-label="Transfer funds"
          style={{
            background: "linear-gradient(145deg, #f5f7fa, #e8ecef)",
            boxShadow: "4px 4px 8px #d1d9e6, -4px -4px 8px #ffffff"
          }}
        >
          <ArrowUpRight className="w-4 h-4" aria-hidden="true" />
          Transfer
        </button>
      </div>
    </div>
  );
}

export const RoyalTreasuryCard = () => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("RoyalTreasuryCard error:", error, errorInfo);
      }}
      fallback={
        <div className="neu-card min-h-[240px] flex items-center justify-center" role="alert">
          <p className="text-red-400 text-center">Royal Treasury를 불러올 수 없습니다.</p>
        </div>
      }
    >
      <RoyalTreasuryCardContent />
    </ErrorBoundary>
  );
};

export default RoyalTreasuryCard;
