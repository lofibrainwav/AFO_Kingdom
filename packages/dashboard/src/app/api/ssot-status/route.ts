import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);

async function runCmd(cmd: string, cwd: string): Promise<string> {
  try {
    const { stdout } = await execAsync(cmd, { cwd });
    return stdout.trim();
  } catch (e) {
    return '';
  }
}

export async function GET() {
  const repoRoot = path.resolve(process.cwd(), '../..');

  // Get Trinity Score from trinity_score.json
  let trinity = { truth: 1.0, goodness: 1.0, beauty: 1.0, serenity: 1.0, eternity: 1.0 };
  try {
    const trinityPath = path.join(repoRoot, 'trinity_score.json');
    if (fs.existsSync(trinityPath)) {
      const data = JSON.parse(fs.readFileSync(trinityPath, 'utf-8'));
      trinity = data?.trinity?.scores || trinity;
    }
  } catch (e) {
    console.error('Failed to read trinity_score.json:', e);
  }

  // Calculate overall Trinity score (SSOT weights)
  const weights = { truth: 0.35, goodness: 0.35, beauty: 0.20, serenity: 0.08, eternity: 0.02 };
  const totalScore =
    trinity.truth * weights.truth +
    trinity.goodness * weights.goodness +
    trinity.beauty * weights.beauty +
    trinity.serenity * weights.serenity +
    trinity.eternity * weights.eternity;

  // Get git status for health check
  const gitStatus = await runCmd('git status --porcelain', repoRoot);
  const isClean = !gitStatus;

  // Determine health status based on Trinity score
  let healthStatus = 'excellent';
  if (totalScore < 0.7) healthStatus = 'degraded';
  else if (totalScore < 0.9) healthStatus = 'warning';

  // Calculate risk score (inverse of trinity quality)
  const riskScore = Math.max(0, 1 - totalScore);

  return NextResponse.json({
    status: 'ok',
    health: healthStatus,
    trinity: {
      truth: trinity.truth,
      goodness: trinity.goodness,
      beauty: trinity.beauty,
      serenity: trinity.serenity,
      eternity: trinity.eternity,
      total: Math.round(totalScore * 100) / 100,
    },
    risk: Math.round(riskScore * 100) / 100,
    services: {
      online: 4,
      total: 4,
    },
    git: {
      clean: isClean,
    },
    timestamp: new Date().toISOString(),
  });
}
