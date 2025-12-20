'use client';

import { useState } from 'react';
import { Brain, Users, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react';

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

export function CouncilWidget() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<CouncilResponse | null>(null);

  const deliberate = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      const res = await fetch('/api/council/deliberate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, require_consensus: true })
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Council Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getPillarColor = (strategist: string) => {
    switch (strategist) {
      case '제갈량': return 'text-blue-400 border-blue-500/40 bg-blue-900/20';
      case '사마의': return 'text-green-400 border-green-500/40 bg-green-900/20';
      case '주유': return 'text-pink-400 border-pink-500/40 bg-pink-900/20';
      default: return 'text-gray-400 border-gray-500/40 bg-gray-900/20';
    }
  };

  return (
    <div className="p-6 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 rounded-2xl border border-indigo-500/40 backdrop-blur-xl shadow-2xl">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <Brain className="w-8 h-8 text-indigo-400" />
        <h3 className="text-2xl font-bold text-white">지혜의 의회</h3>
        <span className="px-2 py-1 text-xs bg-indigo-500/30 text-indigo-300 rounded-full">
          Council of Minds
        </span>
      </div>

      {/* Query Input */}
      <div className="mb-6">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="의회에 질문하세요... (예: 왕국의 상태를 분석하라)"
          className="w-full p-4 bg-black/30 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500/50"
          rows={3}
        />
        <button
          onClick={deliberate}
          disabled={isLoading || !query.trim()}
          className="mt-3 w-full py-3 bg-indigo-600/80 hover:bg-indigo-500/80 text-white rounded-xl font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              의회 심의 중...
            </>
          ) : (
            <>
              <Users className="w-5 h-5" />
              3책사에게 묻다
            </>
          )}
        </button>
      </div>

      {/* Response */}
      {response && (
        <div className="space-y-4">
          {/* Consensus Status */}
          <div className={`p-4 rounded-xl border ${response.consensus ? 'bg-green-900/20 border-green-500/40' : 'bg-yellow-900/20 border-yellow-500/40'}`}>
            <div className="flex items-center gap-2 mb-2">
              {response.consensus ? (
                <CheckCircle2 className="w-5 h-5 text-green-400" />
              ) : (
                <AlertTriangle className="w-5 h-5 text-yellow-400" />
              )}
              <span className={`font-bold ${response.consensus ? 'text-green-400' : 'text-yellow-400'}`}>
                {response.consensus ? '합의 도달' : '의견 불일치'}
              </span>
              <span className="text-sm text-gray-400">
                (일치율: {(response.agreement_score * 100).toFixed(1)}%)
              </span>
            </div>
            {response.unified_response && (
              <p className="text-white whitespace-pre-line">{response.unified_response}</p>
            )}
          </div>

          {/* Individual Responses */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {response.strategist_responses.map((r, i) => (
              <div key={i} className={`p-4 rounded-xl border ${getPillarColor(r.strategist)}`}>
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
      )}
    </div>
  );
}
