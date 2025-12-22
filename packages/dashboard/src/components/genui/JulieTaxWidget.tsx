/**
 * JulieTaxWidget.tsx
 * 
 * JULIE CPA・TAX ENGINE 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useEffect, useState, useMemo, useCallback } from "react";
import useSound from "use-sound";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calculator, ShieldCheck, TrendingDown } from "lucide-react";
import ErrorBoundary from "@/components/common/ErrorBoundary";

function JulieTaxWidgetContent() {
  const [income, setIncome] = useState(150000);
  const [filingStatus, setFilingStatus] = useState<"single" | "mfj">("single");

  const [taxData, setTaxData] = useState<any>({
    totalTax: 0,
    netIncome: 150000,
    effective_rate: 0,
    risk_level: "neutral",
    fed_tax: 0,
    ca_tax: 0,
    standard_deduction: 0,
  });

  // Memoize currency formatter
  const formatCurrency = useCallback((val: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(val);
  }, []);

  // Memoize fetch function
  const fetchTaxTruth = useCallback(async () => {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";

      const res = await fetch(`${apiBase}/api/julie/calculate-tax`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ income, filing_status: filingStatus }),
      });

      if (res.ok) {
        const data = await res.json();
        setTaxData(data);
      }
    } catch (error) {
      console.error("Failed to consult Julie CPA:", error);
    }
  }, [income, filingStatus]);

  // Debounced API Call
  useEffect(() => {
    const timer = setTimeout(fetchTaxTruth, 300);
    return () => clearTimeout(timer);
  }, [fetchTaxTruth]);

  // Sensory Immersion (Beauty)
  const [playBell] = useSound("/sounds/jade_bell.mp3", { volume: 0.5 });

  // Memoize risk styles
  const riskStyles = useMemo(() => {
    const riskColor =
      taxData.risk_level === "safe"
        ? "text-emerald-700"
        : taxData.risk_level === "risk"
          ? "text-red-700"
          : "text-amber-700";
    const riskBg =
      taxData.risk_level === "safe"
        ? "bg-emerald-50/50 border-emerald-100"
        : taxData.risk_level === "risk"
          ? "bg-red-50/50 border-red-100"
          : "bg-amber-50/50 border-amber-100";
    const gradientColor =
      taxData.risk_level === "safe"
        ? "from-emerald-400 via-teal-500 to-emerald-600"
        : taxData.risk_level === "risk"
          ? "from-red-500 to-orange-500"
          : "from-amber-400 to-orange-400";
    return { riskColor, riskBg, gradientColor };
  }, [taxData.risk_level]);

  // Memoize formatted values
  const formattedValues = useMemo(() => {
    return {
      income: formatCurrency(income),
      totalTax: formatCurrency(taxData.total_tax || 0),
      netIncome: formatCurrency(taxData.net_income || 0),
      standardDeduction: formatCurrency(taxData.standard_deduction || 0),
      fedTax: formatCurrency(taxData.fed_tax || 0),
      caTax: formatCurrency(taxData.ca_tax || 0),
      effectiveRate: taxData.effective_rate?.toFixed(1) || "0",
      marginalRate: taxData.marginal_rate || 0,
      mentalHealthSurtax: taxData.mental_health_surtax > 0
        ? `Active (${formatCurrency(taxData.mental_health_surtax)})`
        : "Inactive",
    };
  }, [income, taxData, formatCurrency]);

  // Memoize handlers
  const handleIncomeChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setIncome(Number(e.target.value));
  }, []);

  const handleFilingStatusChange = useCallback((status: "single" | "mfj") => {
    setFilingStatus(status);
  }, []);

  const handleAdviceCardClick = useCallback(() => {
    playBell();
  }, [playBell]);

  return (
    <Card
      className="bg-white/80 backdrop-blur-xl border-emerald-100/50 shadow-2xl overflow-hidden relative transition-all duration-500 hover:shadow-emerald-100/50 group/widget"
      role="region"
      aria-labelledby="julie-tax-title"
    >
      <div
        className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${riskStyles.gradientColor} opacity-80 group-hover/widget:opacity-100 transition-opacity`}
        aria-hidden="true"
      />

      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle
          id="julie-tax-title"
          className="text-sm font-bold text-slate-800 flex items-center gap-2"
        >
          <Calculator className="w-5 h-5 text-emerald-600" aria-hidden="true" />
          JULIE CPA・TAX ENGINE
        </CardTitle>
        <div className="flex gap-2" role="group" aria-label="Filing status">
          <Button
            variant={filingStatus === "single" ? "default" : "outline"}
            size="sm"
            onClick={() => handleFilingStatusChange("single")}
            className="h-6 text-[10px] px-2 shadow-sm"
            aria-pressed={filingStatus === "single"}
            aria-label="Single filing status"
          >
            Single
          </Button>
          <Button
            variant={filingStatus === "mfj" ? "default" : "outline"}
            size="sm"
            onClick={() => handleFilingStatusChange("mfj")}
            className="h-6 text-[10px] px-2 shadow-sm"
            aria-pressed={filingStatus === "mfj"}
            aria-label="Married filing jointly status"
          >
            MFJ
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Input Section */}
        <section aria-label="Income input">
          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-500 mb-2">
              <span>Projected Gross Income</span>
              <span className="font-mono text-slate-700" aria-live="polite">
                {formattedValues.income}
              </span>
            </div>
            <input
              type="range"
              min="50000"
              max="1200000"
              step="5000"
              value={income}
              onChange={handleIncomeChange}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-500 hover:accent-emerald-400 transition-all"
              aria-label="Projected Gross Income"
              aria-valuemin={50000}
              aria-valuemax={1200000}
              aria-valuenow={income}
            />
            <div className="text-[10px] text-slate-400 mt-1 flex justify-between">
              <span>Standard Ded: {formattedValues.standardDeduction}</span>
              <span>CA Surtax: {formattedValues.mentalHealthSurtax}</span>
            </div>
          </div>
        </section>

        {/* Analysis Cards */}
        <section aria-label="Tax analysis">
          <div className="grid grid-cols-2 gap-4">
            <div
              className={`p-3 rounded-xl border ${riskStyles.riskBg} transition-all duration-300 hover:scale-[1.02] hover:shadow-md`}
              role="region"
              aria-label={`Tax liability: ${formattedValues.totalTax}, Effective rate: ${formattedValues.effectiveRate}%`}
            >
              <div className={`text-xs font-medium mb-1 ${riskStyles.riskColor}`}>Tax Liability</div>
              <div className={`text-lg font-bold ${riskStyles.riskColor}`}>
                {formattedValues.totalTax}
              </div>
              <div className={`text-[10px] mt-1 ${riskStyles.riskColor} opacity-80`}>
                Eff. Rate: {formattedValues.effectiveRate}%
              </div>
            </div>
            <div
              className="p-3 bg-white/50 rounded-xl border border-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-md hover:bg-white/80"
              role="region"
              aria-label={`Net income: ${formattedValues.netIncome}, Status: ${taxData.risk_level === "safe" ? "Efficient" : "Optimization Needed"}`}
            >
              <div className="text-xs text-slate-500 font-medium mb-1">Net (Safe to Spend)</div>
              <div className="text-lg font-bold text-slate-700">{formattedValues.netIncome}</div>
              <div className="text-[10px] text-slate-400 mt-1 flex items-center gap-1">
                {taxData.risk_level === "safe" ? (
                  <ShieldCheck className="w-3 h-3 text-emerald-500" aria-hidden="true" />
                ) : (
                  <TrendingDown className="w-3 h-3 text-amber-500" aria-hidden="true" />
                )}
                {taxData.risk_level === "safe" ? "Efficient" : "Optimization Needed"}
              </div>
            </div>
          </div>
        </section>

        {/* Breakdown */}
        <section aria-label="Tax breakdown">
          <div className="text-xs space-y-2 border-t border-slate-100 pt-4" role="list">
            <div className="flex justify-between" role="listitem">
              <span className="text-slate-500">Federal Tax (IRS)</span>
              <span className="font-mono text-slate-700">{formattedValues.fedTax}</span>
            </div>
            <div className="flex justify-between" role="listitem">
              <span className="text-slate-500">CA State Tax (FTB)</span>
              <span className="font-mono text-slate-700">{formattedValues.caTax}</span>
            </div>
            <div className="flex justify-between pt-1 opacity-75" role="listitem">
              <span className="text-slate-400">Marginal Rate (Last $)</span>
              <span className="font-mono text-slate-600">{formattedValues.marginalRate}%</span>
            </div>
          </div>
        </section>

        {/* Julie's Strategic Advice */}
        {taxData.advice_cards && taxData.advice_cards.length > 0 && (
          <section aria-label="Optimization strategy">
            <div className="space-y-3 mt-5">
              <div className="flex items-center gap-2">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  Julie's Optimization Strategy
                </div>
                <div className="h-px bg-slate-100 flex-1" aria-hidden="true" />
              </div>
              <div className="grid grid-cols-1 gap-3" role="list" aria-label="Advice cards">
                {taxData.advice_cards.map((card: any, idx: number) => (
                  <div
                    key={idx}
                    onClick={handleAdviceCardClick}
                    className="relative overflow-hidden flex items-center justify-between p-3 bg-gradient-to-br from-emerald-50/40 to-white border border-emerald-100/50 rounded-xl hover:shadow-lg hover:shadow-emerald-100/50 hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] transition-all duration-300 cursor-pointer group/card"
                    role="listitem"
                    aria-label={`Advice: ${card.title}, Action: ${card.action}, Impact: ${card.impact}`}
                  >
                    <div
                      className="absolute inset-0 bg-emerald-400/5 opacity-0 group-hover/card:opacity-100 transition-opacity"
                      aria-hidden="true"
                    />
                    <div className="flex gap-3 items-center relative z-10">
                      <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 group-hover/card:bg-emerald-600 group-hover/card:text-white transition-colors duration-300">
                        {card.type === "savings" ? (
                          <TrendingDown className="w-4 h-4" aria-hidden="true" />
                        ) : (
                          <ShieldCheck className="w-4 h-4" aria-hidden="true" />
                        )}
                      </div>
                      <div>
                        <div className="text-xs font-bold text-slate-700 font-sans group-hover/card:text-emerald-800 transition-colors">
                          {card.title}
                        </div>
                        <div className="text-[10px] text-slate-500 font-medium group-hover/card:text-slate-600">
                          {card.action}
                        </div>
                      </div>
                    </div>
                    <Badge
                      variant="secondary"
                      className="bg-white/80 backdrop-blur-sm text-emerald-700 text-[10px] h-6 px-2 border-emerald-100 shadow-sm group-hover/card:bg-emerald-600 group-hover/card:text-white group-hover/card:border-transparent transition-all duration-300"
                    >
                      {card.impact}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}
      </CardContent>
    </Card>
  );
}

export const JulieTaxWidget = () => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("JulieTaxWidget error:", error, errorInfo);
      }}
      fallback={
        <Card
          className="bg-white/80 backdrop-blur-xl border-red-100/50"
          role="alert"
        >
          <CardContent className="p-6">
            <p className="text-red-400 text-center">Julie Tax 위젯을 불러올 수 없습니다.</p>
          </CardContent>
        </Card>
      }
    >
      <JulieTaxWidgetContent />
    </ErrorBoundary>
  );
};

export default JulieTaxWidget;
