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

  // Trinity Score
  let trinityScore = {
    total: 100,
    truth: 1.0,
    goodness: 1.0,
    beauty: 1.0,
    serenity: 1.0,
    eternity: 1.0,
  };
  try {
    const trinityPath = path.join(repoRoot, "trinity_score.json");
    if (fs.existsSync(trinityPath)) {
      const data = JSON.parse(fs.readFileSync(trinityPath, "utf-8"));
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

  try {
    const backendUrl = process.env.SOUL_ENGINE_URL || "http://127.0.0.1:8010";
    const healthRes = await fetch(`${backendUrl}/health`);
    if (healthRes.ok) {
        const healthData = await healthRes.json();

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
          const bOrgans = healthData.organs || {};

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
    organs,
    trackedFiles: parseInt(trackedFiles.trim()) || 0,
    timeline,
    generatedAt: new Date().toISOString(),
  });
}