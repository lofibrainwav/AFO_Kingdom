# Operational Metrics

> **As-of: 2025-12-29 | Version: v1.1**
> **眞善美孝영** - Chancellor Graph V2 핵심 운영 메트릭 및 알람 정책

## 1. 핵심 메트릭 (The Big 5)

| 메트릭 명 | 설명 | 정상 범위 (SLO) | Prometheus 쿼리 |
|-----------|------|-----------------|----------------|
| **Verify Pass Rate** | 전체 실행 중 검증 통과 비율 | ≥ 95% | `sum(chancellor_v2_verify_pass_total) / sum(chancellor_v2_trace_created_total)` |
| **Execute Success Rate** | Skill 실행 성공률 | ≥ 90% | `sum(chancellor_v2_execute_success_total) / sum(chancellor_v2_execute_total)` |
| **Execute Blocked Rate** | 보안 정책에 의한 차단율 | < 1% | `sum(chancellor_v2_execute_blocked_total) / sum(chancellor_v2_execute_total)` |
| **Execution Latency P95** | 상위 5% 실행 지연 시간 | < 30s | `histogram_quantile(0.95, sum(chancellor_v2_duration_seconds_bucket) by (le))` |
| **Trace Creation Rate** | 시스템 활성 트래픽 | > 0 | `rate(chancellor_v2_trace_created_total[5m])` |

---

## 2. Prometheus AlertManager 규칙

```yaml
groups:
- name: ChancellorV2Alerts
  rules:
  # 1. 검증 실패율 급증 (眞/善 위기)
  - alert: ChancellorVerifyFailHigh
    expr: rate(chancellor_v2_verify_fail_total[5m]) / rate(chancellor_v2_trace_created_total[5m]) > 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Chancellor V2 Verify failure rate is high ({{ $value | humanizePercentage }})"
      description: "에러 누적 또는 3책사 합의 실패가 빈번하게 발생하고 있습니다."

  # 2. 실행 차단 급증 (보안 게이트 작동)
  - alert: ChancellorExecutionBlocked
    expr: rate(chancellor_v2_execute_blocked_total[5m]) > 1
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "High skill execution block rate"
      description: "Allowlist에 없는 스킬 호출이 감지되었습니다. 공격 의도 여부 확인이 필요합니다."

  # 3. 레이턴시 폭증 (孝/永 위기)
  - alert: ChancellorLatencyP95Critical
    expr: histogram_quantile(0.95, sum(rate(chancellor_v2_duration_seconds_bucket[5m])) by (le)) > 60
    for: 3m
    labels:
      severity: warning
    annotations:
      summary: "Chancellor V2 P95 Latency > 60s"
      description: "시스템 응답성 저하로 사령관의 평온(孝)이 깨지고 있습니다."
```

---

## 3. 참고 자료

- [SSOT Import Paths](./SSOT_IMPORT_PATHS.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/SSOT_IMPORT_PATHS.md)
- [Failure Mode Matrix](./FAILURE_MODE_MATRIX.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/FAILURE_MODE_MATRIX.md)
- [Chancellor Graph V2 완전 가이드](./CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md) | [Local Access](file://<LOCAL_WORKSPACE>/AFO_Kingdom/docs/CHANCELLOR_GRAPH_V2_COMPLETE_GUIDE.md)

---

**Trinity Score**: 眞 95% | 善 100% | 美 90% | 孝 95% | 永 100%
