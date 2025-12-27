# AFO Kingdom — Council Protocol (Multi-Chancellor Consensus)

## Rule
- 외부 승상(Grok/NotebookLM 등)의 레거시 지혜를 존중한다.
- 최종 집행은 SSOT/로그/근거 기반으로 '충돌 제거' 후 진행한다.

## Input Format (외부 승상에게 전달)
- 결론(1줄)
- 근거(3~7줄, 불확실성 표시)
- 실행 커맨드(복붙)
- 리스크/롤백

## Merge Policy
- 공통 결론은 Truth 강화
- 충돌 결론은 재검증 항목으로 격리 후 로그/근거로 판정
