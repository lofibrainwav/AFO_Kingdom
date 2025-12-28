# Dependabot Vulnerability Management Policy (AFO)

## Triage 기준
- 기본 정렬: Security > Dependabot alerts > "Most important"
- 우선순위 판단 요소:
  - Severity (CVSS)
  - Exploit likelihood (EPSS)
  - Dependency scope (runtime vs development)
  - Actionability (패치 PR 가능 여부)

## SLA (권장)
- Critical: 24시간 내 조치(패치 PR 머지 또는 완화)
- High: 7일 내 조치
- Moderate: 30일 내 조치(EPSS/스코프가 높으면 High처럼 처리)
- Low: 자동 트리아지(개발 전용/저영향이면 presets 또는 규칙 기반 처리)

## Auto-merge 원칙
- patch/minor 업데이트만 자동 승인 + 자동 머지
- major 업데이트는 자동 머지 금지(리뷰/테스트 후 수동 머지)
- CI/브랜치 보호 룰 통과가 선행 조건
