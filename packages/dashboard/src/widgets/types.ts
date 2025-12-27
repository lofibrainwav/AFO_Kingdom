export type WidgetCategory = "card" | "panel" | "chart" | "legacy";

export type WidgetVisibility = "public" | "internal" | "hidden";

export type WidgetMeta = {
  id: string;
  title: string;
  description?: string;
  category: WidgetCategory;
  visibility: WidgetVisibility;
  defaultEnabled: boolean;
  order: number;
  source?: "react" | "legacy-html" | "generated";
  tags?: string[];
  route?: string;
  component?: () => Promise<{ default: React.ComponentType<any> }>;
};

export type WidgetRegistryEntry = {
  meta: WidgetMeta;
};