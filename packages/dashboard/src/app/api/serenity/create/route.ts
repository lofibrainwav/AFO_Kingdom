import { NextRequest, NextResponse } from 'next/server';
import { API_BASE_URL } from '@/lib/constants';

export const dynamic = 'force-dynamic';
export const maxDuration = 300; // 5 minutes max for Vercel/Edge

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Call the backend with a long timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 min

    // Get backend URL from environment variable with fallback
    const backendUrl = process.env.SOUL_ENGINE_URL || API_BASE_URL;

    const response = await fetch(`${backendUrl}/api/serenity/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        {
          error: `Backend error: ${response.statusText}`,
          detail: errorText.substring(0, 200)
        },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Serenity API error:', error);

    // Check if it's a connection error
    if (error instanceof Error && error.name === 'AbortError') {
      return NextResponse.json(
        { error: 'Request timeout: Backend took too long to respond' },
        { status: 504 }
      );
    }

    if (error instanceof TypeError && error.message.includes('fetch')) {
      return NextResponse.json(
        {
          error: 'Failed to connect to backend',
          detail: 'API 서버가 실행 중이지 않습니다. 포트 8010에서 서버를 시작해주세요.'
        },
        { status: 503 }
      );
    }

    return NextResponse.json(
      {
        error: 'Failed to communicate with Serenity backend',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
