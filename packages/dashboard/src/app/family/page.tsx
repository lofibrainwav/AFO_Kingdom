"use client";

import React, { useEffect, useState } from "react";
import { createEventSource } from "@/lib/sse";
import FamilyMemberCard from "@/components/family/FamilyMemberCard";
import HappinessChart from "@/components/family/HappinessChart";
import FamilyTimeline from "@/components/family/FamilyTimeline";
import { Sparkles, RefreshCw } from "lucide-react";
import { logError } from "@/lib/logger";

export default function FamilyPage() {
  const [members, setMembers] = useState<any[]>([]);
  const [happiness, setHappiness] = useState<number>(0);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [memories, setMemories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  // SSE: Matrix Thought Stream
  useEffect(() => {
    const eventSource = createEventSource("/api/mcp/thoughts");
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const logLine = `[${new Date().toLocaleTimeString()}] ${data.agent || "SYSTEM"}: ${data.message || "Processing..."}`;
        setMemories((prev) => [logLine, ...prev].slice(0, 50)); // Keep last 50 lines
      } catch (err) {
        logError("SSE Parse Error", {
          error: err instanceof Error ? err.message : "Unknown error",
        });
      }
    };
    eventSource.onerror = (err) => {
      logError("SSE Error", { error: err });
      eventSource.close();
    };
    return () => {
      eventSource.close();
    };
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch Members
      const memRes = await fetch("/api/proxy/family/members");
      if (memRes.ok) {
        const data = await memRes.json();
        setMembers(data.members || []);
      }

      // Fetch Happiness
      const happyRes = await fetch("/api/proxy/family/happiness");
      if (happyRes.ok) {
        const data = await happyRes.json();
        setHappiness(data.happiness_score || 0);
      }

      // Fetch Timeline (Mock or if API supports it later)
      // For now, let's assume Members endpoint doesn't give full timeline,
      // asking for improvement might be needed.
      // But let's check if the FamilyTimeline component logic can work with what we have.
      // Actually, the API returns timeline as activity logs.
      // We'll mock it for now or assume a separate endpoint exists or we derive it.
      // Let's create a temporary mock timeline based on member statuses if real API is missing.
      // Wait, implemented router has /activity POST but no explicit GET timeline?
      // Ah, let's check `packages/afo-core/api/routers/family.py`.
      // It has `get_family_members` and `calculate_happiness`.
      // Let's add a quick mock timeline for visualization feasibility.

      const mockTimeline = [
        {
          member_id: "m1",
          activity_type: "System",
          description: "Family Hub Initialized",
          impact_score: 0,
          timestamp: new Date().toISOString(),
        },
      ];
      setTimeline(mockTimeline);
    } catch (err) {
      logError("Failed to fetch family data", {
        error: err instanceof Error ? err.message : "Unknown error",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-[#080808] text-white p-8 relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-purple-900/10 via-black to-blue-900/10 pointer-events-none"></div>
      <div className="absolute top-[-20%] right-[-10%] w-[500px] h-[500px] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none"></div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Header */}
        <div className="flex justify-between items-end mb-8 border-b border-white/10 pb-6">
          <div>
            <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 flex items-center gap-3">
              <Sparkles className="w-8 h-8 text-yellow-400" />
              Family Hub
            </h1>
            <p className="text-gray-400 mt-2 text-sm tracking-widest uppercase">
              AFO Kingdom • SerenityOS
            </p>
          </div>
          <button onClick={fetchData} className="p-2 rounded-full hover:bg-white/10 transition-all">
            <RefreshCw className={`w-5 h-5 text-gray-400 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>

        {/* Top Row: Chart & Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="md:col-span-3">
            <HappinessChart score={happiness} />
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Family Members */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-xl font-bold">Members</h2>
              <span className="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded-full">
                {members.length} Active
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {members.length > 0 ? (
                members.map((m: any) => (
                  <FamilyMemberCard
                    key={m.id}
                    name={m.name}
                    role={m.role}
                    status={m.status}
                    mood={m.mood}
                    avatar_url={m.avatar_url} // Assuming API returns this or undefined
                  />
                ))
              ) : (
                <div className="col-span-2 text-center py-10 text-gray-500 bg-white/5 rounded-xl border border-white/5 border-dashed">
                  Connecting to Soul Engine...
                </div>
              )}
            </div>
          </div>

          {/* Right: Timeline & Copilot */}
          <div className="lg:col-span-1 space-y-6">
            <div className="h-[400px]">
              <FamilyTimeline activities={timeline} />
            </div>
            <div className="h-[300px] bg-black border border-green-900/50 rounded-lg p-4 font-mono text-xs overflow-hidden relative shadow-[0_0_15px_rgba(0,255,0,0.1)]">
              <div className="absolute top-0 left-0 w-full h-8 bg-gradient-to-b from-green-900/20 to-transparent pointer-events-none"></div>
              <div className="h-full overflow-y-auto space-y-1 text-green-400/80">
                {memories.length === 0 && (
                  <span className="animate-pulse">Waiting for Neural Link...</span>
                )}
                {memories.map((log, i) => (
                  <div
                    key={i}
                    className="border-l-2 border-green-800 pl-2 hover:bg-green-900/20 transition-colors"
                  >
                    {log}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
