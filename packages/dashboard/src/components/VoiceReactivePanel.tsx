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
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { TrinityGlowCard } from "./TrinityGlowCard";
import { useSpatialAudio } from "../hooks/useSpatialAudio";
import { useVoiceReaction } from "../hooks/useVoiceReaction";
import ErrorBoundary from "./common/ErrorBoundary";

interface VoiceReactivePanelProps {
  baseTrinityScore?: number;
  baseRiskScore?: number;
}

function VoiceReactivePanelContent({
  baseTrinityScore = 0.85,
  baseRiskScore = 0.15,
}: VoiceReactivePanelProps) {
  const [trinityScore, setTrinityScore] = useState(baseTrinityScore);
  const [riskScore, setRiskScore] = useState(baseRiskScore);

  const { playTrinityUp, playRiskUp, initAudio } = useSpatialAudio();
  const { metrics, isListening, startListening, stopListening, getScoreAdjustments } =
    useVoiceReaction();

  // Memoize score adjustments
  const scoreAdjustments = useMemo(() => {
    if (!isListening) return { trinityDelta: 0, riskDelta: 0 };
    return getScoreAdjustments();
  }, [isListening, getScoreAdjustments]);

  // Memoize formatted metrics
  const formattedMetrics = useMemo(() => {
    return {
      volume: metrics.volume * 100,
      volumePercent: (metrics.volume * 100).toFixed(0),
      pitch: metrics.pitch.toFixed(0),
      pitchLabel:
        metrics.pitch < 150 ? "🔊 Low" : metrics.pitch > 300 ? "🔔 High" : "🎵 Normal",
      volumeColor: metrics.volume > 0.5 ? "#ef4444" : "#22c55e",
    };
  }, [metrics.volume, metrics.pitch]);

  // Memoize toggle handler
  const handleToggleListening = useCallback(() => {
    if (isListening) {
      stopListening();
    } else {
      initAudio();
      startListening();
    }
  }, [isListening, stopListening, initAudio, startListening]);

  // Update scores based on voice input
  useEffect(() => {
    if (!isListening) return;

    const { trinityDelta, riskDelta } = scoreAdjustments;

    // Use setTimeout to avoid synchronous setState in effect
    setTimeout(() => {
      setTrinityScore((prev) => {
        const newScore = Math.min(1.0, Math.max(0.0, prev + trinityDelta));
        // Play audio on significant increase
        if (newScore > prev + 0.03) playTrinityUp();
        return newScore;
      });

      setRiskScore((prev) => {
        const newScore = Math.min(1.0, Math.max(0.0, prev + riskDelta));
        // Play warning on risk increase
        if (newScore > 0.25 && riskDelta > 0) playRiskUp();
        return newScore;
      });
    }, 0);
  }, [scoreAdjustments, isListening, playTrinityUp, playRiskUp]);

  // Memoize button styles
  const buttonStyles = useMemo(() => {
    return isListening
      ? "bg-gradient-to-br from-red-600 to-red-800 shadow-[0_0_20px_rgba(220,38,38,0.4)]"
      : "bg-gradient-to-br from-green-500 to-green-600 shadow-[0_0_20px_rgba(34,197,94,0.4)]";
  }, [isListening]);

  return (
    <div
      className="max-w-[500px] mx-auto p-6"
      role="region"
      aria-labelledby="voice-panel-title"
    >
      <h2
        id="voice-panel-title"
        className="text-white text-xl font-bold mb-4 text-center"
      >
        🎙️ Voice-Reactive Trinity
      </h2>

      <TrinityGlowCard trinityScore={trinityScore} riskScore={riskScore}>
        {/* Voice Metrics Display */}
        <div className="text-center mb-4" role="status" aria-live="polite">
          <div className="text-5xl mb-2" aria-hidden="true">
            {isListening ? "🎤" : "🔇"}
          </div>
          <span className="sr-only">
            {isListening ? "Listening" : "Not listening"}
          </span>

          {isListening && (
            <div
              className="grid grid-cols-2 gap-4 mt-4"
              role="list"
              aria-label="Voice metrics"
            >
              <div
                className="bg-white/10 p-3 rounded-lg"
                role="listitem"
                aria-label={`Volume: ${formattedMetrics.volumePercent}%`}
              >
                <div className="text-gray-400 text-xs">Volume</div>
                <div className="text-white font-bold font-mono">
                  {formattedMetrics.volumePercent}%
                </div>
                <div
                  className="h-1 bg-white/20 rounded mt-1 overflow-hidden"
                  role="progressbar"
                  aria-valuenow={formattedMetrics.volume}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label={`Volume level: ${formattedMetrics.volumePercent}%`}
                >
                  <div
                    className="h-full transition-all duration-100"
                    style={{
                      width: `${formattedMetrics.volume}%`,
                      background: formattedMetrics.volumeColor,
                    }}
                  />
                </div>
              </div>

              <div
                className="bg-white/10 p-3 rounded-lg"
                role="listitem"
                aria-label={`Pitch: ${formattedMetrics.pitch} Hz, ${formattedMetrics.pitchLabel}`}
              >
                <div className="text-gray-400 text-xs">Pitch</div>
                <div className="text-white font-bold font-mono">
                  {formattedMetrics.pitch} Hz
                </div>
                <div className="text-gray-400 text-[10px] mt-1">
                  {formattedMetrics.pitchLabel}
                </div>
              </div>
            </div>
          )}
        </div>
      </TrinityGlowCard>

      {/* Control Button */}
      <button
        onClick={handleToggleListening}
        className={`w-full py-3.5 mt-4 rounded-xl text-white font-bold text-sm cursor-pointer border-none transition-all duration-300 ${buttonStyles}`}
        aria-label={isListening ? "Stop listening" : "Start voice reaction"}
        aria-pressed={isListening}
      >
        {isListening ? "⏹️ Stop Listening" : "🎙️ Start Voice Reaction"}
      </button>

      <p className="text-gray-500 text-xs text-center mt-3" aria-live="polite">
        Your voice tone affects Trinity Score in real-time
      </p>
    </div>
  );
}

export function VoiceReactivePanel(props: VoiceReactivePanelProps) {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("VoiceReactivePanel error:", error, errorInfo);
      }}
      fallback={
        <div
          className="max-w-[500px] mx-auto p-6"
          role="alert"
        >
          <p className="text-red-400 text-center">
            Voice Reactive Panel을 불러올 수 없습니다.
          </p>
        </div>
      }
    >
      <VoiceReactivePanelContent {...props} />
    </ErrorBoundary>
  );
}

export default VoiceReactivePanel;
