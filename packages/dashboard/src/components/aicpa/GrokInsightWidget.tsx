import React, { useState, useCallback, useMemo } from "react";
import {
  Sparkles,
  Brain,
  TrendingUp,
  TrendingDown,
  Minus,
  RefreshCw,
  Zap,
  DollarSign,
} from "lucide-react";

interface GrokAnalysis {
  source: string;
  cost_saved?: boolean;
  model_used?: string;
  grok_analysis: {
    is_mock: boolean;
    sentiment: "bullish" | "bearish" | "neutral";
    score: number;
    analysis: string;
    action_items: string[];
    message?: string;
  };
}

export function GrokInsightWidget() {
  const [data, setData] = useState<GrokAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Memoize fetch function
  const fetchGrokWisdom = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/julie/budget/consult-grok");
      if (!res.ok) throw new Error("Failed to consult Grok");
      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Memoize sentiment display
  const sentimentDisplay = useMemo(() => {
    if (!data?.grok_analysis) return null;
    const sentiment = data.grok_analysis.sentiment;
    if (sentiment === "bullish") {
      return (
        <span className="flex items-center gap-1 text-emerald-400 font-bold">
          <TrendingUp className="w-4 h-4" /> Bullish
        </span>
      );
    }
    if (sentiment === "bearish") {
      return (
        <span className="flex items-center gap-1 text-rose-400 font-bold">
          <TrendingDown className="w-4 h-4" /> Bearish
        </span>
      );
    }
    return (
      <span className="flex items-center gap-1 text-yellow-400 font-bold">
        <Minus className="w-4 h-4" /> Neutral
      </span>
    );
  }, [data?.grok_analysis?.sentiment]);

  return (
    <div className="glass-card p-6 relative overflow-hidden group">
      {/* Background Cosmic Effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/10 to-purple-900/10 opacity-50 pointer-events-none" />

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
              <Brain className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                Grok Insight
                {data?.grok_analysis.is_mock && (
                  <span className="text-xs px-2 py-0.5 bg-yellow-500/20 text-yellow-400 rounded-full border border-yellow-500/30">
                    Mock
                  </span>
                )}
              </h3>
              <p className="text-sm text-indigo-300/70">The Sage from the Stars</p>
            </div>
          </div>

          <button
            onClick={fetchGrokWisdom}
            disabled={loading}
            className={`p-2 rounded-full hover:bg-white/5 border border-white/5 transition-all ${loading ? "animate-spin" : ""}`}
            aria-label={loading ? "Loading Grok insight" : "Fetch Grok insight"}
            aria-busy={loading}
          >
            <RefreshCw className="w-5 h-5 text-indigo-300" />
          </button>
        </div>

        {error && (
          <div className="p-4 bg-red-900/20 border border-red-500/30 rounded-lg text-red-300 text-sm mb-4">
            {error}
          </div>
        )}

        {!data && !loading && !error && (
          <div className="text-center py-10 text-white/30">
            <Sparkles className="w-12 h-12 mx-auto mb-3 opacity-20" />
            <p>Consult Grok for cosmic economic wisdom.</p>
            <button
              onClick={fetchGrokWisdom}
              className="mt-4 px-6 py-2 bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/30 rounded-full text-indigo-200 transition-all font-medium"
              aria-label="Connect to xAI Grok"
            >
              Connect to xAI
            </button>
          </div>
        )}

        {loading && (
          <div className="py-12 flex flex-col items-center justify-center space-y-4">
            <div className="w-16 h-16 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin" />
            <p className="text-indigo-300 animate-pulse text-sm">Analyzing global timeline...</p>
          </div>
        )}

        {data && !loading && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Cost Guardian Badge */}
            <div className="flex items-center gap-2 text-xs">
              {data.cost_saved && (
                <span className="flex items-center gap-1 text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
                  <DollarSign className="w-3 h-3" /> Cost Saved (Cached)
                </span>
              )}
              {data.model_used && (
                <span className="flex items-center gap-1 text-indigo-300 bg-indigo-500/10 px-2 py-1 rounded border border-indigo-500/20">
                  <Zap className="w-3 h-3" /> {data.model_used}
                </span>
              )}
            </div>

            {/* Sentiment Meter */}
            <div className="flex items-center justify-between p-4 bg-black/20 rounded-xl border border-white/5">
              <div className="flex items-center gap-3">
                <span className="text-sm text-white/50">Market Mood</span>
                {sentimentDisplay}
              </div>
              <div className="flex items-end gap-1">
                <span className="text-2xl font-black text-white">{data.grok_analysis.score}</span>
                <span className="text-xs text-white/40 mb-1">/100</span>
              </div>
            </div>

            {/* Main Analysis */}
            <div className="p-5 bg-indigo-900/10 border border-indigo-500/20 rounded-xl relative">
              <Sparkles className="w-4 h-4 absolute top-4 right-4 text-indigo-400/50" />
              <p className="text-indigo-100 leading-relaxed font-light">
                "{data.grok_analysis.analysis}"
              </p>
              {data.grok_analysis.message && (
                <p className="mt-3 text-xs text-white/30 border-t border-white/5 pt-2 uppercase tracking-wider">
                  Transmission: {data.grok_analysis.message}
                </p>
              )}
            </div>

            {/* Action Items */}
            <div>
              <h4 className="text-xs font-bold text-white/40 uppercase tracking-widest mb-3">
                Strategic Decrees
              </h4>
              <ul className="space-y-2">
                {data.grok_analysis.action_items.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-white/70">
                    <span className="w-1.5 h-1.5 mt-1.5 rounded-full bg-indigo-500 shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
