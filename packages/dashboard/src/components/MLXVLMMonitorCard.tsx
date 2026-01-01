export default async function MLXVLMMonitorCard() {
  const res = await fetch("http://localhost:3000/api/mlx/vlm/latest", { cache: "no-store" });
  const data = await res.json();

  if (!data?.ok) {
    return (
      <div className="rounded-2xl border p-4">
        <div className="text-lg font-semibold">MLX VLM Monitor</div>
        <div className="mt-2 text-sm opacity-80">No SSOT data.</div>
        <pre className="mt-3 text-xs opacity-80">{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  }

  const last = data.last ?? {};
  return (
    <div className="rounded-2xl border p-4">
      <div className="text-lg font-semibold">MLX VLM Monitor</div>
      <div className="mt-2 text-sm opacity-80">Last run (JSONL tail)</div>

      <div className="mt-3 grid gap-2 text-sm">
        <div><span className="opacity-70">ts:</span> {String(last.ts ?? "")}</div>
        <div><span className="opacity-70">mode:</span> {String(last.mode ?? "")}</div>
        <div><span className="opacity-70">ok:</span> {String(last.ok ?? "")}</div>
        <div><span className="opacity-70">secs:</span> {String(last.secs ?? "")}</div>
        <div><span className="opacity-70">max_rss_bytes:</span> {last.max_rss_bytes ? `${(last.max_rss_bytes / 1024 / 1024 / 1024).toFixed(3)} GiB` : ""}</div>
        <div><span className="opacity-70">cutline_bytes:</span> {last.cutline_bytes ? `${(last.cutline_bytes / 1024 / 1024 / 1024).toFixed(3)} GiB` : ""}</div>
        <div><span className="opacity-70">notes:</span> {String(last.notes ?? "")}</div>
      </div>

      <pre className="mt-4 text-xs opacity-80">{JSON.stringify(last, null, 2)}</pre>
    </div>
  );
}
