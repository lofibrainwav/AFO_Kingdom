import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function RoyalCommandHierarchyCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Royal Command Hierarchy</CardTitle>
        <CardDescription>왕(형님) → 사령관 → 승상(오케스트레이터)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <div className="text-xl">👑</div>
            <div className="space-y-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium">왕 (형님)</span>
                <Badge variant="secondary">Vision & Constitution</Badge>
              </div>
              <p className="text-sm text-muted-foreground">비전·가치·헌법(SSOT)을 하사합니다.</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="text-xl">⚔️</div>
            <div className="space-y-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium">사령관</span>
                <Badge variant="secondary">Translate & Enforce</Badge>
              </div>
              <p className="text-sm text-muted-foreground">왕의 뜻을 "실행 가능한 명세/명령"으로 번역하고, 국법(예/기강)을 수호합니다.</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="text-xl">📜</div>
            <div className="space-y-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium">승상 (오케스트레이터)</span>
                <Badge variant="secondary">Execute & Seal</Badge>
              </div>
              <p className="text-sm text-muted-foreground">명세를 코드/워크플로우로 집행하고, 증거(artifacts/docs)를 봉인해 영속성을 보장합니다.</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}