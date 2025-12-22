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
  } catch {
    return '';
  }
}

export async function GET() {
  const repoRoot = path.resolve(process.cwd(), '../..');

  // Git stats
  const totalCommits = await runCmd('git rev-list --count HEAD', repoRoot);
  const todayCommits = await runCmd("git log --oneline --since='midnight' | wc -l", repoRoot);
  const headSha = await runCmd('git rev-parse --short HEAD', repoRoot);
  const branch = await runCmd('git branch --show-current', repoRoot);
  const status = await runCmd('git status --porcelain', repoRoot);
  const synced = !status;

  // Trinity Score
  let trinityScore = { total: 100, truth: 1.0, goodness: 1.0, beauty: 1.0, serenity: 1.0, eternity: 1.0 };
  try {
    const trinityPath = path.join(repoRoot, 'trinity_score.json');
    if (fs.existsSync(trinityPath)) {
      const data = JSON.parse(fs.readFileSync(trinityPath, 'utf-8'));
      const scores = data?.trinity?.scores || {};
      trinityScore = {
        total: Math.round((data?.trinity?.total || 1) * 100 * 10) / 10,
        truth: scores.truth || 1.0,
        goodness: scores.goodness || 1.0,
        beauty: scores.beauty || 1.0,
        serenity: scores.serenity || 1.0,
        eternity: scores.eternity || 1.0,
      };
    }
  } catch {
    // Failed to read trinity score, using defaults
  }

  // Tracked files
  const trackedFiles = await runCmd('git ls-tree -r HEAD --name-only | wc -l', repoRoot);

  // Recent commits for timeline
  const recentCommits = await runCmd('git log --oneline -10', repoRoot);
  const timeline = recentCommits.split('\n').map((line, i) => {
    const [hash, ...msgParts] = line.split(' ');
    return { num: i + 1, hash, msg: msgParts.join(' ').substring(0, 50) };
  });

  return NextResponse.json({
    git: {
      totalCommits: parseInt(totalCommits) || 0,
      todayCommits: parseInt(todayCommits.trim()) || 0,
      head: headSha,
      branch,
      synced,
    },
    trinity: trinityScore,
    trackedFiles: parseInt(trackedFiles.trim()) || 0,
    timeline,
    generatedAt: new Date().toISOString(),
  });
}
