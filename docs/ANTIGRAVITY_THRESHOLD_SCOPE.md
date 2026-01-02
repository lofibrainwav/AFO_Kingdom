# 안티그라비티 임계값 스코프 명확화 (SSOT)

**As-of:** 2026-01-01T20:59:30Z
**HEAD:** `6512354d068dfaf7f4b04e54ebd57a88e8fe85cf`
**Evidence:** `artifacts/antigravity_verify_20260101_205720/evidence_log.txt`
**Decision:** ASK_COMMANDER (임계값 스코프 명확화 필요)
**Reproduce:** `./afo seal antigravity-threshold-scope`

---

## 1. 현상 분석

### Antigravity 모듈의 임계값 설정
```python
# packages/afo-core/config/antigravity.py
AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD = 80
AGENTS_MD_AUTO_RUN_RISK_THRESHOLD = 3
```

### AGENTS.md의 AUTO_RUN 기준
```
Trinity Score ≥ 90 AND Risk ≤ 10이면 AUTO_RUN
```

**문제점**: 동일한 상수명이지만 다른 임계값이 충돌 가능성 존재

---

## 2. 스코프 명확화 (SSOT)

### 전역 AUTO_RUN 판단: AGENTS.md 기준 (최종 결정권)
- **Trinity Score ≥ 90** AND **Risk Score ≤ 10** → AUTO_RUN
- **그 외 모든 경우** → ASK_COMMANDER
- **적용 범위**: 모든 왕국 의사결정의 최종 게이트

### Antigravity 80/3 임계값: 내부 경고/프리체크용
- **Trinity Score ≥ 80** AND **Risk Score ≤ 3** → 내부 추천/경고
- **목적**: 자동화 후보 탐색, 사전 경고 발행
- **권한**: 결정권 없음, ASK_COMMANDER 권고만 가능
- **적용 범위**: Antigravity 모듈 내부 프리체크

---

## 3. 의사결정 플로우

```
┌─────────────────────────────────────────┐
│           Antigravity 프리체크           │
│  Trinity ≥ 80 AND Risk ≤ 3 ?           │
│                                         │
│  YES → 내부 추천 발행                   │
│  NO  → ASK_COMMANDER 권고               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        AGENTS.md 최종 게이트            │
│  Trinity ≥ 90 AND Risk ≤ 10 ?         │
│                                         │
│  YES → AUTO_RUN                        │
│  NO  → ASK_COMMANDER                    │
└─────────────────────────────────────────┘
```

---

## 4. 구현 권장사항

### Antigravity 모듈 상수명 변경 (권장)
```python
# 변경 전
AGENTS_MD_AUTO_RUN_TRINITY_THRESHOLD = 80
AGENTS_MD_AUTO_RUN_RISK_THRESHOLD = 3

# 변경 후 (스코프 명확화)
ANTIGRAVITY_PRECHECK_TRINITY_THRESHOLD = 80
ANTIGRAVITY_PRECHECK_RISK_THRESHOLD = 3
```

### 문서화 요구사항
- 모든 antigravity 관련 문서에서 "프리체크용 임계값" 명시
- AGENTS.md 90/10 기준을 "최종 결정권"으로 표기
- 충돌 가능성에 대한 경고 추가

---

## 5. 결론

**Antigravity 80/3**: 내부 추천/경고용 (결정권 없음)
**AGENTS.md 90/10**: 최종 AUTO_RUN 결정권 (SSOT)

임계값 충돌 방지를 위해 상수명 변경 및 문서화 강력 권장.
