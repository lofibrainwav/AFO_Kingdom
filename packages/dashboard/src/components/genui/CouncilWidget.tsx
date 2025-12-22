/**
 * CouncilWidget.tsx
 * 
 * 지혜의 의회 위젯
 * 
 * Optimized with:
 * - useMemo, useCallback for performance
 * - ARIA labels for accessibility
 * - ErrorBoundary for error handling
 */
"use client";

import { useState, useMemo, useCallback } from "react";
import { Brain, Users, CheckCircle2, AlertTriangle, Loader2 } from "lucide-react";
import { logError } from "@/lib/logger";
import ErrorBoundary from "@/components/common/ErrorBoundary";

interface StrategistResponse {
  strategist: string;
  model: string;
  response: string;
  confidence: number;
}

interface CouncilResponse {
  status: string;
  consensus: boolean;
  unified_response: string | null;
  strategist_responses: StrategistResponse[];
  agreement_score: number;
  requires_commander: boolean;
}

function CouncilWidgetContent() {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<CouncilResponse | null>(null);

  // Memoize deliberate function
  const deliberate = useCallback(async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const res = await fetch("/api/council/deliberate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, require_consensus: true }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      logError("Council Error", {
        error: error instanceof Error ? error.message : "Unknown error",
      });
    } finally {
      setIsLoading(false);
    }
  }, [query]);

  // Memoize pillar color getter
  const getPillarColor = useCallback((strategist: string) => {
    switch (strategist) {
      case "제갈량":
        return "text-blue-400 border-blue-500/40 bg-blue-900/20";
      case "사마의":
        return "text-green-400 border-green-500/40 bg-green-900/20";
      case "주유":
        return "text-pink-400 border-pink-500/40 bg-pink-900/20";
      default:
        return "text-gray-400 border-gray-500/40 bg-gray-900/20";
    }
  }, []);

  // Memoize input handlers
  const handleQueryChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setQuery(e.target.value);
  }, []);

  // Memoize button disabled state
  const isButtonDisabled = useMemo(() => {
    return isLoading || !query.trim();
  }, [isLoading, query]);

  // Memoize formatted agreement score
  const formattedAgreementScore = useMemo(() => {
    if (!response) return null;
    return (response.agreement_score * 100).toFixed(1);
  }, [response]);

  return (
    <div
      className="p-6 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 rounded-2xl border border-indigo-500/40 backdrop-blur-xl shadow-2xl"
      role="region"
      aria-labelledby="council-title"
    >
      {/* Header */}
      <header className="flex items-center gap-3 mb-6">
        <Brain className="w-8 h-8 text-indigo-400" aria-hidden="true" />
        <h3 id="council-title" className="text-2xl font-bold text-white">
          지혜의 의회
        </h3>
        <span
          className="px-2 py-1 text-xs bg-indigo-500/30 text-indigo-300 rounded-full"
          aria-label="Council of Minds"
        >
          Council of Minds
        </span>
      </header>

      {/* Query Input */}
      <section aria-label="Query input">
        <div className="mb-6">
          <label htmlFor="council-query" className="sr-only">
            Enter your question to the council
          </label>
          <textarea
            id="council-query"
            value={query}
            onChange={handleQueryChange}
            placeholder="의회에 질문하세요... (예: 왕국의 상태를 분석하라)"
            className="w-full p-4 bg-black/30 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500/50"
            rows={3}
            aria-label="Question for the council"
            aria-required="false"
          />
          <button
            onClick={deliberate}
            disabled={isButtonDisabled}
            className="mt-3 w-full py-3 bg-indigo-600/80 hover:bg-indigo-500/80 text-white rounded-xl font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            aria-label={isLoading ? "Deliberating..." : "Ask the three strategists"}
            aria-disabled={isButtonDisabled}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" />
                의회 심의 중...
              </>
            ) : (
              <>
                <Users className="w-5 h-5" aria-hidden="true" />
                3책사에게 묻다
              </>
            )}
          </button>
        </div>
      </section>

      {/* Response */}
      {response && (
        <section aria-label="Council response">
          <div className="space-y-4">
            {/* Consensus Status */}
            <div
              className={`p-4 rounded-xl border ${response.consensus ? "bg-green-900/20 border-green-500/40" : "bg-yellow-900/20 border-yellow-500/40"}`}
              role="status"
              aria-live="polite"
              aria-label={response.consensus ? "Consensus reached" : "No consensus"}
            >
              <div className="flex items-center gap-2 mb-2">
                {response.consensus ? (
                  <CheckCircle2 className="w-5 h-5 text-green-400" aria-hidden="true" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-yellow-400" aria-hidden="true" />
                )}
                <span
                  className={`font-bold ${response.consensus ? "text-green-400" : "text-yellow-400"}`}
                >
                  {response.consensus ? "합의 도달" : "의견 불일치"}
                </span>
                <span className="text-sm text-gray-400">
                  (일치율: {formattedAgreementScore}%)
                </span>
              </div>
              {response.unified_response && (
                <p className="text-white whitespace-pre-line" aria-live="polite">
                  {response.unified_response}
                </p>
              )}
            </div>

            {/* Individual Responses */}
            <div
              className="grid grid-cols-1 md:grid-cols-3 gap-4"
              role="list"
              aria-label="Strategist responses"
            >
              {response.strategist_responses.map((r, i) => (
                <div
                  key={i}
                  className={`p-4 rounded-xl border ${getPillarColor(r.strategist)}`}
                  role="listitem"
                  aria-label={`${r.strategist} response, confidence: ${(r.confidence * 100).toFixed(0)}%`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-bold">{r.strategist}</span>
                    <span className="text-xs opacity-60">({r.model})</span>
                  </div>
                  <p className="text-sm opacity-80">{r.response}</p>
                  <div className="mt-2 text-xs opacity-60">
                    신뢰도: {(r.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export function CouncilWidget() {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error("CouncilWidget error:", error, errorInfo);
      }}
      fallback={
        <div
          className="p-6 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 rounded-2xl border border-red-500/40"
          role="alert"
        >
          <p className="text-red-400 text-center">지혜의 의회 위젯을 불러올 수 없습니다.</p>
        </div>
      }
    >
      <CouncilWidgetContent />
    </ErrorBoundary>
  );
}

export default CouncilWidget;
