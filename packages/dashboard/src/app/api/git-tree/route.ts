import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export const dynamic = 'force-dynamic';
export const maxDuration = 30;

interface Commit {
  hash: string;
  date: string;
  author: string;
  message: string;
}

interface PhaseStats {
  count: number;
  percentage: number;
  start_date: string;
  end_date: string;
  commits: Commit[];
}

interface GitTreeAnalysis {
  total_commits: number;
  first_commit: Commit | null;
  latest_commit: Commit | null;
  phases: Record<string, PhaseStats>;
  analyzed_at: string;
}

function detectPhase(message: string): string {
  const msg = message.toLowerCase();
  
  if (['genesis', 'initial', 'setup', 'first', '승상', 'cursor'].some(kw => msg.includes(kw))) {
    return 'Phase 0: Genesis';
  }
  if (['awakening', 'phase 1', 'trinity', 'philosophy', 'v1.0'].some(kw => msg.includes(kw))) {
    return 'Phase 1: Awakening';
  }
  if (['harmony', 'phase 2', 'dashboard', 'cpa', 'family hub', 'v2.0'].some(kw => msg.includes(kw))) {
    return 'Phase 2: Harmony';
  }
  if (['expansion', 'phase 3', 'self-expanding', 'genui', 'serenity', 'v2.5'].some(kw => msg.includes(kw))) {
    return 'Phase 3: Expansion';
  }
  if (['v100', 'v100.0', 'eternal', 'perfect', 'ascended', 'digital robot'].some(kw => msg.includes(kw))) {
    return 'Phase 4: Eternal';
  }
  if (['fix', 'bug', 'chore', 'refactor', 'mypy', 'ruff', 'type'].some(kw => msg.includes(kw))) {
    return 'Maintenance';
  }
  if (['feat', 'add', 'implement', 'create'].some(kw => msg.includes(kw))) {
    return 'Features';
  }
  return 'Other';
}

export async function GET() {
  try {
    // Git 트리 분석 실행
    // 프로젝트 루트로 이동 (packages/dashboard에서 상위로)
    const repoRoot = process.cwd().includes('packages/dashboard')
      ? process.cwd().replace('/packages/dashboard', '')
      : process.cwd();
    
    const { stdout } = await execAsync(
      'git log --reverse --format="%h|%ad|%an|%s" --date=short',
      { cwd: repoRoot, timeout: 10000, shell: '/bin/bash' }
    );

    const commits: Commit[] = [];
    for (const line of stdout.trim().split('\n')) {
      if (line) {
        const parts = line.split('|', 4);
        if (parts.length === 4) {
          commits.push({
            hash: parts[0],
            date: parts[1],
            author: parts[2],
            message: parts[3],
          });
        }
      }
    }

    // Phase별로 분류
    const phases: Record<string, Commit[]> = {};
    for (const commit of commits) {
      const phase = detectPhase(commit.message);
      if (!phases[phase]) {
        phases[phase] = [];
      }
      phases[phase].push(commit);
    }

    // 통계 계산
    const phaseStats: Record<string, PhaseStats> = {};
    for (const [phaseName, phaseCommits] of Object.entries(phases)) {
      if (phaseCommits.length > 0) {
        phaseStats[phaseName] = {
          count: phaseCommits.length,
          percentage: (phaseCommits.length / commits.length) * 100,
          start_date: phaseCommits[0].date,
          end_date: phaseCommits[phaseCommits.length - 1].date,
          commits: phaseCommits.slice(0, 20), // 최대 20개만
        };
      }
    }

    const analysis: GitTreeAnalysis = {
      total_commits: commits.length,
      first_commit: commits[0] || null,
      latest_commit: commits[commits.length - 1] || null,
      phases: phaseStats,
      analyzed_at: new Date().toISOString(),
    };

    return NextResponse.json(analysis);
  } catch (error) {
    console.error('Git tree analysis error:', error);
    return NextResponse.json(
      {
        error: 'Failed to analyze git tree',
        detail: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

