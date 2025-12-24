import { NextResponse } from "next/server";
import { readFile } from "node:fs/promises";
import path from "node:path";

export async function GET() {
  const p = path.join(process.cwd(), "public", "ops", "revalidate_canary.json");
  try {
    const raw = await readFile(p, "utf8");
    return NextResponse.json(JSON.parse(raw));
  } catch {
    return NextResponse.json(
      { ok: false, error: "missing public/ops/revalidate_canary.json" },
      { status: 404 }
    );
  }
}