/**
 * SSE (Server-Sent Events) utilities for AFO Dashboard
 * Provides consistent URL construction and SSR-safe EventSource creation
 *
 * Client-only: Must only be imported in client components
 */
'use client';

/**
 * Build absolute SSE stream URL using current origin or environment URL
 * Handles SSR/proxy/tunnel environment differences
 * Supports both client and server environments with environment variable fallback
 */
export function buildSseUrl(path: string): string {
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path : `/${path}`;

  // Check for environment variable (Docker/container environment)
  const soulEngineUrl = process.env.SOUL_ENGINE_URL;
  if (soulEngineUrl) {
    // Use environment variable URL for container environments
    return `${soulEngineUrl}${cleanPath}`;
  }

  // Fallback to current origin for client/browser environments
  if (typeof window === 'undefined') {
    throw new Error('SSE URL must be built in the browser or with SOUL_ENGINE_URL env var. Use createEventSource() in useEffect.');
  }

  return `${window.location.origin}${cleanPath}`;
}

/**
 * Create EventSource with absolute URL (must be called in client context only)
 * Automatically handles origin/path resolution issues
 */
export function createEventSource(path: string, options?: EventSourceInit): EventSource {
  const url = buildSseUrl(path);
  return new EventSource(url, options);
}

/**
 * Common SSE endpoints used across the dashboard
 */
export const SSE_ENDPOINTS = {
  LOGS: '/api/logs/stream',
  MCP_THOUGHTS: '/api/mcp/thoughts',
  MCP_THOUGHTS_SSE: '/api/stream/mcp/thoughts',
  GROK_STREAM: '/api/grok/stream',
  LEARNING_LOG: '/api/learning-log/stream',
  DEBUGGING: '/api/debugging/stream',
  STREAM_MCP_THOUGHTS: '/api/stream/mcp/thoughts',
} as const;

/**
 * Pre-built URLs for common endpoints
 */
export const SSE_URLS = {
  LOGS: () => buildSseUrl(SSE_ENDPOINTS.LOGS),
  MCP_THOUGHTS: () => buildSseUrl(SSE_ENDPOINTS.MCP_THOUGHTS),
  MCP_THOUGHTS_SSE: () => buildSseUrl(SSE_ENDPOINTS.MCP_THOUGHTS_SSE),
  GROK_STREAM: () => buildSseUrl(SSE_ENDPOINTS.GROK_STREAM),
  LEARNING_LOG: () => buildSseUrl(SSE_ENDPOINTS.LEARNING_LOG),
  DEBUGGING: () => buildSseUrl(SSE_ENDPOINTS.DEBUGGING),
  STREAM_MCP_THOUGHTS: () => buildSseUrl(SSE_ENDPOINTS.STREAM_MCP_THOUGHTS),
} as const;
