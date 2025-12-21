'use client';

import { useEffect, useState, useCallback } from 'react';
import { TrinityGlowCard } from './TrinityGlowCard';
import { VoiceReactivePanel } from './VoiceReactivePanel';

import { SandboxCanvas } from './genui/SandboxCanvas';
import { AICPAJulieWidget } from './genui/AICPAJulieWidget';
import { SSOTMonitor } from './genui/SSOTMonitor';
import { JulieCPAWidget } from './genui/JulieCPAWidget';
import { GenesisWidget } from './genui/GenesisWidget';
import { FinalEternalVictoryWidget } from './genui/FinalEternalVictoryWidget';
import AutomatedDebuggingStreamWidget from './genui/AutomatedDebuggingStreamWidget';
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

  // Helper function for status color
  const getStatusColor = () => {
    switch (state.healthStatus) {
      case 'excellent': return '#22c55e';
      case 'good': return '#84cc16';
      case 'warning': return '#eab308';
      case 'critical': return '#ef4444';
      default: return '#6b7280';
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
    fetchState();
    const interval = setInterval(fetchState, 15000); // Refresh every 15s
    return () => clearInterval(interval);
  }, [fetchState]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900 p-8">
      {/* Header */}
      <h1 className="text-white text-center text-3xl mb-8 font-sans">
        🏰 AFO Pantheon - Command Center
      </h1>

      {/* Main Grid */}
      <div className="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6 max-w-[1400px] mx-auto">
        {/* Trinity Score Card */}
        <TrinityGlowCard
            trinityScore={state.trinityScore}
            riskScore={state.riskScore}
            breakdown={state.breakdown}
        >
          <div className="text-center">
            <div className="text-5xl mb-2">⚖️</div>
            <h2 className="text-white m-0">Trinity Score</h2>
            <div 
              className="text-4xl font-bold mt-2"
              style={{
                color: state.trinityScore === null ? '#6b7280' : state.trinityScore >= 0.9 ? '#22c55e' : state.trinityScore >= 0.7 ? '#eab308' : '#ef4444',
              }}
            >
              {state.trinityScore !== null ? `${(state.trinityScore * 100).toFixed(0)}%` : 'Loading...'}
            </div>
          </div>
        </TrinityGlowCard>

        {/* System Health Card */}
        <div 
          className="p-6 bg-black/60 rounded-2xl"
          style={{
            border: `2px solid ${getStatusColor()}`,
            boxShadow: `0 0 20px ${getStatusColor()}40`,
          }}
        >
          <div className="text-center">
            <div className="text-5xl mb-2">💚</div>
            <h2 className="text-white m-0">System Health</h2>
            <div 
              className="text-xl font-bold mt-2 uppercase"
              style={{ color: getStatusColor() }}
            >
              {state.healthStatus}
            </div>
            <div className="text-gray-400 mt-2 text-sm">
              {state.servicesOnline}/{state.totalServices} Services Online
            </div>
          </div>
        </div>

        {/* Alerts Card */}
        <div className="p-6 bg-black/60 rounded-2xl border border-white/10">
          <h3 className="text-white m-0 mb-4">🔔 Recent Alerts</h3>
          {alerts.length === 0 ? (
            <p className="text-green-500 text-sm">✅ No active alerts</p>
          ) : (
            <div className="max-h-[150px] overflow-auto">
              {alerts.slice(-5).map((alert, i) => (
                <div key={i} className="p-2 mb-2 bg-red-500/20 rounded-lg text-red-300 text-xs">
                  {alert}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* SSOT Monitor (Compass) - 상단 배치 */}
        <SSOTMonitor />



        {/* Matrix Stream Card (The Soul) */}
        <div 
          className="col-span-full p-6 bg-black/80 rounded-2xl transition-all duration-300"
          style={{
            border: `1px solid ${isMatrixActive ? '#22c55e' : 'rgba(34,197,94,0.3)'}`,
            boxShadow: isMatrixActive ? '0 0 15px rgba(34,197,94,0.3)' : 'none',
          }}
        >
           <h3 className="text-green-500 m-0 mb-4 font-mono flex justify-between">
             <span>👁️ MATRIX STREAM (OBSERVABILITY)</span>
             <span className={`text-xs ${isMatrixActive ? 'opacity-100' : 'opacity-50'}`}>
               {isMatrixActive ? '● RECEIVING' : '○ IDLE'}
             </span>
           </h3>
           <div className="h-[150px] overflow-y-auto font-mono text-xs text-green-400 flex flex-col-reverse">
             {thoughts.length === 0 ? (
                <div className="text-green-800">Waiting for system thoughts...</div>
             ) : (
                thoughts.map((t, i) => (
                  <div key={i} className="mb-1 border-b border-green-500/10">
                    {t}
                  </div>
                ))
             )}
           </div>
        </div>

        {/* 자동화 디버깅 시스템 (Real-time Monitoring) */}
        <div className="col-span-full mt-6">
             <AutomatedDebuggingStreamWidget />
        </div>

        {/* Project Genesis (Self-Expanding Kingdom - v100.0) */}
        <div className="col-span-full mt-6">
             <GenesisWidget />
        </div>

        {/* Julie CPA (Financial Guardian - Phase 12) */}
        <div className="col-span-full mt-4">
             <JulieCPAWidget />
        </div>


        {/* 🏆 FINAL ETERNAL VICTORY SEAL (v100.0) */}
        <div className="col-span-full mt-12 mb-16">
             <FinalEternalVictoryWidget />
        </div>
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
