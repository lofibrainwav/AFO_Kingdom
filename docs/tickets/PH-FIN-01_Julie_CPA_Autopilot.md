# PH-FIN-01 — Julie CPA Finance Autopilot (Input → Label → Queue) — SSOT

## 목표
재무 데이터 정리를 “자율 주행 보조(Autopilot Assist)”로 만들되,
최종 판단(세무/회계/윤리)은 Julie CPA 승인으로만 확정한다.

## 3-Step Minimal-Invasive
1) Input: CSV/문서/이메일(옵션)을 Inbox로 수집  
2) Labeling: 카테고리 + 리스크 플래그(사마의 필터)  
3) Queue: Julie 리뷰 큐 생성 → 승인 후 후속 작업(수동/반자동)

## 안전장치
- 자동 posting/auto-commit 금지
- PII/시크릿 저장 금지(Repo 밖 raw)
- 모든 결과물은 artifacts로 분리
