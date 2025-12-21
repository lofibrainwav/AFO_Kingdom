import { NextResponse } from 'next/server';
import { API_BASE_URL } from '@/lib/constants';

const API_BASE = process.env.SOUL_ENGINE_URL || process.env.API_BASE_URL || API_BASE_URL;

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/family/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store'
    });

    if (!res.ok) {
      return NextResponse.json(
        { error: `Backend Error: ${res.statusText}` },
        { status: res.status }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Family API Proxy Error:', error);
    return NextResponse.json(
      { error: 'Failed to connect to backend' },
      { status: 500 }
    );
  }
}
