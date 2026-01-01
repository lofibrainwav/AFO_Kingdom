/**
 * Julie CPA Tax Estimate Card - 2026 여성 사용자 트렌드 적용
 *
 * 2026 트렌드 적용:
 * - 텍스처 체크: 블러 글래스 + 유리 질감
 * - 초개인화: 사용자 맞춤 메시지 + 감성적 라이팅
 * - 휴먼 인 더 루프: Julie의 공감 메시지
 * - 마이크로 인터랙션: 부드러운 애니메이션
 * - 한 손 조작: 모바일 최적화
 *
 * SSOT 기반 세금 계산기:
 * - Trinity Score: 眞善美孝永 철학 준수
 * - API 연동: /api/tax/estimate
 * - SSOT 보장: Evidence Bundle ID 추적
 * - 실시간 계산: 입력 변경 시 자동 업데이트
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, Calculator, CheckCircle, ExternalLink, Heart, Sparkles, Zap } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface TaxEstimateRequest {
  filing_status: string;
  gross_income: number;
  adjustments: number;
  itemized_deductions?: number;
  is_dependent: boolean;
  age_65_or_over: boolean;
  blind: boolean;
  spouse_age_65_or_over?: boolean;
  spouse_blind?: boolean;
  magi?: number;
}

interface TaxEstimateResponse {
  federal: {
    tax: number;
    taxable_income: number;
    deduction: number;
  };
  california: {
    tax: number;
    taxable_income: number;
    deduction: number;
  };
  total_tax: number;
  effective_rate: number;
  evidence_bundle_id: string;
  calculated_at: string;
  ssot_version: string;
  input_summary: any;
}

const TaxEstimateCard: React.FC = () => {
  // 입력 상태
  const [request, setRequest] = useState<TaxEstimateRequest>({
    filing_status: 'SINGLE',
    gross_income: 75000,
    adjustments: 0,
    itemized_deductions: undefined,
    is_dependent: false,
    age_65_or_over: false,
    blind: false,
    spouse_age_65_or_over: false,
    spouse_blind: false,
    magi: undefined,
  });

  // 결과 상태
  const [result, setResult] = useState<TaxEstimateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 자동 계산 (디바운스)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (request.gross_income > 0) {
        calculateTax();
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [request]);

  const calculateTax = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/tax/estimate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '세금 계산 중 오류 발생');
      }

      const data: TaxEstimateResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatPercent = (rate: number): string => {
    return `${(rate).toFixed(2)}%`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Card className="w-full max-w-4xl mx-auto relative overflow-hidden">
        {/* 텍스처 백그라운드 - 2026 트렌드 적용 */}
        <div className="absolute inset-0 bg-gradient-to-br from-rose-50/30 via-pink-50/20 to-purple-50/30 opacity-50"></div>
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-pink-200/10 to-purple-200/10 rounded-full blur-3xl"></div>

        <CardHeader className="bg-gradient-to-r from-rose-50/80 via-pink-50/80 to-purple-50/80 backdrop-blur-sm border-b border-white/20 relative z-10">
          <CardTitle className="flex items-center gap-3 text-xl">
            <motion.div
              whileHover={{ scale: 1.1, rotate: 5 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
            >
              <Heart className="h-7 w-7 text-pink-500" />
            </motion.div>
            <span className="bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent font-bold">
              Julie CPA 세금 추정기
            </span>
            <Badge variant="secondary" className="ml-auto bg-pink-100 text-pink-700 border-pink-200">
              <Sparkles className="h-3 w-3 mr-1" />
              SSOT 2026 ✨
            </Badge>
          </CardTitle>
          <p className="text-sm text-gray-600 italic">
            "세금 계산이 이렇게 아름다울 수 있다니 💕 IRS/FTB 공식 세법 기반 정확한 계산"
          </p>
        </CardHeader>

        <CardContent className="p-6 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 입력 섹션 */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                세금 정보 입력
              </h3>

              {/* 신고 상태 */}
              <div className="space-y-2">
                <Label htmlFor="filing_status">신고 상태</Label>
                <Select
                  value={request.filing_status}
                  onValueChange={(value) =>
                    setRequest(prev => ({ ...prev, filing_status: value }))
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="신고 상태 선택" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="SINGLE">독신 (Single)</SelectItem>
                    <SelectItem value="MARRIED_FILING_JOINTLY">부부 공동 신고 (MFJ)</SelectItem>
                    <SelectItem value="MARRIED_FILING_SEPARATELY">부부 별도 신고 (MFS)</SelectItem>
                    <SelectItem value="HEAD_OF_HOUSEHOLD">가족주부 (HOH)</SelectItem>
                    <SelectItem value="QUALIFYING_SURVIVING_SPOUSE">생존 배우자 (QSS)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* 소득 및 공제 */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="gross_income">총 소득 ($)</Label>
                  <Input
                    id="gross_income"
                    type="number"
                    value={request.gross_income}
                    onChange={(e) =>
                      setRequest(prev => ({
                        ...prev,
                        gross_income: parseFloat(e.target.value) || 0
                      }))
                    }
                    placeholder="75000"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="adjustments">조정액 ($)</Label>
                  <Input
                    id="adjustments"
                    type="number"
                    value={request.adjustments}
                    onChange={(e) =>
                      setRequest(prev => ({
                        ...prev,
                        adjustments: parseFloat(e.target.value) || 0
                      }))
                    }
                    placeholder="0"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="itemized_deductions">항목별 공제 (선택사항) ($)</Label>
                <Input
                  id="itemized_deductions"
                  type="number"
                  value={request.itemized_deductions || ''}
                  onChange={(e) =>
                    setRequest(prev => ({
                      ...prev,
                      itemized_deductions: e.target.value ? parseFloat(e.target.value) : undefined
                    }))
                  }
                  placeholder="표준공제보다 큰 경우에만 입력"
                />
              </div>

              {/* 개인 플래그 */}
              <div className="space-y-3">
                <Label>개인 상황</Label>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="is_dependent"
                      checked={request.is_dependent}
                      onCheckedChange={(checked) =>
                        setRequest(prev => ({ ...prev, is_dependent: checked as boolean }))
                      }
                    />
                    <Label htmlFor="is_dependent">부양가족 (미성년 자녀 등)</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="age_65_or_over"
                      checked={request.age_65_or_over}
                      onCheckedChange={(checked) =>
                        setRequest(prev => ({ ...prev, age_65_or_over: checked as boolean }))
                      }
                    />
                    <Label htmlFor="age_65_or_over">65세 이상 (OBBBA 고령자 공제 적용)</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="blind"
                      checked={request.blind}
                      onCheckedChange={(checked) =>
                        setRequest(prev => ({ ...prev, blind: checked as boolean }))
                      }
                    />
                    <Label htmlFor="blind">시각장애인</Label>
                  </div>
                </div>
              </div>

              {/* 배우자 플래그 (부부 신고 시) */}
              {(request.filing_status === 'MARRIED_FILING_JOINTLY' ||
                request.filing_status === 'MARRIED_FILING_SEPARATELY') && (
                <div className="space-y-3">
                  <Label>배우자 상황</Label>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="spouse_age_65_or_over"
                        checked={request.spouse_age_65_or_over || false}
                        onCheckedChange={(checked) =>
                          setRequest(prev => ({ ...prev, spouse_age_65_or_over: checked as boolean }))
                        }
                      />
                      <Label htmlFor="spouse_age_65_or_over">배우자 65세 이상</Label>
                    </div>

                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="spouse_blind"
                        checked={request.spouse_blind || false}
                        onCheckedChange={(checked) =>
                          setRequest(prev => ({ ...prev, spouse_blind: checked as boolean }))
                        }
                      />
                      <Label htmlFor="spouse_blind">배우자 시각장애</Label>
                    </div>
                  </div>
                </div>
              )}

              {/* MAGI (고령자 공제 계산용) */}
              {(request.age_65_or_over || request.spouse_age_65_or_over) && (
                <div className="space-y-2">
                  <Label htmlFor="magi">Modified AGI (MAGI) - 고령자 공제 계산용 ($)</Label>
                  <Input
                    id="magi"
                    type="number"
                    value={request.magi || ''}
                    onChange={(e) =>
                      setRequest(prev => ({
                        ...prev,
                        magi: e.target.value ? parseFloat(e.target.value) : undefined
                      }))
                    }
                    placeholder="총 소득과 유사한 경우 생략 가능"
                  />
                </div>
              )}
            </div>

            {/* 결과 섹션 */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <Calculator className="h-5 w-5 text-green-600" />
                세금 계산 결과
              </h3>

              {loading && (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-2 text-sm text-muted-foreground">세금 계산 중...</p>
                </div>
              )}

              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {result && !loading && (
                <div className="space-y-4">
                  {/* 총 세금 요약 */}
                  <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-950 dark:to-blue-950">
                    <CardContent className="p-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-700 dark:text-green-300">
                          {formatCurrency(result.total_tax)}
                        </div>
                        <div className="text-sm text-muted-foreground">총 세금 (연방 + CA)</div>
                        <div className="text-lg font-semibold text-blue-600 mt-1">
                          유효 세율: {formatPercent(result.effective_rate)}
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* 세부 내역 */}
                  <div className="grid grid-cols-2 gap-4">
                    {/* 연방 세금 */}
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">연방 세금</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm">세금:</span>
                          <span className="font-semibold">{formatCurrency(result.federal.tax)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm">과세소득:</span>
                          <span>{formatCurrency(result.federal.taxable_income)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm">공제:</span>
                          <span>{formatCurrency(result.federal.deduction)}</span>
                        </div>
                      </CardContent>
                    </Card>

                    {/* CA 주세 */}
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">캘리포니아 주세</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm">세금:</span>
                          <span className="font-semibold">{formatCurrency(result.california.tax)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm">과세소득:</span>
                          <span>{formatCurrency(result.california.taxable_income)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm">공제:</span>
                          <span>{formatCurrency(result.california.deduction)}</span>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* SSOT 증거 정보 */}
                  <Card className="bg-gray-50 dark:bg-gray-900">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-base flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        SSOT 증거 정보
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Evidence Bundle ID:</span>
                        <code className="bg-gray-200 dark:bg-gray-800 px-2 py-1 rounded text-xs">
                          {result.evidence_bundle_id.substring(0, 8)}...
                        </code>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>SSOT 버전:</span>
                        <Badge variant="outline">{result.ssot_version}</Badge>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>계산 시각:</span>
                        <span>{new Date(result.calculated_at).toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>공식 문서:</span>
                        <a
                          href="https://www.irs.gov/publications/p17"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline flex items-center gap-1"
                        >
                          IRS Pub 17 <ExternalLink className="h-3 w-3" />
                        </a>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Trinity Score 배지 */}
                  <div className="flex justify-center gap-2">
                    <Badge variant="secondary">眞 SSOT 기반</Badge>
                    <Badge variant="secondary">善 OBBBA 준수</Badge>
                    <Badge variant="secondary">美 실시간 계산</Badge>
                    <Badge variant="secondary">孝 안전한 API</Badge>
                    <Badge variant="secondary">永 증거 추적</Badge>
                  </div>
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default TaxEstimateCard;
