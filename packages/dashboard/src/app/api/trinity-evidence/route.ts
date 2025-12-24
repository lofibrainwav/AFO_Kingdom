import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(request: NextRequest) {
  try {
    // 최신 Trinity Evidence 찾기
    const artifactsDir = path.join(process.cwd(), '../../../artifacts/trinity');

    if (!fs.existsSync(artifactsDir)) {
      return NextResponse.json({
        error: 'Trinity Evidence 디렉토리가 존재하지 않습니다',
        status: 'not_found'
      }, { status: 404 });
    }

    // 가장 최신 날짜 디렉토리 찾기
    const dateDirs = fs.readdirSync(artifactsDir)
      .filter(dir => fs.statSync(path.join(artifactsDir, dir)).isDirectory())
      .sort()
      .reverse();

    if (dateDirs.length === 0) {
      return NextResponse.json({
        error: 'Trinity Evidence가 아직 생성되지 않았습니다',
        status: 'no_evidence'
      }, { status: 404 });
    }

    const latestDateDir = dateDirs[0];
    const evidenceDir = path.join(artifactsDir, latestDateDir);

    // evidence.json 파일 읽기 (통합 파일)
    const evidencePath = path.join(evidenceDir, 'evidence.json');

    if (!fs.existsSync(evidencePath)) {
      return NextResponse.json({
        error: '통합 증거 파일이 존재하지 않습니다',
        status: 'evidence_file_missing'
      }, { status: 404 });
    }

    const evidenceData = JSON.parse(fs.readFileSync(evidencePath, 'utf-8'));

    // verdict.md 파일도 함께 제공
    const verdictPath = path.join(evidenceDir, 'verdict.md');
    let verdictContent = '';
    if (fs.existsSync(verdictPath)) {
      verdictContent = fs.readFileSync(verdictPath, 'utf-8');
    }

    return NextResponse.json({
      date: latestDateDir,
      evidence: evidenceData,
      verdict: verdictContent,
      status: 'success'
    });

  } catch (error) {
    console.error('Trinity Evidence API 오류:', error);
    return NextResponse.json({
      error: 'Trinity Evidence 조회 중 오류가 발생했습니다',
      status: 'error',
      details: error instanceof Error ? error.message : '알 수 없는 오류'
    }, { status: 500 });
  }
}