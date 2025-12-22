/**
 * 공통 타입 정의
 * AFO Kingdom Dashboard - Single Source of Truth for Types
 */

// API 응답 기본 타입
export interface ApiResponse<T = unknown> {
  data?: T;
  error?: string;
  detail?: string;
  status?: number;
}

// 로딩 상태
export type LoadingState = "idle" | "loading" | "success" | "error";

// 에러 상태
export interface ErrorState {
  message: string;
  code?: string;
  details?: unknown;
}

// Trinity Score 타입
export interface TrinityScore {
  truth: number;
  goodness: number;
  beauty: number;
  serenity: number;
  eternity: number;
  total?: number;
}

// Health Status 타입
export type HealthStatus = "excellent" | "good" | "warning" | "critical" | "loading";

// Phase 타입
export type Phase =
  | "Phase 0: Genesis"
  | "Phase 1: Awakening"
  | "Phase 2: Harmony"
  | "Phase 3: Expansion"
  | "Phase 4: Eternal"
  | "Maintenance"
  | "Features"
  | "Other";

// Git Commit 타입
export interface GitCommit {
  hash: string;
  date: string;
  author: string;
  message: string;
}

// Phase 통계 타입
export interface PhaseStats {
  count: number;
  percentage: number;
  start_date: string;
  end_date: string;
  commits: GitCommit[];
}

// Git Tree 분석 타입
export interface GitTreeAnalysis {
  total_commits: number;
  first_commit: GitCommit | null;
  latest_commit: GitCommit | null;
  phases: Record<string, PhaseStats>; // Phase 키는 동적으로 생성될 수 있음
  analyzed_at: string;
}

// API 클라이언트 옵션
export interface ApiClientOptions {
  timeout?: number;
  retries?: number;
  retryDelay?: number;
  headers?: Record<string, string>;
}

// 컴포넌트 Props 기본 타입
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

// 카드 컴포넌트 Props
export interface CardProps extends BaseComponentProps {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  gradient?: string;
  border?: string;
}

// 로딩 컴포넌트 Props
export interface LoadingProps extends BaseComponentProps {
  size?: "sm" | "md" | "lg";
  text?: string;
  fullScreen?: boolean;
}

// 에러 컴포넌트 Props
export interface ErrorProps extends BaseComponentProps {
  message: string;
  onRetry?: () => void;
  retryText?: string;
}
