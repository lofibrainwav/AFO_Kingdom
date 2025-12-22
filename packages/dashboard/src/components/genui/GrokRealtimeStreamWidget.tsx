/**
 * GrokRealtimeStreamWidget.tsx
 * 
 * Grok Real-time Stream 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { Zap, Activity } from "lucide-react";
import { logError } from "@/lib/logger";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface StreamMessage {
  id: number;
  timestamp: string;
  content: string;
  source: "grok" | "system";
}

function GrokRealtimeStreamWidgetContent() {
  const [messages, setMessages] = useState<StreamMessage[]>([]);
  const [connected, setConnected] = useState(false);

  // Memoize connection status styles
  const connectionStyles = useMemo(() => {
    return connected
      ? "bg-emerald-500/20 border-emerald-500/50 text-emerald-400"
      : "bg-red-500/20 border-red-500/50 text-red-400";
  }, [connected]);

  // Memoize message source styles
  const getMessageStyles = useCallback((source: "grok" | "system") => {
    return source === "grok"
      ? "bg-cyan-900/30 border-cyan-500/30 hover:bg-cyan-900/40"
      : "bg-purple-900/20 border-purple-500/20 hover:bg-purple-900/30";
  }, []);

  // Memoize message source color
  const getSourceColor = useCallback((source: "grok" | "system") => {
    return source === "grok" ? "text-cyan-300" : "text-purple-300";
  }, []);

  useEffect(() => {
    // Connect to the Heartbeat of the Kingdom
    const eventSource = new EventSource("/api/grok/stream");

    eventSource.onopen = () => setConnected(true);
    eventSource.onerror = () => setConnected(false);

    eventSource.onmessage = (event) => {
      try {
        const newMsg: StreamMessage = JSON.parse(event.data);
        // Keep only the latest 30 messages to avoid clutter (Beauty)
        setMessages((prev) => [newMsg, ...prev].slice(0, 30));
      } catch (err) {
        logError("Stream parse error", {
          error: err instanceof Error ? err.message : "Unknown error",
        });
      }
    };

    return () => eventSource.close();
  }, []);

  return (
    <div
      className="glass-card p-8 bg-gradient-to-br from-cyan-900/20 to-purple-900/20 rounded-3xl border border-cyan-500/30 shadow-2xl relative overflow-hidden"
      role="region"
      aria-labelledby="grok-stream-title"
    >
      {/* Background Pulse Animation */}
      <div
        className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl transition-opacity duration-1000 ${connected ? "opacity-100 animate-pulse" : "opacity-0"}`}
        aria-hidden="true"
      ></div>

      <header className="flex items-center justify-between mb-6 relative z-10">
        <h3
          id="grok-stream-title"
          className="text-2xl font-bold text-cyan-400 flex items-center gap-3"
        >
          <Activity
            className={`w-8 h-8 ${connected ? "animate-pulse text-cyan-400" : "text-gray-500"}`}
            aria-hidden="true"
          />
          Grok Real-time Stream
        </h3>
        <div
          className={`px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2 border ${connectionStyles}`}
          role="status"
          aria-live="polite"
          aria-label={connected ? "Cloud uplink active" : "Connecting..."}
        >
          <div
            className={`w-2 h-2 rounded-full ${connected ? "bg-emerald-400 animate-ping" : "bg-red-400"}`}
            aria-hidden="true"
          ></div>
          {connected ? "Cloud Uplink Active" : "Connecting..."}
        </div>
      </header>

      <section
        className="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar relative z-10"
        role="log"
        aria-label="Grok stream messages"
        aria-live="polite"
      >
        {messages.length === 0 ? (
          <div
            className="flex flex-col items-center justify-center py-12 text-white/50"
            role="status"
            aria-label="Waiting for stream messages"
          >
            <Zap className="w-12 h-12 mb-4 animate-bounce opacity-30" aria-hidden="true" />
            <p>Listening for the Kingdom's Pulse...</p>
          </div>
        ) : (
          <div role="list" aria-label="Stream messages list">
            {messages.map((msg, index) => (
              <div
                key={msg.id}
                className={`p-4 rounded-xl border backdrop-blur-sm transition-all duration-500 ${
                  index === 0 ? "scale-[1.02] shadow-lg ring-1 ring-cyan-400/30" : "scale-100"
                } ${getMessageStyles(msg.source)}`}
                role="listitem"
                aria-label={`Message from ${msg.source}: ${msg.content.substring(0, 50)}...`}
              >
                <div className="flex items-start gap-3">
                  <span className="mt-1" aria-hidden="true">
                    {msg.source === "grok" ? "🧠" : "⚙️"}
                  </span>
                  <div className="flex-1">
                    <p className="text-white text-sm font-medium leading-relaxed">{msg.content}</p>
                    <div className="flex justify-between items-center mt-2">
                      <span
                        className={`text-[10px] uppercase tracking-wider font-bold ${getSourceColor(msg.source)}`}
                        aria-label={`Source: ${msg.source}`}
                      >
                        {msg.source.toUpperCase()}
                      </span>
                      <span
                        className="text-white/40 text-[10px] font-mono"
                        aria-label={`Time: ${new Date(msg.timestamp).toLocaleTimeString()}`}
                      >
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <footer className="mt-8 pt-4 border-t border-white/10 relative z-10" aria-label="Footer">
        <p className="text-center text-cyan-300/80 italic text-sm" aria-live="polite">
          "The wisdom of the Cloud flows into the Kingdom in real-time."
        </p>
      </footer>
    </div>
  );
}

export default function GrokRealtimeStreamWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("GrokRealtimeStreamWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-8 bg-gradient-to-br from-cyan-900/20 to-purple-900/20 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">Grok Real-time Stream 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <GrokRealtimeStreamWidgetContent />
    </ErrorBoundary>
  );
}
