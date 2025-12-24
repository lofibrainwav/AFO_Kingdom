import { NextRequest, NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

/**
 * 문서 파일을 읽어오는 API 라우트
 * 
 * @example
 * GET /api/docs/AGENTS.md
 * GET /api/docs/CLAUDE.md
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ filename: string }> }
) {
  try {
    const { filename } = await params;
    
    // 허용된 파일명만 처리 (보안)
    const allowedFiles = [
      "AGENTS.md",
      "CLAUDE.md",
      "CODEX.md",
      "CURSOR.md",
      "GROK.md",
    ];
    
    if (!allowedFiles.includes(filename)) {
      return NextResponse.json(
        { error: "File not allowed" },
        { status: 403 }
      );
    }
    
    // 프로젝트 루트에서 파일 읽기
    const filePath = join(process.cwd(), "..", "..", "..", filename);
    const content = await readFile(filePath, "utf-8");
    
    return NextResponse.json({ content }, {
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Failed to read file:", error);
    return NextResponse.json(
      { error: "Failed to read file", content: "" },
      { status: 500 }
    );
  }
}

