'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { invokeChancellor, fetchHealthStatus, fetchFamilyStatus, ChancellorResponse, HealthResponse, FamilyHubResponse } from '@/lib/api';

// Persona Definitions
const PERSONAS: Record<string, { color: string; bg: string; border: string; icon: string }> = {
  jegalryang: {
    color: 'text-cyan-400',
    bg: 'bg-cyan-950/30',
    border: 'border-cyan-500', 
    icon: '⚔️ 제갈량 (眞)'
  },
  samaui: {
    color: 'text-amber-500',
    bg: 'bg-amber-950/30',
    border: 'border-amber-600',
    icon: '🛡️ 사마의 (善)'
  },
  juyu: {
    color: 'text-pink-400',
    bg: 'bg-pink-950/30',
    border: 'border-pink-500',
    icon: '🌉 주유 (美)'
  },
  chancellor: {
    color: 'text-green-500',
    bg: 'bg-green-950/30',
    border: 'border-green-500',
    icon: '👑 승상'
  },
  system: {
    color: 'text-gray-400',
    bg: 'bg-gray-900',
    border: 'border-gray-600',
    icon: '🖥️ SYSTEM'
  }
};

// Family Status Colors
const STATUS_COLORS: Record<string, string> = {
  'WORKING': 'text-green-400 animate-pulse',
  'AUDITING': 'text-yellow-400 animate-pulse',
  'IDLE': 'text-gray-500',
  'ACTIVE': 'text-blue-400'
};

// Decision color mapping
const DECISION_COLORS: Record<string, string> = {
  'AUTO_RUN': 'text-green-500',
  'ASK_COMMANDER': 'text-yellow-500',
  'TRY_AGAIN': 'text-red-500'
};

