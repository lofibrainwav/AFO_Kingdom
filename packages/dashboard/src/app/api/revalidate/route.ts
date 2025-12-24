import { NextRequest, NextResponse } from "next/server";
import { revalidatePath } from "next/cache";

export const runtime = "edge";

const HEADER = "x-revalidate-secret";
const KEY_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;

export async function POST(req: NextRequest) {
  if (req.nextUrl.searchParams.size > 0) {
    return NextResponse.json({ ok: false, error: "query_params_not_allowed" }, { status: 400 });
  }

  const expected = process.env.REVALIDATE_SECRET;
  const provided = req.headers.get(HEADER);

  if (!expected || !provided || provided !== expected) {
    return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });
  }

  let json: unknown;
  try {
    json = await req.json();
  } catch {
    return NextResponse.json({ ok: false, error: "invalid_json" }, { status: 400 });
  }

  const fragmentKey = (json as { fragmentKey?: unknown })?.fragmentKey;
  if (typeof fragmentKey !== "string" || !KEY_RE.test(fragmentKey)) {
    return NextResponse.json({ ok: false, error: "invalid_fragmentKey" }, { status: 400 });
  }

  const path = `/fragments/${fragmentKey}.html`;
  revalidatePath(path);

  return NextResponse.json({ ok: true, revalidated: [path] });
}

export async function GET() {
  return NextResponse.json({ ok: false, error: "method_not_allowed" }, { status: 405 });
}

