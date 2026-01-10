// AFO 왕국 시스템 상태 API Route
// 승상의 지피지기 철학 적용: 백엔드 상태를 대시보드에서 안전하게 확인

import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // 백엔드 API 직접 호출 (서버 사이드 - CORS 문제 해결)
    // 컨테이너 환경에서는 SOUL_ENGINE_URL 환경변수 사용
    const backendUrl = process.env.SOUL_ENGINE_URL
      ? `${process.env.SOUL_ENGINE_URL}/api/health/comprehensive`
      : 'http://127.0.0.1:8010/api/health/comprehensive';
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5초 타임아웃

    const response = await fetch(backendUrl, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'AFO-Dashboard/1.0',
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    const data = await response.json();

    // 프론트엔드용으로 최적화된 응답
    return NextResponse.json({
      status: 'healthy',
      backend_available: true,
      trinity_score: data.trinity_score,
      risk_score: data.risk_score ?? 0.05,
      breakdown: {
        truth: data.breakdown?.truth ?? data.metrics?.truth ?? 0.85,
        goodness: data.breakdown?.goodness ?? data.metrics?.goodness ?? 0.85,
        beauty: data.breakdown?.beauty ?? data.metrics?.beauty ?? 0.75,
        filial_serenity: data.breakdown?.filial_serenity ?? data.metrics?.filial_serenity ?? 0.80,
        eternity: data.breakdown?.eternity ?? data.metrics?.eternity ?? 0.80,
        iccls_gap: data.iccls_gap ?? 0.10,
        sentiment: data.sentiment ?? 0.70,
      },
      organs: data.organs,
      timestamp: new Date().toISOString(),
      dashboard_health: 'healthy'
    });

  } catch (error) {
    // 백엔드 연결 실패 시에도 대시보드는 작동
    return NextResponse.json({
      status: 'degraded',
      backend_available: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
      dashboard_health: 'healthy'
    }, { status: 503 });
  }
}