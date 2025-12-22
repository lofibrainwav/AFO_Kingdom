'use client';

import { useEffect, useState } from 'react';
import { Bug, Activity, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { logError } from '@/lib/logger';

interface DebuggingEvent {
  type: string;
  timestamp: string;
  data: {
    phase?: string;
    name?: string;
    description?: string;
    result?: any;
    error_id?: string;
    progress?: { current: number; total: number };
    success?: boolean;
    reason?: string;
    session_id?: string;
    total_errors?: number;
    auto_fixed?: number;
    manual_required?: number;
    trinity_score?: any;
    execution_time?: number;
  };
}

export default function AutomatedDebuggingStreamWidget() {
  const [events, setEvents] = useState<DebuggingEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<string | null>(null);
  const [stats, setStats] = useState({
    totalErrors: 0,
    autoFixed: 0,
    manualRequired: 0,
    trinityScore: 0,
  });

  useEffect(() => {
    // Connect to the Automated Debugging System Stream
    const eventSource = new EventSource('/api/debugging/stream');

    eventSource.onopen = () => {
      setConnected(true);
      console.log('🔌 Automated Debugging Stream 연결됨');
    };

    eventSource.onerror = () => {
      setConnected(false);
      console.error('❌ Automated Debugging Stream 연결 실패');
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Handle different event types
        if (data.type === 'connection') {
          // Initial connection message
          return;
        }

        if (data.type === 'keep-alive') {
          // Keep-alive ping, ignore
          return;
        }

        // Parse SSE event format
        const debuggingEvent: DebuggingEvent = typeof data === 'string' ? JSON.parse(data) : data;
        
        // Update state based on event type
        if (debuggingEvent.type === 'phase_start') {
          setCurrentPhase(debuggingEvent.data.phase || null);
        } else if (debuggingEvent.type === 'phase_complete') {
          setCurrentPhase(null);
        } else if (debuggingEvent.type === 'debugging_complete') {
          setStats({
            totalErrors: debuggingEvent.data.total_errors || 0,
            autoFixed: debuggingEvent.data.auto_fixed || 0,
            manualRequired: debuggingEvent.data.manual_required || 0,
            trinityScore: typeof debuggingEvent.data.trinity_score === 'object' 
              ? debuggingEvent.data.trinity_score.overall || 0
              : debuggingEvent.data.trinity_score || 0,
          });
        }

        // Keep only the latest 50 events to avoid clutter (Beauty)
        setEvents(prev => [debuggingEvent, ...prev].slice(0, 50));
      } catch (err) {
        logError("Debugging stream parse error", { 
          error: err instanceof Error ? err.message : 'Unknown error' 
        });
      }
    };

    return () => {
      eventSource.close();
      setConnected(false);
    };
  }, []);

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'phase_start':
        return <Activity className="w-4 h-4 text-blue-400" />;
      case 'phase_complete':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'error_detected':
        return <AlertCircle className="w-4 h-4 text-yellow-400" />;
      case 'fix_applied':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'fix_failed':
        return <XCircle className="w-4 h-4 text-red-400" />;
      case 'debugging_complete':
        return <CheckCircle className="w-4 h-4 text-emerald-400" />;
      default:
        return <Bug className="w-4 h-4 text-gray-400" />;
    }
  };

  const getEventColor = (eventType: string) => {
    switch (eventType) {
      case 'phase_start':
        return 'bg-blue-900/30 border-blue-500/30';
      case 'phase_complete':
        return 'bg-green-900/30 border-green-500/30';
      case 'error_detected':
        return 'bg-yellow-900/30 border-yellow-500/30';
      case 'fix_applied':
        return 'bg-green-900/30 border-green-500/30';
      case 'fix_failed':
        return 'bg-red-900/30 border-red-500/30';
      case 'debugging_complete':
        return 'bg-emerald-900/30 border-emerald-500/30';
      default:
        return 'bg-gray-900/30 border-gray-500/30';
    }
  };

  return (
    <div className="glass-card p-8 bg-gradient-to-br from-purple-900/20 to-blue-900/20 rounded-3xl border border-purple-500/30 shadow-2xl relative overflow-hidden">
      {/* Background Pulse Animation */}
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl transition-opacity duration-1000 ${connected ? 'opacity-100 animate-pulse' : 'opacity-0'}`}></div>

      <div className="flex items-center justify-between mb-6 relative z-10">
        <h3 className="text-2xl font-bold text-purple-400 flex items-center gap-3">
          <Bug className={`w-8 h-8 ${connected ? 'animate-pulse text-purple-400' : 'text-gray-500'}`} />
          자동화 디버깅 시스템
        </h3>
        <div className={`px-4 py-2 rounded-full text-sm font-bold flex items-center gap-2 border ${connected ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-400' : 'bg-red-500/20 border-red-500/50 text-red-400'}`}>
          <div className={`w-2 h-2 rounded-full ${connected ? 'bg-emerald-400 animate-ping' : 'bg-red-400'}`}></div>
          {connected ? '실시간 모니터링 활성' : '연결 중...'}
        </div>
      </div>

      {/* Current Phase Indicator */}
      {currentPhase && (
        <div className="mb-4 p-4 bg-blue-900/30 border border-blue-500/30 rounded-xl relative z-10">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400 animate-spin" />
            <span className="text-blue-300 font-semibold">
              Phase {currentPhase}: 진행 중...
            </span>
          </div>
        </div>
      )}

      {/* Statistics Summary */}
      {stats.totalErrors > 0 && (
        <div className="mb-4 grid grid-cols-2 md:grid-cols-4 gap-3 relative z-10">
          <div className="p-3 bg-gray-900/30 border border-gray-500/30 rounded-lg">
            <div className="text-xs text-gray-400 mb-1">총 에러</div>
            <div className="text-lg font-bold text-white">{stats.totalErrors}</div>
          </div>
          <div className="p-3 bg-green-900/30 border border-green-500/30 rounded-lg">
            <div className="text-xs text-green-400 mb-1">자동 수정</div>
            <div className="text-lg font-bold text-green-300">{stats.autoFixed}</div>
          </div>
          <div className="p-3 bg-yellow-900/30 border border-yellow-500/30 rounded-lg">
            <div className="text-xs text-yellow-400 mb-1">수동 필요</div>
            <div className="text-lg font-bold text-yellow-300">{stats.manualRequired}</div>
          </div>
          <div className="p-3 bg-purple-900/30 border border-purple-500/30 rounded-lg">
            <div className="text-xs text-purple-400 mb-1">Trinity Score</div>
            <div className="text-lg font-bold text-purple-300">{stats.trinityScore.toFixed(1)}</div>
          </div>
        </div>
      )}

      {/* Event Stream */}
      <div className="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar relative z-10">
        {events.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-white/50">
            <Bug className="w-12 h-12 mb-4 animate-bounce opacity-30" />
            <p>디버깅 이벤트 대기 중...</p>
          </div>
        ) : (
          events.map((event, index) => (
            <div
              key={`${event.timestamp}-${index}`}
              className={`p-4 rounded-xl border backdrop-blur-sm transition-all duration-500 ${
                index === 0 ? 'scale-[1.02] shadow-lg ring-1 ring-purple-400/30' : 'scale-100'
              } ${getEventColor(event.type)}`}
            >
              <div className="flex items-start gap-3">
                <span className="mt-1">{getEventIcon(event.type)}</span>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-white text-sm font-medium">
                      {event.data.name || event.type}
                    </span>
                    <span className="text-white/40 text-[10px] font-mono">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  {event.data.description && (
                    <p className="text-white/70 text-xs mb-2">{event.data.description}</p>
                  )}
                  {event.data.progress && (
                    <div className="mt-2">
                      <div className="flex justify-between text-xs text-white/60 mb-1">
                        <span>진행률</span>
                        <span>
                          {event.data.progress.current} / {event.data.progress.total}
                        </span>
                      </div>
                      <div className="w-full bg-gray-700/50 rounded-full h-2">
                        <div
                          className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                          style={{
                            width: `${(event.data.progress.current / event.data.progress.total) * 100}%`,
                          }}
                        ></div>
                      </div>
                    </div>
                  )}
                  {event.data.result && (
                    <div className="mt-2 text-xs text-white/60">
                      {JSON.stringify(event.data.result, null, 2)}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-8 pt-4 border-t border-white/10 relative z-10">
        <p className="text-center text-purple-300/80 italic text-sm">
          "眞善美孝永 철학에 기반한 자동화 디버깅 시스템"
        </p>
      </div>
    </div>
  );
}

