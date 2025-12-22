/**
 * JulieSuggestions.tsx
 *
 * Phase 12-3: Smart Guardian - Julie CPA의 스마트 제안
 * "Julie가 제안해요: 지출 줄여보세요 – 잔고 안전 업그레이드 ✨"
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import React, { useMemo, useCallback } from "react";
import { useApi } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/common";
import { REFRESH_INTERVALS } from "@/lib/constants";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface Suggestion {
  priority: "critical" | "warning" | "info" | "success";
  icon: string;
  title: string;
  message: string;
  action: string | null;
  expected_saving: number;
}

interface SuggestionsData {
  spend_rate: number;
  suggestion_count: number;
  suggestions: Suggestion[];
  total_potential_saving: number;
  summary: string;
}

function JulieSuggestionsContent() {
  const { data, loading } = useApi<SuggestionsData>("/api/julie/budget/suggestions", {
    refetchInterval: REFRESH_INTERVALS.NORMAL, // 30초마다 자동 업데이트
  });

  // Memoize priority color getter
  const getPriorityColor = useCallback((priority: string) => {
    switch (priority) {
      case "critical":
        return { bg: "rgba(239, 68, 68, 0.15)", border: "rgba(239, 68, 68, 0.4)", text: "#EF4444" };
      case "warning":
        return {
          bg: "rgba(251, 191, 36, 0.15)",
          border: "rgba(251, 191, 36, 0.4)",
          text: "#FBBF24",
        };
      case "info":
        return {
          bg: "rgba(59, 130, 246, 0.15)",
          border: "rgba(59, 130, 246, 0.4)",
          text: "#3B82F6",
        };
      case "success":
        return { bg: "rgba(34, 197, 94, 0.15)", border: "rgba(34, 197, 94, 0.4)", text: "#22C55E" };
      default:
        return {
          bg: "rgba(107, 114, 128, 0.15)",
          border: "rgba(107, 114, 128, 0.4)",
          text: "#6B7280",
        };
    }
  }, []);

  // Memoize currency formatter
  const formatCurrency = useCallback((amount: number) => {
    return new Intl.NumberFormat("ko-KR", {
      style: "currency",
      currency: "KRW",
      maximumFractionDigits: 0,
    }).format(amount);
  }, []);

  // Memoize suggestions with colors
  const suggestionsWithColors = useMemo(() => {
    if (!data?.suggestions) return [];
    return data.suggestions.map((suggestion) => ({
      ...suggestion,
      colors: getPriorityColor(suggestion.priority),
      formattedSaving: formatCurrency(suggestion.expected_saving),
    }));
  }, [data, getPriorityColor, formatCurrency]);

  // Memoize formatted total saving
  const formattedTotalSaving = useMemo(() => {
    if (!data || data.total_potential_saving <= 0) return null;
    return formatCurrency(data.total_potential_saving);
  }, [data, formatCurrency]);

  if (loading) {
    return (
      <div
        className="bg-gradient-to-br from-gray-900/90 to-purple-500/10 rounded-2xl p-8"
        role="status"
        aria-live="polite"
        aria-label="Loading suggestions"
      >
        <LoadingSpinner size="md" text="제안 분석 중..." />
      </div>
    );
  }

  if (!data) return null;

  return (
    <div
      className="bg-gradient-to-br from-gray-900/95 to-purple-500/15 backdrop-blur-xl rounded-3xl border border-purple-500/20 p-7 shadow-2xl"
      role="region"
      aria-labelledby="julie-suggestions-title"
    >
      {/* Header */}
      <header className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-3">
          <span className="text-4xl" aria-hidden="true">
            💡
          </span>
          <div>
            <h2 id="julie-suggestions-title" className="text-xl font-bold text-white m-0">
              Julie CPA의 스마트 제안
            </h2>
            <p className="text-white/60 text-xs m-0">Phase 12-3 · Smart Guardian</p>
          </div>
        </div>
        {formattedTotalSaving && (
          <div
            className="bg-green-500/20 border border-green-500/40 rounded-xl px-4 py-2"
            role="status"
            aria-label={`Total potential saving: ${formattedTotalSaving}`}
          >
            <span className="text-green-500 font-bold text-sm">
              💰 {formattedTotalSaving} 절감 가능
            </span>
          </div>
        )}
      </header>

      {/* Suggestions List */}
      <section aria-label="Suggestions list">
        <div className="mb-4" role="list" aria-label="Budget suggestions">
          {suggestionsWithColors.map((suggestion, i) => (
            <div
              key={i}
              className="rounded-xl p-4 mb-3 transition-transform duration-200 ease-in-out hover:translate-x-1"
              style={{
                background: suggestion.colors.bg,
                border: `1px solid ${suggestion.colors.border}`,
              }}
              role="listitem"
              aria-label={`${suggestion.priority} priority: ${suggestion.title}`}
            >
              <div className="flex items-start gap-3">
                <span className="text-2xl" aria-hidden="true">
                  {suggestion.icon}
                </span>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-bold m-0" style={{ color: suggestion.colors.text }}>
                      {suggestion.title}
                    </h3>
                    {suggestion.expected_saving > 0 && (
                      <span className="text-green-500 text-xs font-semibold">
                        +{suggestion.formattedSaving}
                      </span>
                    )}
                  </div>
                  <p className="text-white/85 text-sm mt-2 m-0 leading-relaxed">
                    {suggestion.message}
                  </p>
                  {suggestion.action && (
                    <button
                      className="mt-3 rounded-lg px-3 py-1.5 text-xs font-semibold cursor-pointer"
                      style={{
                        background: `${suggestion.colors.text}20`,
                        border: `1px solid ${suggestion.colors.text}50`,
                        color: suggestion.colors.text,
                      }}
                      aria-label={`Action: ${suggestion.action}`}
                    >
                      {suggestion.action} →
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Summary */}
      <section aria-label="Summary">
        <div className="bg-purple-500/10 rounded-xl px-4 py-3 text-center">
          <p className="text-purple-400 text-[13px] m-0" aria-live="polite">
            {data.summary}
          </p>
        </div>
      </section>
    </div>
  );
}

export function JulieSuggestions() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("JulieSuggestions error:", error, errorInfo);
      }}
      fallback={
        <div
          className="bg-gradient-to-br from-gray-900/90 to-purple-500/10 rounded-2xl p-8"
          role="alert"
        >
          <p className="text-red-400 text-center">Julie 제안 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <JulieSuggestionsContent />
    </ErrorBoundary>
  );
}

export default JulieSuggestions;
