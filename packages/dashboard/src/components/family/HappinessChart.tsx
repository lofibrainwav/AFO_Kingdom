import React from "react";
import { Activity } from "lucide-react";

interface HappinessChartProps {
  score: number;
}

const HappinessChart: React.FC<HappinessChartProps> = ({ score }) => {
  // Color logic based on score
  let color = "bg-blue-500";
  let textColor = "text-blue-400";
  if (score >= 90) {
    color = "bg-pink-500";
    textColor = "text-pink-400";
  } else if (score >= 70) {
    color = "bg-green-500";
    textColor = "text-green-400";
  } else if (score >= 50) {
    color = "bg-yellow-500";
    textColor = "text-yellow-400";
  } else {
    color = "bg-red-500";
    textColor = "text-red-400";
  }

  return (
    <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Activity className="w-5 h-5 text-purple-400" />
          Happiness Score
        </h3>
        <span className={`text-2xl font-black ${textColor}`}>{score.toFixed(1)}</span>
      </div>

      <div className="w-full bg-gray-700/50 rounded-full h-4 overflow-hidden border border-white/10">
        <div
          className={`h-full ${color} transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(255,255,255,0.3)]`}
          style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
        ></div>
      </div>

      <p className="mt-4 text-sm text-gray-400 text-center italic">
        "Serenity is the key to a happy kingdom."
      </p>
    </div>
  );
};

export default HappinessChart;
