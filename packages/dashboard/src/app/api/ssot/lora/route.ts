import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import path from "path";

async function findRepoRoot(): Promise<string> {
  let cur = process.cwd();
  for (let i = 0; i < 8; i++) {
    const p = path.join(cur, "artifacts");
    try {
      await readFile(path.join(p, "ticket024_dashboard_bundle.json"), "utf-8");
      return cur;
    } catch {}
    const parent = path.dirname(cur);
    if (parent === cur) break;
    cur = parent;
  }
  return process.cwd();
}

export async function GET() {
  const root = await findRepoRoot();
  const p = path.join(root, "artifacts", "ticket024_dashboard_bundle.json");
  const raw = await readFile(p, "utf-8");
  return NextResponse.json(JSON.parse(raw), { headers: { "Cache-Control": "no-store" } });
}
