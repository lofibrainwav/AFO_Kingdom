#!/usr/bin/env node
/**
 * HTML 파서 → generated JSON → Registry 자동등록
 * 
 * kingdom_dashboard.html에서 data-widget-id를 읽어서
 * widgets.generated.json 생성
 * 
 * 사용법:
 *   node packages/dashboard/scripts/generate_widgets_from_html.mjs
 *   또는
 *   pnpm -C packages/dashboard gen:widgets
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const repoRoot = path.resolve(__dirname, "../../..");
const srcHtml = path.resolve(repoRoot, "packages/dashboard/public/legacy/kingdom_dashboard.html");

const outDir = path.resolve(repoRoot, "packages/dashboard/src/generated");
const outFile = path.resolve(outDir, "widgets.generated.json");

function slugify(s) {
  return String(s)
    .trim()
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9\u3131-\uD79D\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

function pickTitle(html, el) {
  // 간단한 정규식으로 h1, h2, h3 추출
  const sectionHtml = el.outerHTML || "";
  const h1Match = sectionHtml.match(/<h1[^>]*>(.*?)<\/h1>/i);
  if (h1Match) return h1Match[1].replace(/<[^>]+>/g, "").trim();
  
  const h2Match = sectionHtml.match(/<h2[^>]*>(.*?)<\/h2>/i);
  if (h2Match) return h2Match[1].replace(/<[^>]+>/g, "").trim();
  
  const h3Match = sectionHtml.match(/<h3[^>]*>(.*?)<\/h3>/i);
  if (h3Match) return h3Match[1].replace(/<[^>]+>/g, "").trim();
  
  return null;
}

function extractText(html) {
  let text = html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  
  // JSON 안전성을 위해 제어 문자 제거
  text = text.replace(/[\x00-\x1F\x7F]/g, "");
  
  return text;
}

function safeSlice(text, maxLength) {
  if (text.length <= maxLength) return text;
  
  // 유니코드 서로게이트 페어를 고려하여 안전하게 자르기
  let sliced = text.slice(0, maxLength);
  
  // 마지막 문자가 서로게이트 페어의 첫 번째 부분인지 확인
  const lastChar = sliced.charCodeAt(sliced.length - 1);
  if (lastChar >= 0xD800 && lastChar <= 0xDBFF) {
    // 서로게이트 페어의 첫 번째 부분이면 하나 더 제거
    sliced = sliced.slice(0, -1);
  }
  
  // 잘린 유니코드 이스케이프 시퀀스 제거 (예: \ud83c)
  sliced = sliced.replace(/\\u[dD][0-9a-fA-F]{0,2}$/, "");
  
  return sliced;
}

function main() {
  console.log("📐 HTML 파서 → generated JSON 생성 시작...\n");

  if (!fs.existsSync(srcHtml)) {
    console.error(`❌ Source HTML not found: ${srcHtml}`);
    process.exit(1);
  }

  console.log(`1. HTML 파일 읽기: ${srcHtml}`);
  const html = fs.readFileSync(srcHtml, "utf-8");
  console.log(`   ✅ 파일 크기: ${html.length} bytes\n`);

  console.log("2. 섹션 파싱 중...");
  const widgets = [];
  const seen = new Set();

  // data-widget-id가 있는 섹션 찾기
  const dataWidgetIdRegex = /<section[^>]*data-widget-id=["']([^"']+)["'][^>]*>([\s\S]*?)<\/section>/gi;
  const idRegex = /<section[^>]*id=["']([^"']+)["'][^>]*>([\s\S]*?)<\/section>/gi;

  // data-widget-id 우선 매칭
  let match;
  while ((match = dataWidgetIdRegex.exec(html)) !== null) {
    const dataWidgetId = match[1].trim();
    const sectionHtml = match[0];
    const fullMatch = match[0];
    
    // id 추출
    const idMatch = fullMatch.match(/id=["']([^"']+)["']/i);
    const sourceId = idMatch ? idMatch[1].trim() : null;

    const title = pickTitle(html, { outerHTML: sectionHtml });
    const text = extractText(sectionHtml);
    
    if (text.length < 20) continue;

    const baseId = slugify(dataWidgetId);
    if (!baseId) continue;

    let id = baseId;
    let i = 2;
    while (seen.has(id)) id = `${baseId}-${i++}`;
    seen.add(id);

    // preview를 안전하게 처리 (유니코드 서로게이트 페어 고려)
    const preview = safeSlice(text, 160);

    widgets.push({
      id,
      dataWidgetId: dataWidgetId || null,
      sourceId: sourceId || null,
      // [Ticket 3] fragment_key: 표준 fragment 포인터 (id와 1:1 매칭)
      fragment_key: id, // slug = id (이미 slugify됨)
      title: (title || dataWidgetId || sourceId || id).replace(/[\u0000-\u001F\u007F-\u009F]/g, ""),
      preview: preview,
      route: `/docs/${id}`,
      order: 100 + widgets.length * 10,
      visibility: "internal",
      category: "panel",
      defaultEnabled: true,
      source: "generated",
      tags: ["generated", "html"],
    });
  }

  // data-widget-id가 없는 섹션도 찾기 (id만 있는 경우)
  while ((match = idRegex.exec(html)) !== null) {
    const sourceId = match[1].trim();
    const sectionHtml = match[0];
    
    // 이미 data-widget-id로 처리된 섹션은 스킵
    if (sectionHtml.includes("data-widget-id")) continue;
    
    const title = pickTitle(html, { outerHTML: sectionHtml });
    const text = extractText(sectionHtml);
    
    if (text.length < 20) continue;

    const baseId = slugify(sourceId);
    if (!baseId) continue;

    let id = baseId;
    let i = 2;
    while (seen.has(id)) id = `${baseId}-${i++}`;
    seen.add(id);

    // preview를 안전하게 처리 (유니코드 서로게이트 페어 고려)
    const preview = safeSlice(text, 160);

    widgets.push({
      id,
      dataWidgetId: null,
      sourceId: sourceId || null,
      // [Ticket 3] fragment_key: 표준 fragment 포인터 (id와 1:1 매칭)
      fragment_key: id, // slug = id (이미 slugify됨)
      title: (title || sourceId || id).replace(/[\u0000-\u001F\u007F-\u009F]/g, ""),
      preview: preview,
      route: `/docs/${id}`,
      order: 100 + widgets.length * 10,
      visibility: "internal",
      category: "panel",
      defaultEnabled: true,
      source: "generated",
      tags: ["generated", "html"],
    });
  }

  console.log(`   ✅ ${widgets.length}개 위젯 발견\n`);

  const payload = {
    source: "packages/dashboard/public/legacy/kingdom_dashboard.html",
    generatedAt: new Date().toISOString(),
    count: widgets.length,
    widgets,
  };

  console.log("3. JSON 파일 생성...");
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(outFile, JSON.stringify(payload, null, 2), "utf-8");

  console.log(`   ✅ 생성 완료: ${outFile}`);
  console.log(`   ✅ 위젯 개수: ${widgets.length}\n`);

  console.log("✅ HTML 파서 → generated JSON 생성 완료!\n");
}

try {
  main();
} catch (error) {
  console.error("❌ 오류 발생:", error.message);
  console.error(error.stack);
  process.exit(1);
}

