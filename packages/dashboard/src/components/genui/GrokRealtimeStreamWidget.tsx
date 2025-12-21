'use client';

import { useEffect, useState } from 'react';
import { Zap, Activity } from 'lucide-react';
import { logError } from '@/lib/logger';

interface StreamMessage {
  id: number;
  timestamp: string;
  content: string;
  source: 'grok' | 'system';
}

export default function GrokRealtimeStreamWidget() {
  const [messages, setMessages] = useState<StreamMessage[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Connect to the Heartbeat of the Kingdom
    const eventSource = new EventSource('/api/grok/stream');

    eventSource.onopen = () => setConnected(true);
    eventSource.onerror = () => setConnected(false);

    eventSource.onmessage = (event) => {
      try {
        const newMsg: StreamMessage = JSON.parse(event.data);
         // Keep only the latest 30 messages to avoid clutter (Beauty)
        setMessages(prev => [newMsg, ...prev].slice(0, 30));
      } catch (e) {
        logError("Stream parse error", { error: e instanceof Error ? e.message : 'Unknown error' });
      }
    };

    return () => eventSource.close();
  }, []);

  return (
    <div className="glass-card p-8 bg-gradient-to-br from-cyan-900/20 to-purple-900/20 rounded-3xl border border-cyan-500/30 shadow-2xl relative overflow-hidden">
      {/* Background Pulse Animation */}
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl transition-opacity duration-1000 ${connected ? 'opacity-100 animate-pulse' : 'opacity-0'}`}></div>

      <div className="flex items-center justify-between mb-6 relative z-10">
        <h3 className="text-2xl font-bold text-cyan-400 flex items-center gap-3">
          <Activity className={`w-8 h-8 ${connected ? 'animate-pulse text-cyan-400' : 'text-gray-500'}`} />
          Grok Real-time Stream
        </h3>
        <div className={`px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2 border ${connected ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-400' : 'bg-red-500/20 border-red-500/50 text-red-400'}`}>
          <div className={`w-2 h-2 rounded-full ${connected ? 'bg-emerald-400 animate-ping' : 'bg-red-400'}`}></div>
          {connected ? 'Cloud Uplink Active' : 'Connecting...'}
        </div>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar relative z-10">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-white/50">
            <Zap className="w-12 h-12 mb-4 animate-bounce opacity-30" />
            <p>Listening for the Kingdom's Pulse...</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div 
              key={msg.id} 
              className={`p-4 rounded-xl border backdrop-blur-sm transition-all duration-500 ${
                  index === 0 ? 'scale-[1.02] shadow-lg ring-1 ring-cyan-400/30' : 'scale-100'
              } ${
                msg.source === 'grok' 
                  ? 'bg-cyan-900/30 border-cyan-500/30 hover:bg-cyan-900/40' 
                  : 'bg-purple-900/20 border-purple-500/20 hover:bg-purple-900/30'
              }`}
            >
              <div className="flex items-start gap-3">
                <span className="mt-1">
                    {msg.source === 'grok' ? '🧠' : '⚙️'}
                </span>
                <div className="flex-1">
                    <p className="text-white text-sm font-medium leading-relaxed">{msg.content}</p>
                    <div className="flex justify-between items-center mt-2">
                        <span className={`text-[10px] uppercase tracking-wider font-bold ${msg.source === 'grok' ? 'text-cyan-300' : 'text-purple-300'}`}>
                            {msg.source.toUpperCase()}
                        </span>
                        <span className="text-white/40 text-[10px] font-mono">
                            {new Date(msg.timestamp).toLocaleTimeString()}
                        </span>
                    </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-8 pt-4 border-t border-white/10 relative z-10">
        <p className="text-center text-cyan-300/80 italic text-sm">
          "The wisdom of the Cloud flows into the Kingdom in real-time."
        </p>
      </div>
    </div>
  );
}
