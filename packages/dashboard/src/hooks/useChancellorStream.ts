"use client";

import { useEffect } from "react";
import { useChancellorStore } from "@/state/chancellorStore";

function safeJsonParse(s: string): unknown {
  try {
    return JSON.parse(s);
  } catch {
    return s;
  }
}

export function useChancellorStream() {
  const setConnected = useChancellorStore((s) => s.setConnected);
  const setTrinityScore = useChancellorStore((s) => s.setTrinityScore);
  const setActivePillar = useChancellorStore((s) => s.setActivePillar);
  const pushThought = useChancellorStore((s) => s.pushThought);
  const pushEvent = useChancellorStore((s) => s.pushEvent);

  useEffect(() => {
    const es = new EventSource("/api/stream");

    es.onopen = () => setConnected(true);
    es.onerror = () => setConnected(false);

    const onThought = (e: MessageEvent) => {
      const data = safeJsonParse(String(e.data));
      const text = typeof data === "string" ? data : JSON.stringify(data);
      pushThought(text);
      pushEvent({ at: Date.now(), type: "thought", data });
    };

    const onTrinity = (e: MessageEvent) => {
      const raw = String(e.data);
      const data = safeJsonParse(raw);
      const n =
        typeof data === "number"
          ? data
          : typeof data === "string"
          ? Number(data)
          : typeof (data as any)?.trinity_score === "number"
          ? (data as any).trinity_score
          : null;
      if (typeof n === "number" && Number.isFinite(n)) setTrinityScore(n);
      pushEvent({ at: Date.now(), type: "trinity_score", data });
    };

    const onPillar = (e: MessageEvent) => {
      const data = safeJsonParse(String(e.data));
      const p =
        typeof data === "string"
          ? data
          : typeof (data as any)?.active_pillar === "string"
          ? (data as any).active_pillar
          : null;
      if (p) setActivePillar(p);
      pushEvent({ at: Date.now(), type: "active_pillar", data });
    };

    es.addEventListener("thought", onThought as any);
    es.addEventListener("trinity_score", onTrinity as any);
    es.addEventListener("active_pillar", onPillar as any);

    es.onmessage = (e) => {
      pushEvent({ at: Date.now(), type: "message", data: safeJsonParse(String(e.data)) });
    };

    return () => {
      es.close();
      setConnected(false);
    };
  }, [setConnected, setTrinityScore, setActivePillar, pushThought, pushEvent]);
}
