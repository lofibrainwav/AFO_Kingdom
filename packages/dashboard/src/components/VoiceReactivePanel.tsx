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
    
    // Use setTimeout to avoid synchronous setState in effect
    setTimeout(() => {
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
    }, 0);
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
    <div className="max-w-[500px] mx-auto p-6">
      <h2 className="text-white text-xl font-bold mb-4 text-center">
        🎙️ Voice-Reactive Trinity
      </h2>
      
      <TrinityGlowCard trinityScore={trinityScore} riskScore={riskScore}>
        {/* Voice Metrics Display */}
        <div className="text-center mb-4">
          <div className="text-5xl mb-2">
            {isListening ? '🎤' : '🔇'}
          </div>
          
          {isListening && (
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="bg-white/10 p-3 rounded-lg">
                <div className="text-gray-400 text-xs">Volume</div>
                <div className="text-white font-bold font-mono">
                  {(metrics.volume * 100).toFixed(0)}%
                </div>
                <div className="h-1 bg-white/20 rounded mt-1 overflow-hidden">
                  <div 
                    className="h-full transition-all duration-100"
                    style={{
                      width: `${metrics.volume * 100}%`,
                      background: metrics.volume > 0.5 ? '#ef4444' : '#22c55e',
                    }}
                  />
                </div>
              </div>
              
              <div className="bg-white/10 p-3 rounded-lg">
                <div className="text-gray-400 text-xs">Pitch</div>
                <div className="text-white font-bold font-mono">
                  {metrics.pitch.toFixed(0)} Hz
                </div>
                <div className="text-gray-400 text-[10px] mt-1">
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
        className={`w-full py-3.5 mt-4 rounded-xl text-white font-bold text-sm cursor-pointer border-none transition-all duration-300 ${
          isListening 
            ? 'bg-gradient-to-br from-red-600 to-red-800 shadow-[0_0_20px_rgba(220,38,38,0.4)]' 
            : 'bg-gradient-to-br from-green-500 to-green-600 shadow-[0_0_20px_rgba(34,197,94,0.4)]'
        }`}
      >
        {isListening ? '⏹️ Stop Listening' : '🎙️ Start Voice Reaction'}
      </button>
      
      <p className="text-gray-500 text-xs text-center mt-3">
        Your voice tone affects Trinity Score in real-time
      </p>
    </div>
  );
}

export default VoiceReactivePanel;
