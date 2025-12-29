"use client";

import dynamic from "next/dynamic";
import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { TrinityGlowCard } from "./TrinityGlowCard";
import { VoiceReactivePanel } from "./VoiceReactivePanel";

import { logWarn } from "@/lib/logger";
import { useSpatialAudio } from "../hooks/useSpatialAudio";
import { KingdomMessageBoard } from "./genui";
import AutomatedDebuggingStreamWidget from "./genui/AutomatedDebuggingStreamWidget";
import { SSOTMonitor } from "./genui/SSOTMonitor";
import { TrinityMirrorStatus } from "./genui/TrinityMirrorStatus";
import { VisualAgentOverlay } from "./visual-agent/VisualAgentOverlay";

// Lazy load heavy widgets
const FinalEternalVictoryWidget = dynamic(
  () => import("./genui/FinalEternalVictoryWidget").then((mod) => mod.FinalEternalVictoryWidget),
  {
    loading: () => (
      <div className="h-96 w-full max-w-7xl mx-auto bg-slate-800/20 rounded-3xl animate-pulse flex items-center justify-center border border-white/5">
        <span className="text-white/30 text-lg">Summoning Eternal Victory...</span>
      </div>
    ),
    ssr: false,
  }
);

const RoyalAnalyticsWidget = dynamic(
  () => import("./genui/RoyalAnalyticsWidget").then((mod) => mod.default),
  {
    loading: () => (
      <div className="h-[400px] w-full bg-slate-800/20 rounded-3xl animate-pulse border border-white/5" />
    ),
  }
);

const GenesisWidget = dynamic(() => import("./genui/GenesisWidget").then((mod) => mod.GenesisWidget));
const JulieCPAWidget = dynamic(() => import("./genui/JulieCPAWidget").then((mod) => mod.JulieCPAWidget));
const JulieTaxWidget = dynamic(() => import("./genui/JulieTaxWidget").then((mod) => mod.JulieTaxWidget));

