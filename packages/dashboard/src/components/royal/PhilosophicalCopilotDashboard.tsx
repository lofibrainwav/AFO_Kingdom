"use client";
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { apiClient } from '@/lib/api-client';
import { useVerdictStream } from '@/lib/useVerdictStream';
import {
    AlertTriangle,
    BookOpen,
    CheckCircle,
    Crown,
    Heart,
    Infinity,
    Shield,
    Sword,
    XCircle,
    Zap
} from 'lucide-react';
import { useEffect, useState } from 'react';

// 철학적 상수들 (AFO 왕국 사서에서 영감)
const PHILOSOPHICAL_CONSTANTS = {
  // 손자병법
  sunzi: {
    wisdom: "지피지기면 백전불패",
    strategy: "선확인, 후보고",
    victory: "불전지승"
  },
  // 맹자
  mencius: {
    virtue: "인정지심",
    governance: "민위천",
    courage: "대담함"
  },
  // 플라톤
  plato: {
    truth: "이데아의 세계",
    justice: "각자의 본분",
    harmony: "영혼의 조화"
  }
};

// 眞善美孝永 아이콘 매핑
const TRINITY_ICONS = {
  truth: Sword,
  goodness: Shield,
  beauty: Heart,
  serenity: Crown,
  eternity: Infinity
};

// 철학적 색상 테마
const PHILOSOPHICAL_COLORS = {
  truth: "text-blue-600 bg-blue-50",
  goodness: "text-green-600 bg-green-50",
  beauty: "text-purple-600 bg-purple-50",
  serenity: "text-orange-600 bg-orange-50",
  eternity: "text-indigo-600 bg-indigo-50"
};

