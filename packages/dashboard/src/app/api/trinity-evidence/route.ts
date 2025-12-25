import fs from 'fs';
import { NextRequest, NextResponse } from 'next/server';
import path from 'path';

function findRepoRoot(startDir: string): string {
  let dir = startDir;
  for (let i = 0; i < 8; i++) {
    if (
      fs.existsSync(path.join(dir, 'pnpm-workspace.yaml')) ||
      fs.existsSync(path.join(dir, '.git'))
    ) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return startDir;
}

export async function GET(request: NextRequest) {
  try {
    // 최신 Trinity Evidence 찾기 - Repo root 기준으로 동적 경로 계산
    const repoRoot = findRepoRoot(process.cwd());
    const artifactsDir = process.env.TRINITY_ARTIFACTS_DIR ?? path.join(repoRoot, 'artifacts', 'trinity');

    if (!fs.existsSync(artifactsDir)) {
      // 증거물이 없어도 200 OK로 응답 (데이터 없음 명시)
      return NextResponse.json({
        date: null,
        evidence: {},
        verdict: '',
        status: 'no_evidence_available',
        message: 'Trinity Evidence가 아직 생성되지 않았습니다. 시스템이 정상 작동 중입니다.'
      });
    }

    // 가장 최신 날짜 디렉토리 찾기
    const dateDirs = fs.readdirSync(artifactsDir)
      .filter(dir => fs.statSync(path.join(artifactsDir, dir)).isDirectory())
      .sort()
      .reverse();

    if (dateDirs.length === 0) {
      return NextResponse.json({
        date: null,
        evidence: {},
        verdict: '',
        status: 'no_evidence_available',
        message: 'Trinity Evidence가 아직 생성되지 않았습니다. 시스템이 정상 작동 중입니다.'
      });
    }

    const latestDateDir = dateDirs[0];
    const evidenceDir = path.join(artifactsDir, latestDateDir);

    // Trinity evidence 데이터 수집 (여러 파일 포맷 지원)
    let evidenceData: any = {};
    let verdictContent = '';

    // evidence.json 우선 시도 (통합 파일)
    const evidencePath = path.join(evidenceDir, 'evidence.json');
    if (fs.existsSync(evidencePath)) {
      evidenceData = JSON.parse(fs.readFileSync(evidencePath, 'utf-8'));
    } else {
      // 개별 파일들에서 데이터 수집
      const inputsPath = path.join(evidenceDir, 'inputs.json');
      const scorePath = path.join(evidenceDir, 'score.json');
      const trinityInputsPath = path.join(evidenceDir, 'trinity_inputs.json');
      const trinityScorePath = path.join(evidenceDir, 'trinity_score.json');

      if (fs.existsSync(inputsPath)) {
        evidenceData.inputs = JSON.parse(fs.readFileSync(inputsPath, 'utf-8'));
      } else if (fs.existsSync(trinityInputsPath)) {
        evidenceData.inputs = JSON.parse(fs.readFileSync(trinityInputsPath, 'utf-8'));
      }

      if (fs.existsSync(scorePath)) {
        evidenceData.score = JSON.parse(fs.readFileSync(scorePath, 'utf-8'));
      } else if (fs.existsSync(trinityScorePath)) {
        evidenceData.score = JSON.parse(fs.readFileSync(trinityScorePath, 'utf-8'));
      }
    }

    // verdict 파일 읽기 (여러 포맷 지원)
    const verdictPaths = [
      path.join(evidenceDir, 'verdict.md'),
      path.join(evidenceDir, 'trinity_verdict.md')
    ];

    for (const verdictPath of verdictPaths) {
      if (fs.existsSync(verdictPath)) {
        verdictContent = fs.readFileSync(verdictPath, 'utf-8');
        break;
      }
    }

    // 최소한 하나의 데이터가 있어야 함
    if (Object.keys(evidenceData).length === 0 && !verdictContent) {
      return NextResponse.json({
        error: 'Trinity Evidence 데이터가 존재하지 않습니다',
        status: 'no_evidence_data'
      }, { status: 404 });
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

// HEAD 요청도 GET과 동일하게 처리
export async function HEAD(request: NextRequest) {
  return GET(request);
}