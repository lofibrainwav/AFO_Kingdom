/**
 * API Bridge to AFO Backend
 * Dynamic Trinity Score & Health Integration
 */

import { logError } from './logger';

export interface ChancellorResponse {
  response: string;
  speaker: string;
  full_history: string[];
}

export interface TrinityStatus {
  truth: number;
  goodness: number;
  beauty: number;
  filial_serenity: number;
  eternity: number;
  trinity_score: number;
  balance_status: string;
  weights: {
    truth: number;
    goodness: number;
    beauty: number;
    filial_serenity: number;
    eternity: number;
  };
}

export interface HealthResponse {
  status: string;
  health_percentage: number;
  decision: string;
  decision_message: string;
  trinity: TrinityStatus;
  issues: string[] | null;
  suggestions: string[] | null;
  organs: Record<string, { status: string; output: string }>;
  method: string;
  timestamp: string;
}

/**
 * Fetch real-time health status from backend
 */
export async function fetchHealthStatus(): Promise<HealthResponse> {
  const response = await fetch('/api/health', {
    method: 'GET',
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`Health API Error: ${response.statusText}`);
  }

  return await response.json();
}

/**
 * Invoke Chancellor with dynamic Trinity Score
 */
export async function invokeChancellor(
  query: string,
  trinityScore?: number,
  riskScore?: number
): Promise<ChancellorResponse> {
  // LLM calls can be slow (4 strategists + synthesis), so we need a long timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes

  try {
    // Use dedicated API route instead of proxy for better timeout handling
    const response = await fetch('/api/chancellor', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        trinity_score: trinityScore ?? 0.9, // Use passed value or default
        risk_score: riskScore ?? 0.1,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Chancellor Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    logError('Failed to invoke Chancellor', { error: error instanceof Error ? error.message : 'Unknown error' });
    throw error;
  }
}

export interface FamilyMember {
  name: string;
  role: string;
  pillars: {
      truth: number;
      goodness: number;
      beauty: number;
      serenity: number;
      forever: number;
  };
  message: string;
  status: 'ACTIVE' | 'IDLE' | 'WORKING' | 'AUDITING';
  updated_at: string;
}

export interface FamilyHubResponse {
  members: Record<string, FamilyMember>;
  total_members: number;
  average_trinity_score: number;
}

/**
 * Fetch Family Hub Status (Julie, etc.)
 */
export async function fetchFamilyStatus(): Promise<FamilyHubResponse> {
  const response = await fetch('/api/family', {
    method: 'GET',
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`Family API Error: ${response.statusText}`);
  }

  return await response.json();
}
