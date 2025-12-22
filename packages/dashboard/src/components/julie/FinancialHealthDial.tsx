import React from "react";
import { TrendingUp, TrendingDown, ShieldCheck } from "lucide-react";

interface FinancialHealthDialProps {
  score: number;
  trend: "up" | "down" | "stable";
  risk_level: "low" | "medium" | "high";
}

export default function FinancialHealthDial({
  score,
  trend,
  risk_level,
}: FinancialHealthDialProps) {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "high":
        return "text-red-500";
      case "medium":
        return "text-yellow-500";
      default:
        return "text-emerald-500";
    }
  };

  return (
    <div className="bg-[#0A0F1C] border border-gray-800 rounded-2xl p-6 relative overflow-hidden backdrop-blur-xl">
      {/* Background Glow */}
      <div
        className={`absolute top-0 right-0 w-32 h-32 rounded-full blur-[80px] opacity-20 ${score >= 90 ? "bg-emerald-500" : "bg-amber-500"}`}
      ></div>

      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-gray-400 text-sm font-medium tracking-wider uppercase">
            Financial Trinity Score
          </h3>
          <p className="text-xs text-gray-500 mt-1">Real-time Wealth Integrity</p>
        </div>
        <ShieldCheck className={`w-6 h-6 ${getRiskColor(risk_level)}`} />
      </div>

      <div className="flex items-baseline gap-2 mb-2">
        <span
          className={`text-5xl font-black ${score >= 90 ? "text-emerald-400" : "text-amber-400"}`}
        >
          {score.toFixed(1)}
        </span>
        <span className="text-gray-500 font-medium">/ 100</span>
      </div>

      <div className="flex items-center gap-2 mt-2">
        {trend === "up" ? (
          <div className="flex items-center gap-1 text-emerald-500 text-sm bg-emerald-500/10 px-2 py-1 rounded-full">
            <TrendingUp className="w-3 h-3" />
            <span>+2.4% vs last week</span>
          </div>
        ) : (
          <div className="flex items-center gap-1 text-red-500 text-sm bg-red-500/10 px-2 py-1 rounded-full">
            <TrendingDown className="w-3 h-3" />
            <span>-0.5% vs last week</span>
          </div>
        )}
        <div className="text-gray-600 text-xs ml-auto">
          Risk:{" "}
          <span className={`font-bold ${getRiskColor(risk_level)} uppercase`}>{risk_level}</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-2 bg-gray-800 rounded-full mt-6 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ${score >= 90 ? "bg-gradient-to-r from-emerald-600 to-emerald-400" : "bg-gradient-to-r from-amber-600 to-amber-400"}`}
          style={{ width: `${score}%` }}
        ></div>
      </div>
    </div>
  );
}
