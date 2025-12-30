/**
 * SSE Log Stream API Route Handler
 * 
 * This route acts as a proxy for the backend SSE stream,
 * handling the long-lived connection properly unlike Next.js rewrites.
 * 
 * SSOT Path: /api/logs/stream
 */
import { NextRequest } from 'next/server';

// Disable static generation for SSE
export const dynamic = 'force-dynamic';

// Backend URL - environment-aware
const SOUL_ENGINE_URL = process.env.SOUL_ENGINE_URL || 'http://localhost:8010';

export async function GET(request: NextRequest) {
  try {
    // Fetch the SSE stream from the backend
    const response = await fetch(`${SOUL_ENGINE_URL}/api/logs/stream`, {
      headers: {
        'Accept': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
      // Critical: Keep the connection open for SSE
      // @ts-expect-error - Next.js extended fetch options
      signal: request.signal,
    });

    if (!response.ok) {
      return new Response(
        JSON.stringify({ error: `Backend returned ${response.status}` }),
        { status: response.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    if (!response.body) {
      return new Response(
        JSON.stringify({ error: 'No response body from backend' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Stream the SSE response to the client
    return new Response(response.body, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache, no-transform',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
      },
    });
  } catch (error) {
    console.error('[SSE Proxy] Error:', error);
    return new Response(
      JSON.stringify({ error: 'SSE proxy error', details: String(error) }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