export default function ChancellorView() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState<ChancellorResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [familyData, setFamilyData] = useState<FamilyHubResponse | null>(null);
  const [latency, setLatency] = useState<number>(0);

  // Fetch health status on mount and every 5 seconds (faster for status updates)
  const refreshHealth = useCallback(async () => {
    const startTime = Date.now();
    try {
      const [healthData, familyRes] = await Promise.all([
        fetchHealthStatus(),
        fetchFamilyStatus()
      ]);
      setHealth(healthData);
      setFamilyData(familyRes);
      setLatency(Date.now() - startTime);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  }, []);

  useEffect(() => {
    refreshHealth();
    const interval = setInterval(refreshHealth, 5000); // 5s refresh
    return () => clearInterval(interval);
  }, [refreshHealth]);

  // Helper to get persona style safely
  const getPersona = (speaker: string = 'system') => {
    const key = speaker.toLowerCase();
    return PERSONAS[key] || PERSONAS['system'];
  };

  const activePersona = response ? getPersona(response.speaker) : PERSONAS['chancellor'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    try {
      // Use real trinity score from health API
      const trinityScore = health?.trinity?.trinity_score ?? 0.9;
      const res = await invokeChancellor(input, trinityScore);
      setResponse(res);
      setInput('');
      // Refresh health after command
      await refreshHealth();
    } catch (err) {
      console.error(err);
      setResponse({
        speaker: 'System',
        response: 'Error communicating with the Chancellor. Ensure backend Docker services are running.',
        full_history: []
      } as ChancellorResponse);
    } finally {
      setLoading(false);
    }
  };

  // Format percentage display
  const formatPercent = (value: number | undefined) => {
    if (value === undefined) return '-.-%';
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4 space-y-6">
      {/* Header / Status Cartridge */}
      <div className={`bg-black/90 border-2 ${activePersona.border} rounded-lg p-4 shadow-[0_0_15px_rgba(0,0,0,0.5)] transition-colors duration-500`}>
        <div className="flex items-center justify-between mb-3">
          <h2 className={`${activePersona.color} font-mono text-xl tracking-wider flex items-center gap-2`}>
            <span className="animate-pulse">●</span> {activePersona.icon}
          </h2>
          {health && (
            <span className={`font-mono text-sm ${DECISION_COLORS[health.decision] || 'text-gray-400'}`}>
              {health.decision}
            </span>
          )}
        </div>
        
        {/* 5-Pillar Trinity Display */}
        <div className="grid grid-cols-5 gap-2 text-xs font-mono mb-3">
          <div className="border border-cyan-800/50 p-2 text-center">
            <div className="text-cyan-400 text-lg">{formatPercent(health?.trinity?.truth)}</div>
            <div className="text-gray-500">眞 35%</div>
          </div>
          <div className="border border-amber-800/50 p-2 text-center">
            <div className="text-amber-400 text-lg">{formatPercent(health?.trinity?.goodness)}</div>
            <div className="text-gray-500">善 35%</div>
          </div>
          <div className="border border-pink-800/50 p-2 text-center">
            <div className="text-pink-400 text-lg">{formatPercent(health?.trinity?.beauty)}</div>
            <div className="text-gray-500">美 20%</div>
          </div>
          <div className="border border-green-800/50 p-2 text-center group relative cursor-pointer hover:bg-green-900/30 transition-colors">
            <Link href="/wallet" className="absolute inset-0 z-10" aria-label="Open Wallet Manager"></Link>
            <div className="text-green-400 text-lg group-hover:scale-110 transition-transform">💳</div>
            <div className="text-gray-500 text-[10px] mt-1">WALLET</div>
          </div>
          <div className="border border-green-800/50 p-2 text-center">
            <div className="text-green-400 text-lg">{formatPercent(health?.trinity?.filial_serenity)}</div>
            <div className="text-gray-500">孝 8%</div>
          </div>
          <div className="border border-purple-800/50 p-2 text-center">
            <div className="text-purple-400 text-lg">{formatPercent(health?.trinity?.eternity)}</div>
            <div className="text-gray-500">永 2%</div>
          </div>
        </div>

        {/* System Status */}
        <div className="grid grid-cols-3 gap-4 text-xs font-mono text-gray-400">
          <div className="border border-gray-800 p-2">
            TRINITY_SCORE: <span className="text-green-400">{health?.health_percentage?.toFixed(1) ?? '-'}%</span>
          </div>
          <div className="border border-gray-800 p-2">
            STATUS: <span className={health?.status === 'balanced' ? 'text-green-400' : 'text-yellow-400'}>
              {health?.status?.toUpperCase() ?? 'LOADING'}
            </span>
          </div>
          <div className="border border-gray-800 p-2">
            LATENCY: <span className="text-blue-400">{latency}ms</span>
          </div>
        </div>

        {/* Issues & Suggestions */}
        {health?.issues && health.issues.length > 0 && (
          <div className="mt-3 p-2 border border-red-800/50 rounded bg-red-950/20">
            <div className="text-red-400 text-xs font-mono">⚠️ ISSUES:</div>
            {health.issues.map((issue, i) => (
              <div key={i} className="text-red-300 text-xs ml-2">{issue}</div>
            ))}
            {health.suggestions && (
              <div className="text-yellow-400 text-xs mt-1">
                💡 {health.suggestions.join(' | ')}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Family Hub Status Grid */}
      {familyData && familyData.members && Object.keys(familyData.members).length > 0 && (
         <div className="bg-black/80 border border-gray-800 rounded-lg p-3">
            <h3 className="text-gray-500 font-mono text-xs mb-2 flex items-center gap-2">
              <span>FAMILY HUB STATUS [BETA]</span>
              <div className="h-px bg-gray-800 flex-1"></div>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
               {Object.entries(familyData.members).map(([key, member]) => (
                  <div key={key} className={`border border-gray-800 p-3 rounded bg-gray-900/50 flex align-top gap-3 ${member.status === 'WORKING' ? 'border-green-900/50 shadow-[0_0_10px_rgba(34,197,94,0.1)]' : ''}`}>
                     <div className="text-2xl font-none">{member.name === 'Julie' ? '👩‍💼' : '🤖'}</div>
                     <div className="flex-1 min-w-0">
                        <div className="flex justify-between items-center mb-1">
                           <span className="text-gray-300 font-mono text-xs font-bold truncate pr-2">{member.name}</span>
                           <span className={`text-[10px] font-mono border px-1.5 py-0.5 rounded-full whitespace-nowrap ${member.status === 'WORKING' ? 'border-green-600 text-green-400 bg-green-950/30' : 'border-gray-700 text-gray-500'}`}>
                              {member.status}
                           </span>
                        </div>
                        <p className={`text-xs font-mono truncate ${STATUS_COLORS[member.status] || 'text-gray-500'}`}>
                           {member.message || 'No active task'}
                        </p>
                        <div className="mt-2 flex gap-2 text-[9px] text-gray-500 font-mono bg-black/50 p-1 rounded w-fit">
                           <span className="text-cyan-400">眞{Math.round((member.pillars?.truth || 0) * 100)}</span>
                           <span className="text-amber-400">善{Math.round((member.pillars?.goodness || 0) * 100)}</span>
                           <span className="text-pink-400">美{Math.round((member.pillars?.beauty || 0) * 100)}</span>
                        </div>
                     </div>
                  </div>
               ))}
            </div>
         </div>
      )}

      {/* Main Display Area */}
      <div className={`bg-black border-2 ${activePersona.border} rounded-lg min-h-[400px] p-6 relative overflow-hidden transition-colors duration-500`}>
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-green-500/50 to-transparent opacity-50"></div>
        
        {response ? (
          <div className="space-y-4">
            <div className={`flex items-center gap-2 ${activePersona.color} font-mono text-sm border-b border-white/10 pb-2`}>
              <span className={`${activePersona.bg} px-2 py-0.5 rounded text-xs border ${activePersona.border} bg-opacity-20`}>
                FROM: {response.speaker.toUpperCase()}
              </span>
              <span className="text-gray-500 text-xs" suppressHydrationWarning>{new Date().toLocaleTimeString()}</span>
            </div>
            <div className="prose prose-invert max-w-none font-sans text-gray-200 leading-relaxed whitespace-pre-wrap">
              {response.response}
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-gray-800 font-mono animate-pulse">
            <div className="text-4xl mb-4">♔</div>
            <p>WAITING FOR INPUT...</p>
            {health?.decision_message && (
              <p className="text-sm text-gray-600 mt-2">{health.decision_message}</p>
            )}
          </div>
        )}
      </div>

      {/* Input Cartridge */}
      <form onSubmit={handleSubmit} className="relative group">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg opacity-20 group-hover:opacity-40 transition duration-500 blur"></div>
        <div className="relative flex bg-black rounded-lg border border-gray-800">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter command or query..."
            className="flex-1 bg-transparent text-white p-4 font-mono focus:outline-none placeholder-gray-700"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-8 font-mono text-green-500 hover:text-green-400 disabled:opacity-50 disabled:cursor-not-allowed border-l border-gray-800 hover:bg-green-900/10 transition-colors"
          >
            {loading ? 'PROCESSING...' : 'EXECUTE'}
          </button>
        </div>
      </form>
    </div>
  );
}
