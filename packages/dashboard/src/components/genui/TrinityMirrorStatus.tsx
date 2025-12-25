/**
 * TrinityMirrorStatus.tsx
 * 
 * 승상의 거울 (Mirror of Chancellor) 상태 위젯
 * 실시간 Trinity Score 감시 체계의 상태를 시각화합니다.
 */
"use client";

import { Eye } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

interface MirrorThought {
  content: string;
  level: string;
  timestamp: string;
}

export function TrinityMirrorStatus() {
  const [thoughts, setThoughts] = useState<MirrorThought[]>([]);
  const [isActive, setIsActive] = useState(false);
  const [lastHeartbeat, setLastHeartbeat] = useState<Date | null>(null);

  useEffect(() => {
    // Matrix Stream(SSE)에서 Mirror 관련 생각만 필터링하여 수신
    const eventSource = new EventSource("/api/mcp/thoughts/sse");

    eventSource.onmessage = (event) => {
      try {
        if (event.data === "keep-alive") return;
        const data = JSON.parse(event.data);
        
        if (data.source === "Mirror") {
          const newThought: MirrorThought = {
            content: data.content,
            level: data.level || "info",
            timestamp: data.timestamp || new Date().toISOString(),
          };
          
          setThoughts((prev) => [newThought, ...prev].slice(0, 5));
          setIsActive(true);
          setLastHeartbeat(new Date());
        }
      } catch (_err) {
        // Silent fail for stream parsing
      }
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // 1분 이상 하트비트가 없으면 IDLE 상태로 전환
  useEffect(() => {
    const interval = setInterval(() => {
      if (lastHeartbeat && new Date().getTime() - lastHeartbeat.getTime() > 600000) {
        setIsActive(false);
      }
    }, 10000);
    return () => clearInterval(interval);
  }, [lastHeartbeat]);

  const statusColor = useMemo(() => {
    if (!isActive) return "text-zinc-500 border-zinc-500/20";
    const latest = thoughts[0];
    if (latest?.level === "critical") return "text-red-500 border-red-500/50 shadow-red-500/20";
    if (latest?.level === "warning") return "text-yellow-500 border-yellow-500/50 shadow-yellow-500/20";
    return "text-green-500 border-green-500/50 shadow-green-500/20";
  }, [isActive, thoughts]);

  return (
    <div className={`p-4 rounded-2xl border bg-black/40 backdrop-blur-md transition-all duration-500 ${statusColor}`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold uppercase tracking-widest flex items-center gap-2">
          <Eye className={`w-4 h-4 ${isActive ? "animate-pulse" : ""}`} />
          Chancellor Mirror
        </h3>
        <div className="flex items-center gap-1.5">
          <div className={`w-2 h-2 rounded-full ${isActive ? "bg-green-500 animate-ping" : "bg-zinc-600"}`} />
          <span className="text-[10px] font-mono">{isActive ? "LIVE" : "IDLE"}</span>
        </div>
      </div>

      <div className="space-y-2">
        {thoughts.length === 0 ? (
          <div className="text-[10px] italic text-zinc-600 p-2 text-center border border-zinc-500/10 rounded-lg">
            Waiting for surveillance sync...
          </div>
        ) : (
          thoughts.map((t, i) => (
            <div 
              key={i} 
              className={`text-[10px] p-2 rounded-lg border leading-tight transition-all ${
                i === 0 ? "bg-white/5 opacity-100" : "opacity-40"
              } ${
                t.level === "critical" ? "border-red-500/20 text-red-200" :
                t.level === "warning" ? "border-yellow-500/20 text-yellow-200" :
                "border-white/5 text-zinc-300"
              }`}
            >
              <div className="flex justify-between mb-1 opacity-50">
                <span className="font-bold">{t.level.toUpperCase()}</span>
                <span>{new Date(t.timestamp).toLocaleTimeString()}</span>
              </div>
              {t.content}
            </div>
          ))
        )}
      </div>

      {isActive && (
        <div className="mt-3 pt-3 border-t border-white/5 flex items-center justify-between text-[8px] text-zinc-500 font-mono italic">
          <span>Continuous Monitoring Active</span>
          <span>Buffer: 100%</span>
        </div>
      )}
    </div>
  );
}
