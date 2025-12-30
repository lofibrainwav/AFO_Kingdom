import { NextResponse } from "next/server";

/**
 * SSE Health Status Endpoint
 * Returns mock SSE health data for the SSEHealthWidget
 * 
 * TODO: Connect to actual SSE metrics when available
 */
export async function GET() {
  // Basic SSE health check - if we can respond, SSE proxy should work
  const isLive = true;
  
  return NextResponse.json({
    status: isLive ? "connected" : "disconnected",
    connections: isLive ? 1 : 0,
    reconnects: 0,
    lastEvent: new Date().toISOString(),
    uptime: Date.now(),
  });
}

export async function POST(request: Request) {
  // Accept metrics reports from frontend
  try {
    const body = await request.json();
    console.log("[SSEHealth] Metrics received:", body);
    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json({ success: false }, { status: 400 });
  }
}
