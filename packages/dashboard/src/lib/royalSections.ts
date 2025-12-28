/**
 * Royal Sections Data Contract (SSOT)
 *
 * PH20-02: Royal sections routing and data contract
 * Trinity Score: 眞 (Truth) - Single Source of Truth for royal sections
 */

export type RoyalSectionKey =
  | "home"
  | "chancellor"
  | "logs"
  | "metrics"
  | "kingdom-status";

export interface RoyalSection {
  /** Unique section key */
  key: RoyalSectionKey;
  /** Display title */
  title: string;
  /** Route path */
  href: string;
  /** Sort order (lower = first) */
  order: number;
  /** Visibility toggle */
  enabled: boolean;
  /** Optional icon name (lucide-react) */
  icon?: string;
  /** Optional description */
  description?: string;
}

/**
 * Royal Sections Registry (SSOT)
 *
 * All royal sections should be defined here.
 * Components should import from this file, not define their own lists.
 */
export const ROYAL_SECTIONS: readonly RoyalSection[] = [
  {
    key: "home",
    title: "Home",
    href: "/",
    order: 10,
    enabled: true,
    icon: "Home",
    description: "Kingdom Dashboard Home",
  },
  {
    key: "chancellor",
    title: "Chancellor",
    href: "/royal/chancellor",
    order: 20,
    enabled: true,
    icon: "Crown",
    description: "Chancellor AI Stream",
  },
  {
    key: "logs",
    title: "Logs",
    href: "/royal/logs",
    order: 30,
    enabled: true,
    icon: "ScrollText",
    description: "Real-time SSE Log Stream",
  },
  {
    key: "metrics",
    title: "Metrics",
    href: "/royal/metrics",
    order: 40,
    enabled: true,
    icon: "BarChart3",
    description: "System Metrics & Trinity Score",
  },
  {
    key: "kingdom-status",
    title: "Kingdom Status",
    href: "/royal/kingdom-status",
    order: 50,
    enabled: true,
    icon: "Shield",
    description: "Full Kingdom Health Status",
  },
] as const;

/**
 * Get enabled sections sorted by order
 */
export function getEnabledSections(): RoyalSection[] {
  return [...ROYAL_SECTIONS]
    .filter((section) => section.enabled)
    .sort((a, b) => a.order - b.order);
}

/**
 * Get section by key
 */
export function getSectionByKey(key: RoyalSectionKey): RoyalSection | undefined {
  return ROYAL_SECTIONS.find((section) => section.key === key);
}
