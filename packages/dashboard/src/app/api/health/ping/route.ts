// AFO Dashboard Lightweight Health Check
// Trinity Score: 眞 (Truth) - Accurate container readiness

import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    message: 'Dashboard is alive (pong)'
  });
}
