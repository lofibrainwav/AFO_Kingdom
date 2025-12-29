/**
 * SSE (Server-Sent Events) utilities for AFO Dashboard
 * Provides consistent URL construction and SSR-safe EventSource creation
 */

/**
 * Build absolute SSE stream URL using current origin
 * Handles SSR/proxy/tunnel environment differences
 */
export function buildSseUrl(path: string): string {
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path : `/${path}`;

  // Build absolute URL using current origin (SSR-safe)
  if (typeof window !== 'undefined') {
    return `${window.location.origin}${cleanPath}`;
  }

  // Fallback for SSR (should not happen in client components)
  console.warn('[SSE] buildSseUrl called in SSR context, using fallback');
  return cleanPath;
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
  MCP_THOUGHTS_SSE: '/api/mcp/thoughts/sse',
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
