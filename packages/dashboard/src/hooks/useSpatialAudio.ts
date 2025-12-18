'use client';

import { useCallback, useEffect, useRef } from 'react';

interface SpatialAudioOptions {
  trinityUp?: boolean;  // Bright chime from above
  riskUp?: boolean;     // Low rumble from behind
}

/**
 * useSpatialAudio - Phase 7 Sensory Integration
 * 
 * Provides 3D spatial audio feedback:
 * - Trinity increase: Clear, bright tone from above (positive)
 * - Risk increase: Low, rumbling warning from behind (alert)
 */
export function useSpatialAudio() {
  const audioContextRef = useRef<AudioContext | null>(null);

  // Initialize AudioContext lazily (requires user interaction)
  const initAudio = useCallback(() => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }
    return audioContextRef.current;
  }, []);

  // Play Trinity Success Sound (bright, from above)
  const playTrinityUp = useCallback(() => {
    try {
      const ctx = initAudio();
      
      // Create oscillator for bright chime
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();
      const panner = ctx.createPanner();
      
      // Position sound above the listener (y = 1)
      panner.positionX.value = 0;
      panner.positionY.value = 1;
      panner.positionZ.value = 0;
      panner.panningModel = 'HRTF';
      
      // Bright, pleasant frequency
      oscillator.type = 'sine';
      oscillator.frequency.value = 880; // A5 - bright note
      
      // Quick fade in/out
      gainNode.gain.setValueAtTime(0, ctx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.1);
      gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.5);
      
      // Connect audio graph
      oscillator.connect(gainNode);
      gainNode.connect(panner);
      panner.connect(ctx.destination);
      
      // Play
      oscillator.start(ctx.currentTime);
      oscillator.stop(ctx.currentTime + 0.5);
    } catch (e) {
      console.warn('Spatial audio not available:', e);
    }
  }, [initAudio]);

  // Play Risk Warning Sound (low rumble from behind)
  const playRiskUp = useCallback(() => {
    try {
      const ctx = initAudio();
      
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();
      const panner = ctx.createPanner();
      
      // Position sound behind the listener (z = -1)
      panner.positionX.value = 0;
      panner.positionY.value = 0;
      panner.positionZ.value = -1;
      panner.panningModel = 'HRTF';
      
      // Low, ominous frequency
      oscillator.type = 'sawtooth';
      oscillator.frequency.value = 110; // A2 - low rumble
      
      // Gradual fade
      gainNode.gain.setValueAtTime(0, ctx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.2, ctx.currentTime + 0.2);
      gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.8);
      
      oscillator.connect(gainNode);
      gainNode.connect(panner);
      panner.connect(ctx.destination);
      
      oscillator.start(ctx.currentTime);
      oscillator.stop(ctx.currentTime + 0.8);
    } catch (e) {
      console.warn('Spatial audio not available:', e);
    }
  }, [initAudio]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      audioContextRef.current?.close();
    };
  }, []);

  return {
    playTrinityUp,
    playRiskUp,
    initAudio, // Call on first user interaction
  };
}

export default useSpatialAudio;
