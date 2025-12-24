#!/usr/bin/env node
/**
 * HTML Fragment Generator (Ticket 3)
 * 
 * HTML에서 위젯별 innerHTML을 뽑아서 파일로 저장
 * 경로: packages/dashboard/public/fragments/{fragment_key}.html
 * 
 * 사용법:
 *   node packages/dashboard/scripts/generate_fragments.mjs
 *   또는
 *   pnpm -C packages/dashboard gen:fragments
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as cheerio from "cheerio";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const repoRoot = path.resolve(__dirname, "../../..");
const srcHtml = path.resolve(repoRoot, "packages/dashboard/public/legacy/kingdom_dashboard.html");
const widgetsJson = path.resolve(repoRoot, "packages/dashboard/src/generated/widgets.generated.json");
const fragmentsDir = path.resolve(repoRoot, "packages/dashboard/public/fragments");

function main() {
  console.log("📐 HTML Fragment 생성 시작...\n");

  // 1. widgets.generated.json 읽기
  if (!fs.existsSync(widgetsJson)) {
    console.error(`❌ widgets.generated.json not found: ${widgetsJson}`);
    console.error("   Run: pnpm -C packages/dashboard gen:widgets");
    process.exit(1);
  }

  const widgetsData = JSON.parse(fs.readFileSync(widgetsJson, "utf-8"));
  const widgets = widgetsData.widgets || [];

  // 2. HTML 파일 읽기
  if (!fs.existsSync(srcHtml)) {
    console.error(`❌ Source HTML not found: ${srcHtml}`);
    process.exit(1);
  }

  const html = fs.readFileSync(srcHtml, "utf-8");
  const $ = cheerio.load(html);

  // 3. fragments 디렉토리 생성
  fs.mkdirSync(fragmentsDir, { recursive: true });

  // 4. 각 위젯의 fragment 생성
  let successCount = 0;
  let failCount = 0;

  for (const widget of widgets) {
    const fragmentKey = widget.fragment_key || widget.id;
    const dataWidgetId = widget.dataWidgetId;
    const sourceId = widget.sourceId;

    // 섹션 찾기 (우선순위: data-widget-id > id)
    let section = null;
    
    if (dataWidgetId) {
      // 1순위: data-widget-id 속성
      section = $(`[data-widget-id="${dataWidgetId}"]`).first();
    }
    
    if (!section && sourceId) {
      // 2순위: id 속성 (fallback)
      section = $(`#${sourceId}`).first();
    }

    if (!section) {
      console.warn(`⚠️  섹션을 찾을 수 없음: ${fragmentKey} (dataWidgetId: ${dataWidgetId}, sourceId: ${sourceId})`);
      failCount++;
      continue;
    }

    // innerHTML 추출
    const innerHTML = section.html() || "";
    
    if (!innerHTML.trim()) {
      console.warn(`⚠️  빈 섹션: ${fragmentKey}`);
      failCount++;
      continue;
    }

    // Fragment 파일 저장
    const fragmentFile = path.resolve(fragmentsDir, `${fragmentKey}.html`);
    fs.writeFileSync(fragmentFile, innerHTML, "utf-8");
    console.log(`✅ ${fragmentKey}.html 생성 완료`);
    successCount++;
  }

  console.log("\n📊 결과:");
  console.log(`   ✅ 성공: ${successCount}개`);
  if (failCount > 0) {
    console.log(`   ⚠️  실패: ${failCount}개`);
  }
  console.log(`   📁 저장 경로: ${fragmentsDir}`);
  console.log("\n✅ HTML Fragment 생성 완료!");
}

main();

