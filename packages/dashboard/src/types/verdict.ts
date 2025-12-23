/**
 * Chancellor Graph Verdict Event Types (TypeScript)
 *
 * SSOT type definitions for SSE verdict events consumed by the dashboard.
 * Ensures type safety between backend Python events and frontend TypeScript.
 */

export type Decision = "AUTO_RUN" | "ASK";

export interface VerdictFlags {
  dry_run: boolean;
  residual_doubt: boolean;
}

export interface VerdictExtra {
  query?: string;
  status?: string;
  reason?: string;
  [key: string]: unknown;
}

export interface VerdictEvent {
  trace_id: string;
  graph_node_id: string;
  step: number;
  decision: Decision;
  rule_id: string;
  trinity_score: number;
  risk_score: number;
  flags: VerdictFlags;
  timestamp: string;
  extra?: VerdictExtra;
  // 🏛️ SSOT 스탬프: weights_version + weights_hash (관찰 고정 모드)
  weights_version: string;
  weights_hash: string;
}

// SSE Message wrapper for real-time streaming
export interface SSEVerdictMessage {
  event: "verdict";
  data: VerdictEvent;
}

// Dashboard state for verdict tracking
export interface VerdictDashboardState {
  currentVerdict: VerdictEvent | null;
  verdictHistory: VerdictEvent[];
  isLoading: boolean;
  error: string | null;
}

// Rule ID constants (mirrored from Python)
export const RULE_IDS = {
  DRY_RUN_OVERRIDE: "R1_DRY_RUN_OVERRIDE",
  RESIDUAL_DOUBT: "R2_RESIDUAL_DOUBT",
  VETO_LOW_PILLARS: "R3_VETO_LOW_PILLARS",
  AUTORUN_THRESHOLD: "R4_AUTORUN_THRESHOLD",
  FALLBACK_ASK: "R5_FALLBACK_ASK",
} as const;

export type RuleId = typeof RULE_IDS[keyof typeof RULE_IDS];

// Rule descriptions for UI display
export const RULE_DESCRIPTIONS: Record<RuleId, string> = {
  [RULE_IDS.DRY_RUN_OVERRIDE]: "Global DRY_RUN flag overrides all decisions",
  [RULE_IDS.RESIDUAL_DOUBT]: "High uncertainty or incomplete pillar assessment",
  [RULE_IDS.VETO_LOW_PILLARS]: "Any pillar score below minimum threshold vetoes AUTO_RUN",
  [RULE_IDS.AUTORUN_THRESHOLD]: "Trinity Score >= 90 AND Risk Score <= 10 enables AUTO_RUN",
  [RULE_IDS.FALLBACK_ASK]: "Default fallback to ASK_COMMANDER for all other cases",
} as const;
