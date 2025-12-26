// AFO Skills Manager Widget Types
// 眞善美孝 철학을 반영한 타입 시스템

export interface PhilosophyScore {
  truth: number;      // 眞 (Truth) - 기술적 확실성
  goodness: number;   // 善 (Goodness) - 윤리적 우선순위
  beauty: number;     // 美 (Beauty) - 명확한 스토리텔링
  serenity: number;   // 孝 (Serenity) - 마찰 없는 운영
}

export interface AFOSkill {
  skill_id: string;
  name: string;
  description: string;
  category: SkillCategory;
  version: string;
  philosophy_scores: PhilosophyScore;
  status: SkillStatus;
  capabilities: string[];
  execution_mode: ExecutionMode;
  tags?: string[];
}

export type SkillCategory =
  | "strategic_command"
  | "rag_systems"
  | "workflow_automation"
  | "health_monitoring"
  | "memory_management"
  | "browser_automation"
  | "analysis_evaluation"
  | "integration"
  | "metacognition";

export type SkillStatus = "active" | "deprecated" | "experimental" | "maintenance";

export type ExecutionMode = "sync" | "async" | "streaming" | "background";

export interface SkillExecutionRequest {
  skillId: string;
  parameters?: Record<string, any>;
  dryRun?: boolean;
}

export interface SkillExecutionResult {
  skill_id: string;
  status: 'dry_run_success' | 'executing' | 'completed' | 'failed';
  result?: any;
  error?: string;
  parameters?: Record<string, any>;
  dry_run?: boolean;
}

export interface SkillsApiResponse {
  skills: AFOSkill[];
  total: number;
  categories: string[];
}

export interface SkillFilterOptions {
  category?: SkillCategory;
  search?: string;
  minPhilosophyAvg?: number;
  executionMode?: ExecutionMode;
  status?: SkillStatus;
}

// UI 컴포넌트용 타입
export interface SkillCardProps {
  skill: AFOSkill;
  onExecute: (skillId: string, dryRun?: boolean) => void;
  isExecuting?: boolean;
  executionResult?: SkillExecutionResult;
}

export interface SkillsRegistryProps {
  filters?: SkillFilterOptions;
  autoRefresh?: boolean;
  refreshInterval?: number;
  onSkillExecute?: (result: SkillExecutionResult) => void;
}

export interface SkillExecutionState {
  [skillId: string]: {
    isExecuting: boolean;
    result?: SkillExecutionResult;
    lastExecuted?: Date;
  };
}

// Trinity Score 계산 헬퍼
export const calculatePhilosophyAverage = (scores: PhilosophyScore): number => {
  return (scores.truth + scores.goodness + scores.beauty + scores.serenity) / 4;
};

export const getPhilosophyGrade = (score: number): 'S' | 'A' | 'B' | 'C' | 'D' => {
  if (score >= 95) return 'S';
  if (score >= 85) return 'A';
  if (score >= 75) return 'B';
  if (score >= 65) return 'C';
  return 'D';
};

export const getTrinityScore = (scores: PhilosophyScore): number => {
  // AFO Trinity 가중치 적용 (眞35% 善35% 美20% 孝8% 永2%)
  const weights = { truth: 0.35, goodness: 0.35, beauty: 0.20, serenity: 0.08 };
  return (
    scores.truth * weights.truth +
    scores.goodness * weights.goodness +
    scores.beauty * weights.beauty +
    scores.serenity * weights.serenity
  );
};