import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';
export const maxDuration = 300; // 5 minutes max for Vercel/Edge

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Call the backend with a long timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 min

    // Get backend URL from environment variable with fallback
    const backendUrl = process.env.SOUL_ENGINE_URL || 'http://localhost:8010';
    
    const response = await fetch(`${backendUrl}/chancellor/invoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return NextResponse.json(
        { error: `Backend error: ${response.statusText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Chancellor API error:', error);
    return NextResponse.json(
      { error: 'Failed to communicate with Chancellor backend' },
      { status: 500 }
    );
  }
}
