import { useEffect, useState } from 'react';

interface SSOTData {
  status: string;
  health: string;
  trinity: {
    truth: number;
    goodness: number;
    beauty: number;
    serenity: number;
    eternity: number;
    total: number;
  };
  risk: number;
  services: { online: number; total: number };
  git: { clean: boolean };
  timestamp: string;
}

export function SSOTMonitor() {
  const [ssot, setSsot] = useState<SSOTData | null>(null);

  useEffect(() => {
    const fetchSSOT = async () => {
      try {
        const res = await fetch('/api/ssot-status');
        if (res.ok) {
           const data = await res.json();
           setSsot(data);
        }
      } catch (e) {
        console.error("SSOT Fetch Error", e);
      }
    };
    fetchSSOT();
    const interval = setInterval(fetchSSOT, 30000); // 30s update
    return () => clearInterval(interval);
  }, []);

  if (!ssot) return (
     <div className="glass-card p-6 max-w-md mx-auto bg-black/40 rounded-3xl border border-white/10 animate-pulse text-center">
        <p className="text-white/70">SSOT 점검 중... 곧 정렬 완료돼요 ✨</p>
     </div>
  );

  const pillarScores = {
    '眞': ssot.trinity.truth,
    '善': ssot.trinity.goodness,
    '美': ssot.trinity.beauty,
    '孝': ssot.trinity.serenity,
    '永': ssot.trinity.eternity,
  };

  return (
    <div className="glass-card p-6 max-w-md mx-auto bg-gradient-to-br from-cyan-900/20 to-emerald-900/20 rounded-3xl border border-cyan-500/30 shadow-xl backdrop-blur-md">
      <h3 className="text-xl font-bold text-cyan-400 mb-4 text-center tracking-widest font-mono">왕국 SSOT 상태</h3>

      <div className="flex justify-center items-end gap-2 mb-4">
          <span className="text-5xl font-black text-emerald-400 drop-shadow-[0_0_10px_rgba(52,211,153,0.5)]">
            {(ssot.trinity.total * 100).toFixed(1)}
          </span>
          <span className="text-xl text-emerald-600 font-bold mb-2">/100</span>
      </div>

      <div className="bg-black/30 rounded-xl p-3 mb-6 grid grid-cols-5 gap-1 text-center">
         {Object.entries(pillarScores).map(([key, val]) => (
             <div key={key} className="flex flex-col">
                 <span className="text-xs text-white/50">{key}</span>
                 <span className="text-sm font-bold text-white">{(val * 100).toFixed(0)}</span>
             </div>
         ))}
      </div>

      <p className="text-center text-white/90 mb-2 font-medium bg-emerald-500/10 py-2 rounded-lg border border-emerald-500/20">
        {ssot.health === 'excellent' ? '✅ 眞善美孝永 정렬 완료' : `⚠️ ${ssot.health}`}
      </p>

      <p className="text-[10px] text-white/40 text-center italic font-mono uppercase">
        Last Update: {new Date(ssot.timestamp).toLocaleString()} <br/>
        <span className="text-cyan-500/60">● {ssot.services.online}/{ssot.services.total} SERVICES ONLINE</span>
      </p>
    </div>
  );
}
