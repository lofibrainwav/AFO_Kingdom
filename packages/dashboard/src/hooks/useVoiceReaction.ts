'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { logError } from '@/lib/logger';

interface VoiceMetrics {
  volume: number;    // 0-1 (normalized)
  pitch: number;     // Hz (estimated fundamental frequency)
  isActive: boolean; // Whether voice is detected
}

/**
 * useVoiceReaction - Phase 7 Sensory Integration
 * 
 * Analyzes user voice input in real-time:
 * - Volume: Loudness (high = urgency → affects Risk)
 * - Pitch: Tone (high = excitement, low = calm → affects Trinity)
 */
export function useVoiceReaction() {
  const [metrics, setMetrics] = useState<VoiceMetrics>({
    volume: 0,
    pitch: 0,
    isActive: false,
  });
  const [isListening, setIsListening] = useState(false);
  
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const animationRef = useRef<number | null>(null);

  // Start listening to microphone
  const startListening = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      audioContextRef.current = audioContext;

      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 2048;
      analyserRef.current = analyser;

      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      setIsListening(true);
      
      // Start analysis loop
      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      
      const analyze = () => {
        if (!analyserRef.current) return;
        
        analyserRef.current.getByteFrequencyData(dataArray);
        
        // Calculate volume (average amplitude)
        const sum = dataArray.reduce((a, b) => a + b, 0);
        const avg = sum / dataArray.length;
        const volume = Math.min(1, avg / 128); // Normalize to 0-1
        
        // Estimate pitch (find dominant frequency)
        let maxIndex = 0;
        let maxValue = 0;
        for (let i = 0; i < dataArray.length; i++) {
          if (dataArray[i] > maxValue) {
            maxValue = dataArray[i];
            maxIndex = i;
          }
        }
        const pitch = (maxIndex * audioContext.sampleRate) / analyser.fftSize;
        
        // Detect if voice is active (volume above threshold)
        const isActive = volume > 0.1;
        
        setMetrics({ volume, pitch, isActive });
        
        animationRef.current = requestAnimationFrame(analyze);
      };
      
      analyze();
    } catch (err) {
      logError('Microphone access denied', { error: err instanceof Error ? err.message : 'Unknown error' });
    }
  }, []);

  // Stop listening
  const stopListening = useCallback(() => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    setIsListening(false);
    setMetrics({ volume: 0, pitch: 0, isActive: false });
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopListening();
    };
  }, [stopListening]);

  // Calculate Trinity/Risk adjustments based on voice
  const getScoreAdjustments = useCallback(() => {
    if (!metrics.isActive) return { trinityDelta: 0, riskDelta: 0 };
    
    // High volume suggests urgency → increase Risk
    const riskDelta = metrics.volume > 0.5 ? (metrics.volume - 0.5) * 0.1 : 0;
    
    // Calm, steady tone suggests confidence → increase Trinity
    // Very high pitch (stress) or very low (concern) → decrease Trinity
    const normalPitch = 200; // Average speaking pitch
    const pitchDeviation = Math.abs(metrics.pitch - normalPitch) / normalPitch;
    const trinityDelta = pitchDeviation < 0.3 ? 0.05 : -0.02;
    
    return { trinityDelta, riskDelta };
  }, [metrics]);

  return {
    metrics,
    isListening,
    startListening,
    stopListening,
    getScoreAdjustments,
  };
}

export default useVoiceReaction;
