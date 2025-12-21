/**
 * JulieSuggestions.tsx
 *
 * Phase 12-3: Smart Guardian - Julie CPA의 스마트 제안
 * "Julie가 제안해요: 지출 줄여보세요 – 잔고 안전 업그레이드 ✨"
 */
'use client';

import React, { useEffect, useState } from 'react';

interface Suggestion {
  priority: 'critical' | 'warning' | 'info' | 'success';
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

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010';

export function JulieSuggestions() {
  const [data, setData] = useState<SuggestionsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/julie/budget/suggestions`);
        if (response.ok) {
          const json = await response.json();
          setData(json);
        }
      } catch (err) {
        console.warn('Suggestions fetch failed:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
    const interval = setInterval(fetchSuggestions, 60000);
    return () => clearInterval(interval);
  }, []);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return { bg: 'rgba(239, 68, 68, 0.15)', border: 'rgba(239, 68, 68, 0.4)', text: '#EF4444' };
      case 'warning': return { bg: 'rgba(251, 191, 36, 0.15)', border: 'rgba(251, 191, 36, 0.4)', text: '#FBBF24' };
      case 'info': return { bg: 'rgba(59, 130, 246, 0.15)', border: 'rgba(59, 130, 246, 0.4)', text: '#3B82F6' };
      case 'success': return { bg: 'rgba(34, 197, 94, 0.15)', border: 'rgba(34, 197, 94, 0.4)', text: '#22C55E' };
      default: return { bg: 'rgba(107, 114, 128, 0.15)', border: 'rgba(107, 114, 128, 0.4)', text: '#6B7280' };
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  if (loading) {
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(168, 85, 247, 0.1))',
        borderRadius: '20px',
        padding: '24px',
        textAlign: 'center',
        color: 'rgba(255,255,255,0.7)',
      }}>
        🔄 제안 분석 중...
      </div>
    );
  }

  if (!data) return null;

  return (
    <div
      style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(168, 85, 247, 0.15))',
        backdropFilter: 'blur(20px)',
        borderRadius: '24px',
        border: '1px solid rgba(168, 85, 247, 0.2)',
        padding: '28px',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '32px' }}>💡</span>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: 'bold', color: 'white', margin: 0 }}>
              Julie CPA의 스마트 제안
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', margin: 0 }}>
              Phase 12-3 · Smart Guardian
            </p>
          </div>
        </div>
        {data.total_potential_saving > 0 && (
          <div style={{
            background: 'rgba(34, 197, 94, 0.2)',
            border: '1px solid rgba(34, 197, 94, 0.4)',
            borderRadius: '12px',
            padding: '8px 16px',
          }}>
            <span style={{ color: '#22C55E', fontWeight: 'bold', fontSize: '14px' }}>
              💰 {formatCurrency(data.total_potential_saving)} 절감 가능
            </span>
          </div>
        )}
      </div>

      {/* Suggestions List */}
      <div style={{ marginBottom: '16px' }}>
        {data.suggestions.map((suggestion, i) => {
          const colors = getPriorityColor(suggestion.priority);
          return (
            <div
              key={i}
              style={{
                background: colors.bg,
                border: `1px solid ${colors.border}`,
                borderRadius: '12px',
                padding: '16px',
                marginBottom: '12px',
                transition: 'transform 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateX(4px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateX(0)';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                <span style={{ fontSize: '24px' }}>{suggestion.icon}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <h3 style={{ color: colors.text, fontSize: '16px', fontWeight: 'bold', margin: 0 }}>
                      {suggestion.title}
                    </h3>
                    {suggestion.expected_saving > 0 && (
                      <span style={{ color: '#22C55E', fontSize: '12px', fontWeight: '600' }}>
                        +{formatCurrency(suggestion.expected_saving)}
                      </span>
                    )}
                  </div>
                  <p style={{ color: 'rgba(255,255,255,0.85)', fontSize: '14px', margin: '8px 0 0 0', lineHeight: '1.5' }}>
                    {suggestion.message}
                  </p>
                  {suggestion.action && (
                    <button
                      style={{
                        marginTop: '12px',
                        background: `${colors.text}20`,
                        border: `1px solid ${colors.text}50`,
                        borderRadius: '8px',
                        padding: '6px 12px',
                        color: colors.text,
                        fontSize: '12px',
                        fontWeight: '600',
                        cursor: 'pointer',
                      }}
                    >
                      {suggestion.action} →
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary */}
      <div style={{
        background: 'rgba(168, 85, 247, 0.1)',
        borderRadius: '12px',
        padding: '12px 16px',
        textAlign: 'center',
      }}>
        <p style={{ color: '#A855F7', fontSize: '13px', margin: 0 }}>
          {data.summary}
        </p>
      </div>
    </div>
  );
}

export default JulieSuggestions;
