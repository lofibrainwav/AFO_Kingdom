"use client";

import useSWR from "swr";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export default function ChancellorPage() {
  const { data, error, isLoading } = useSWR("/api/ops/revalidate-canary", fetcher, {
    refreshInterval: 5000,
  });

  return (
    <div className="p-6 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Revalidate Canary</CardTitle>
          <CardDescription>제갈량의 전략적 판단: Vercel Revalidate E2E 상태 모니터링</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          {isLoading && <div>📡 실시간 상태 확인 중...</div>}
          {error && <div>⚠️ 상태 확인 실패</div>}
          {data && (
            <div className="space-y-1 text-sm">
              <div>⏰ As-of (UTC): {data.as_of_utc ?? "-"}</div>
              <div>🎯 Fragment: {data.fragment_http ?? "-"} {data.fragment_http === 200 ? "✅" : "❌"}</div>
              <div>🔄 Revalidate: {data.revalidate_http ?? "-"} {data.revalidate_http === 200 ? "✅" : "❌"}</div>
              {data.fragment_http === 200 && data.revalidate_http === 200 && (
                <div className="text-green-600 font-medium">🏰 왕국의 문이 완벽하게 작동합니다</div>
              )}
              {(data.fragment_http !== 200 || data.revalidate_http !== 200) && (
                <div className="text-orange-600 font-medium">⚡ 전략적 검토가 필요합니다</div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* 철학적 맥락 */}
      <Card className="border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50">
        <CardHeader>
          <CardTitle className="text-amber-800">제갈량의 전략적 통찰</CardTitle>
        </CardHeader>
        <CardContent>
          <blockquote className="text-amber-700 italic text-lg">
            "지피지기면 백전불패 - 왕국의 문을 실시간으로 모니터링하라"
          </blockquote>
          <p className="text-amber-600 mt-2">
            이 Canary는 Vercel 배포 후 revalidate 기능이 정상 작동하는지 지속적으로 검증합니다.
            SSOT 원칙에 따라 모든 결과는 증거 파일로 기록되며, 대시보드에서 실시간으로 확인할 수 있습니다.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}