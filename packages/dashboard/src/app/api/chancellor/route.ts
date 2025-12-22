import { NextRequest, NextResponse } from "next/server";
import { API_BASE_URL } from "@/lib/constants";

export const dynamic = "force-dynamic";
export const maxDuration = 300;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Call the backend with a long timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 min

    // Get backend URL from environment variable with fallback
    const backendUrl = process.env.SOUL_ENGINE_URL || API_BASE_URL;

    const response = await fetch(`${backendUrl}/chancellor/invoke`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return NextResponse.json(
        { error: `Backend error: ${response.statusText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    // Log error (logger는 서버 사이드에서 사용 불가하므로 console.error 유지)
    console.error("Chancellor API error:", error);
    return NextResponse.json(
      { error: "Failed to communicate with Chancellor backend" },
      { status: 500 }
    );
  }
}
