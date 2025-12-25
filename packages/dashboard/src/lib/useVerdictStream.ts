"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { VerdictEvent } from "../types/verdict";

/**
 * SSE Deeplink Configuration
 * 眞 (Truth): Type-safe filter definitions
 * 善 (Goodness): Safe default values
 * 美 (Beauty): Clean API design
 */
export interface SSEDeeplinkOptions {
  /** Filter events by category (e.g., 'finance', 'reasoning') */
  category?: string;
  /** Filter events by specific trace_id */
  traceId?: string;
  /** Filter events by rule_id prefix */
  rulePrefix?: string;
  /** Maximum events to keep in history */
  maxHistory?: number;
  /** Auto-reconnect on error */
  autoReconnect?: boolean;
}

/**
 * Enhanced useVerdictStream Hook with Deeplink Support
 * 
 * 주유의 美: 단순하면서도 강력한 필터링 기능
 * 
 * @param apiBase - Backend API base URL
 * @param options - Optional deeplink filter configuration
 */
export function useVerdictStream(
  apiBase: string,
  options: SSEDeeplinkOptions = {}
) {
  const {
    category,
    traceId,
    rulePrefix,
    maxHistory = 100,
    autoReconnect = true,
  } = options;

  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState<VerdictEvent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [reconnectCount, setReconnectCount] = useState(0);

  // Build URL with deeplink query params
  const streamUrl = useMemo(() => {
    // [Modified] Standardized /api/system/logs/stream
    const url = new URL(`${apiBase}/api/system/logs/stream`);
    if (category) url.searchParams.set('category', category);
    if (traceId) url.searchParams.set('trace_id', traceId);
    if (rulePrefix) url.searchParams.set('rule_prefix', rulePrefix);
    return url.toString();
  }, [apiBase, category, traceId, rulePrefix]);

  // Event filter function for client-side filtering
  const matchesFilter = useCallback((event: VerdictEvent): boolean => {
    if (category && event.extra?.category !== category) return false;
    if (traceId && event.trace_id !== traceId) return false;
    if (rulePrefix && !event.rule_id?.startsWith(rulePrefix)) return false;
    return true;
  }, [category, traceId, rulePrefix]);

  useEffect(() => {
    if (!apiBase) return;

    const es = new EventSource(streamUrl);
    let reconnectTimer: ReturnType<typeof setTimeout>;

    // 연결 준비 완료
    es.addEventListener("ready", () => {
      setConnected(true);
      setError(null);
      setReconnectCount(0);
    });

    // keep-alive 신호
    es.addEventListener("ping", () => {
      setConnected(true);
    });

    // verdict 이벤트 수신
    es.addEventListener("verdict", (ev) => {
      try {
        const data = JSON.parse((ev as MessageEvent).data || "{}");

        // VerdictEvent 형식으로 변환 (헌법 v1.0 준수)
        const verdictEvent: VerdictEvent = {
          trace_id: data.trace_id || "unknown",
          graph_node_id: data.graph_node_id || "unknown",
          step: data.step || 0,
          decision: data.decision || "ASK",
          rule_id: data.rule_id || "unknown",
          trinity_score: data.trinity || 0,
          risk_score: data.risk || 0,
          flags: {
            dry_run: data.flags?.dry_run || false,
            residual_doubt: data.flags?.residual_doubt || false
          },
          timestamp: data.timestamp || new Date().toISOString(),
          extra: data.extra,
          weights_version: data.weights_version || "unknown",
          weights_hash: data.weights_hash || "unknown",
        };

        // Client-side filtering for precise deeplink matching
        if (!matchesFilter(verdictEvent)) return;

        // 이벤트 히스토리 관리
        setEvents((prev) => [verdictEvent, ...prev].slice(0, maxHistory));
        setConnected(true);
        setError(null);
      } catch (err) {
        console.error("Verdict 이벤트 파싱 실패:", err);
        setError("Verdict 이벤트 파싱 실패");
      }
    });

    // 에러 처리 with exponential backoff
    es.onerror = () => {
      setConnected(false);
      setError("SSE 스트리밍 연결 실패");

      if (autoReconnect && reconnectCount < 5) {
        const delay = Math.min(1000 * Math.pow(2, reconnectCount), 30000);
        reconnectTimer = setTimeout(() => {
          setReconnectCount((c) => c + 1);
        }, delay);
      }
    };

    // 클린업
    return () => {
      es.close();
      clearTimeout(reconnectTimer);
      setConnected(false);
    };
  }, [apiBase, streamUrl, matchesFilter, maxHistory, autoReconnect, reconnectCount]);

  // Derived state for convenience
  const latestEvent = events[0] || null;
  const eventCount = events.length;
  
  // Filter statistics
  const stats = useMemo(() => ({
    total: events.length,
    byDecision: events.reduce((acc, e) => {
      acc[e.decision] = (acc[e.decision] || 0) + 1;
      return acc;
    }, {} as Record<string, number>),
    avgTrinityScore: events.length > 0
      ? events.reduce((sum, e) => sum + (e.trinity_score || 0), 0) / events.length
      : 0,
  }), [events]);

  return {
    connected,
    events,
    error,
    latestEvent,
    eventCount,
    stats,
    reconnectCount,
    // Deeplink state
    activeFilters: { category, traceId, rulePrefix },
  };
}
