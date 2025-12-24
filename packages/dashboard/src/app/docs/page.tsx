import Link from "next/link";
import { listWidgets } from "@/widgets/registry";

export default function DocsHome() {
  const widgets = listWidgets().filter((w) => w.route?.startsWith("/docs"));

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">📚 Docs</h1>

      <div className="flex gap-3">
        <Link className="underline" href="/legacy/kingdom_dashboard.html">
          Legacy (HTML)
        </Link>
      </div>

      <div className="mt-6">
        <h2 className="text-lg font-medium mb-4">Generated Widgets ({widgets.length})</h2>
        <ul className="space-y-3">
          {widgets.map((w) => (
            <li key={w.id} className="rounded-xl border p-4">
              <Link className="text-lg font-medium underline" href={w.route!}>
                {w.title}
              </Link>
              {w.description ? (
                <div className="text-sm opacity-80 mt-1">{w.description}</div>
              ) : null}
              <div className="text-xs opacity-60 mt-2">
                ID: {w.id} | Source: {w.source || "unknown"}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
