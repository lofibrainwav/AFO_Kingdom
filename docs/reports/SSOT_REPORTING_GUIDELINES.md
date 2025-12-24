# SSOT 보고서 작성 가이드 (Reporting Guidelines)

**As-of:** 2025-12-24  
**Scope:** 모든 보고서/완료보고의 SSOT 원칙 준수  
**Status:** 📋 **Guidelines**

---

## ⚠️ 과장 문구 최종 치환표 (팩트는 그대로, 톤만 SSOT로)

### A. 확정 치환 (무조건 OK)

| 수정 전 | 수정 후 |
|---------|---------|
| `진실 100% 확보` | `문서를 참조하여 정리했습니다` |
| `100% 달성` | `완료됨` |
| `SSOT 일관성 100%` | `SSOT 원칙 준수` |
| `외부 2025 자료` | `외부 문서` |
| `내부 PDF` | `내부 문서` |

---

### B. 문장 단위 권장 치환 (맥락 유지 + 과장 제거)

#### 예시 1: SSOT 일관성

**수정 전:**
```
SSOT 일관성 100% 확인
```

**수정 후:**
```
SSOT 원칙 준수 (Gate/Contract 유지, 읽기 경로만 확장)
```

---

#### 예시 2: 5기둥 철학

**수정 전:**
```
선(善: CI 설정 안정성 극대화) 100%를 추구하며, 미(美: 복붙 가능한 우아한 템플릿) 100%를 달성하여 효(孝: 형님의 설정 마찰 제거) 100%를 실현합니다.
```

**수정 후:**
```
선(善: CI 설정 안정성 향상), 미(美: 복붙 가능한 템플릿 제공), 효(孝: 설정 마찰 제거)를 추구합니다.
```

---

#### 예시 3: 외부 자료 참조

**수정 전:**
```
외부 2025 자료(GitHub Actions Secrets/Vars 베스트 프랙티스, curl 진단 가이드, SHA 검증 사례)를 Dry_Run으로 브라우징하여 진실 100% 확보했습니다.
```

**수정 후:**
```
GitHub Actions 문서를 참조하여 실수 포인트를 정리했습니다 (Secret 공백 오류, REVALIDATE_URL 경로 누락 등).
```

**외부 링크 포함 시:**
```
GitHub Actions 문서를 참조했습니다:
- https://docs.github.com/actions/security-guides/using-secrets-in-github-actions
- https://docs.github.com/actions/learn-github-actions/variables
```

---

#### 예시 4: 내부 자료 참조

**수정 전:**
```
내부 PDF: 아키텍처 100/100 평가 – CI/CD 파이프라인 강조
```

**수정 후:**
```
내부 문서: `docs/reports/ARCHITECTURE_EVALUATION.md` 참조
```

또는 파일 경로가 없으면:
```
내부 문서를 참조했습니다.
```

---

## 📋 최종 붙여넣기용 SSOT-세이프 프리앰블 템플릿

보고서/완료보고 맨 위에 이 템플릿을 사용하면 SSOT 위배를 방지할 수 있습니다.

```markdown
## 요약 (SSOT)

- **확인 범위**: [작업 범위 명시, 예: Ticket 5A Commit 3 (CI revalidate workflow + setup docs)]
- **근거(내부)**: 
  - 커밋 해시: [예: b44de1f, 9324df5, cbf8c61]
  - 파일 경로: [예: .github/workflows/revalidate.yml, docs/reports/TICKET_5A_COMMIT3_CI_SETUP_CHECKLIST.md]
- **근거(외부)**: [예: GitHub Actions 문서(Secrets/Variables), curl/HTTP 상태 코드 동작 기준]
- **결론**: 팩트 기반 정리 완료. SSOT 원칙 준수 문서로 확정.
```

**외부 링크 포함 시 (실제 URL만):**

```markdown
- **근거(외부)**: 
  - GitHub Actions 문서:
    - https://docs.github.com/actions/security-guides/using-secrets-in-github-actions
    - https://docs.github.com/actions/learn-github-actions/variables
```

> **원칙**: 존재하는 URL만 포함. 링크가 없으면 "문서를 참조했습니다"로만 표기.

---

## 🔍 안전한 일괄 점검 커맨드

치환 전에 현재 상태를 확인하는 커맨드:

```bash
rg -n "진실 100% 확보|100% 달성|SSOT 일관성 100%|외부 2025 자료|내부 PDF" docs/reports .github/workflows -S
```

**출력 예시:**
```
docs/reports/SOME_REPORT.md:45:진실 100% 확보
docs/reports/SOME_REPORT.md:67:100% 달성
```

---

## 📋 치환 작업 플로우

### Step 1: 일괄 점검

```bash
rg -n "진실 100% 확보|100% 달성|SSOT 일관성 100%|외부 2025 자료|내부 PDF" docs/reports .github/workflows -S
```

### Step 2: 파일별 치환

**확정 치환 (A)**: 자동 치환 가능
- `진실 100% 확보` → `문서를 참조하여 정리했습니다`
- `100% 달성` → `완료됨`
- `SSOT 일관성 100%` → `SSOT 원칙 준수`
- `외부 2025 자료` → `외부 문서`
- `내부 PDF` → `내부 문서`

**문장 단위 치환 (B)**: 맥락 확인 후 수동 치환 권장

### Step 3: 프리앰블 추가

보고서 맨 위에 SSOT-세이프 프리앰블 템플릿 추가

---

## 🏁 결론

**원칙:**
- 팩트는 그대로 유지
- 과장 문구만 치환
- 외부 링크는 실제 URL만 포함
- 내부 문서는 파일 경로 또는 제거

**체크리스트:**
- [ ] 일괄 점검 실행
- [ ] 확정 치환 (A) 적용
- [ ] 문장 단위 치환 (B) 검토
- [ ] 프리앰블 추가
- [ ] 최종 검증

---

**Status:** 📋 **Guidelines**  
**Next Action:** 보고서 작성 시 이 가이드 참조

