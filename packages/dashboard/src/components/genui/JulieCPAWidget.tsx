/**
 * JulieCPAWidget.tsx
 *
 * 수호자 Julie CPA - 왕국의 금고를 지키는 재무 수호자
 * Phase 12: Complete Awakening
 *
 * "금고가 튼튼해야 왕국이 번영한다"
 */
'use client';

import React, { useEffect, useState } from 'react';

interface Transaction {
  id: string;
  merchant: string;
  amount: number;
  date: string;
  category: string;
}

interface RiskAlert {
  level: 'info' | 'warning' | 'critical';
  message: string;
}

interface FinanceDashboard {
  financial_health_score: number;
  monthly_spending: number;
  budget_remaining: number;
  recent_transactions: Transaction[];
  risk_alerts: RiskAlert[];
  advice: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010';

export function JulieCPAWidget() {
  const [data, setData] = useState<FinanceDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/finance/dashboard`);
        if (!response.ok) {
          if (response.status === 503 || response.status === 0) {
            throw new Error('API 서버가 실행 중이지 않습니다. 포트 8010에서 서버를 시작해주세요.');
          }
          throw new Error(`Failed to fetch financial data: ${response.statusText}`);
        }
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        if (err instanceof TypeError && err.message.includes('fetch')) {
          setError('API 서버 연결 실패: 포트 8010에서 서버가 실행 중인지 확인해주세요.');
        } else {
          setError(err instanceof Error ? err.message : 'Unknown error');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
    const interval = setInterval(fetchDashboard, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const getHealthColor = (score: number) => {
    if (score >= 80) return '#22C55E'; // Green
    if (score >= 60) return '#FBBF24'; // Yellow
    if (score >= 40) return '#F97316'; // Orange
    return '#EF4444'; // Red
  };

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'critical': return '#EF4444';
      case 'warning': return '#FBBF24';
      default: return '#3B82F6';
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
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(59, 130, 246, 0.2))',
        backdropFilter: 'blur(20px)',
        borderRadius: '20px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '24px',
        textAlign: 'center',
        color: 'rgba(255,255,255,0.7)',
      }}>
        🔄 Julie CPA 각성 중...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(239, 68, 68, 0.2))',
        backdropFilter: 'blur(20px)',
        borderRadius: '20px',
        border: '1px solid rgba(239, 68, 68, 0.3)',
        padding: '24px',
        textAlign: 'center',
        color: '#EF4444',
      }}>
        ⚠️ 금고 연결 실패: {error}
      </div>
    );
  }

  if (!data) return null;

  const healthColor = getHealthColor(data.financial_health_score);
  const healthPercentage = data.financial_health_score;

  return (
    <div
      style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(59, 130, 246, 0.15))',
        backdropFilter: 'blur(20px)',
        borderRadius: '24px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '28px',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '32px' }}>💰</span>
          <div>
            <h2 style={{
              fontSize: '20px',
              fontWeight: 'bold',
              color: 'white',
              margin: 0,
            }}>
              Julie CPA
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', margin: 0 }}>
              수호자 시대 · Phase 12
            </p>
          </div>
        </div>
        <div
          style={{
            background: `${healthColor}20`,
            border: `1px solid ${healthColor}50`,
            borderRadius: '12px',
            padding: '8px 16px',
          }}
        >
          <span style={{ color: healthColor, fontWeight: 'bold', fontSize: '14px' }}>
            {healthPercentage >= 80 ? '✅ 안정' : healthPercentage >= 60 ? '⚠️ 주의' : '🚨 위험'}
          </span>
        </div>
      </div>

      {/* Health Score Gauge */}
      <div style={{
        background: 'rgba(0,0,0,0.3)',
        borderRadius: '16px',
        padding: '20px',
        marginBottom: '20px',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <span style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px' }}>재무 건강도</span>
          <span style={{ color: healthColor, fontSize: '28px', fontWeight: 'bold' }}>
            {data.financial_health_score}%
          </span>
        </div>
        <div style={{
          width: '100%',
          height: '12px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '6px',
          overflow: 'hidden',
        }}>
          <div style={{
            width: `${healthPercentage}%`,
            height: '100%',
            background: `linear-gradient(90deg, ${healthColor}, ${healthColor}80)`,
            borderRadius: '6px',
            transition: 'width 0.5s ease',
          }} />
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '16px',
        marginBottom: '20px',
      }}>
        <div style={{
          background: 'rgba(59, 130, 246, 0.1)',
          borderRadius: '12px',
          padding: '16px',
          border: '1px solid rgba(59, 130, 246, 0.2)',
        }}>
          <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', marginBottom: '4px' }}>
            월간 지출
          </div>
          <div style={{ color: '#3B82F6', fontSize: '18px', fontWeight: 'bold' }}>
            {formatCurrency(data.monthly_spending)}
          </div>
        </div>
        <div style={{
          background: 'rgba(34, 197, 94, 0.1)',
          borderRadius: '12px',
          padding: '16px',
          border: '1px solid rgba(34, 197, 94, 0.2)',
        }}>
          <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', marginBottom: '4px' }}>
            잔여 예산
          </div>
          <div style={{ color: '#22C55E', fontSize: '18px', fontWeight: 'bold' }}>
            {formatCurrency(data.budget_remaining)}
          </div>
        </div>
      </div>

      {/* Risk Alerts */}
      {data.risk_alerts.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px', marginBottom: '12px', fontWeight: '600' }}>
            🛡️ 리스크 알림
          </div>
          {data.risk_alerts.map((alert, i) => (
            <div
              key={i}
              style={{
                background: `${getAlertColor(alert.level)}15`,
                border: `1px solid ${getAlertColor(alert.level)}30`,
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
              }}
            >
              <span style={{ fontSize: '16px' }}>
                {alert.level === 'critical' ? '🚨' : alert.level === 'warning' ? '⚠️' : 'ℹ️'}
              </span>
              <span style={{ color: 'rgba(255,255,255,0.9)', fontSize: '13px' }}>
                {alert.message}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Recent Transactions */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px', marginBottom: '12px', fontWeight: '600' }}>
          📊 최근 거래
        </div>
        {data.recent_transactions.slice(0, 3).map((tx) => (
          <div
            key={tx.id}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '10px 0',
              borderBottom: '1px solid rgba(255,255,255,0.05)',
            }}
          >
            <div>
              <div style={{ color: 'white', fontSize: '14px' }}>{tx.merchant}</div>
              <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px' }}>{tx.category} · {tx.date}</div>
            </div>
            <div style={{ color: '#F97316', fontWeight: '600', fontSize: '14px' }}>
              -{formatCurrency(tx.amount)}
            </div>
          </div>
        ))}
      </div>

      {/* AI Advice */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(59, 130, 246, 0.15))',
        borderRadius: '12px',
        padding: '16px',
        border: '1px solid rgba(168, 85, 247, 0.2)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span style={{ fontSize: '16px' }}>🤖</span>
          <span style={{ color: '#A855F7', fontSize: '12px', fontWeight: '600' }}>Julie's Advice</span>
        </div>
        <p style={{
          color: 'rgba(255,255,255,0.85)',
          fontSize: '13px',
          lineHeight: '1.6',
          margin: 0,
        }}>
          {data.advice}
        </p>
      </div>

      {/* Footer */}
      <div style={{
        marginTop: '16px',
        textAlign: 'center',
        color: 'rgba(255,255,255,0.4)',
        fontSize: '11px'
      }}>
        眞善美孝永 · Julie CPA Phase 12 Active
      </div>
    </div>
  );
}

export default JulieCPAWidget;
