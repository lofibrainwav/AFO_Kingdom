# PH-ST-06 — Obsidian Scripting Orchestration (Active Neural Network) — SSOT

## 목적
Visual SSOT Vault를 “실행 가능한 지식(Active)”로 확장하되,
보안/프라이버시/자동실행 리스크를 0에 가깝게 유지한다.

## 원칙 (Non-negotiables)
- 기본값은 **OFF** (자동 실행 금지)
- 로컬 경로/시크릿 유출 금지
- 실행 스크립트는 Vault 밖(`scripts/`)에서 실행하고 결과만 Vault에 반영

## 1차 범위(MVP)
- Auto-MOC-Updater: Vault 링크/허브 문서 자동 갱신
- Link Density 리포트: 노드 수/링크 수/고립 노드 수 산출

## 산출물
- `scripts/obsidian/` 아래에 “생성/업데이트 스크립트”
- `config/obsidian/vault/_moc/`에 결과 요약 노트(수동 검토 후 반영)
