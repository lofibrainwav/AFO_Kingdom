"use client";

import { useEffect, useState } from "react";

type Props = { fragmentKey: string };

export default function LiveEditPoller({ fragmentKey }: Props) {
  const [fragmentContent, setFragmentContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [source, setSource] = useState<"draft" | "publish" | null>(null);

  useEffect(() => {
    let stopped = false;

    const fetchFragment = async () => {
      try {
        // [Ticket 5-A Commit 2] Draft 우선, 없으면 Publish fallback
        const draftUrl = `/fragments/draft/${fragmentKey}.html`;
        const r1 = await fetch(draftUrl, { cache: "no-store" });

        if (r1.ok) {
          const content = await r1.text();
          if (stopped) return;
          setFragmentContent(content);
          setLastUpdate(new Date());
          setError(null);
          setSource("draft");
          setLoading(false);
          return;
        }

        // Draft 없으면 Publish로 fallback
        const publishUrl = `/fragments/${fragmentKey}.html`;
        const r2 = await fetch(publishUrl, { cache: "no-store" });

        if (r2.ok) {
          const content = await r2.text();
          if (stopped) return;
          setFragmentContent(content);
          setLastUpdate(new Date());
          setError(null);
          setSource("publish");
          setLoading(false);
          return;
        }

        // 둘 다 없으면 에러
        if (stopped) return;
        setError("Fragment not found (draft/publish)");
        setFragmentContent(null);
        setSource(null);
        setLoading(false);
      } catch (e: any) {
        if (stopped) return;
        setError(e?.message ?? "Unknown error");
        setFragmentContent(null);
        setSource(null);
        setLoading(false);
      }
    };

    // 초기 로드
    fetchFragment();
    
    // [Ticket 5-A Commit 2] Polling (2초 간격)
    const interval = window.setInterval(fetchFragment, 2000);

    return () => {
      stopped = true;
      window.clearInterval(interval);
    };
  }, [fragmentKey]);

  return (
    <div className="space-y-3">
      <div className="flex gap-3 items-center text-xs text-gray-400">
        <span className="px-2 py-1 rounded border border-gray-600">
          source: {source ?? "-"}
        </span>
        <span>poll: 2000ms</span>
        {lastUpdate && <span>updated: {lastUpdate.toLocaleTimeString()}</span>}
      </div>

      {loading && (
        <div className="text-center py-8 text-gray-400">Loading fragment...</div>
      )}

      {error && (
        <div className="p-4 bg-red-500/20 border border-red-500/30 rounded">
          <p className="text-red-400">Error: {error}</p>
        </div>
      )}

      {fragmentContent && (
        <div
          className="prose prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: fragmentContent }}
        />
      )}
    </div>
  );
}

