import type { WidgetMeta, WidgetRegistryEntry } from "./types";

const entries = new Map<string, WidgetRegistryEntry>();

export function registerWidget(meta: WidgetMeta) {
  if (!meta.id) throw new Error("WidgetMeta.id is required");
  if (entries.has(meta.id)) throw new Error(`Duplicate widget id: ${meta.id}`);
  entries.set(meta.id, { meta });
}

export function getWidget(id: string) {
  return entries.get(id) || null;
}

export function listWidgets() {
  return Array.from(entries.values())
    .map((e) => e.meta)
    .sort((a, b) => a.order - b.order);
}

export function listEnabledWidgets() {
  return listWidgets().filter((w) => w.defaultEnabled && w.visibility !== "hidden");
}

/**
 * Bootstrap: keep this minimal.
 * Real widgets will be added as we migrate components.
 */
registerWidget({
  id: "legacy-kingdom-dashboard",
  title: "Legacy Kingdom Dashboard (HTML)",
  description: "Served from /public/legacy for reference and rollback.",
  category: "legacy",
  visibility: "internal",
  defaultEnabled: true,
  order: 10,
  source: "legacy-html",
  route: "/legacy/kingdom_dashboard.html",
  tags: ["legacy", "html", "reference"],
});

registerWidget({
  id: "docs-hub",
  title: "Docs Hub",
  description: "Registry-driven docs entry point.",
  category: "panel",
  visibility: "public",
  defaultEnabled: true,
  order: 20,
  source: "react",
  route: "/docs",
  tags: ["docs"],
});

// [Phase 2-2] Generated widgets 자동 등록 (안전 방식)
// 중복/불량 무시로 부팅 안전성 보장
try {
  const generated = require("@/generated/widgets.generated.json");

  type GeneratedPayload = {
    widgets?: Array<{
      id: string;
      title: string;
      preview?: string;
      category?: "card" | "panel" | "chart" | "legacy";
      visibility?: "public" | "internal" | "hidden";
      defaultEnabled?: boolean;
      order?: number;
      route?: string;
      tags?: string[];
    }>;
  };

  function registerGeneratedWidgets() {
    const payload = generated as unknown as GeneratedPayload;
    const list = payload.widgets || [];
    for (const w of list) {
      try {
        registerWidget({
          id: w.id,
          title: w.title,
          description: w.preview || w.title,
          category: w.category || "panel",
          visibility: w.visibility || "internal",
          defaultEnabled: w.defaultEnabled ?? true,
          order: w.order ?? 9999,
          source: "generated",
          route: w.route,
          tags: w.tags || ["generated"],
        });
      } catch {
        // duplicates or bad entries are ignored to keep boot safe
      }
    }
  }

  registerGeneratedWidgets();
} catch {
  // generated 파일이 없으면 무시 (개발 중일 수 있음)
}

