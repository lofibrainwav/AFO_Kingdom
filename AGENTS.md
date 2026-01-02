# AGENTS.md — Root Rules (KO_ONLY + SSOT-first)

## 0) 적용 범위
- 이 저장소에서 작업하는 모든 AI 에이전트/도구/사람에게 동일 적용합니다.

## 1) Language Lock (KO_ONLY)
- 기본 언어: 한국어(존댓말).
- 원칙: 설명/결론/판정/요약은 한국어로만 씁니다.

### 예외 1) 기술 용어/식별자
- 코드 식별자, 파일/경로, CLI 명령, 라이브러리/제품명은 원문(영문) 그대로 허용합니다.
- 단, "문장 전체"를 영어로 쓰지 않습니다. (필요 시 괄호로 짧게만)

### 예외 2) 철학적 사자성어/동서양 철학 교훈
- 사자성어(한글/한자) 사용을 허용합니다. (예: 지피지기, 眞善美孝永)
- 필수 조건:
  1) 사자성어 직후에 **자연스러운 한국어 뜻풀이 1줄**을 붙입니다.
  2) 필요할 때만 **짧은 영어 글로스(Gloss)**를 괄호로 덧붙입니다. (문장 금지, 한 줄/한 구절만)
- 금지:
  - 일본어(히라가나/가타카나) 사용 금지
  - 중국어/일본어 "문장" 삽입 금지
  - 멀티언어 슬로건(영문/일문 구호) 금지

예시:
- 지피지기: 상대를 알고 나를 알면, 무리한 실행을 피할 수 있습니다. (Know yourself, know your enemy)
- 도원결의: 한 팀이 같은 목표로 움직이면 마찰이 줄어듭니다. (Brotherhood oath for shared goals)
- 전장의 안개: 정보가 부족하면 먼저 정찰하고 움직입니다. (Fog of war)

## 2) No Roleplay / No Hype
- "승상/사령관/제국/봉인" 등 역할극 문구를 사용하지 않습니다.
- 과장 수치(예: 20배 증폭), 근거 없는 단정, 감정적 선동을 금지합니다.

## 3) Truth Policy (SSOT-first)
- 사실/수치/성능/완료 선언은 **증거(SSOT)** 없이는 쓰지 않습니다.
- 허용되는 증거:
  - repo 내부 파일(코드/문서/로그)
  - artifacts/ 내 결과 파일(JSON/LOG/MD 등)
  - 실행 로그(명령어 + stdout/stderr)
  - 해시/매니페스트(sha256, manifest json)
- 증거가 없으면:
  - "UNKNOWN"으로 표시하고, 필요한 증거 파일/명령만 요청합니다.

## 4) Execution Protocol (필수 순서)
1) Backup
2) Check
3) Execute (최소 변경)
4) Verify (게이트/테스트/재현)
5) Rollback (즉시 복구 경로 제공)

## 5) Ask-Before-Act (ASK_COMMANDER 강제)
아래는 무조건 실행 전에 확인 요청:
- 데이터 삭제/마이그레이션/대규모 리팩터
- 보안/권한/네트워크/비용이 걸린 변경
- 외부 시스템(클라우드, 결제, 배포) 영향
- "완료/성공/LOCKED/DONE" 같은 상태 판정

## 6) Output Format (복붙 우선)
- 명령어는 바로 실행 가능한 형태로 제공합니다.
- 한 번에 너무 길게 몰아주지 않습니다.
- 경로/파일명/명령어는 정확히 적습니다.

## 7) SSOT Evidence Pack 표준
- 산출물은 artifacts/ 아래에 타임스탬프 포함 파일명으로 저장합니다.
- 권장 구성:
  - ssot_*_env_*.json (환경)
  - ssot_*_run_*.log (실행 로그)
  - *_result.json (결과 지표)
  - ssot_*_reproducibility_info.md (재현 가이드)
  - ssot_*_hashes_*.txt (sha256)
  - ssot_*_manifest_*.json (목록/크기/경로)

## 8) Git 규칙
- 커밋 메시지: type(scope): summary
- "상태 선언(DONE/LOCKED)"은 SSOT evidence pack 경로를 함께 남깁니다.

## 9) Guard (재발 방지)
- (존재할 경우) scripts/guard_no_japanese_kana.py 통과가 필수입니다.
