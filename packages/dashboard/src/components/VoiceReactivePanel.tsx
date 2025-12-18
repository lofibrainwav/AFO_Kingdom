'use client';

import { useEffect, useState } from 'react';
import { TrinityGlowCard } from './TrinityGlowCard';
import { useSpatialAudio } from '../hooks/useSpatialAudio';
import { useVoiceReaction } from '../hooks/useVoiceReaction';

interface VoiceReactivePanelProps {
  baseTrinityScore?: number;
  baseRiskScore?: number;
}

/**
 * VoiceReactivePanel - Final Sensory Integration
 * 
 * Combines:
 * - Voice input analysis (volume/pitch)
 * - Trinity Glow animation
 * - Spatial Audio feedback
 * 
 * 美 (Beauty): Visual + Audio immersion
 * 孝 (Serenity): Responsive, friction-free interaction
 */
export function VoiceReactivePanel({ 
  baseTrinityScore = 0.85,
  baseRiskScore = 0.15 
}: VoiceReactivePanelProps) {
  const [trinityScore, setTrinityScore] = useState(baseTrinityScore);
  const [riskScore, setRiskScore] = useState(baseRiskScore);
  
  const { playTrinityUp, playRiskUp, initAudio } = useSpatialAudio();
  const { 
    metrics, 
    isListening, 
    startListening, 
    stopListening,
    getScoreAdjustments 
  } = useVoiceReaction();

  // Update scores based on voice input
  useEffect(() => {
    if (!isListening) return;
    
    const { trinityDelta, riskDelta } = getScoreAdjustments();
    
    setTrinityScore(prev => {
      const newScore = Math.min(1.0, Math.max(0.0, prev + trinityDelta));
      // Play audio on significant increase
      if (newScore > prev + 0.03) playTrinityUp();
      return newScore;
    });
    
    setRiskScore(prev => {
      const newScore = Math.min(1.0, Math.max(0.0, prev + riskDelta));
      // Play warning on risk increase
      if (newScore > 0.25 && riskDelta > 0) playRiskUp();
      return newScore;
    });
  }, [metrics, isListening, getScoreAdjustments, playTrinityUp, playRiskUp]);

  const handleToggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      initAudio();
      startListening();
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '1.5rem' }}>
      <h2 style={{ 
        color: 'white', 
        fontSize: '1.25rem', 
        fontWeight: 'bold',
        marginBottom: '1rem',
        textAlign: 'center'
      }}>
        🎙️ Voice-Reactive Trinity
      </h2>
      
      <TrinityGlowCard trinityScore={trinityScore} riskScore={riskScore}>
        {/* Voice Metrics Display */}
        <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
          <div style={{ 
            fontSize: '3rem',
            marginBottom: '0.5rem'
          }}>
            {isListening ? '🎤' : '🔇'}
          </div>
          
          {isListening && (
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '1rem',
              marginTop: '1rem',
            }}>
              <div style={{
                background: 'rgba(255,255,255,0.1)',
                padding: '0.75rem',
                borderRadius: '8px',
              }}>
                <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>Volume</div>
                <div style={{ 
                  color: 'white', 
                  fontWeight: 'bold',
                  fontFamily: 'monospace'
                }}>
                  {(metrics.volume * 100).toFixed(0)}%
                </div>
                <div style={{
                  height: '4px',
                  background: 'rgba(255,255,255,0.2)',
                  borderRadius: '2px',
                  marginTop: '4px',
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${metrics.volume * 100}%`,
                    background: metrics.volume > 0.5 ? '#ef4444' : '#22c55e',
                    transition: 'all 0.1s',
                  }} />
                </div>
              </div>
              
              <div style={{
                background: 'rgba(255,255,255,0.1)',
                padding: '0.75rem',
                borderRadius: '8px',
              }}>
                <div style={{ color: '#9ca3af', fontSize: '0.75rem' }}>Pitch</div>
                <div style={{ 
                  color: 'white', 
                  fontWeight: 'bold',
                  fontFamily: 'monospace'
                }}>
                  {metrics.pitch.toFixed(0)} Hz
                </div>
                <div style={{
                  color: '#9ca3af',
                  fontSize: '0.625rem',
                  marginTop: '4px',
                }}>
                  {metrics.pitch < 150 ? '🔊 Low' : metrics.pitch > 300 ? '🔔 High' : '🎵 Normal'}
                </div>
              </div>
            </div>
          )}
        </div>
      </TrinityGlowCard>
      
      {/* Control Button */}
      <button
        onClick={handleToggleListening}
        style={{
          width: '100%',
          padding: '0.875rem',
          marginTop: '1rem',
          borderRadius: '12px',
          background: isListening 
            ? 'linear-gradient(135deg, #dc2626, #991b1b)' 
            : 'linear-gradient(135deg, #22c55e, #16a34a)',
          color: 'white',
          fontWeight: 'bold',
          fontSize: '0.875rem',
          cursor: 'pointer',
          border: 'none',
          boxShadow: isListening 
            ? '0 0 20px rgba(220, 38, 38, 0.4)' 
            : '0 0 20px rgba(34, 197, 94, 0.4)',
          transition: 'all 0.3s',
        }}
      >
        {isListening ? '⏹️ Stop Listening' : '🎙️ Start Voice Reaction'}
      </button>
      
      <p style={{
        color: '#6b7280',
        fontSize: '0.75rem',
        textAlign: 'center',
        marginTop: '0.75rem',
      }}>
        Your voice tone affects Trinity Score in real-time
      </p>
    </div>
  );
}

export default VoiceReactivePanel;
