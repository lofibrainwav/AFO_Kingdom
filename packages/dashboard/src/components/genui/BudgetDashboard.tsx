/**
 * BudgetDashboard.tsx
 *
 * Phase 12 Extension: 실시간 예산 대시보드
 * "금고 안전! Julie CPA가 왕국 부를 지켜요" 🛡️💰
 */
'use client';

import React, { useEffect, useState } from 'react';

interface BudgetCategory {
  id: number;
  category: string;
  allocated: number;
  spent: number;
  remaining: number;
}

interface BudgetData {
  budgets: BudgetCategory[];
  total_allocated: number;
  total_spent: number;
  total_remaining: number;
  utilization_rate: number;
  risk_score: number;
  risk_level: 'safe' | 'warning' | 'critical';
  summary: string;
  timestamp: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010';

export function BudgetDashboard() {
  const [data, setData] = useState<BudgetData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/julie/budget`);
        if (!response.ok) throw new Error('예산 데이터 로드 실패');
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchBudget();
    const interval = setInterval(fetchBudget, 60000); // 1분마다 갱신
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'safe': return '#22C55E';
      case 'warning': return '#FBBF24';
      case 'critical': return '#EF4444';
      default: return '#6B7280';
    }
  };

  const getUtilizationColor = (rate: number) => {
    if (rate < 60) return '#22C55E';
    if (rate < 80) return '#FBBF24';
    return '#EF4444';
  };

  if (loading) {
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(34, 197, 94, 0.1))',
        backdropFilter: 'blur(20px)',
        borderRadius: '20px',
        padding: '24px',
        textAlign: 'center',
        color: 'rgba(255,255,255,0.7)',
      }}>
        🔄 예산 데이터 로딩 중...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(239, 68, 68, 0.2))',
        borderRadius: '20px',
        padding: '24px',
        textAlign: 'center',
        color: '#EF4444',
      }}>
        ⚠️ {error}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div
      style={{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(34, 197, 94, 0.1))',
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
          <span style={{ fontSize: '32px' }}>📊</span>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: 'bold', color: 'white', margin: 0 }}>
              예산 대시보드
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', margin: 0 }}>
              Phase 12 · Julie CPA 확장
            </p>
          </div>
        </div>
        <div
          style={{
            background: `${getRiskColor(data.risk_level)}20`,
            border: `1px solid ${getRiskColor(data.risk_level)}50`,
            borderRadius: '12px',
            padding: '8px 16px',
          }}
        >
          <span style={{ color: getRiskColor(data.risk_level), fontWeight: 'bold', fontSize: '14px' }}>
            Risk: {data.risk_score}
          </span>
        </div>
      </div>

      {/* Summary Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <div style={{
          background: 'rgba(34, 197, 94, 0.1)',
          borderRadius: '12px',
          padding: '16px',
          textAlign: 'center',
        }}>
          <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', marginBottom: '4px' }}>
            총 예산
          </div>
          <div style={{ color: '#22C55E', fontSize: '18px', fontWeight: 'bold' }}>
            {formatCurrency(data.total_allocated)}
          </div>
        </div>
        <div style={{
          background: 'rgba(251, 191, 36, 0.1)',
          borderRadius: '12px',
          padding: '16px',
          textAlign: 'center',
        }}>
          <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', marginBottom: '4px' }}>
            지출
          </div>
          <div style={{ color: '#FBBF24', fontSize: '18px', fontWeight: 'bold' }}>
            {formatCurrency(data.total_spent)}
          </div>
        </div>
        <div style={{
          background: 'rgba(59, 130, 246, 0.1)',
          borderRadius: '12px',
          padding: '16px',
          textAlign: 'center',
        }}>
          <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: '12px', marginBottom: '4px' }}>
            잔여
          </div>
          <div style={{ color: '#3B82F6', fontSize: '18px', fontWeight: 'bold' }}>
            {formatCurrency(data.total_remaining)}
          </div>
        </div>
      </div>

      {/* Utilization Bar */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px' }}>예산 사용률</span>
          <span style={{ color: getUtilizationColor(data.utilization_rate), fontWeight: 'bold' }}>
            {data.utilization_rate}%
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
            width: `${Math.min(data.utilization_rate, 100)}%`,
            height: '100%',
            background: `linear-gradient(90deg, ${getUtilizationColor(data.utilization_rate)}, ${getUtilizationColor(data.utilization_rate)}80)`,
            borderRadius: '6px',
            transition: 'width 0.5s ease',
          }} />
        </div>
      </div>

      {/* Category Breakdown */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px', marginBottom: '12px', fontWeight: '600' }}>
          📋 카테고리별 현황
        </div>
        {data.budgets.map((budget) => {
          const rate = (budget.spent / budget.allocated) * 100;
          return (
            <div
              key={budget.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px',
                marginBottom: '8px',
                background: 'rgba(255,255,255,0.03)',
                borderRadius: '8px',
              }}
            >
              <div style={{ flex: 1 }}>
                <div style={{ color: 'white', fontSize: '14px', marginBottom: '4px' }}>
                  {budget.category}
                </div>
                <div style={{
                  width: '100%',
                  height: '4px',
                  background: 'rgba(255,255,255,0.1)',
                  borderRadius: '2px',
                }}>
                  <div style={{
                    width: `${Math.min(rate, 100)}%`,
                    height: '100%',
                    background: getUtilizationColor(rate),
                    borderRadius: '2px',
                  }} />
                </div>
              </div>
              <div style={{ textAlign: 'right', marginLeft: '16px' }}>
                <div style={{ color: getUtilizationColor(rate), fontSize: '14px', fontWeight: '600' }}>
                  {formatCurrency(budget.remaining)}
                </div>
                <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px' }}>
                  {rate.toFixed(0)}% 사용
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Julie Summary */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(59, 130, 246, 0.1))',
        borderRadius: '12px',
        padding: '16px',
        textAlign: 'center',
      }}>
        <p style={{
          color: getRiskColor(data.risk_level),
          fontSize: '14px',
          fontWeight: '600',
          margin: 0,
        }}>
          {data.summary}
        </p>
      </div>
    </div>
  );
}

export default BudgetDashboard;
