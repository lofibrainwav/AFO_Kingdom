import { NextResponse } from "next/server";
import { exec } from "child_process";
import { promisify } from "util";
import * as fs from "fs";
import * as path from "path";

const execAsync = promisify(exec);

async function runCmd(cmd: string, cwd: string): Promise<string> {
  try {
    const { stdout } = await execAsync(cmd, { cwd });
    return stdout.trim();
  } catch {
    return "";
  }
}

export async function GET() {
  const repoRoot = path.resolve(process.cwd(), "../..");

  // Git stats
  const totalCommits = await runCmd("git rev-list --count HEAD", repoRoot);
  const todayCommits = await runCmd("git log --oneline --since='midnight' | wc -l", repoRoot);
  const headSha = await runCmd("git rev-parse --short HEAD", repoRoot);
  const branch = await runCmd("git branch --show-current", repoRoot);
  const status = await runCmd("git status --porcelain", repoRoot);
  const synced = !status;

  // Trinity Score - will be populated from backend /health endpoint (real-time data)
  // Static file fallback removed to ensure truth (眞)
  let trinityScore = {
    total: 0,
    truth: 0,
    goodness: 0,
    beauty: 0,
    serenity: 0,
    eternity: 0,
  };

  // Tracked files
  const trackedFiles = await runCmd("git ls-tree -r HEAD --name-only | wc -l", repoRoot);

  // Recent commits for timeline
  const recentCommits = await runCmd("git log --oneline -10", repoRoot);
  const timeline = recentCommits.split("\n").map((line, i) => {
    const [hash, ...msgParts] = line.split(" ");
    return { num: i + 1, hash, msg: msgParts.join(" ").substring(0, 50) };
  });

  // Fetch Backend Health (Organs)
  let organs = [
    { name: "Heart", score: 0, metric: "Offline" },
    { name: "Brain", score: 0, metric: "Offline" },
    { name: "Lungs", score: 0, metric: "Offline" },
    { name: "Stomach", score: 0, metric: "Offline" },
    { name: "Eyes", score: 0, metric: "Offline" },
  ];

  let buildVersion = "unknown";
  let backendStatus = "unknown";

  try {
    const backendUrl = process.env.SOUL_ENGINE_URL || "http://127.0.0.1:8010";
    const healthRes = await fetch(`${backendUrl}/health`, { cache: "no-store", next: { revalidate: 0 } });
    if (healthRes.ok) {
        const healthData = await healthRes.json();
        buildVersion = healthData.build_version || "unknown";
        backendStatus = healthData.status || "unstable";

        // Extract REAL-TIME Trinity Score from backend (眞: Truth)
        const backendTrinity = healthData.trinity || {};
        trinityScore = {
          total: Math.round((backendTrinity.trinity_score || 0) * 100 * 10) / 10,
          truth: backendTrinity.truth || 0,
          goodness: backendTrinity.goodness || 0,
          beauty: backendTrinity.beauty || 0,
          serenity: backendTrinity.filial_serenity || 0,
          eternity: backendTrinity.eternity || 0,
        };

        // T21: Check for organs_v2 (11 organs) first
        const v2 = healthData.organs_v2 || null;

        if (v2) {
          // True 11-ORGANS system with v2
          const order = [
            "心_Redis",
            "肝_PostgreSQL",
            "肺_API_Server",
            "脾_Ollama",
            "腎_Qdrant",
            "眼_Dashboard",
            "神経_MCP",
            "耳_Observability",
            "口_Docs",
            "骨_CI",
            "免疫_Trinity_Gate",
          ] as const;

          organs = order.map((k) => {
            const o = v2[k];
            const score = typeof o?.score === "number" ? o.score : 0;
            const metric = typeof o?.output === "string" ? o.output : "Unknown";
            return { name: k, score, metric };
          });
        } else {
          // T20: Legacy 4→5 mapping (fallback for compatibility)
          let bOrgans = healthData.organs || {};
          
          // Bugfix: Backend returns list, frontend expects dict/map
          if (Array.isArray(bOrgans)) {
              bOrgans = bOrgans.reduce((acc: any, curr: any) => {
                  acc[curr.organ] = curr;
                  return acc;
              }, {});
          }

          organs = [
              {
                  name: "Heart", // Redis (Memory/Blood)
                  score: bOrgans["心_Redis"]?.status === "healthy" ? 98 : 40,
                  metric: bOrgans["心_Redis"]?.output || "Disconnected"
              },
              {
                  name: "Brain", // Ollama (Intelligence)
                  score: bOrgans["脾_Ollama"]?.status === "healthy" ? 95 : 20,
                  metric: bOrgans["脾_Ollama"]?.output || "Disconnected"
              },
              {
                  name: "Lungs", // API Server (Breath/Interface)
                  score: bOrgans["肺_API_Server"]?.status === "healthy" ? 100 : 0,
                  metric: bOrgans["肺_API_Server"]?.output || "No Signal"
              },
              {
                  name: "Stomach", // Postgres (Digestion/Storage)
                  score: bOrgans["肝_PostgreSQL"]?.status === "healthy" ? 99 : 30,
                  metric: bOrgans["肝_PostgreSQL"]?.output || "Indigestion"
              },
              {
                  name: "Eyes", // GenUI/Frontend (Vision)
                  score: 92, // Self-reported
                  metric: "Active: Port 3000"
              },
          ];
        }
    }
  } catch (e) {
    console.error("Backend fetch failed", e);
  }

  return NextResponse.json({
    git: {
      totalCommits: parseInt(totalCommits) || 0,
      todayCommits: parseInt(todayCommits.trim()) || 0,
      head: headSha,
      branch,
      synced,
    },
    trinity: trinityScore,
    // Frontend compatibility: RoyalLayout expects trinity_score (number)
    trinity_score: trinityScore.total,
    // Frontend compatibility: RoyalOpsCenter expects trinity_breakdown (flat object)
    trinity_breakdown: {
      truth: trinityScore.truth,
      goodness: trinityScore.goodness,
      beauty: trinityScore.beauty,
      filial_serenity: trinityScore.serenity,
      eternity: trinityScore.eternity,
    },
    organs,
    trackedFiles: parseInt(trackedFiles.trim()) || 0,
    timeline,
    generatedAt: new Date().toISOString(),
    buildVersion: buildVersion || "unknown",
    backendStatus: backendStatus || "unknown",
  });
}