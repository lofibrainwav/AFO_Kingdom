/**
 * RoyalTreasuryCard.tsx
 * 
 * Royal Treasury Card 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo, useCallback } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Coins, Zap, ArrowUpRight, TrendingUp } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function RoyalTreasuryCardContent() {
  // Memoize treasury data
  const treasuryData = useMemo(
    () => ({
      totalAssets: 4520000,
      tokens: 452000,
      growth: 12.5,
      manaReserves: 92,
    }),
    []
  );

  // Memoize formatted values
  const formattedData = useMemo(() => {
    return {
      totalAssets: new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0,
      }).format(treasuryData.totalAssets),
      tokens: new Intl.NumberFormat("en-US").format(treasuryData.tokens),
      growth: `${treasuryData.growth > 0 ? "+" : ""}${treasuryData.growth}%`,
    };
  }, [treasuryData]);

  // Memoize button handlers
  const handleDeposit = useCallback(() => {
    console.log("Deposit action");
    // In a real app, this would trigger a deposit flow
  }, []);

  const handleTransfer = useCallback(() => {
    console.log("Transfer action");
    // In a real app, this would trigger a transfer flow
  }, []);

  return (
    <Card
      className="bg-gradient-to-br from-amber-50 to-orange-50 border-orange-200/50 shadow-lg hover:shadow-orange-200/50 transition-all duration-300"
      role="region"
      aria-labelledby="royal-treasury-title"
    >
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle
          id="royal-treasury-title"
          className="text-sm font-bold text-amber-800 flex items-center gap-2"
        >
          <Coins className="w-5 h-5 text-amber-500" aria-hidden="true" />
          ROYAL TREASURY
        </CardTitle>
        <Badge
          className="bg-amber-100 text-amber-800 hover:bg-amber-200 border-amber-200"
          role="status"
          aria-label="Treasury status: Active"
        >
          Active
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Gold Balance */}
          <section aria-label="Total assets">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-amber-600/70 uppercase">
                  Total Assets
                </span>
                <span
                  className="text-xs font-bold text-green-600 flex items-center gap-1"
                  aria-label={`Growth: ${formattedData.growth}`}
                >
                  <TrendingUp className="w-3 h-3" aria-hidden="true" /> {formattedData.growth}
                </span>
              </div>
              <div className="text-3xl font-black text-slate-800" aria-live="polite">
                {formattedData.totalAssets}
              </div>
              <p className="text-xs text-amber-600/60 font-medium mt-1">
                ≈ {formattedData.tokens} AFO Tokens
              </p>
            </div>
          </section>

          {/* Mana Reserves */}
          <section aria-label="Mana reserves">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-600">
                <span className="flex items-center gap-1">
                  <Zap className="w-3 h-3 text-purple-500" aria-hidden="true" /> Mana Reserves
                </span>
                <span className="font-bold" aria-label={`Mana reserves: ${treasuryData.manaReserves}%`}>
                  {treasuryData.manaReserves}%
                </span>
              </div>
              <div
                className="h-2 w-full bg-slate-200 rounded-full overflow-hidden"
                role="progressbar"
                aria-valuenow={treasuryData.manaReserves}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={`Mana reserves: ${treasuryData.manaReserves}%`}
              >
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full transition-all duration-300"
                  style={{ width: `${treasuryData.manaReserves}%` }}
                />
              </div>
            </div>
          </section>

          {/* Actions */}
          <section aria-label="Treasury actions">
            <div className="grid grid-cols-2 gap-3 pt-2">
              <Button
                onClick={handleDeposit}
                className="w-full bg-amber-500 hover:bg-amber-600 text-white shadow-amber-200 font-bold"
                aria-label="Deposit funds"
              >
                Deposit
              </Button>
              <Button
                onClick={handleTransfer}
                variant="outline"
                className="w-full border-amber-200 text-amber-700 hover:bg-amber-50 font-bold"
                aria-label="Transfer funds"
              >
                <ArrowUpRight className="w-4 h-4 mr-1" aria-hidden="true" /> Transfer
              </Button>
            </div>
          </section>
        </div>
      </CardContent>
    </Card>
  );
}

export const RoyalTreasuryCard = () => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("RoyalTreasuryCard error:", error, errorInfo);
      }}
      fallback={
        <Card
          className="bg-gradient-to-br from-amber-50 to-orange-50 border-red-200/50"
          role="alert"
        >
          <CardContent className="p-6">
            <p className="text-red-400 text-center">Royal Treasury Card를 불러올 수 없습니다.</p>
          </CardContent>
        </Card>
      }
    >
      <RoyalTreasuryCardContent />
    </ErrorBoundary>
  );
};

export default RoyalTreasuryCard;