interface PantheonState {
  trinityScore: number | null;
  riskScore: number | null;
  healthStatus: "excellent" | "good" | "warning" | "critical" | "loading";
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

export function AFOPantheon() {
  const [state, setState] = useState<PantheonState>({
    trinityScore: null,
    riskScore: null,
    healthStatus: "loading",
    servicesOnline: 0,
    totalServices: 0,
    lastUpdate: new Date().toISOString(),
  });

  const [showVoicePanel] = useState(false);
  const [alerts] = useState<string[]>([]);
  const [thoughts, setThoughts] = useState<string[]>([]);
  const [isMatrixActive, setIsMatrixActive] = useState(false);

  const {
    playTrinityUp: _playTrinityUp,
    playRiskUp: _playRiskUp,
    initAudio: _initAudio,
  } = useSpatialAudio();

  // Memoize status color getter
  const getStatusColorClass = useCallback(() => {
    switch (state.healthStatus) {
      case "excellent":
        return "text-green-500 border-green-500 shadow-green-500/20";
      case "good":
        return "text-lime-500 border-lime-500 shadow-lime-500/20";
      case "warning":
        return "text-yellow-500 border-yellow-500 shadow-yellow-500/20";
      case "critical":
        return "text-red-500 border-red-500 shadow-red-500/20";
      default:
        return "text-gray-500 border-gray-500 shadow-gray-500/20";
    }
  }, [state.healthStatus]);

  // Memoize status color class
  const statusColorClass = useMemo(() => getStatusColorClass(), [getStatusColorClass]);

  useEffect(() => {
    const eventSource = new EventSource(`${window.location.origin}/api/mcp/thoughts/sse`);

    eventSource.onmessage = (event) => {
      try {
        if (event.data === "keep-alive") return;
        const thoughtData = JSON.parse(event.data);
        const timestamp = new Date().toLocaleTimeString();
        let thoughtText = `[${timestamp}] `;

        if (thoughtData.source) thoughtText += `[${thoughtData.source}] `;
        if (thoughtData.content) thoughtText += thoughtData.content;
        else thoughtText += JSON.stringify(thoughtData).slice(0, 100);

        setThoughts((prev) => [thoughtText, ...prev].slice(0, 50));
        setIsMatrixActive(true);
        setTimeout(() => setIsMatrixActive(false), 2000);
      } catch (err) {
        logWarn("Matrix Parse Error", {
          error: err instanceof Error ? err.message : "Unknown error",
        });
      }
    };

    eventSource.onerror = (e) => {
      logWarn("Matrix Stream Disconnected. Reconnecting...", { error: e });
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const fetchState = useCallback(async () => {
    try {
      const res = await fetch("/api/ssot-status");
      if (res.ok) {
        const data = await res.json();

        setState((prev) => ({
          ...prev,
          trinityScore: data.trinity?.total ?? prev.trinityScore,
          riskScore: data.risk ?? 0.0,
          healthStatus: data.health ?? prev.healthStatus,
          servicesOnline: data.services?.online ?? prev.servicesOnline,
          totalServices: data.services?.total ?? prev.totalServices,
          breakdown: {
            truth: data.trinity?.truth ?? null,
            goodness: data.trinity?.goodness ?? null,
            beauty: data.trinity?.beauty ?? null,
            filial_serenity: data.trinity?.serenity ?? null,
            eternity: data.trinity?.eternity ?? null,
          },
          lastUpdate: data.timestamp ?? new Date().toISOString(),
        }));
      }
    } catch (err) {
      logWarn("SSOT fetch failed", { error: err instanceof Error ? err.message : "Unknown error" });
    }
  }, []);

  useEffect(() => {
    const initFetch = async () => {
      await fetchState();
    };
    initFetch();
    const interval = setInterval(fetchState, 15000);
    return () => clearInterval(interval);
  }, [fetchState]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900 p-8">
      <h1 className="text-white text-center text-3xl mb-8 font-sans">
        🏰 AFO Pantheon - Command Center
      </h1>

      <div className="max-w-[1600px] mx-auto space-y-12">
        <section>
          <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
            🏛️ Command Center
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <TrinityGlowCard
              trinityScore={state.trinityScore}
              riskScore={state.riskScore}
              breakdown={state.breakdown}
            >
              <div className="text-center">
                <div className="text-5xl mb-2">⚖️</div>
                <h2 className="text-white m-0">Trinity Score</h2>
                <div
                  className={`text-4xl font-bold mt-2 ${
                    state.trinityScore === null
                      ? "text-gray-500"
                      : state.trinityScore >= 0.9
                        ? "text-green-500"
                        : state.trinityScore >= 0.7
                          ? "text-yellow-500"
                          : "text-red-500"
                  }`}
                >
                  {state.trinityScore !== null
                    ? `${(state.trinityScore * 100).toFixed(0)}%`
                    : "Loading..."}
                </div>
              </div>
            </TrinityGlowCard>

            <div
              className={`p-6 bg-black/60 rounded-2xl flex flex-col items-center justify-center transition-all duration-300 hover:bg-white/5 border ${statusColorClass}`}
              role="region"
              aria-label={`System Health: ${state.healthStatus}, ${state.servicesOnline} out of ${state.totalServices} services online`}
            >
              <div className="text-5xl mb-2" aria-hidden="true">💚</div>
              <h2 className="text-white m-0">System Health</h2>
              <div
                className={`text-xl font-bold mt-2 uppercase ${statusColorClass.split(" ")[0]}`}
                aria-live="polite"
                aria-atomic="true"
              >
                {state.healthStatus}
              </div>
              <div className="text-gray-400 mt-2 text-sm" aria-label={`${state.servicesOnline} out of ${state.totalServices} services online`}>
                {state.servicesOnline}/{state.totalServices} Services Online
              </div>
            </div>

            <div className="p-6 bg-black/60 rounded-2xl border border-white/10 flex flex-col hover:border-white/30 transition-colors">
              <h3 className="text-white m-0 mb-4 flex items-center justify-between">
                <span>🔔 Recent Alerts</span>
                <span className="text-xs bg-red-500/20 text-red-300 px-2 py-1 rounded-full">
                  {alerts.length}
                </span>
              </h3>
              {alerts.length === 0 ? (
                <div className="flex-1 flex items-center justify-center text-green-500/50 italic text-sm">
                  ✅ No active alerts
                </div>
              ) : (
                <div className="flex-1 overflow-auto max-h-[120px] pr-2 scrollbar-thin scrollbar-thumb-white/20">
                  {alerts.slice(-5).map((alert: string, i: number) => (
                    <div
                      key={i}
                      className="p-2 mb-2 bg-red-500/10 border-l-2 border-red-500 text-red-300 text-xs"
                    >
                      {alert}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="md:col-span-1">
              <TrinityMirrorStatus />
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
            👁️ Intelligence Layer
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <SSOTMonitor />
            </div>

            <div
              className="lg:col-span-2 p-6 bg-black/80 rounded-2xl transition-all duration-300"
              style={{
                border: `1px solid ${isMatrixActive ? "#22c55e" : "rgba(34,197,94,0.3)"}`,
                boxShadow: isMatrixActive ? "0 0 15px rgba(34,197,94,0.3)" : "none",
              }}
            >
              <h3 className="text-green-500 m-0 mb-4 font-mono flex justify-between items-center text-sm">
                <span className="tracking-widest">MATRIX STREAM</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded ${isMatrixActive ? "bg-green-500/20 text-green-300" : "text-zinc-600"}`}
                >
                  {isMatrixActive ? "● LIVE" : "○ IDLE"}
                </span>
              </h3>
              <div
                className="h-[200px] overflow-y-auto font-mono text-xs text-green-400/90 flex flex-col-reverse scrollbar-thin scrollbar-thumb-green-900"
                role="log"
                aria-live="polite"
                aria-label="Matrix stream thoughts"
              >
                {thoughts.length === 0 ? (
                  <div className="text-green-900/50 italic p-4 text-center" aria-label="Waiting for neural signals">
                    Waiting for neural signals...
                  </div>
                ) : (
                  thoughts.map((t: string, i: number) => (
                    <div
                      key={i}
                      className="py-1 border-b border-green-500/10 leading-relaxed hover:bg-green-500/5 px-2"
                      aria-label={`Thought ${i + 1}: ${t}`}
                    >
                      {t}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="mt-6">
            <AutomatedDebuggingStreamWidget />
          </div>
        </section>

        <section>
          <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
            📜 Royal Decrees (Beauty)
          </h2>
          <div className="w-full">
            <KingdomMessageBoard />
          </div>
        </section>

        <section>
          <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
            💰 Royal Finance (Goodness)
          </h2>
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 items-start">
            <div className="w-full">
              <Suspense fallback={<div className="text-white/50 text-center py-8">Loading Finance...</div>}>
                <JulieCPAWidget />
              </Suspense>
            </div>

            <div className="w-full">
              <Suspense fallback={<div className="text-white/50 text-center py-8">Loading Tax...</div>}>
                <JulieTaxWidget />
              </Suspense>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-white/50 text-sm font-bold uppercase tracking-widest mb-4 border-b border-white/10 pb-2">
            🌌 Evolution Engine (Serenity)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="w-full">
              <GenesisWidget />
            </div>

            <div className="w-full">
              <RoyalAnalyticsWidget />
            </div>
          </div>
        </section>

        <section className="flex justify-center pb-20 pt-10 opacity-80 hover:opacity-100 transition-opacity">
          <FinalEternalVictoryWidget />
        </section>
      </div>

      {showVoicePanel && (
        <div className="fixed bottom-8 right-8 z-[100] bg-black/90 rounded-2xl border border-white/20 shadow-2xl">
          <VoiceReactivePanel
            baseTrinityScore={state.trinityScore ?? undefined}
            baseRiskScore={state.riskScore ?? undefined}
          />
        </div>
      )}

      {/* Janus Visual Agent Overlay */}
      <VisualAgentOverlay />
    </div>
  );
}

export default AFOPantheon;
