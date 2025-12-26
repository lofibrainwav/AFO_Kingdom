'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { RefreshCw, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

interface TrinityEvidence {
  date: string;
  evidence: {
    calculation: {
      truth: number;
      goodness: number;
      beauty: number;
      serenity: number;
      eternity: number;
      total: number;
      gate: string;
      philosophy: string;
    };
  };
  verdict: string;
  status: string;
}

export function TrinityEvidenceWidget() {
  const [evidence, setEvidence] = useState<TrinityEvidence | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEvidence = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/api/trinity-evidence');
      const data = await response.json();

      if (data.status === 'success') {
        setEvidence(data);
      } else {
        setError(data.error || '증거를 불러올 수 없습니다');
      }
    } catch (err) {
      setError('네트워크 오류가 발생했습니다');
      console.error('Trinity Evidence fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvidence();
  }, []);

  const getGateColor = (gate: string) => {
    switch (gate) {
      case 'AUTO_RUN':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'ASK_COMMANDER':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default:
        return 'bg-red-100 text-red-800 border-red-300';
    }
  };

  const getGateIcon = (gate: string) => {
    switch (gate) {
      case 'AUTO_RUN':
        return <CheckCircle className="h-4 w-4" />;
      case 'ASK_COMMANDER':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return <XCircle className="h-4 w-4" />;
    }
  };

  if (loading) {
    return (
      <Card className="w-full">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Trinity Evidence</CardTitle>
          <RefreshCw className="h-4 w-4 animate-spin" />
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error || !evidence) {
    return (
      <Card className="w-full">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Trinity Evidence</CardTitle>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchEvidence}
            disabled={loading}
          >
            <RefreshCw className={`h-3 w-3 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">
            <XCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
            <p className="text-sm text-gray-600">
              {error || '증거를 불러올 수 없습니다'}
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const calculation = evidence.evidence.calculation || evidence.evidence.score;

  if (!calculation) {
    return (
      <Card className="w-full">
        <CardContent className="pt-6">
          <div className="text-center">
            <AlertTriangle className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
            <p className="text-sm text-gray-600">데이터 형식이 올바르지 않습니다</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const gate = calculation.gate || 'UNKNOWN';

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">
          Trinity Evidence — {evidence.date}
        </CardTitle>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className={getGateColor(gate)}>
            {getGateIcon(gate)}
            <span className="ml-1">{gate}</span>
          </Badge>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchEvidence}
            disabled={loading}
          >
            <RefreshCw className={`h-3 w-3 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {/* 총점 표시 */}
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">총점</span>
          <span className="text-2xl font-bold text-blue-600">
            {calculation.total.toFixed(3)}
          </span>
        </div>

        {/* 각 기둥 점수 */}
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="flex justify-between">
            <span>眞 Truth</span>
            <span className="font-medium">{calculation.truth.toFixed(3)}</span>
          </div>
          <div className="flex justify-between">
            <span>善 Goodness</span>
            <span className="font-medium">{calculation.goodness.toFixed(3)}</span>
          </div>
          <div className="flex justify-between">
            <span>美 Beauty</span>
            <span className="font-medium">{calculation.beauty.toFixed(3)}</span>
          </div>
          <div className="flex justify-between">
            <span>孝 Serenity</span>
            <span className="font-medium">{(calculation.serenity ?? calculation.filial ?? 0).toFixed(3)}</span>
          </div>
          <div className="flex justify-between">
            <span>永 Eternity</span>
            <span className="font-medium">{calculation.eternity.toFixed(3)}</span>
          </div>
        </div>

        {/* 철학 표시 */}
        <div className="pt-2 border-t">
          <p className="text-xs text-gray-600 italic">
            "{calculation.philosophy}"
          </p>
        </div>
      </CardContent>
    </Card>
  );
}