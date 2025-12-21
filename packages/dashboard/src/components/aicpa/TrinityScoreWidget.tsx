import React, { useState, useEffect } from 'react';
import { Compass, Star } from 'lucide-react';
import { logError } from '@/lib/logger';

interface SSOTData {
  trinity_score: number;
  status: string;
}

export function TrinityScoreWidget() {
  const [data, setData] = useState<SSOTData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/ssot-status')
      .then(res => res.json())
      .then(setData)
      .catch((err) => logError('Failed to fetch trinity score', { error: err instanceof Error ? err.message : 'Unknown error' }))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) return null;

  return (
    <div className="glass-card p-8 bg-gradient-to-br from-cyan-900/20 to-emerald-900/20 rounded-3xl border border-cyan-500/40 relative overflow-hidden">
        {/* Background Animation */}
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 animate-pulse-slow"></div>

        <div className="relative z-10 flex flex-col items-center">
            <div className="mb-4 relative">
                <Compass className="w-16 h-16 text-cyan-400 animate-spin-slow" />
                <Star className="w-6 h-6 text-yellow-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse" fill="currentColor" />
            </div>

            <h3 className="text-2xl font-bold text-cyan-400 mb-2 tracking-widest text-center">TRINITY SCORE</h3>
            
            <div className="relative">
                <p className="text-6xl font-black text-center text-emerald-400 mb-4 drop-shadow-[0_0_15px_rgba(52,211,153,0.5)]">
                    {data.trinity_score.toFixed(2)}<span className="text-2xl text-white/50">/100</span>
                </p>
            </div>

            <div className="bg-black/30 px-6 py-2 rounded-full border border-white/10 backdrop-blur-sm">
                <p className="text-center text-white/90 text-sm font-medium">
                    {data.trinity_score >= 95 ? "✨ 왕국 완벽 – 초심 만점!" : "🔧 튜닝이 조금 필요해요"}
                </p>
            </div>
            
            <p className="text-center text-white/50 mt-6 italic text-xs max-w-xs">
                "Trinity Score가 높을수록<br/>모든 자동화가 더 안전하고 똑똑해져요!"
            </p>
        </div>
    </div>
  );
}
