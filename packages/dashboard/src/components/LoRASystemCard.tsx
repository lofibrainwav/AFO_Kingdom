"use client";
import * as React from "react";

type Bundle = {
  as_of_utc: string;
  paths: Record<string, string | null>;
  ticket023_releases: Array<any>;
  latest: Record<string, any>;
};

export function LoRASystemCard() {
  const [data, setData] = React.useState<Bundle | null>(null);
  const [err, setErr] = React.useState<string | null>(null);

  React.useEffect(() => {
    fetch("/api/ssot/lora", { cache: "no-store" as any })
      .then(async (r) => {
        if (!r.ok) throw new Error(String(r.status));
        return (await r.json()) as Bundle;
      })
      .then(setData)
      .catch((e) => setErr(e?.message ?? "error"));
  }, []);

  if (err) return <div className="rounded-2xl border p-4">LoRA SSOT load failed: {err}</div>;
  if (!data) return <div className="rounded-2xl border p-4">Loading LoRA SSOT…</div>;

  const rel = data.latest?.ticket023;
  const releases = data.ticket023_releases ?? [];

  return (
    <div className="rounded-2xl border p-4 space-y-3">
      <div className="flex items-baseline justify-between">
        <div className="text-lg font-semibold">LoRA Ops</div>
        <div className="text-xs opacity-70">as_of {data.as_of_utc}</div>
      </div>

      <div className="text-sm space-y-1">
        <div><span className="opacity-70">Latest release:</span> {rel?.dir ?? "N/A"}</div>
        <div><span className="opacity-70">adapter_sha256 lines:</span> {rel?.adapter_sha256_lines ?? 0}</div>
        <div className="opacity-70">Paths: {Object.entries(data.paths).filter(([,v])=>v).map(([k,v])=>`${k}=${v}`).join(" · ") || "N/A"}</div>
      </div>

      <div className="text-sm">
        <div className="font-medium mb-2">Last 5 releases</div>
        <div className="space-y-2">
          {releases.map((r, i) => (
            <div key={i} className="rounded-xl border px-3 py-2">
              <div className="flex justify-between">
                <div className="font-medium">{r.dir}</div>
                <div className="text-xs opacity-70">{r.adapter_sha256_lines} lines</div>
              </div>
              <div className="text-xs opacity-70">
                {r.manifest_json?.git_sha ? `git ${r.manifest_json.git_sha}` : "git N/A"}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
