import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function FieldManualLawCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Field Manual: Unbreakable Law</CardTitle>
        <CardDescription>자동 실행과 안전을 동시에 보장하는 국법</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline">Backup → Check → Execute → Verify</Badge>
          <Badge variant="outline">Evidence-First</Badge>
          <Badge variant="outline">Ask-Before-Act</Badge>
        </div>

        <div className="space-y-2">
          <div className="text-sm font-medium">AUTO_RUN 조건</div>
          <div className="rounded-md border p-3 text-sm">
            Trinity Score ≥ 90 <span className="text-muted-foreground">AND</span> Risk Score ≤ 10
          </div>
        </div>

        <div className="space-y-2">
          <div className="text-sm font-medium">5대 게이트(LOCK)</div>
          <div className="rounded-md border p-3 text-sm">
            MyPy(眞) → Security(善) → Ruff(美) → Pytest(孝) → SBOM/Artifacts(永)
          </div>
        </div>

        <div className="text-sm text-muted-foreground">
          전체 국법 전문은 <Link className="underline" href="/docs/manual">/docs/manual</Link> 에서 확인하실 수 있습니다.
        </div>
      </CardContent>
    </Card>
  );
}