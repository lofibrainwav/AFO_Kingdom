# SARIF 형식 가이드

## SARIF란?

**Static Analysis Results Interchange Format** - OASIS 표준 JSON 형식으로 정적 분석 결과 교환.

## AFO Kingdom 적용 현황 ✅

| 도구 | SARIF 출력 | GitHub Security 탭 |
|------|-----------|-------------------|
| Trivy | ✅ `trivy-results.sarif` | ✅ 업로드 |
| Snyk | ✅ `snyk.sarif` | ✅ 업로드 |
| Scorecard | ✅ `scorecard.sarif` | ✅ 업로드 |

---

## SARIF 구조

```json
{
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": {
      "driver": {
        "name": "Trivy",
        "rules": [...]
      }
    },
    "results": [{
      "ruleId": "CVE-2024-XXXX",
      "level": "error",
      "message": { "text": "..." },
      "locations": [...]
    }]
  }]
}
```

---

## GitHub 매핑

| SARIF | GitHub Security |
|-------|-----------------|
| `ruleId` | Alert Type |
| `level` (error/warning) | Severity |
| `properties.security-severity` | CVSS 기반 |

---

## CI 설정 예시

```yaml
# 1. Trivy SARIF 생성
- uses: aquasecurity/trivy-action@...
  with:
    format: 'sarif'
    output: 'trivy-results.sarif'

# 2. GitHub Security 탭 업로드
- uses: github/codeql-action/upload-sarif@...
  with:
    sarif_file: 'trivy-results.sarif'
```

---

## 眞善美孝永 연계

| 기둥 | SARIF 적용 |
|------|-----------|
| 眞 | 표준 형식으로 진실성 |
| 善 | 취약점 중앙화 |
| 美 | 통합 대시보드 |
| 孝 | 자동 업로드 |
| 永 | 추이 추적 |
