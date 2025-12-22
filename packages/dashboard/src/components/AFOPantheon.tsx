'use client';

import { useEffect, useState, useCallback } from 'react';
import { TrinityGlowCard } from './TrinityGlowCard';
import { VoiceReactivePanel } from './VoiceReactivePanel';

import { SandboxCanvas } from './genui/SandboxCanvas';
import { AICPAJulieWidget } from './genui/AICPAJulieWidget';
import { SSOTMonitor } from './genui/SSOTMonitor';
import { JulieCPAWidget } from './genui/JulieCPAWidget';
import { JulieTaxWidget } from './genui/JulieTaxWidget';
import { GenesisWidget } from './genui/GenesisWidget';
import { FinalEternalVictoryWidget } from './genui/FinalEternalVictoryWidget';
import AutomatedDebuggingStreamWidget from './genui/AutomatedDebuggingStreamWidget';
import RoyalAnalyticsWidget from './genui/RoyalAnalyticsWidget';
import { useSpatialAudio } from '../hooks/useSpatialAudio';
import { logWarn, logError } from '@/lib/logger';

interface PantheonState {
  trinityScore: number | null;
  riskScore: number | null;
  healthStatus: 'excellent' | 'good' | 'warning' | 'critical' | 'loading';
  servicesOnline: number;
  totalServices: number;
  lastUpdate: string;
  breakdown?: {
      truth: number | null;
      goodness: number | null;
      beauty: number | null;
      filial_serenity: number | null;
      eternity: number | null;
  };
}

// ... (omitted)

