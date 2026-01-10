import { NextResponse } from "next/server";
import fs from "node:fs";
import path from "node:path";

function readLastJsonlLine(filePath: string) {
  const buf = fs.readFileSync(filePath, "utf8");
  const lines = buf.split("\n").filter(Boolean);
  if (lines.length === 0) return null;
  return JSON.parse(lines[lines.length - 1]);
}

export async function GET() {
  const artifactsDir =
    process.env.AFO_ARTIFACTS_DIR ??
    path.resolve(process.cwd(), "..", "..", "artifacts");

  const fp = path.join(artifactsDir, "ticket016_mlx_monitor_ssot.jsonl");

  if (!fs.existsSync(fp)) {
    return NextResponse.json(
      { ok: false, error: "SSOT file not found", path: fp },
      { status: 404 }
    );
  }

  const last = readLastJsonlLine(fp);
  return NextResponse.json({ ok: true, last, path: fp });
}
