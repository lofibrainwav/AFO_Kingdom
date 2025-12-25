import { NextRequest, NextResponse } from "next/server";

export const runtime = "edge";

interface VisualAgentAction {
  type: "click" | "type" | "scroll" | "wait" | "goto";
  bbox: { x: number; y: number; w: number; h: number };
  text?: string;
  confidence: number;
  why: string;
  safety: "safe" | "confirm" | "block";
}

interface VisualAgentResponse {
  goal: string;
  actions: VisualAgentAction[];
  stop: boolean;
  summary: string;
}

export async function POST(req: NextRequest) {
  try {
    const { screenshot, goal, maxSteps = 3 } = await req.json();

    if (!screenshot || !goal) {
      return NextResponse.json(
        { error: "screenshot and goal are required" },
        { status: 400 }
      );
    }

    // Trinity Gate 검증 (안전 우선)
    const trinityScore = 95; // 실제로는 Trinity Calculator에서 가져와야 함
    const riskScore = 5;     // 실제로는 Risk Calculator에서 가져와야 함

    if (trinityScore < 90 || riskScore > 10) {
      return NextResponse.json({
        error: "Trinity Gate blocked: insufficient safety score",
        trinityScore,
        riskScore,
        status: "blocked"
      }, { status: 403 });
    }

    // LLM Router로 Visual Agent 호출 (Ollama Qwen3-VL 우선)
    const response = await callVisualAgentLLM(screenshot, goal, maxSteps);

    return NextResponse.json(response);
  } catch (error) {
    console.error("Visual Agent API error:", error);
    return NextResponse.json(
      { error: "Visual Agent processing failed" },
      { status: 500 }
    );
  }
}

async function callVisualAgentLLM(
  screenshot: string,
  goal: string,
  maxSteps: number
): Promise<VisualAgentResponse> {
  // 실제로는 LLM Router를 통해 Ollama Qwen3-VL 호출
  // 여기서는 모의 응답

  const mockResponse: VisualAgentResponse = {
    goal,
    actions: [
      {
        type: "click",
        bbox: { x: 100, y: 200, w: 150, h: 50 },
        confidence: 0.95,
        why: "Login button detected with high confidence",
        safety: "safe"
      }
    ],
    stop: false,
    summary: "Identified login button for user authentication"
  };

  return mockResponse;
}

export async function GET() {
  return NextResponse.json({
    message: "Visual Agent API - POST screenshot and goal to analyze",
    status: "ready"
  });
}