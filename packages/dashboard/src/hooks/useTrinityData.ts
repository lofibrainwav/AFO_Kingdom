"use client";

import { useState, useEffect, useCallback } from "react";
import type { TrinityBreakdown } from "@/components/TrinityGlowCard";

export interface TrinityData {
  trinityScore: number | null;
  riskScore: number | null;
  breakdown: TrinityBreakdown;
  loading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

interface HealthResponse {
  status: string;
  backend_available: boolean;
  trinity_score?: number;
  risk_score?: number;
  breakdown?: {
    truth?: number;
    goodness?: number;
    beauty?: number;
    filial_serenity?: number;
    eternity?: number;
    iccls_gap?: number;
    sentiment?: number;
  };
  timestamp: string;
}

/**
 * useTrinityData - 실시간 Trinity 데이터 훅
 *
 * /api/health에서 데이터를 가져와 TrinityGlowCard/TrinityRadar에 전달
 *
 * @param refreshInterval - 데이터 갱신 주기 (ms), 기본 15초
 */
export function useTrinityData(refreshInterval = 15000): TrinityData {
  const [data, setData] = useState<TrinityData>({
    trinityScore: null,
    riskScore: null,
    breakdown: {
      truth: null,
      goodness: null,
      beauty: null,
      filial_serenity: null,
      eternity: null,
      iccls_score: null,
      sentiment_score: null,
    },
    loading: true,
    error: null,
    lastUpdated: null,
  });

  const fetchTrinityData = useCallback(async () => {
    try {
      const response = await fetch("/api/health");
      const json: HealthResponse = await response.json();

      if (json.backend_available && json.breakdown) {
        setData({
          trinityScore: json.trinity_score ?? null,
          riskScore: json.risk_score ?? 0.05,
          breakdown: {
            truth: json.breakdown.truth ?? null,
            goodness: json.breakdown.goodness ?? null,
            beauty: json.breakdown.beauty ?? null,
            filial_serenity: json.breakdown.filial_serenity ?? null,
            eternity: json.breakdown.eternity ?? null,
            iccls_score: json.breakdown.iccls_gap ?? null,
            sentiment_score: json.breakdown.sentiment ?? null,
          },
          loading: false,
          error: null,
          lastUpdated: new Date(json.timestamp),
        });
      } else {
        // 백엔드 연결 실패 시 기본값 (데모용)
        setData({
          trinityScore: 0.88,
          riskScore: 0.05,
          breakdown: {
            truth: 0.92,
            goodness: 0.88,
            beauty: 0.75,
            filial_serenity: 0.90,
            eternity: 0.85,
            iccls_score: 0.15,
            sentiment_score: 0.75,
          },
          loading: false,
          error: json.backend_available ? null : "Backend not available (using demo data)",
          lastUpdated: new Date(),
        });
      }
    } catch (err) {
      setData((prev) => ({
        ...prev,
        loading: false,
        error: err instanceof Error ? err.message : "Unknown error",
      }));
    }
  }, []);

  useEffect(() => {
    fetchTrinityData();
    const interval = setInterval(fetchTrinityData, refreshInterval);
    return () => clearInterval(interval);
  }, [fetchTrinityData, refreshInterval]);

  return data;
}

export default useTrinityData;
