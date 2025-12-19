/**
 * JuliePrediction.tsx
 * 
 * Phase 12-4: Predictive Guardian - Julie CPA의 미래 예측
 * "Julie가 미래를 봐요 – 다음 달 예상 지출 알려줄게요 ✨"
 */
'use client';

import React, { useEffect, useState } from 'react';

interface HistoryPoint {
  month: string;
  spent: number;
}

interface PredictionData {
  current_month_spending: number;
  next_month_predicted: number;
  difference: number;
  difference_percent: number;
  confidence: number;
  confidence_note: string;
  trend: 'increasing' | 'decreasing' | 'stable';
  trend_slope: number;
  risk_level: 'safe' | 'warning' | 'info';
  advice: string;
  history: HistoryPoint[];
  summary: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8011';

export function JuliePrediction() {
  const [data, setData] = useState<PredictionData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/julie/budget/prediction`);
        if (response.ok) {
          const json = await response.json();
          setData(json);
        }
      } catch (err) {
        console.warn('Prediction fetch failed:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
    const interval = setInterval(fetchPrediction, 120000); // Refresh every 2 min
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return '📈';
      case 'decreasing': return '📉';
      default: return '📊';
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'increasing': return '#FBBF24';
      case 'decreasing': return '#22C55E';
      default: return '#3B82F6';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#22C55E';
    if (confidence >= 0.5) return '#FBBF24';
    return '#EF4444';
  };

  if (loading) {
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(34, 197, 94, 0.1))',
        borderRadius: '20px',
        padding: '24px',
        textAlign: 'center',
        color: 'rgba(255,255,255,0.7)',
      }}>
        🔮 미래 예측 중...
      </div>
    );
  }

  if (!data) return null;

  const maxSpent = Math.max(...data.history.map(h => h.spent), data.next_month_predicted);

  return (
    <div
      style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(34, 197, 94, 0.15))',
        backdropFilter: 'blur(20px)',
        borderRadius: '24px',
        border: '1px solid rgba(34, 197, 94, 0.2)',
        padding: '28px',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '32px' }}>🔮</span>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: 'bold', color: 'white', margin: 0 }}>
              Julie CPA의 미래 예측
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', margin: 0 }}>
              Phase 12-4 · Predictive Guardian
            </p>
          </div>
        </div>
        <div style={{
          background: 'rgba(34, 197, 94, 0.2)',
          border: '1px solid rgba(34, 197, 94, 0.4)',
          borderRadius: '12px',
          padding: '8px 16px',
        }}>
          <span style={{ color: getTrendColor(data.trend), fontWeight: 'bold', fontSize: '14px' }}>
            {getTrendIcon(data.trend)} {data.trend === 'increasing' ? '증가 추세' : data.trend === 'decreasing' ? '감소 추세' : '안정 추세'}
          </span>
        </div>
      </div>

      {/* Main Prediction */}
      <div style={{
        background: 'rgba(0,0,0,0.3)',
        borderRadius: '16px',
        padding: '24px',
        marginBottom: '20px',
        textAlign: 'center',
      }}>
        <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '14px', marginBottom: '8px' }}>
          다음 달 예상 지출
        </p>
        <div style={{ 
          fontSize: '36px', 
          fontWeight: 'bold', 
          color: '#22C55E',
          marginBottom: '8px',
        }}>
          {formatCurrency(data.next_month_predicted)}
        </div>
        <div style={{ 
          display: 'inline-block',
          background: data.difference > 0 ? 'rgba(251, 191, 36, 0.2)' : 'rgba(34, 197, 94, 0.2)',
          borderRadius: '20px',
          padding: '6px 14px',
          color: data.difference > 0 ? '#FBBF24' : '#22C55E',
          fontSize: '14px',
          fontWeight: '600',
        }}>
          {data.difference > 0 ? '↑' : '↓'} {Math.abs(data.difference_percent)}% vs 현재
        </div>
      </div>

      {/* Confidence Meter */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px' }}>예측 신뢰도</span>
          <span style={{ color: getConfidenceColor(data.confidence), fontWeight: 'bold' }}>
            {(data.confidence * 100).toFixed(0)}% {data.confidence_note}
          </span>
        </div>
        <div style={{ 
          width: '100%', 
          height: '8px', 
          background: 'rgba(255,255,255,0.1)', 
          borderRadius: '4px',
          overflow: 'hidden',
        }}>
          <div style={{ 
            width: `${data.confidence * 100}%`, 
            height: '100%', 
            background: `linear-gradient(90deg, ${getConfidenceColor(data.confidence)}, ${getConfidenceColor(data.confidence)}80)`,
            borderRadius: '4px',
            transition: 'width 0.5s ease',
          }} />
        </div>
      </div>

      {/* Mini Chart (Simple Bar Chart) */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px', marginBottom: '12px', fontWeight: '600' }}>
          📊 지출 추이 (6개월)
        </div>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px', height: '80px' }}>
          {data.history.map((point, i) => {
            const height = (point.spent / maxSpent) * 100;
            return (
              <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{
                  width: '100%',
                  height: `${height}%`,
                  background: 'linear-gradient(to top, #3B82F6, #60A5FA)',
                  borderRadius: '4px 4px 0 0',
                  minHeight: '8px',
                }} />
                <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: '10px', marginTop: '4px' }}>
                  {point.month.split('-')[1]}월
                </span>
              </div>
            );
          })}
          {/* Prediction Bar */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{
              width: '100%',
              height: `${(data.next_month_predicted / maxSpent) * 100}%`,
              background: 'linear-gradient(to top, #22C55E, #4ADE80)',
              borderRadius: '4px 4px 0 0',
              minHeight: '8px',
              border: '2px dashed rgba(255,255,255,0.3)',
            }} />
            <span style={{ color: '#22C55E', fontSize: '10px', marginTop: '4px', fontWeight: 'bold' }}>
              예측
            </span>
          </div>
        </div>
      </div>

      {/* Advice */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(59, 130, 246, 0.1))',
        borderRadius: '12px',
        padding: '16px',
      }}>
        <p style={{ 
          color: getTrendColor(data.trend), 
          fontSize: '14px', 
          margin: 0,
          lineHeight: '1.6',
        }}>
          {data.advice}
        </p>
      </div>
    </div>
  );
}

export default JuliePrediction;
