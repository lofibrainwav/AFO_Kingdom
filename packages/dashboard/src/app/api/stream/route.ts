export const runtime = "nodejs";

function getEnv(name: string, fallback?: string): string {
  const v = process.env[name];
  if (v && v.trim().length > 0) return v;
  if (fallback) return fallback;
  throw new Error(`Missing env: ${name}`);
}

export async function GET(request: Request) {
  const backendBase = getEnv("BACKEND_BASE_URL", "http://127.0.0.1:8000");
  const ssePath = getEnv("CHANCELLOR_SSE_PATH", "/api/stream/mcp/thoughts");
  const target = new URL(ssePath, backendBase).toString();

  const ac = new AbortController();
  const abort = () => ac.abort();
  request.signal.addEventListener("abort", abort, { once: true });

  try {
    const upstream = await fetch(target, {
      signal: ac.signal,
      headers: {
        Accept: "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
      cache: "no-store",
    });

    if (!upstream.ok || !upstream.body) {
      return new Response(
        `Upstream SSE failed: ${upstream.status} ${upstream.statusText}`,
        { status: 502 }
      );
    }

    const reader = upstream.body.getReader();

    const stream = new ReadableStream<Uint8Array>({
      async start(controller) {
        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            controller.enqueue(value);
          }
        } catch {
          // client closed or upstream aborted
        } finally {
          controller.close();
          try {
            reader.releaseLock();
          } catch {}
        }
      },
      cancel() {
        ac.abort();
      },
    });

    return new Response(stream, {
      headers: {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache, no-transform",
        Connection: "keep-alive",
        "X-Accel-Buffering": "no",
      },
    });
  } finally {
    request.signal.removeEventListener("abort", abort);
  }
}
