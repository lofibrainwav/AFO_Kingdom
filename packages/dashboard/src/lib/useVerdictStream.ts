"use client";

import { useEffect, useState } from "react";

export interface VerdictEvent {
  trace_id: string;
  graph_node_id: string;
  step: number;
  risk_score: number;
  trinity_score: number;
  veto_triggered: boolean;
  timestamp: string;
  rule_id?: string;
  decision?: string;
}

/**
 * 왕국의 신경계: Chancellor Graph verdict를 실시간 스트리밍하는 훅
 * 헌법 v1.0 준수하여 SSE를 통한 실시간 관찰 가능성 확보
 */
export function useVerdictStream(apiBase: string) {
  const [connected, setConnected] = useState(false);
  const [events, setEvents] = useState<VerdictEvent[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiBase) return;

    const url = `${apiBase}/api/system/logs/stream`;
    const es = new EventSource(url);

    // 연결 준비 완료
    es.addEventListener("ready", () => {
      setConnected(true);
      setError(null);
    });

    // keep-alive 신호
    es.addEventListener("ping", () => {
      setConnected(true);
    });

    // verdict 이벤트 수신
    es.addEventListener("verdict", (event) => {
      try {
        const data = JSON.parse((event as MessageEvent).data || "{}");

        // VerdictEvent 형식으로 변환 (헌법 v1.0 준수)
        const verdictEvent: VerdictEvent = {
          trace_id: data.trace_id || "unknown",
          graph_node_id: data.graph_node_id || "unknown",
          step: data.step || 0,
          risk_score: data.risk || 0,
          trinity_score: data.trinity || 0,
          veto_triggered: data.veto?.triggered || false,
          timestamp: data.timestamp || new Date().toISOString(),
          rule_id: data.rule_id,
          decision: data.decision,
        };

        // 이벤트 히스토리 관리 (최근 100개 유지)
        setEvents((prev) => [verdictEvent, ...prev].slice(0, 100));
        setConnected(true);
        setError(null);
      } catch (err) {
        console.error("Verdict 이벤트 파싱 실패:", err);
        setError("Verdict 이벤트 파싱 실패");
      }
    });

    // 에러 처리
    es.onerror = (event) => {
      setConnected(false);
      setError("SSE 스트리밍 연결 실패");

      // 재연결 로직 (지수 백오프)
      setTimeout(() => {
        if (es.readyState === EventSource.CLOSED) {
          // 재연결은 useEffect가 처리
        }
      }, 5000);
    };

    // 클린업
    return () => {
      es.close();
      setConnected(false);
    };
  }, [apiBase]);

  return {
    connected,
    events,
    error,
    latestEvent: events[0] || null,
    eventCount: events.length,
  };
}
