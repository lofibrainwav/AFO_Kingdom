"use client";

import { motion } from "framer-motion";
import { useState, useEffect, useRef } from "react";
import clsx from "clsx";

interface TrinityGlowProps {
  score?: number; // 0-100
  isActive?: boolean;
}

export default function TrinityGlow({ score = 85, isActive = false }: TrinityGlowProps) {
  const [audioLevel, setAudioLevel] = useState(0);
  const [initialized, setInitialized] = useState(false);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const rafRef = useRef<number | null>(null);

  const initializeAudio = async () => {
    try {
      if (!audioContextRef.current) {
        const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
        audioContextRef.current = new AudioContextClass();
        analyserRef.current = audioContextRef.current.createAnalyser();
        analyserRef.current.fftSize = 256;
        
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = audioContextRef.current.createMediaStreamSource(stream);
        source.connect(analyserRef.current);
        
        const update = () => {
          if (analyserRef.current) {
            const bufferLength = analyserRef.current.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            analyserRef.current.getByteFrequencyData(dataArray);
            
            // Calculate average volume
            let sum = 0;
            for (let i = 0; i < bufferLength; i++) {
              sum += dataArray[i];
            }
            const average = sum / bufferLength;
            // Normalize to 0-1 range roughly
            setAudioLevel(Math.min(average / 50, 2.0)); 
          }
          rafRef.current = requestAnimationFrame(update);
        };
        update();
        setInitialized(true);
      } else if (audioContextRef.current.state === 'suspended') {
        await audioContextRef.current.resume();
        setInitialized(true);
      }
    } catch (e) {
      console.error("Audio initialization failed (Mic permission denied?):", e);
      // Fallback: simulate breathing if audio fails
      setInitialized(true); 
    }
  };

  useEffect(() => {
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      if (audioContextRef.current) audioContextRef.current.close();
    };
  }, []);

  // Map Trinity Score to color themes
  // > 90: Divine Platinum/Blue
  // > 70: Stable Green
  // < 70: Warning Red/Orange
  const getGradient = () => {
    if (score >= 90) return "from-indigo-500/20 via-purple-500/10 to-transparent"; // Platinum/Divine
    if (score >= 70) return "from-emerald-500/20 via-teal-500/10 to-transparent";   // Goodness
    return "from-rose-500/20 via-orange-500/10 to-transparent";                    // Warning
  };

  return (
    <>
      {/* Background Glow Layer */}
      <motion.div
        className={clsx(
          "fixed inset-0 pointer-events-none -z-10 bg-gradient-to-br transition-colors duration-1000",
          getGradient()
        )}
        animate={{
          opacity: [0.3, 0.5 + (audioLevel * 0.2), 0.3],
          scale: [1, 1.05 + (audioLevel * 0.1), 1],
        }}
        transition={{
          duration: initialized && audioLevel > 0.1 ? 0.2 : 4, // Fast response to audio, slow breathe otherwise
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* Initialize Button (Only visible if not initialized) */}
      {!initialized && (
        <div className="fixed bottom-8 right-8 z-50">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={initializeAudio}
            className="neu-btn px-6 py-3 rounded-full text-xs font-bold tracking-widest text-slate-500 bg-slate-200/50 backdrop-blur-md border border-white/50 shadow-lg flex items-center gap-2"
          >
            <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse"/>
            INITIALIZE NERVOUS SYSTEM
          </motion.button>
        </div>
      )}
    </>
  );
}
