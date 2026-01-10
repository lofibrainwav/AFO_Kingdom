"use client";

import { useMemo, useState } from "react";

export function JulieTaxWidget() {
  const [annualIncome, setAnnualIncome] = useState(120000);
  const [savingsRate, setSavingsRate] = useState(0.15);
  const [effectiveTaxRate, setEffectiveTaxRate] = useState(0.22);

  const result = useMemo(() => {
    const tax = annualIncome * effectiveTaxRate;
    const savings = annualIncome * savingsRate;
    const safeToSpendAnnual = Math.max(0, annualIncome - tax - savings);
    return {
      tax,
      savings,
      safeToSpendAnnual,
      safeToSpendMonthly: safeToSpendAnnual / 12,
    };
  }, [annualIncome, savingsRate, effectiveTaxRate]);

  const fmt = (n: number) =>
    n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

  return (
    <div className="mt-8 rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
      <div className="flex items-center justify-between">
        <div className="text-lg font-semibold">Julie Tax Engine</div>
        <div className="text-xs opacity-70">Demo estimator</div>
      </div>

      <div className="mt-4 grid gap-4 md:grid-cols-3">
        <label className="grid gap-2 text-sm">
          Annual Income
          <input
            type="range"
            min={0}
            max={600000}
            step={1000}
            value={annualIncome}
            onChange={(e) => setAnnualIncome(Number(e.target.value))}
          />
          <div className="text-base font-medium">{fmt(annualIncome)}</div>
        </label>

        <label className="grid gap-2 text-sm">
          Effective Tax Rate
          <input
            type="range"
            min={0}
            max={0.45}
            step={0.005}
            value={effectiveTaxRate}
            onChange={(e) => setEffectiveTaxRate(Number(e.target.value))}
          />
          <div className="text-base font-medium">{Math.round(effectiveTaxRate * 1000) / 10}%</div>
        </label>

        <label className="grid gap-2 text-sm">
          Savings Rate
          <input
            type="range"
            min={0}
            max={0.40}
            step={0.005}
            value={savingsRate}
            onChange={(e) => setSavingsRate(Number(e.target.value))}
          />
          <div className="text-base font-medium">{Math.round(savingsRate * 1000) / 10}%</div>
        </label>
      </div>

      <div className="mt-5 grid gap-3 rounded-2xl border border-white/10 bg-black/30 p-4">
        <div className="flex justify-between text-sm">
          <span className="opacity-70">Estimated Tax</span>
          <span className="font-medium">{fmt(result.tax)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="opacity-70">Savings Reserve</span>
          <span className="font-medium">{fmt(result.savings)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="opacity-70">Safe to Spend (Monthly)</span>
          <span className="text-lg font-semibold">{fmt(result.safeToSpendMonthly)}</span>
        </div>
      </div>

      <div className="mt-3 text-xs opacity-60">
        This is a demo estimator. Final numbers should be verified under Julie’s CPA rules.
      </div>
    </div>
  );
}
