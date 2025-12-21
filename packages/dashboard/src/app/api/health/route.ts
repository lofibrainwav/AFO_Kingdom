/**
 * Health API Route - Proxy to backend /health endpoint
 */
import { NextResponse } from 'next/server';

import { API_BASE_URL } from '@/lib/constants';
// Server-side: use environment variable or default
const API_BASE = process.env.SOUL_ENGINE_URL || process.env.API_BASE_URL || API_BASE_URL;

export async function GET() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

    const response = await fetch(`${API_BASE}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return NextResponse.json(
        { error: `Backend health check failed: ${response.statusText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Health API Error:', error);
    return NextResponse.json(
      {
        error: 'Failed to connect to backend',
        status: 'error',
        health_percentage: 0,
        decision: 'TRY_AGAIN',
        decision_message: 'Backend connection failed. Please check if Docker services are running.',
        trinity: null,
      },
      { status: 503 }
    );
  }
}
