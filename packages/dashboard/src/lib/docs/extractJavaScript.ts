/**
 * JavaScript 로직 추출 유틸리티
 */

export interface ExtractedFunction {
  name: string;
  code: string;
  type: "function" | "arrow" | "async" | "class" | "const" | "let" | "var";
  dependencies: string[];
}

/**
 * JavaScript 코드에서 함수 추출
 * 
 * @param jsCode - JavaScript 코드 문자열
 * @returns 추출된 함수 배열
 */
export function extractFunctions(jsCode: string): ExtractedFunction[] {
  const functions: ExtractedFunction[] = [];

  // 함수 선언: function name() {}
  const functionRegex = /function\s+(\w+)\s*\([^)]*\)\s*\{[\s\S]*?\n\}/g;
  let match;
  while ((match = functionRegex.exec(jsCode)) !== null) {
    functions.push({
      name: match[1],
      code: match[0],
      type: "function",
      dependencies: extractDependencies(match[0]),
    });
  }

  // 화살표 함수: const name = () => {}
  const arrowRegex = /(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{[\s\S]*?\n\}/g;
  while ((match = arrowRegex.exec(jsCode)) !== null) {
    functions.push({
      name: match[1],
      code: match[0],
      type: match[0].includes("async") ? "async" : "arrow",
      dependencies: extractDependencies(match[0]),
    });
  }

  // 클래스: class Name {}
  const classRegex = /class\s+(\w+)[\s\S]*?\n\}/g;
  while ((match = classRegex.exec(jsCode)) !== null) {
    functions.push({
      name: match[1],
      code: match[0],
      type: "class",
      dependencies: extractDependencies(match[0]),
    });
  }

  return functions;
}

/**
 * 코드에서 의존성 추출 (함수 호출, 변수 참조)
 */
function extractDependencies(code: string): string[] {
  const dependencies: Set<string> = new Set();

  // 함수 호출: functionName()
  const functionCallRegex = /(\w+)\s*\(/g;
  let match;
  while ((match = functionCallRegex.exec(code)) !== null) {
    const name = match[1];
    // 예약어 제외
    if (!["if", "for", "while", "switch", "return", "await", "async"].includes(name)) {
      dependencies.add(name);
    }
  }

  // 전역 객체 접근: window.xxx, document.xxx
  const globalRegex = /(window|document|console)\.(\w+)/g;
  while ((match = globalRegex.exec(code)) !== null) {
    dependencies.add(`${match[1]}.${match[2]}`);
  }

  return Array.from(dependencies);
}

/**
 * 위젯 레지스트리 코드 추출
 */
export function extractWidgetRegistry(jsCode: string): {
  widgets: Array<{ id: string; name: string; section: string }>;
  registryCode: string;
} {
  const widgets: Array<{ id: string; name: string; section: string }> = [];
  let registryCode = "";

  // WidgetRegistry.register() 호출 찾기
  const registerRegex = /WidgetRegistry\.register\([\s\S]*?\);/g;
  let match;
  while ((match = registerRegex.exec(jsCode)) !== null) {
    registryCode += match[0] + "\n";

    // 위젯 ID 추출
    const idMatch = match[0].match(/id:\s*['"]([^'"]+)['"]/);
    const nameMatch = match[0].match(/name:\s*['"]([^'"]+)['"]/);
    const sectionMatch = match[0].match(/section:\s*['"]([^'"]+)['"]/);

    if (idMatch) {
      widgets.push({
        id: idMatch[1],
        name: nameMatch ? nameMatch[1] : idMatch[1],
        section: sectionMatch ? sectionMatch[1] : idMatch[1].replace("-widget", ""),
      });
    }
  }

  return { widgets, registryCode };
}

