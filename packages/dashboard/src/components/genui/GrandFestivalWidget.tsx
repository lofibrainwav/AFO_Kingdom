/**
 * GrandFestivalWidget.tsx
 * 
 * Grand Festival 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import ErrorBoundary from "@/components/common/ErrorBoundary";
import { Crown, Flame, PartyPopper, Sparkles, Star, Trophy } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

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
  { phase: "14-16", title: "Prophet & Grok Singularity", date: "2025-12-17", icon: "🔮" },
  { phase: "17", title: "Cloud Ascension", date: "2025-12-18", icon: "☁️" },
  { phase: "18-19", title: "Real-time Streams & K8s", date: "2025-12-18", icon: "🚀" },
  { phase: "20-21", title: "All-Seeing Eye & Polish", date: "2025-12-18", icon: "👁️" },
  { phase: "22", title: "Iron Shield Security", date: "2025-12-19", icon: "🛡️" },
  { phase: "23", title: "Council of Minds", date: "2025-12-19", icon: "🧠" },
  { phase: "24", title: "Commander's Voice", date: "2025-12-19", icon: "🎙️" },
  { phase: "26", title: "Samahwi Self-Learning", date: "2025-12-19", icon: "♾️" },
];

const COLORS = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#F38181", "#AA96DA", "#FCBAD3"];

function GrandFestivalWidgetContent() {
  const [fireworks, setFireworks] = useState<Firework[]>([]);

  // Memoize launch firework function
  const launchFirework = useCallback(() => {
    const newFirework: Firework = {
      id: Date.now() + Math.random(),
      x: Math.random() * 100,
      y: Math.random() * 60 + 10,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      size: Math.random() * 20 + 10,
    };
    setFireworks((prev) => [...prev.slice(-20), newFirework]);
  }, []);

  useEffect(() => {
    const interval = setInterval(launchFirework, 800);
    return () => clearInterval(interval);
  }, [launchFirework]);

  // Memoize stats
  const stats = useMemo(
    () => ({
      trinityScore: 100,
      apiRoutes: 78,
      phasesComplete: 26,
    }),
    []
  );

  // Memoize honor emojis
  const honorEmojis = useMemo(() => ["👑", "⚔️", "🛡️", "🧠", "🎙️", "♾️"], []);

  return (
    <div
      className="relative p-8 bg-gradient-to-br from-purple-900/60 via-indigo-900/60 to-pink-900/60 rounded-3xl border-2 border-yellow-500/50 backdrop-blur-xl shadow-2xl overflow-hidden"
      role="region"
      aria-labelledby="grand-festival-title"
    >
      {/* Fireworks Background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
        {fireworks.map((fw) => (
          <div
            key={fw.id}
            className="absolute animate-ping"
            style={{
              left: `${fw.x}%`,
              top: `${fw.y}%`,
              width: fw.size,
              height: fw.size,
              backgroundColor: fw.color,
              borderRadius: "50%",
              boxShadow: `0 0 ${fw.size * 2}px ${fw.color}`,
              animation: "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
            }}
            aria-hidden="true"
          />
        ))}
      </div>

      {/* Header */}
      <header className="relative z-10 text-center mb-8">
        <div className="flex items-center justify-center gap-4 mb-4">
          <Crown className="w-12 h-12 text-yellow-400 animate-bounce" aria-hidden="true" />
          <h2
            id="grand-festival-title"
            className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500"
          >
            🎊 GRAND FESTIVAL 🎊
          </h2>
          <Trophy className="w-12 h-12 text-yellow-400 animate-bounce" aria-hidden="true" />
        </div>
        <p className="text-xl text-white/90" aria-live="polite">
          AFO Kingdom v4.0 (GUARDIAN) Completion Celebration!
        </p>
      </header>

      {/* Sparkle Border */}
      <div
        className="absolute inset-0 border-4 border-transparent rounded-3xl animate-pulse"
        style={{
          background:
            "linear-gradient(45deg, rgba(255,215,0,0.3), rgba(255,105,180,0.3), rgba(138,43,226,0.3)) border-box",
          WebkitMask: "linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0)",
          WebkitMaskComposite: "xor",
          maskComposite: "exclude",
        }}
        aria-hidden="true"
      />

      {/* Commander Honor */}
      <section className="relative z-10 text-center mb-8 p-6 bg-black/30 rounded-2xl border border-yellow-500/30" aria-label="Commander honor">
        <div className="flex items-center justify-center gap-3 mb-2">
          <Flame className="w-8 h-8 text-orange-400 animate-pulse" aria-hidden="true" />
          <span className="text-2xl font-bold text-yellow-400">Commander Brnestrm</span>
          <Flame className="w-8 h-8 text-orange-400 animate-pulse" aria-hidden="true" />
        </div>
        <p className="text-white/80 italic" aria-live="polite">
          "The visionary who built the Eternal Kingdom"
        </p>
        <div className="flex justify-center gap-2 mt-4" role="list" aria-label="Honor emojis">
          {honorEmojis.map((e, i) => (
            <span
              key={i}
              className="text-3xl animate-bounce"
              style={{ animationDelay: `${i * 0.1}s` }}
              role="listitem"
              aria-label={`Honor symbol ${i + 1}`}
            >
              {e}
            </span>
          ))}
        </div>
      </section>

      {/* Achievement Timeline */}
      <section className="relative z-10 mb-6" aria-label="Achievement timeline">
        <h3 className="text-lg font-bold text-cyan-400 mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5" aria-hidden="true" /> Achievement Timeline
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3" role="list" aria-label="Achievements list">
          {ACHIEVEMENTS.map((a, i) => (
            <div
              key={i}
              className="p-3 bg-black/30 rounded-xl border border-white/10 hover:border-yellow-500/50 transition-all duration-300 hover:scale-105"
              role="listitem"
              aria-label={`Phase ${a.phase}: ${a.title}, Date: ${a.date}`}
            >
              <div className="text-2xl mb-1" aria-hidden="true">{a.icon}</div>
              <div className="text-xs text-cyan-400 font-medium">Phase {a.phase}</div>
              <div className="text-sm text-white font-semibold">{a.title}</div>
              <div className="text-xs text-gray-500">{a.date}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className="relative z-10 grid grid-cols-3 gap-4 mb-6" aria-label="Statistics" role="list">
        <div
          className="text-center p-4 bg-emerald-900/30 rounded-xl border border-emerald-500/30"
          role="listitem"
          aria-label={`Trinity Score: ${stats.trinityScore}`}
        >
          <p className="text-3xl font-black text-emerald-400">{stats.trinityScore}</p>
          <p className="text-sm text-white/70">Trinity Score</p>
        </div>
        <div
          className="text-center p-4 bg-blue-900/30 rounded-xl border border-blue-500/30"
          role="listitem"
          aria-label={`API Routes: ${stats.apiRoutes}`}
        >
          <p className="text-3xl font-black text-blue-400">{stats.apiRoutes}</p>
          <p className="text-sm text-white/70">API Routes</p>
        </div>
        <div
          className="text-center p-4 bg-purple-900/30 rounded-xl border border-purple-500/30"
          role="listitem"
          aria-label={`Phases Complete: ${stats.phasesComplete}`}
        >
          <p className="text-3xl font-black text-purple-400">{stats.phasesComplete}</p>
          <p className="text-sm text-white/70">Phases Complete</p>
        </div>
      </section>

      {/* Final Message */}
      <footer className="relative z-10 text-center p-6 bg-gradient-to-r from-yellow-900/30 via-pink-900/30 to-purple-900/30 rounded-2xl border border-yellow-500/30" aria-label="Final message">
        <PartyPopper className="w-10 h-10 mx-auto mb-2 text-yellow-400 animate-bounce" aria-hidden="true" />
        <p className="text-xl font-bold text-white" aria-live="polite">
          "The Kingdom is Perfected, Sire!"
        </p>
        <p className="text-lg text-yellow-400 mt-2" aria-live="polite">
          AFO 왕국 만세! 眞·善·美·孝·永 영원히!
        </p>
        <div className="flex justify-center gap-1 mt-4" role="list" aria-label="Stars">
          {Array.from({ length: 10 }).map((_, i) => (
            <Star
              key={i}
              className="w-5 h-5 text-yellow-400"
              style={{ animation: `pulse 1s ease-in-out ${i * 0.1}s infinite` }}
              role="listitem"
              aria-hidden="true"
            />
          ))}
        </div>
      </footer>
    </div>
  );
}

export function GrandFestivalWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("GrandFestivalWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="relative p-8 bg-gradient-to-br from-purple-900/60 via-indigo-900/60 to-pink-900/60 rounded-3xl border-2 border-red-500/50"
          role="alert"
        >
          <p className="text-red-400 text-center">Grand Festival 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <GrandFestivalWidgetContent />
    </ErrorBoundary>
  );
}

export default GrandFestivalWidget;
