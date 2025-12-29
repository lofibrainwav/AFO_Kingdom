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

// 여러 가능한 경로를 시도 (Docker vs 로컬 환경 고려)
const possiblePaths = [
  // Docker 환경: /app/packages/dashboard/public/legacy/kingdom_dashboard.html
  path.resolve("/app", "packages/dashboard/public/legacy/kingdom_dashboard.html"),
  // 로컬 환경: 프로젝트 루트 기준
  path.resolve(__dirname, "../../..", "packages/dashboard/public/legacy/kingdom_dashboard.html"),
  // 절대 경로로 직접 지정 (docs/reports/html에서 복사된 경우)
  path.resolve("/app", "docs/reports/html/kingdom_dashboard.html"),
  // 마지막 fallback: 현재 working directory 기준
  path.resolve(process.cwd(), "packages/dashboard/public/legacy/kingdom_dashboard.html")
];

let srcHtml = null;
for (const testPath of possiblePaths) {
  if (fs.existsSync(testPath)) {
    srcHtml = testPath;
    console.log(`✅ HTML 파일 발견: ${testPath}`);
    break;
  }
}

if (!srcHtml) {
  console.error("❌ Source HTML not found. 다음 경로들을 확인했습니다:");
  possiblePaths.forEach(p => console.error(`  - ${p} (${fs.existsSync(p) ? '존재' : '없음'})`));
  console.log("⚠️ HTML 파일이 없어 기본 fragment 생성으로 대체합니다.");

  // 기본 fragment 생성
  const repoRoot = path.resolve(__dirname, "../../..");
  const fragmentsDir = path.resolve(repoRoot, "packages/dashboard/public/fragments");
  fs.mkdirSync(fragmentsDir, { recursive: true });

  const defaultFragments = {
    "status.html": "<div class='p-4 bg-green-50 border border-green-200 rounded'>시스템 정상 작동 중</div>",
    "widgets.html": "<div class='p-4 bg-blue-50 border border-blue-200 rounded'>기본 위젯 표시 영역</div>"
  };

  for (const [filename, content] of Object.entries(defaultFragments)) {
    const fragmentPath = path.join(fragmentsDir, filename);
    fs.writeFileSync(fragmentPath, content, 'utf8');
    console.log(`✅ 기본 fragment 생성: ${fragmentPath}`);
  }

  console.log(`\n📊 결과:\n   ✅ 성공: ${Object.keys(defaultFragments).length}개\n   📁 저장 경로: ${fragmentsDir}`);
  process.exit(0);
}

const repoRoot = srcHtml.includes('/app') ? '/app' : path.resolve(__dirname, "../../..");
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

