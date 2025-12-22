/**
 * AgentLearningTimeline.tsx
 * 
 * 왕국 자율 학습 타임라인 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useEffect, useState, memo, useMemo, useCallback } from "react";
import { Bot, Swords, Palette, Search, X, Sparkles } from "lucide-react";
import { logError } from "@/lib/logger";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface LogEntry {
  id: number;
  timestamp: string;
  agent: "samahwi" | "jooyu";
  action: string;
  delta: number;
  feedback: string;
}

type AgentFilter = "all" | "samahwi" | "jooyu";

const LOG_LIMIT = 50;

function AgentLearningTimelineContent() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [filter, setFilter] = useState<AgentFilter>("all");
  const [search, setSearch] = useState("");
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  // Memoize tabs
  const tabs = useMemo(
    () => [
      { id: "all" as const, label: "전체", icon: Bot },
      { id: "samahwi" as const, label: "사마휘", icon: Swords },
      { id: "jooyu" as const, label: "주유", icon: Palette },
    ],
    []
  );

  // Memoize filtered logs
  const filteredLogs = useMemo(() => {
    return logs.filter((log) => {
      const matchesFilter = filter === "all" || log.agent === filter;
      const matchesSearch =
        log.action.toLowerCase().includes(search.toLowerCase()) ||
        log.feedback.toLowerCase().includes(search.toLowerCase());
      return matchesFilter && matchesSearch;
    });
  }, [logs, filter, search]);

  // Memoize handlers
  const handleFilterChange = useCallback((newFilter: AgentFilter) => {
    setFilter(newFilter);
  }, []);

  const handleSearchChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  }, []);

  const handleSearchClear = useCallback(() => {
    setSearch("");
  }, []);

  const handleLogClick = useCallback((log: LogEntry) => {
    setSelectedLog(log);
  }, []);

  const handleCloseModal = useCallback(() => {
    setSelectedLog(null);
  }, []);

  // Memoize connection status styles
  const connectionStyles = useMemo(() => {
    return isConnected
      ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
      : "bg-red-500/20 text-red-400 border border-red-500/30";
  }, [isConnected]);

  // EventSource setup with cleanup
  useEffect(() => {
    if (typeof window === "undefined") return;

    const eventSource = new EventSource("/api/learning-log/stream");

    eventSource.onopen = () => setIsConnected(true);
    eventSource.onerror = () => setIsConnected(false);

    const handleMessage = (event: MessageEvent) => {
      try {
        const newLog: LogEntry = JSON.parse(event.data);
        setLogs((prev) => {
          const updated = [newLog, ...prev.filter((l) => l.id !== newLog.id)];
          return updated.slice(0, LOG_LIMIT);
        });
      } catch (err) {
        logError("Failed to parse log", {
          error: err instanceof Error ? err.message : "Unknown error",
        });
      }
    };

    eventSource.onmessage = handleMessage;

    return () => {
      eventSource.removeEventListener("message", handleMessage);
      eventSource.close();
    };
  }, []);

  return (
    <div
      className="glass-card p-8 bg-gradient-to-br from-purple-900/20 to-emerald-900/20 rounded-3xl border border-purple-500/30 shadow-2xl transition-all duration-300 hover:shadow-purple-500/20"
      role="region"
      aria-labelledby="learning-timeline-title"
    >
      {/* 헤더 + 탭 + 검색 */}
      <header className="flex flex-col gap-6 mb-8">
        <div className="flex items-center justify-between">
          <h3
            id="learning-timeline-title"
            className="text-2xl font-bold text-purple-400 flex items-center gap-3"
          >
            <Bot className="w-8 h-8 animate-bounce-slow" aria-hidden="true" />
            왕국 자율 학습 타임라인
          </h3>
          <div
            className={`px-4 py-2 rounded-full text-sm font-bold transition-colors duration-300 ${connectionStyles}`}
            role="status"
            aria-live="polite"
            aria-label={isConnected ? "Real-time connection active" : "Connecting..."}
          >
            {isConnected ? "● 실시간 연결" : "○ 연결 중..."}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex gap-2" role="tablist" aria-label="Agent filter tabs">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => handleFilterChange(tab.id)}
                  className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all duration-200 ease-out hover:scale-105 active:scale-95 ${
                    filter === tab.id
                      ? "bg-purple-600 text-white shadow-lg shadow-purple-500/30"
                      : "bg-white/5 text-white/70 hover:bg-white/15 border border-white/5"
                  }`}
                  role="tab"
                  aria-selected={filter === tab.id}
                  aria-controls="log-list"
                >
                  <IconComponent className="w-5 h-5" aria-hidden="true" />
                  {tab.label}
                </button>
              );
            })}
          </div>
          <div className="relative flex-1 group">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/40 group-focus-within:text-purple-400 transition-colors"
              aria-hidden="true"
            />
            <input
              type="text"
              value={search}
              onChange={handleSearchChange}
              placeholder="행동/피드백 검색..."
              className="w-full pl-10 pr-10 py-3 bg-white/5 backdrop-blur-md border border-white/10 rounded-xl text-white placeholder-white/40 focus:outline-none focus:border-purple-400/50 focus:bg-white/10 transition-all duration-200"
              aria-label="Search logs"
            />
            {search && (
              <button
                onClick={handleSearchClear}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors p-1"
                aria-label="Clear search"
              >
                <X className="w-4 h-4" aria-hidden="true" />
              </button>
            )}
          </div>
        </div>
      </header>

      {/* 로그 목록 */}
      {filteredLogs.length === 0 ? (
        <div
          className="text-center text-white/50 py-16 bg-white/5 rounded-2xl border border-dashed border-white/10"
          role="status"
          aria-live="polite"
        >
          {search ? (
            <>
              <Search className="w-12 h-12 mx-auto mb-4 opacity-50" aria-hidden="true" />
              <p>검색 결과가 없습니다.</p>
              <p className="text-sm mt-2 opacity-70">다른 키워드로 검색해보세요!</p>
            </>
          ) : (
            <>
              <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" aria-hidden="true" />
              <p>아직 학습 기록이 없습니다.</p>
              <p className="text-sm mt-2 opacity-70">곧 사마휘와 주유가 활동을 시작할 거예요! ✨</p>
            </>
          )}
        </div>
      ) : (
        <div
          className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar"
          role="list"
          id="log-list"
          aria-label="Learning logs"
        >
          {filteredLogs.map((log) => {
            const IconComponent = log.agent === "samahwi" ? Swords : Palette;
            return (
              <div
                key={log.id}
                onClick={() => handleLogClick(log)}
                className="group relative p-5 bg-white/5 rounded-2xl border border-white/5 hover:border-purple-500/40 hover:bg-white/10 transition-all duration-200 ease-out cursor-pointer hover:shadow-lg hover:shadow-purple-500/10 hover:-translate-y-0.5"
                role="listitem"
                aria-label={`${log.agent} agent: ${log.action}`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div
                      className={`p-2 rounded-lg ${log.agent === "samahwi" ? "bg-red-500/20 text-red-400" : "bg-pink-500/20 text-pink-400"}`}
                      aria-label={`Agent: ${log.agent}`}
                    >
                      <IconComponent className="w-4 h-4" aria-hidden="true" />
                    </div>
                    <p className="font-bold text-white group-hover:text-purple-200 transition-colors">
                      {log.action}
                    </p>
                  </div>
                  <div
                    className={`flex items-center gap-1 font-bold ${log.delta > 0 ? "text-emerald-400" : log.delta < 0 ? "text-red-400" : "text-gray-400"}`}
                    aria-label={`Score delta: ${log.delta > 0 ? "+" : ""}${log.delta.toFixed(3)}`}
                  >
                    <span>{log.delta > 0 ? "▲" : log.delta < 0 ? "▼" : "-"}</span>
                    <span>{Math.abs(log.delta).toFixed(3)}</span>
                  </div>
                </div>
                <p className="text-white/80 text-sm line-clamp-2 leading-relaxed pl-11 group-hover:text-white transition-colors">
                  {log.feedback}
                </p>
                <div className="flex justify-end mt-3">
                  <p className="text-white/40 text-xs font-mono" aria-label={`Time: ${new Date(log.timestamp).toLocaleTimeString()}`}>
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* 상세 모달 */}
      {selectedLog && (
        <div
          className="fixed inset-0 bg-black/90 backdrop-blur-xl flex items-center justify-center z-50 p-4 animate-in fade-in duration-200"
          onClick={handleCloseModal}
          role="dialog"
          aria-modal="true"
          aria-labelledby="log-detail-title"
        >
          <div
            className="relative glass-card p-8 md:p-12 max-w-3xl w-full bg-gradient-to-br from-purple-900/80 via-gray-900/90 to-emerald-900/80 rounded-[2rem] border border-purple-500/50 shadow-2xl transform transition-all duration-300 ease-out scale-100 animate-in zoom-in-95"
            onClick={(e) => e.stopPropagation()}
            role="document"
          >
            {/* Ambient Glow */}
            <div
              className="absolute -inset-1 bg-gradient-to-r from-purple-500/30 via-cyan-500/30 to-emerald-500/30 rounded-[2rem] blur-2xl -z-10 animate-pulse-slow"
              aria-hidden="true"
            />

            {/* Background Sparkles */}
            <div
              className="absolute inset-0 overflow-hidden rounded-[2rem] -z-10 pointer-events-none"
              aria-hidden="true"
            >
              <Sparkles className="absolute top-10 left-10 w-6 h-6 text-yellow-500/40 animate-ping delay-75" />
              <Sparkles className="absolute bottom-20 right-20 w-8 h-8 text-purple-500/40 animate-ping delay-150" />
              <Sparkles className="absolute top-1/2 right-10 w-4 h-4 text-emerald-500/40 animate-ping delay-300" />
            </div>

            <div className="flex justify-between items-start mb-10">
              <div className="flex items-center gap-6">
                <div
                  className={`p-4 rounded-2xl shadow-inner ${selectedLog.agent === "samahwi" ? "bg-gradient-to-br from-red-600 to-orange-600 shadow-red-900/50" : "bg-gradient-to-br from-pink-600 to-purple-600 shadow-pink-900/50"}`}
                  aria-label={`Agent: ${selectedLog.agent}`}
                >
                  {selectedLog.agent === "samahwi" ? (
                    <Swords className="w-10 h-10 text-white animate-pulse" aria-hidden="true" />
                  ) : (
                    <Palette className="w-10 h-10 text-white animate-pulse" aria-hidden="true" />
                  )}
                </div>
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${selectedLog.agent === "samahwi" ? "bg-red-500/20 text-red-300" : "bg-pink-500/20 text-pink-300"}`}
                    >
                      {selectedLog.agent === "samahwi" ? "Strategist" : "Artist"}
                    </span>
                    <span className="text-white/40 text-xs">ID: #{selectedLog.id}</span>
                  </div>
                  <h3
                    id="log-detail-title"
                    className="text-3xl md:text-4xl font-black text-white drop-shadow-lg leading-tight"
                  >
                    {selectedLog.action}
                  </h3>
                </div>
              </div>
              <button
                onClick={handleCloseModal}
                className="p-2 rounded-full bg-white/5 hover:bg-white/10 text-white/60 hover:text-white transition-all transform hover:rotate-90"
                aria-label="Close modal"
              >
                <X className="w-8 h-8" aria-hidden="true" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
              <div className="col-span-2 bg-black/20 rounded-2xl p-6 border border-white/5">
                <p className="text-white/90 text-lg leading-relaxed font-medium" aria-live="polite">
                  "{selectedLog.feedback}"
                </p>
              </div>
              <div className="flex flex-col items-center justify-center bg-black/20 rounded-2xl p-6 border border-white/5">
                <p className="text-white/50 text-sm mb-2 uppercase tracking-widest font-bold">
                  Score Delta
                </p>
                <p
                  className={`text-5xl font-black drop-shadow-xl ${selectedLog.delta > 0 ? "text-emerald-400" : selectedLog.delta < 0 ? "text-red-400" : "text-gray-400"}`}
                  aria-label={`Score delta: ${selectedLog.delta > 0 ? "+" : ""}${selectedLog.delta.toFixed(3)}`}
                >
                  {selectedLog.delta > 0 ? "+" : ""}
                  {selectedLog.delta.toFixed(3)}
                </p>
              </div>
            </div>

            <div className="flex items-center justify-between border-t border-white/10 pt-6">
              <div className="flex items-center gap-2 text-white/40 text-sm">
                <Sparkles className="w-4 h-4 text-yellow-500" aria-hidden="true" />
                <span>AI Autonomous Reasoning Log</span>
              </div>
              <p className="text-white/60 font-mono text-sm" aria-label={`Timestamp: ${new Date(selectedLog.timestamp).toLocaleString()}`}>
                {new Date(selectedLog.timestamp).toLocaleString(undefined, {
                  dateStyle: "full",
                  timeStyle: "medium",
                })}
              </p>
            </div>

            <p className="text-center text-emerald-300/50 text-sm mt-8 italic" aria-live="polite">
              "왕국이 영원히 진화합니다."
            </p>
          </div>
        </div>
      )}

      <footer className="mt-6 flex items-center justify-center gap-2 text-white/30 text-xs uppercase tracking-widest hover:text-purple-400 transition-colors cursor-default" aria-label="Footer">
        <Sparkles className="w-3 h-3" aria-hidden="true" />
        <span>Live Kingdom Intelligence Timeline</span>
        <Sparkles className="w-3 h-3" aria-hidden="true" />
      </footer>
    </div>
  );
}

const AgentLearningTimeline = memo(function AgentLearningTimeline() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("AgentLearningTimeline error:", error, errorInfo);
      }}
      fallback={
        <div
          className="glass-card p-8 bg-gradient-to-br from-purple-900/20 to-emerald-900/20 rounded-3xl border border-red-500/30"
          role="alert"
        >
          <p className="text-red-400 text-center">자율 학습 타임라인을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <AgentLearningTimelineContent />
    </ErrorBoundary>
  );
});

export default AgentLearningTimeline;