export default function PhilosophicalCopilotDashboard() {
  const [trinityScore, setTrinityScore] = useState<any>(null);
  const [systemHealth, setSystemHealth] = useState<any>(null);
  const [revalidateStatus, setRevalidateStatus] = useState<any>(null);
  const [currentWisdom, setCurrentWisdom] = useState(PHILOSOPHICAL_CONSTANTS.sunzi.wisdom);
  const { events: verdicts, connected: isConnected } = useVerdictStream(process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8010');

  // MCP 도구를 통한 건강 체크 (여포의 맥박 측정)
  useEffect(() => {
    const checkSystemHealth = async () => {
      try {
        const health = await apiClient.get('/api/health');
        setSystemHealth(health);
      } catch (error) {
        console.error('건강 체크 실패:', error);
      }
    };

    // Trinity Score 계산 (관우의 완벽한 검증)
    const calculateTrinityScore = async () => {
      try {
        const score = await apiClient.post('/api/trinity/calculate', {
          // 현재 시스템 상태 기반 계산
          architecture: 100, // 眞: 아키텍처 완성도
          security: 98,      // 善: 보안 수준
          ux: 98,           // 美: 사용자 경험
          automation: 100,   // 孝: 자동화 수준
          persistence: 99    // 永: 영속성
        });
        setTrinityScore(score);
      } catch (error) {
        console.error('Trinity Score 계산 실패:', error);
      }
    };

    // Revalidate 상태 확인
    const checkRevalidateStatus = async () => {
      try {
        const status = await apiClient.get('/api/revalidate/status');
        setRevalidateStatus(status);
      } catch (error) {
        console.error('Revalidate 상태 확인 실패:', error);
      }
    };

    checkSystemHealth();
    calculateTrinityScore();
    checkRevalidateStatus();

    // 실시간 업데이트 (SSE)
    const interval = setInterval(() => {
      checkSystemHealth();
      calculateTrinityScore();
      checkRevalidateStatus();
    }, 30000); // 30초마다

    return () => clearInterval(interval);
  }, []);

  // 철학적 인용 로테이션
  useEffect(() => {
    const wisdoms = [
      PHILOSOPHICAL_CONSTANTS.sunzi.wisdom,
      PHILOSOPHICAL_CONSTANTS.mencius.virtue,
      PHILOSOPHICAL_CONSTANTS.plato.harmony,
      PHILOSOPHICAL_CONSTANTS.sunzi.strategy,
      PHILOSOPHICAL_CONSTANTS.mencius.governance
    ];

    let index = 0;
    const interval = setInterval(() => {
      setCurrentWisdom(wisdoms[index % wisdoms.length]);
      index++;
    }, 10000); // 10초마다 변경

    return () => clearInterval(interval);
  }, []);

  const getTrinityIcon = (pillar: string) => {
    const IconComponent = TRINITY_ICONS[pillar as keyof typeof TRINITY_ICONS] || Sword;
    return IconComponent;
  };

  const getPillarColor = (pillar: string) => {
    return PHILOSOPHICAL_COLORS[pillar as keyof typeof PHILOSOPHICAL_COLORS] || PHILOSOPHICAL_COLORS.truth;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-blue-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* 왕국의 철학적 헤더 */}
        <Card className="border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2 text-2xl">
                  <Crown className="h-8 w-8 text-amber-600" />
                  AFO 왕국 철학적 Copilot Dashboard
                </CardTitle>
                <CardDescription className="text-lg mt-2">
                  眞善美孝永 철학의 실시간 조화 모니터링
                </CardDescription>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-600 mb-1">실시간 지혜</div>
                <div className="text-lg font-serif italic text-amber-800 max-w-xs">
                  "{currentWisdom}"
                </div>
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* 메인 대시보드 탭 */}
        <Tabs defaultValue="trinity" className="space-y-4">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="trinity">삼위일체 조화</TabsTrigger>
            <TabsTrigger value="health">왕국 건강</TabsTrigger>
            <TabsTrigger value="wisdom">철학적 통찰</TabsTrigger>
            <TabsTrigger value="actions">전략적 행동</TabsTrigger>
          </TabsList>

          {/* 삼위일체 조화 탭 */}
          <TabsContent value="trinity" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {trinityScore && Object.entries(trinityScore.pillars).map(([pillar, data]: [string, any]) => {
                const IconComponent = getTrinityIcon(pillar);
                const colorClass = getPillarColor(pillar);

                return (
                  <Card key={pillar} className={`${colorClass} border-2`}>
                    <CardHeader className="pb-2">
                      <CardTitle className="flex items-center gap-2 text-lg">
                        <IconComponent className="h-5 w-5" />
                        {pillar === 'truth' && '眞'}
                        {pillar === 'goodness' && '善'}
                        {pillar === 'beauty' && '美'}
                        {pillar === 'serenity' && '孝'}
                        {pillar === 'eternity' && '永'}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <Progress value={data.score} className="h-2" />
                        <div className="text-2xl font-bold">{data.score}%</div>
                        <Badge variant={data.score >= 95 ? "default" : "secondary"}>
                          {data.score >= 95 ? "완벽" : data.score >= 85 ? "우수" : "개선 필요"}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {/* 총합 Trinity Score */}
            <Card className="border-4 border-amber-300 bg-gradient-to-r from-amber-50 to-yellow-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-xl">
                  <Infinity className="h-6 w-6 text-amber-600" />
                  총합 Trinity Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-6xl font-bold text-amber-800 mb-4">
                    {trinityScore?.total || 0}%
                  </div>
                  <Progress value={trinityScore?.total || 0} className="h-4 mb-4" />
                  <p className="text-lg text-gray-700 font-serif">
                    "왕국의 철학적 조화가 {trinityScore?.total >= 95 ? '완벽한 균형을 이루고 있습니다' :
                      trinityScore?.total >= 85 ? '안정적인 발전을 이어가고 있습니다' :
                      '지혜의 균형을 맞추기 위해 노력하고 있습니다'}"
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* 왕국 건강 탭 */}
          <TabsContent value="health" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* 시스템 건강 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="h-5 w-5 text-green-600" />
                    왕국 건강 상태
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {systemHealth && (
                      <>
                        <div className="flex items-center justify-between">
                          <span>API 서버</span>
                          <Badge variant={systemHealth.api ? "default" : "destructive"}>
                            {systemHealth.api ? <CheckCircle className="h-4 w-4 mr-1" /> : <XCircle className="h-4 w-4 mr-1" />}
                            {systemHealth.api ? "정상" : "오류"}
                          </Badge>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>데이터베이스</span>
                          <Badge variant={systemHealth.database ? "default" : "destructive"}>
                            {systemHealth.database ? <CheckCircle className="h-4 w-4 mr-1" /> : <XCircle className="h-4 w-4 mr-1" />}
                            {systemHealth.database ? "정상" : "오류"}
                          </Badge>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>MCP 도구</span>
                          <Badge variant={systemHealth.mcp ? "default" : "destructive"}>
                            {systemHealth.mcp ? <CheckCircle className="h-4 w-4 mr-1" /> : <XCircle className="h-4 w-4 mr-1" />}
                            {systemHealth.mcp ? "정상" : "오류"}
                          </Badge>
                        </div>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Revalidate 상태 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BookOpen className="h-5 w-5 text-blue-600" />
                    Revalidate 상태
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {revalidateStatus && (
                      <>
                        <div className="flex items-center justify-between">
                          <span>마지막 실행</span>
                          <span className="text-sm text-gray-600">
                            {new Date(revalidateStatus.lastRun).toLocaleString()}
                          </span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>성공률</span>
                          <Badge variant={revalidateStatus.successRate >= 95 ? "default" : "secondary"}>
                            {revalidateStatus.successRate}%
                          </Badge>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>다음 실행</span>
                          <span className="text-sm text-gray-600">
                            {new Date(revalidateStatus.nextRun).toLocaleString()}
                          </span>
                        </div>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 철학적 통찰 탭 */}
          <TabsContent value="wisdom" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* 손자병법 */}
              <Card className="border-blue-200 bg-blue-50">
                <CardHeader>
                  <CardTitle className="text-blue-800">손자병법의 지혜</CardTitle>
                </CardHeader>
                <CardContent>
                  <blockquote className="text-blue-700 italic">
                    "{PHILOSOPHICAL_CONSTANTS.sunzi.wisdom}"
                  </blockquote>
                  <p className="text-sm text-blue-600 mt-2">
                    왕국의 전략적 판단에 적용
                  </p>
                </CardContent>
              </Card>

              {/* 맹자 */}
              <Card className="border-green-200 bg-green-50">
                <CardHeader>
                  <CardTitle className="text-green-800">맹자의 인의</CardTitle>
                </CardHeader>
                <CardContent>
                  <blockquote className="text-green-700 italic">
                    "{PHILOSOPHICAL_CONSTANTS.mencius.virtue}"
                  </blockquote>
                  <p className="text-sm text-green-600 mt-2">
                    윤리적 운영의 기반
                  </p>
                </CardContent>
              </Card>

              {/* 플라톤 */}
              <Card className="border-purple-200 bg-purple-50">
                <CardHeader>
                  <CardTitle className="text-purple-800">플라톤의 이데아</CardTitle>
                </CardHeader>
                <CardContent>
                  <blockquote className="text-purple-700 italic">
                    "{PHILOSOPHICAL_CONSTANTS.plato.harmony}"
                  </blockquote>
                  <p className="text-sm text-purple-600 mt-2">
                    이상적 시스템의 추구
                  </p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* 전략적 행동 탭 */}
          <TabsContent value="actions" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>제갈량의 전략적 조언</CardTitle>
                <CardDescription>
                  현재 상황에 기반한 지혜로운 행동 제안
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* 자동화된 전략적 조언들 */}
                <div className="space-y-2">
                  {trinityScore && trinityScore.total < 95 && (
                    <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <AlertTriangle className="h-5 w-5 text-yellow-600" />
                        <span className="font-medium text-yellow-800">균형 조정 필요</span>
                      </div>
                      <p className="text-yellow-700 mt-1">
                        왕국의 철학적 조화가 {100 - trinityScore.total}% 부족합니다.
                        각 기둥의 균형을 맞추는 전략을 실행하세요.
                      </p>
                    </div>
                  )}

                  {systemHealth && !systemHealth.api && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <XCircle className="h-5 w-5 text-red-600" />
                        <span className="font-medium text-red-800">긴급 복구 필요</span>
                      </div>
                      <p className="text-red-700 mt-1">
                        API 서버에 문제가 발생했습니다. 즉시 진단하고 복구 조치를 취하세요.
                      </p>
                    </div>
                  )}

                  {revalidateStatus && revalidateStatus.successRate < 95 && (
                    <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <AlertTriangle className="h-5 w-5 text-orange-600" />
                        <span className="font-medium text-orange-800">신뢰성 개선 필요</span>
                      </div>
                      <p className="text-orange-700 mt-1">
                        Revalidate 성공률이 {revalidateStatus.successRate}%입니다.
                        Vercel 설정을 검토하고 안정성을 높이세요.
                      </p>
                    </div>
                  )}

                  {trinityScore && trinityScore.total >= 95 && systemHealth && systemHealth.api && revalidateStatus && revalidateStatus.successRate >= 95 && (
                    <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-5 w-5 text-green-600" />
                        <span className="font-medium text-green-800">왕국의 번영</span>
                      </div>
                      <p className="text-green-700 mt-1">
                        모든 시스템이 완벽한 조화를 이루고 있습니다.
                        이 상태를 유지하며 새로운 지혜를 추구하세요.
                      </p>
                    </div>
                  )}
                </div>

                {/* 수동 액션 버튼들 */}
                <div className="flex flex-wrap gap-2 pt-4 border-t">
                  <Button variant="outline" size="sm">
                    <Sword className="h-4 w-4 mr-2" />
                    SSOT 검증 실행
                  </Button>
                  <Button variant="outline" size="sm">
                    <Shield className="h-4 w-4 mr-2" />
                    건강 체크
                  </Button>
                  <Button variant="outline" size="sm">
                    <BookOpen className="h-4 w-4 mr-2" />
                    Revalidate 수동 실행
                  </Button>
                  <Button variant="outline" size="sm">
                    <Crown className="h-4 w-4 mr-2" />
                    철학적 보고서 생성
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* 실시간 Verdict 스트림 (여포의 맥박 모니터링) */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-purple-600" />
              실시간 왕국 Verdict 스트림
            </CardTitle>
            <CardDescription>
              관우의 완벽한 검증 결과를 실시간으로 모니터링
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-32 w-full">
              {verdicts.length > 0 ? (
                <div className="space-y-2">
                  {verdicts.slice(-5).map((verdict, index) => {
                    const status = verdict.decision === 'AUTO_RUN' ? 'default' : 'secondary';
                    const message = `[${verdict.rule_id}] ${verdict.decision} (Trinity: ${verdict.trinity_score.toFixed(2)})`;
                    return (
                    <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                      <Badge variant={status as any}>
                        {verdict.decision}
                      </Badge>
                      <span className="text-sm">{message}</span>
                      <span className="text-xs text-gray-500 ml-auto">
                        {new Date(verdict.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  )})}
                </div>
              ) : (
                <div className="text-center text-gray-500 py-8">
                  {isConnected ? '실시간 Verdict를 기다리는 중...' : 'Verdict 스트림 연결 끊어짐'}
                </div>
              )}
            </ScrollArea>
          </CardContent>
        </Card>

      </div>
    </div>
  );
}