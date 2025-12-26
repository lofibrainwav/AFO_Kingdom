import { NextResponse } from "next/server";

function getBaseUrl(): string {
  const v = process.env.AFO_API_BASE_URL;
  if (!v) throw new Error("AFO_API_BASE_URL is not set");
  return v.replace(/\/+$/, "");
}

export async function POST(req: Request) {
  const payload = await req.text();
  const upstream = new URL("/api/genui/generate", getBaseUrl());

  const res = await fetch(upstream.toString(), {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json" },
    body: payload,
    cache: "no-store",
  });

  const body = await res.text();
  return new NextResponse(body, {
    status: res.status,
    headers: {
      "content-type": res.headers.get("content-type") ?? "application/json; charset=utf-8",
    },
  });
}
