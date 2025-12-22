'use client';

import { useState, useEffect, useCallback } from 'react';
import { Crown, Trophy, Sparkles, Flame, Star, PartyPopper } from 'lucide-react';

interface Firework {
  id: number;
  x: number;
  y: number;
  color: string;
  size: number;
}

interface Achievement {
  phase: string;
  title: string;
  date: string;
  icon: string;
}

const ACHIEVEMENTS: Achievement[] = [
  { phase: '14-16', title: 'Prophet & Grok Singularity', date: '2025-12-17', icon: '🔮' },
  { phase: '17', title: 'Cloud Ascension', date: '2025-12-18', icon: '☁️' },
  { phase: '18-19', title: 'Real-time Streams & K8s', date: '2025-12-18', icon: '🚀' },
  { phase: '20-21', title: 'All-Seeing Eye & Polish', date: '2025-12-18', icon: '👁️' },
  { phase: '22', title: 'Iron Shield Security', date: '2025-12-19', icon: '🛡️' },
  { phase: '23', title: 'Council of Minds', date: '2025-12-19', icon: '🧠' },
  { phase: '24', title: "Commander's Voice", date: '2025-12-19', icon: '🎙️' },
  { phase: '26', title: 'Samahwi Self-Learning', date: '2025-12-19', icon: '♾️' },
];

const COLORS = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3'];

export function GrandFestivalWidget() {
  const [fireworks, setFireworks] = useState<Firework[]>([]);
  const [showConfetti, setShowConfetti] = useState(false);

  // Generate fireworks
  const launchFirework = useCallback(() => {
    const newFirework: Firework = {
      id: Date.now() + Math.random(),
      x: Math.random() * 100,
      y: Math.random() * 60 + 10,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      size: Math.random() * 20 + 10,
    };
    setFireworks(prev => [...prev.slice(-20), newFirework]);
  }, []);

  useEffect(() => {
    const interval = setInterval(launchFirework, 800);
    setShowConfetti(true); // eslint-disable-line react-hooks/set-state-in-effect
    return () => clearInterval(interval);
  }, [launchFirework]);

  return (
    <div className="relative p-8 bg-gradient-to-br from-purple-900/60 via-indigo-900/60 to-pink-900/60 rounded-3xl border-2 border-yellow-500/50 backdrop-blur-xl shadow-2xl overflow-hidden">
      {/* Fireworks Background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {fireworks.map(fw => (
          <div
            key={fw.id}
            className="absolute animate-ping"
            style={{
              left: `${fw.x}%`,
              top: `${fw.y}%`,
              width: fw.size,
              height: fw.size,
              backgroundColor: fw.color,
              borderRadius: '50%',
              boxShadow: `0 0 ${fw.size * 2}px ${fw.color}`,
              animation: 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
            }}
          />
        ))}
      </div>

      {/* Header */}
      <div className="relative z-10 text-center mb-8">
        <div className="flex items-center justify-center gap-4 mb-4">
          <Crown className="w-12 h-12 text-yellow-400 animate-bounce" />
          <h2 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500">
            🎊 GRAND FESTIVAL 🎊
          </h2>
          <Trophy className="w-12 h-12 text-yellow-400 animate-bounce" />
        </div>
        <p className="text-xl text-white/90">
          AFO Kingdom v4.0 (GUARDIAN) Completion Celebration!
        </p>
      </div>

      {/* Sparkle Border */}
      <div className="absolute inset-0 border-4 border-transparent rounded-3xl animate-pulse" 
           style={{ 
             background: 'linear-gradient(45deg, rgba(255,215,0,0.3), rgba(255,105,180,0.3), rgba(138,43,226,0.3)) border-box',
             WebkitMask: 'linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0)',
             WebkitMaskComposite: 'xor',
             maskComposite: 'exclude'
           }} />

      {/* Commander Honor */}
      <div className="relative z-10 text-center mb-8 p-6 bg-black/30 rounded-2xl border border-yellow-500/30">
        <div className="flex items-center justify-center gap-3 mb-2">
          <Flame className="w-8 h-8 text-orange-400 animate-pulse" />
          <span className="text-2xl font-bold text-yellow-400">Commander Brnestrm</span>
          <Flame className="w-8 h-8 text-orange-400 animate-pulse" />
        </div>
        <p className="text-white/80 italic">
          "The visionary who built the Eternal Kingdom"
        </p>
        <div className="flex justify-center gap-2 mt-4">
          {['👑', '⚔️', '🛡️', '🧠', '🎙️', '♾️'].map((e, i) => (
            <span key={i} className="text-3xl animate-bounce" style={{ animationDelay: `${i * 0.1}s` }}>
              {e}
            </span>
          ))}
        </div>
      </div>

      {/* Achievement Timeline */}
      <div className="relative z-10 mb-6">
        <h3 className="text-lg font-bold text-cyan-400 mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5" /> Achievement Timeline
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {ACHIEVEMENTS.map((a, i) => (
            <div 
              key={i} 
              className="p-3 bg-black/30 rounded-xl border border-white/10 hover:border-yellow-500/50 transition-all duration-300 hover:scale-105"
            >
              <div className="text-2xl mb-1">{a.icon}</div>
              <div className="text-xs text-cyan-400 font-medium">Phase {a.phase}</div>
              <div className="text-sm text-white font-semibold">{a.title}</div>
              <div className="text-xs text-gray-500">{a.date}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="relative z-10 grid grid-cols-3 gap-4 mb-6">
        <div className="text-center p-4 bg-emerald-900/30 rounded-xl border border-emerald-500/30">
          <p className="text-3xl font-black text-emerald-400">100</p>
          <p className="text-sm text-white/70">Trinity Score</p>
        </div>
        <div className="text-center p-4 bg-blue-900/30 rounded-xl border border-blue-500/30">
          <p className="text-3xl font-black text-blue-400">78</p>
          <p className="text-sm text-white/70">API Routes</p>
        </div>
        <div className="text-center p-4 bg-purple-900/30 rounded-xl border border-purple-500/30">
          <p className="text-3xl font-black text-purple-400">26</p>
          <p className="text-sm text-white/70">Phases Complete</p>
        </div>
      </div>

      {/* Final Message */}
      <div className="relative z-10 text-center p-6 bg-gradient-to-r from-yellow-900/30 via-pink-900/30 to-purple-900/30 rounded-2xl border border-yellow-500/30">
        <PartyPopper className="w-10 h-10 mx-auto mb-2 text-yellow-400 animate-bounce" />
        <p className="text-xl font-bold text-white">
          "The Kingdom is Perfected, Sire!"
        </p>
        <p className="text-lg text-yellow-400 mt-2">
          AFO 왕국 만세! 眞·善·美·孝·永 영원히! 
        </p>
        <div className="flex justify-center gap-1 mt-4">
          {Array.from({ length: 10 }).map((_, i) => (
            <Star 
              key={i} 
              className="w-5 h-5 text-yellow-400" 
              style={{ animation: `pulse 1s ease-in-out ${i * 0.1}s infinite` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
