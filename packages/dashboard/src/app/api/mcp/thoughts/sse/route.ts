import { NextRequest } from "next/server";

/**
 * Matrix Stream SSE Endpoint
 *
 * Server-Sent Events for real-time LangGraph chancellor_graph observability.
 * Provides live stream of system "thoughts" to the AFO Pantheon dashboard.
 */
export async function GET(request: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      // Send initial connection message
      controller.enqueue(
        encoder.encode(
          `data: ${JSON.stringify({
            source: "SYSTEM",
            content: "🏰 Matrix Stream 연결됨. 왕국 사고 흐름 모니터링 중...",
            timestamp: new Date().toISOString(),
          })}\n\n`
        )
      );

      // Keep-alive ping every 30 seconds
      const keepAlive = setInterval(() => {
        try {
          controller.enqueue(encoder.encode(`data: keep-alive\n\n`));
        } catch {
          clearInterval(keepAlive);
        }
      }, 30000);

      // Simulated LangGraph events for now (후일 chancellor_graph 연동)
      // TODO: Connect to actual Redis pub/sub or LangGraph event stream
      const thoughts = [
        { source: "제갈량", content: "眞: 전략 분석 완료. 최적 경로 계산 중...", delay: 5000 },
        { source: "사마의", content: "善: 윤리 검증 통과. 리스크 수준 낮음.", delay: 10000 },
        { source: "주유", content: "美: UX 정렬 완료. 사용자 경험 최적화.", delay: 15000 },
        { source: "HISTORIAN", content: "永: 기록 보관 완료.", delay: 20000 },
      ];

      // Demo mode: Send sample thoughts
      const timers: NodeJS.Timeout[] = [];
      thoughts.forEach((thought, _i) => {
        const timer = setTimeout(() => {
          try {
            controller.enqueue(
              encoder.encode(
                `data: ${JSON.stringify({
                  source: thought.source,
                  content: thought.content,
                  timestamp: new Date().toISOString(),
                })}\n\n`
              )
            );
          } catch {
            // Connection closed
          }
        }, thought.delay);
        timers.push(timer);
      });

      // Cleanup on close
      request.signal.addEventListener("abort", () => {
        clearInterval(keepAlive);
        timers.forEach((t) => clearTimeout(t));
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
