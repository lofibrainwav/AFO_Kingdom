/**
 * Mermaid 다이어그램 파싱 유틸리티
 */

export interface MermaidConfig {
  code: string;
  title?: string;
  type?: "graph" | "flowchart" | "sequenceDiagram" | "classDiagram" | "stateDiagram";
}

/**
 * HTML에서 Mermaid 다이어그램 코드 추출
 * 
 * @param html - HTML 문자열
 * @returns Mermaid 다이어그램 배열
 */
export function extractMermaidFromHTML(html: string): MermaidConfig[] {
  const mermaidRegex = /<div[^>]*class=["']mermaid["'][^>]*>([\s\S]*?)<\/div>/gi;
  const results: MermaidConfig[] = [];
  let match;

  while ((match = mermaidRegex.exec(html)) !== null) {
    const code = match[1].trim();
    if (code) {
      // 다이어그램 타입 추출
      const type = detectMermaidType(code);
      results.push({ code, type });
    }
  }

  return results;
}

/**
 * Mermaid 코드에서 다이어그램 타입 감지
 */
function detectMermaidType(code: string): MermaidConfig["type"] {
  if (code.startsWith("graph") || code.startsWith("flowchart")) {
    return "flowchart";
  }
  if (code.startsWith("sequenceDiagram")) {
    return "sequenceDiagram";
  }
  if (code.startsWith("classDiagram")) {
    return "classDiagram";
  }
  if (code.startsWith("stateDiagram")) {
    return "stateDiagram";
  }
  return "graph";
}

/**
 * Mermaid 코드 유효성 검사
 */
export function validateMermaidCode(code: string): { valid: boolean; error?: string } {
  if (!code || code.trim().length === 0) {
    return { valid: false, error: "Mermaid 코드가 비어있습니다." };
  }

  // 기본적인 문법 검사
  const validStarters = [
    "graph",
    "flowchart",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
    "requirement",
    "gitgraph",
  ];

  const firstLine = code.trim().split("\n")[0].toLowerCase();
  const isValid = validStarters.some((starter) => firstLine.startsWith(starter));

  if (!isValid) {
    return {
      valid: false,
      error: `유효하지 않은 Mermaid 다이어그램 타입입니다. 시작 키워드: ${validStarters.join(", ")}`,
    };
  }

  return { valid: true };
}

