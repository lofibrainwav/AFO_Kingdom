'use client';

import { useEffect, useState, useCallback } from 'react';
import { TrinityGlowCard } from './TrinityGlowCard';
import { VoiceReactivePanel } from './VoiceReactivePanel';
import { useSpatialAudio } from '../hooks/useSpatialAudio';

interface PantheonState {
  trinityScore: number;
  riskScore: number;
  healthStatus: 'excellent' | 'good' | 'warning' | 'critical';
  servicesOnline: number;
  totalServices: number;
  lastUpdate: string;
}

/**
 * AFOPantheon - Phase 8 Perpetual Governance
 * 
 * Unified Control Tower integrating:
 * - Trinity Score with Glow/Dark Aura
 * - System Health (11 오장육부)
 * - Real-time alerts
 * - Voice Reaction overlay
 * 
 * 永 (Eternity): The ultimate governance interface
 */
export function AFOPantheon() {
  const [state, setState] = useState<PantheonState>({
    trinityScore: 1.0,
    riskScore: 0.0,
    healthStatus: 'excellent',
    servicesOnline: 11,
    totalServices: 11,
    lastUpdate: new Date().toISOString(),
  });
  const [showVoicePanel, setShowVoicePanel] = useState(false);
  const [alerts, setAlerts] = useState<string[]>([]);
  
  const { playTrinityUp, playRiskUp, initAudio } = useSpatialAudio();

  // Fetch system state periodically
  const fetchState = useCallback(async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setState(prev => ({
          ...prev,
          trinityScore: data.trinity_score ?? prev.trinityScore,
          riskScore: data.risk_score ?? prev.riskScore,
          healthStatus: data.status ?? prev.healthStatus,
          servicesOnline: data.services_online ?? prev.servicesOnline,
          lastUpdate: new Date().toISOString(),
        }));
      }
    } catch (e) {
      console.warn('Health fetch failed:', e);
    }
  }, []);

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 10000);
    return () => clearInterval(interval);
  }, [fetchState]);

  // Alert when Trinity drops
  useEffect(() => {
    if (state.trinityScore < 0.8) {
      setAlerts(prev => [...prev, `⚠️ Trinity Score Critical: ${(state.trinityScore * 100).toFixed(0)}%`]);
      playRiskUp();
    }
    if (state.riskScore > 0.2) {
      setAlerts(prev => [...prev, `🛑 Risk Alert: ${(state.riskScore * 100).toFixed(0)}%`]);
      playRiskUp();
    }
  }, [state.trinityScore, state.riskScore, playRiskUp]);

  const getStatusColor = () => {
    switch (state.healthStatus) {
      case 'excellent': return '#22c55e';
      case 'good': return '#84cc16';
      case 'warning': return '#eab308';
      case 'critical': return '#ef4444';
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
      padding: '2rem',
      fontFamily: "'Inter', sans-serif",
    }}>
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '2rem',
        padding: '1rem 1.5rem',
        background: 'rgba(255,255,255,0.05)',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.1)',
      }}>
        <div>
          <h1 style={{ color: 'white', fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>
            👑 AFO Pantheon
          </h1>
          <p style={{ color: '#9ca3af', fontSize: '0.75rem', margin: '0.25rem 0 0' }}>
            眞善美孝永 • Perpetual Governance
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            onClick={() => { initAudio(); setShowVoicePanel(!showVoicePanel); }}
            style={{
              padding: '0.5rem 1rem',
              background: showVoicePanel ? '#7c3aed' : 'rgba(255,255,255,0.1)',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              cursor: 'pointer',
            }}
          >
            🎙️ Voice
          </button>
          <div style={{
            padding: '0.5rem 1rem',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '8px',
            color: '#9ca3af',
            fontSize: '0.75rem',
          }}>
            {new Date(state.lastUpdate).toLocaleTimeString()}
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1.5rem',
      }}>
        {/* Trinity Score Card */}
        <TrinityGlowCard trinityScore={state.trinityScore} riskScore={state.riskScore}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>⚖️</div>
            <h2 style={{ color: 'white', margin: 0 }}>Trinity Score</h2>
            <div style={{
              fontSize: '2.5rem',
              fontWeight: 'bold',
              color: state.trinityScore >= 0.9 ? '#22c55e' : state.trinityScore >= 0.7 ? '#eab308' : '#ef4444',
              marginTop: '0.5rem',
            }}>
              {(state.trinityScore * 100).toFixed(0)}%
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
          <VoiceReactivePanel baseTrinityScore={state.trinityScore} baseRiskScore={state.riskScore} />
        </div>
      )}
    </div>
  );
}

export default AFOPantheon;
