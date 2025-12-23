#!/usr/bin/env node
/* eslint-env node */
/* eslint-disable @typescript-eslint/no-require-imports */

/**
 * 번들 크기 분석 스크립트
 * 
 * Next.js 빌드 후 번들 크기를 분석하고 리포트를 생성합니다.
 * 
 * 사용법:
 *   npm run build
 *   node scripts/analyze-bundle.js
 */

const fs = require("fs");
const path = require("path");

const BUILD_DIR = path.join(__dirname, "..", ".next");
const REPORT_FILE = path.join(__dirname, "..", "bundle-analysis.json");

function formatBytes(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}

function analyzeBundle() {
  console.log("📦 번들 크기 분석 시작...\n");

  const staticDir = path.join(BUILD_DIR, "static");
  const chunksDir = path.join(staticDir, "chunks");

  if (!fs.existsSync(chunksDir)) {
    console.error("❌ 빌드 디렉토리를 찾을 수 없습니다. 먼저 'npm run build'를 실행하세요.");
    process.exit(1);
  }

  const analysis = {
    timestamp: new Date().toISOString(),
    totalSize: 0,
    chunks: [],
    pages: [],
    assets: [],
  };

  // Chunks 분석
  if (fs.existsSync(chunksDir)) {
    const chunkFiles = fs.readdirSync(chunksDir);
    chunkFiles.forEach((file) => {
      const filePath = path.join(chunksDir, file);
      const stats = fs.statSync(filePath);
      const size = stats.size;

      analysis.totalSize += size;
      analysis.chunks.push({
        name: file,
        size,
        formattedSize: formatBytes(size),
      });
    });
  }

  // Pages 분석
  const pagesDir = path.join(BUILD_DIR, "server", "app");
  if (fs.existsSync(pagesDir)) {
    const analyzePages = (dir, prefix = "") => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      entries.forEach((entry) => {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          analyzePages(fullPath, `${prefix}/${entry.name}`);
        } else if (entry.name.endsWith(".js")) {
          const stats = fs.statSync(fullPath);
          const size = stats.size;
          analysis.pages.push({
            route: prefix || "/",
            file: entry.name,
            size,
            formattedSize: formatBytes(size),
          });
        }
      });
    };
    analyzePages(pagesDir);
  }

  // Assets 분석
  const assetsDir = path.join(staticDir, "media");
  if (fs.existsSync(assetsDir)) {
    const assetFiles = fs.readdirSync(assetsDir);
    assetFiles.forEach((file) => {
      const filePath = path.join(assetsDir, file);
      const stats = fs.statSync(filePath);
      const size = stats.size;
      analysis.assets.push({
        name: file,
        size,
        formattedSize: formatBytes(size),
      });
    });
  }

  // 정렬 (크기 순)
  analysis.chunks.sort((a, b) => b.size - a.size);
  analysis.pages.sort((a, b) => b.size - a.size);
  analysis.assets.sort((a, b) => b.size - a.size);

  // 리포트 저장
  fs.writeFileSync(REPORT_FILE, JSON.stringify(analysis, null, 2));

  // 콘솔 출력
  console.log("✅ 번들 분석 완료!\n");
  console.log(`📊 총 번들 크기: ${formatBytes(analysis.totalSize)}\n`);

  console.log("🔝 상위 10개 Chunks:");
  analysis.chunks.slice(0, 10).forEach((chunk, index) => {
    console.log(
      `  ${index + 1}. ${chunk.name}: ${chunk.formattedSize}`
    );
  });

  console.log("\n📄 Pages:");
  analysis.pages.forEach((page) => {
    console.log(`  ${page.route}: ${page.formattedSize}`);
  });

  console.log(`\n📁 리포트 저장: ${REPORT_FILE}`);
  
  // 경고 (500KB 초과)
  const totalMB = analysis.totalSize / (1024 * 1024);
  if (totalMB > 0.5) {
    console.warn(
      `\n⚠️  경고: 총 번들 크기가 500KB를 초과합니다 (${formatBytes(analysis.totalSize)})`
    );
  } else {
    console.log(
      `\n✅ 번들 크기가 목표(500KB) 이하입니다: ${formatBytes(analysis.totalSize)}`
    );
  }
}

analyzeBundle();

