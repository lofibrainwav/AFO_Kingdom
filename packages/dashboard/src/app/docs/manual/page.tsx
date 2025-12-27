export default function ManualPage() {
  return (
    <main className="mx-auto w-full max-w-4xl space-y-6 p-6">
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold">AFO Field Manual</h1>
        <p className="text-sm text-muted-foreground">
          지휘 체계, 자동 실행 게이트, 증거 봉인을 포함한 "Unbreakable Law" 전문입니다.
        </p>
      </div>

      <div className="space-y-6">
        <section className="space-y-2">
          <h2 className="text-lg font-semibold">Ⅰ. 지휘 체계</h2>
          <ul className="list-disc space-y-1 pl-6 text-sm">
            <li>왕(형님): 비전·가치·헌법(SSOT) 하사</li>
            <li>사령관: 왕의 뜻을 실행 가능한 명세/명령으로 번역, 국법(예) 수호</li>
            <li>승상(오케스트레이터): 집행(코드/워크플로우) + 증거 봉인(artifacts/docs)</li>
          </ul>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-semibold">Ⅱ. 자동 실행 게이트</h2>
          <div className="rounded-md border p-3 text-sm">
            AUTO_RUN = (Trinity Score ≥ 90) AND (Risk Score ≤ 10)
          </div>
          <div className="text-sm text-muted-foreground">
            임계 미달 시 ASK(사령관 결재 요청)로 전환합니다.
          </div>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-semibold">Ⅲ. 운영 4단계 안전 파이프라인</h2>
          <ul className="list-disc space-y-1 pl-6 text-sm">
            <li>Backup</li>
            <li>Check</li>
            <li>Execute</li>
            <li>Verify</li>
          </ul>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-semibold">Ⅳ. 5대 게이트(LOCK)</h2>
          <div className="rounded-md border p-3 text-sm">
            MyPy(眞) → Security(善) → Ruff(美) → Pytest(孝) → SBOM/Artifacts(永)
          </div>
        </section>
      </div>
    </main>
  );
}