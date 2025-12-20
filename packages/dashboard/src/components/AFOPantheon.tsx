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
import { useSpatialAudio } from '../hooks/useSpatialAudio';

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
        console.warn('Matrix Parse Error:', e);
      }
    };

    eventSource.onerror = (e) => {
       console.warn('Matrix Stream Disconnected. Reconnecting...', e);
       eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Fetch system state periodically
  const fetchState = useCallback(async () => {
    try {
      const res = await fetch('/api/health'); // Ensure this hits the correct router
      if (res.ok) {
        const data = await res.json();
        // Handle nested structure: data.trinity.trinity_score
        const trinityData = data.trinity || {};
        
        setState(prev => ({
          ...prev,
          trinityScore: trinityData.trinity_score ?? (data.health_percentage ? data.health_percentage/100 : prev.trinityScore),
          riskScore: data.risk_score ?? 0.0,
          healthStatus: data.status ?? prev.healthStatus,
          servicesOnline: data.healthy_organs ?? prev.servicesOnline,
          totalServices: data.total_organs ?? prev.totalServices,
          breakdown: {
              truth: trinityData.truth ?? 1.0,
              goodness: trinityData.goodness ?? 1.0,
              beauty: trinityData.beauty ?? 1.0,
              filial_serenity: trinityData.filial_serenity ?? 1.0,
              eternity: trinityData.eternity ?? 1.0,
          },
          lastUpdate: new Date().toISOString(),
        }));
      }
    } catch (e) {
      console.warn('Health fetch failed:', e);
    }
  }, []);

  // Initial fetch on mount
  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 15000); // Refresh every 15s
    return () => clearInterval(interval);
  }, [fetchState]);

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f0f23, #1a1a2e)',
      padding: '2rem',
    }}>
      {/* Header */}
      <h1 style={{
        color: 'white',
        textAlign: 'center',
        fontSize: '2rem',
        marginBottom: '2rem',
        fontFamily: 'system-ui',
      }}>
        🏰 AFO Pantheon - Command Center
      </h1>

      {/* Main Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1.5rem',
        maxWidth: '1400px',
        margin: '0 auto',
      }}>
        {/* Trinity Score Card */}
        <TrinityGlowCard 
            trinityScore={state.trinityScore} 
            riskScore={state.riskScore}
            breakdown={state.breakdown}
        >
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>⚖️</div>
            <h2 style={{ color: 'white', margin: 0 }}>Trinity Score</h2>
            <div style={{
              fontSize: '2.5rem',
              fontWeight: 'bold',
              color: state.trinityScore === null ? '#6b7280' : state.trinityScore >= 0.9 ? '#22c55e' : state.trinityScore >= 0.7 ? '#eab308' : '#ef4444',
              marginTop: '0.5rem',
            }}>
              {state.trinityScore !== null ? `${(state.trinityScore * 100).toFixed(0)}%` : 'Loading...'}
            </div>
          </div>
        </TrinityGlowCard>

        {/* System Health Card */}
        <div style={{
          padding: '1.5rem',
          background: 'rgba(0,0,0,0.6)',
          borderRadius: '16px',
          border: `2px solid ${getStatusColor()}`,
          boxShadow: `0 0 20px ${getStatusColor()}40`,
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>💚</div>
            <h2 style={{ color: 'white', margin: 0 }}>System Health</h2>
            <div style={{
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: getStatusColor(),
              marginTop: '0.5rem',
              textTransform: 'uppercase',
            }}>
              {state.healthStatus}
            </div>
            <div style={{ color: '#9ca3af', marginTop: '0.5rem', fontSize: '0.875rem' }}>
              {state.servicesOnline}/{state.totalServices} Services Online
            </div>
          </div>
        </div>

        {/* Alerts Card */}
        <div style={{
          padding: '1.5rem',
          background: 'rgba(0,0,0,0.6)',
          borderRadius: '16px',
          border: '1px solid rgba(255,255,255,0.1)',
        }}>
          <h3 style={{ color: 'white', margin: '0 0 1rem' }}>🔔 Recent Alerts</h3>
          {alerts.length === 0 ? (
            <p style={{ color: '#22c55e', fontSize: '0.875rem' }}>✅ No active alerts</p>
          ) : (
            <div style={{ maxHeight: '150px', overflow: 'auto' }}>
              {alerts.slice(-5).map((alert, i) => (
                <div key={i} style={{
                  padding: '0.5rem',
                  marginBottom: '0.5rem',
                  background: 'rgba(239, 68, 68, 0.2)',
                  borderRadius: '8px',
                  color: '#fca5a5',
                  fontSize: '0.75rem',
                }}>
                  {alert}
                </div>
              ))}
            </div>
          )}
        </div>




        {/* Matrix Stream Card (The Soul) */}
        <div style={{
          gridColumn: '1 / -1', // Span full width
          padding: '1.5rem',
          background: 'rgba(0,0,0,0.8)',
          borderRadius: '16px',
          border: `1px solid ${isMatrixActive ? '#22c55e' : 'rgba(34,197,94,0.3)'}`,
          boxShadow: isMatrixActive ? '0 0 15px rgba(34,197,94,0.3)' : 'none',
          transition: 'all 0.3s ease'
        }}>
           <h3 style={{ color: '#22c55e', margin: '0 0 1rem', fontFamily: 'monospace', display: 'flex', justifyContent: 'space-between' }}>
             <span>👁️ MATRIX STREAM (OBSERVABILITY)</span>
             <span style={{ fontSize: '0.8rem', opacity: isMatrixActive ? 1 : 0.5 }}>{isMatrixActive ? '● RECEIVING' : '○ IDLE'}</span>
           </h3>
           <div style={{
             height: '150px',
             overflowY: 'auto',
             fontFamily: 'monospace',
             fontSize: '0.75rem',
             color: '#4ade80',
             display: 'flex',
             flexDirection: 'column-reverse' // Scroll from bottom
           }}>
             {thoughts.length === 0 ? (
                <div style={{ color: '#166534' }}>Waiting for system thoughts...</div>
             ) : (
                thoughts.map((t, i) => (
                  <div key={i} style={{ marginBottom: '0.25rem', borderBottom: '1px solid rgba(34,197,94,0.1)' }}>
                    {t}
                  </div>
                ))
             )}
           </div>
        </div>
        
        {/* Project Genesis (Self-Expanding Kingdom - v100.0) */}
        <div style={{ gridColumn: '1 / -1', marginTop: '1.5rem' }}>
             <GenesisWidget />
        </div>
        
        {/* Julie CPA (Financial Guardian - Phase 12) */}
        <div style={{ gridColumn: '1 / -1', marginTop: '1rem' }}>
             <JulieCPAWidget />
        </div>
        
        {/* SSOT Monitor (Compass) */}
        <div style={{ gridColumn: '1 / -1', marginTop: '1rem' }}>
             <SSOTMonitor />
        </div>

        {/* 🏆 FINAL ETERNAL VICTORY SEAL (v100.0) */}
        <div style={{ gridColumn: '1 / -1', marginTop: '3rem', marginBottom: '4rem' }}>
             <FinalEternalVictoryWidget />
        </div>
      </div>

      {/* Voice Panel Overlay */}
      {showVoicePanel && (
        <div style={{
          position: 'fixed',
          bottom: '2rem',
          right: '2rem',
          zIndex: 100,
          background: 'rgba(0,0,0,0.9)',
          borderRadius: '16px',
          border: '1px solid rgba(255,255,255,0.2)',
          boxShadow: '0 10px 40px rgba(0,0,0,0.5)',
        }}>
          <VoiceReactivePanel baseTrinityScore={state.trinityScore ?? undefined} baseRiskScore={state.riskScore ?? undefined} />
        </div>
      )}
    </div>
  );
}

export default AFOPantheon;