export function AFOPantheon() {
  const [state, setState] = useState<PantheonState>({
    trinityScore: null,      // ✅ Unknown until fetched (no more fake 100%)
    riskScore: null,
    healthStatus: 'loading', // ✅ Shows loading state until verified
    servicesOnline: 0,       // ✅ Zero until backend confirms
    totalServices: 0,
    lastUpdate: new Date().toISOString(),
  });

  const [showVoicePanel, setShowVoicePanel] = useState(false);
  const [showCreativeCanvas, setShowCreativeCanvas] = useState(false);
  const [alerts, setAlerts] = useState<string[]>([]);
  const [thoughts, setThoughts] = useState<string[]>([]);
  const [isMatrixActive, setIsMatrixActive] = useState(false);

  const { playTrinityUp, playRiskUp, initAudio } = useSpatialAudio();

  // Helper function for status color class
  const getStatusColorClass = () => {
    switch (state.healthStatus) {
      case 'excellent': return 'text-green-500 border-green-500 shadow-green-500/20';
      case 'good': return 'text-lime-500 border-lime-500 shadow-lime-500/20';
      case 'warning': return 'text-yellow-500 border-yellow-500 shadow-yellow-500/20';
      case 'critical': return 'text-red-500 border-red-500 shadow-red-500/20';
      default: return 'text-gray-500 border-gray-500 shadow-gray-500/20';
    }
  };

  // Matrix Stream Connection (SSE)
  useEffect(() => {
    const eventSource = new EventSource('/api/mcp/thoughts/sse');

    eventSource.onmessage = (event) => {
      try {
        if (event.data === 'keep-alive') return;
        const thoughtData = JSON.parse(event.data);
        const timestamp = new Date().toLocaleTimeString();
        let thoughtText = `[${timestamp}] `;

        if (thoughtData.source) thoughtText += `[${thoughtData.source}] `;
        if (thoughtData.content) thoughtText += thoughtData.content;
        else thoughtText += JSON.stringify(thoughtData).slice(0, 100);

        setThoughts(prev => [thoughtText, ...prev].slice(0, 50)); // Keep last 50
        setIsMatrixActive(true);
        setTimeout(() => setIsMatrixActive(false), 2000); // Blink effect
      } catch (e) {
        logWarn('Matrix Parse Error', { error: e instanceof Error ? e.message : 'Unknown error' });
      }
    };

    eventSource.onerror = (e) => {
       logWarn('Matrix Stream Disconnected. Reconnecting...', { error: e });
       eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Fetch system state periodically from SSOT
  const fetchState = useCallback(async () => {
    try {
      const res = await fetch('/api/ssot-status'); // SSOT: Single Source of Truth
      if (res.ok) {
        const data = await res.json();

        setState(prev => ({
          ...prev,
          trinityScore: data.trinity?.total ?? prev.trinityScore,
          riskScore: data.risk ?? 0.0,
          healthStatus: data.health ?? prev.healthStatus,
          servicesOnline: data.services?.online ?? prev.servicesOnline,
          totalServices: data.services?.total ?? prev.totalServices,
          breakdown: {
              truth: data.trinity?.truth ?? null,       // No fake fallback
              goodness: data.trinity?.goodness ?? null, // No fake fallback
              beauty: data.trinity?.beauty ?? null,     // No fake fallback
              filial_serenity: data.trinity?.serenity ?? null, // No fake fallback
              eternity: data.trinity?.eternity ?? null, // No fake fallback - 永 real value
          },
          lastUpdate: data.timestamp ?? new Date().toISOString(),
        }));
      }
    } catch (e) {
      logWarn('SSOT fetch failed', { error: e instanceof Error ? e.message : 'Unknown error' });
    }
  }, []);

  // Initial fetch on mount
  useEffect(() => {
    fetchState(); // eslint-disable-line react-hooks/set-state-in-effect
    const interval = setInterval(fetchState, 15000); // Refresh every 15s
    return () => clearInterval(interval);
  }, [fetchState]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900 p-8">
      {/* Header */}
      <h1 className="text-white text-center text-3xl mb-8 font-sans">
        🏰 AFO Pantheon - Command Center
      </h1>

      {/* Main Container - Vertical Stack of Sections */}
      <div className="max-w-[1600px] mx-auto space-y-12">
        
        {/* Section 1: Command Center (Vitals) */}
        <section>
            <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
                🏛️ Command Center
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <TrinityGlowCard
                    trinityScore={state.trinityScore}
                    riskScore={state.riskScore}
                    breakdown={state.breakdown}
                >
                  <div className="text-center">
                    <div className="text-5xl mb-2">⚖️</div>
                    <h2 className="text-white m-0">Trinity Score</h2>
                    <div 
                      className={`text-4xl font-bold mt-2 ${
                        state.trinityScore === null ? 'text-gray-500' : 
                        state.trinityScore >= 0.9 ? 'text-green-500' : 
                        state.trinityScore >= 0.7 ? 'text-yellow-500' : 'text-red-500'
                      }`}
                    >
                      {state.trinityScore !== null ? `${(state.trinityScore * 100).toFixed(0)}%` : 'Loading...'}
                    </div>
                  </div>
                </TrinityGlowCard>

                <div 
                  className={`p-6 bg-black/60 rounded-2xl flex flex-col items-center justify-center transition-all duration-300 hover:bg-white/5 border ${getStatusColorClass()}`}
                >
                  <div className="text-5xl mb-2">💚</div>
                  <h2 className="text-white m-0">System Health</h2>
                  <div 
                    className={`text-xl font-bold mt-2 uppercase ${getStatusColorClass().split(' ')[0]}`}
                  >
                    {state.healthStatus}
                  </div>
                  <div className="text-gray-400 mt-2 text-sm">
                    {state.servicesOnline}/{state.totalServices} Services Online
                  </div>
                </div>

                <div className="p-6 bg-black/60 rounded-2xl border border-white/10 flex flex-col hover:border-white/30 transition-colors">
                  <h3 className="text-white m-0 mb-4 flex items-center justify-between">
                      <span>🔔 Recent Alerts</span>
                      <span className="text-xs bg-red-500/20 text-red-300 px-2 py-1 rounded-full">{alerts.length}</span>
                  </h3>
                  {alerts.length === 0 ? (
                    <div className="flex-1 flex items-center justify-center text-green-500/50 italic text-sm">
                        ✅ No active alerts
                    </div>
                  ) : (
                    <div className="flex-1 overflow-auto max-h-[120px] pr-2 scrollbar-thin scrollbar-thumb-white/20">
                      {alerts.slice(-5).map((alert, i) => (
                        <div key={i} className="p-2 mb-2 bg-red-500/10 border-l-2 border-red-500 text-red-300 text-xs">
                          {alert}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
            </div>
        </section>

        {/* Section 2: Operational Intelligence (Eyes & Soul) */}
        <section>
            <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
                👁️ Intelligence Layer
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                 {/* SSOT Monitor */}
                 <div className="lg:col-span-1">
                    <SSOTMonitor />
                 </div>
                 
                 {/* Matrix Stream */}
                 <div 
                   className="lg:col-span-2 p-6 bg-black/80 rounded-2xl transition-all duration-300"
                   style={{
                     border: `1px solid ${isMatrixActive ? '#22c55e' : 'rgba(34,197,94,0.3)'}`,
                     boxShadow: isMatrixActive ? '0 0 15px rgba(34,197,94,0.3)' : 'none',
                   }}
                 >
                    <h3 className="text-green-500 m-0 mb-4 font-mono flex justify-between items-center text-sm">
                      <span className="tracking-widest">MATRIX STREAM</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded ${isMatrixActive ? 'bg-green-500/20 text-green-300' : 'text-zinc-600'}`}>
                        {isMatrixActive ? '● LIVE' : '○ IDLE'}
                      </span>
                    </h3>
                    <div className="h-[200px] overflow-y-auto font-mono text-xs text-green-400/90 flex flex-col-reverse scrollbar-thin scrollbar-thumb-green-900">
                      {thoughts.length === 0 ? (
                         <div className="text-green-900/50 italic p-4 text-center">Waiting for neural signals...</div>
                      ) : (
                         thoughts.map((t, i) => (
                           <div key={i} className="py-1 border-b border-green-500/10 leading-relaxed hover:bg-green-500/5 px-2">
                             {t}
                           </div>
                         ))
                      )}
                    </div>
                 </div>
            </div>
            
            {/* Auto Debugging Stream (Full Width) */}
            <div className="mt-6">
                <AutomatedDebuggingStreamWidget />
            </div>
        </section>

        {/* Section 3: Royal Finance (Goodness) */}
        <section>
            <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
                💰 Royal Finance (Goodness)
            </h2>
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 items-start">
                 {/* Julie CPA Widget */}
                 <div className="w-full">
                     <JulieCPAWidget />
                 </div>
                 
                 {/* Tax Calculator */}
                 <div className="w-full">
                     <JulieTaxWidget /> 
                 </div>
            </div>
        </section>

        {/* Section 4: Evolution & Creation (Serenity/Eternity) */}
        <section>
            <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
                🌌 Evolution Engine (Serenity)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                 {/* Genesis Controller */}
                 <div className="w-full">
                    <GenesisWidget />
                 </div>
                 
                 {/* Royal Analytics (Output) */}
                 <div className="w-full">
                    <RoyalAnalyticsWidget />
                 </div>
            </div>
        </section>
        
        {/* Section 5: The Seal */}
        <section className="flex justify-center pb-20 pt-10 opacity-80 hover:opacity-100 transition-opacity">
             <FinalEternalVictoryWidget />
        </section>
      </div>

      {/* Voice Panel Overlay */}
      {showVoicePanel && (
        <div className="fixed bottom-8 right-8 z-[100] bg-black/90 rounded-2xl border border-white/20 shadow-2xl">
          <VoiceReactivePanel baseTrinityScore={state.trinityScore ?? undefined} baseRiskScore={state.riskScore ?? undefined} />
        </div>
      )}
    </div>
  );
}

export default AFOPantheon;
