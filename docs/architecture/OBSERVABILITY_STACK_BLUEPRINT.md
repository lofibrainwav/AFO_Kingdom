# AFO Observability Conscience Stack 청사진

## 0) 목표 한 줄

**PR 품질(SSOT/영어비율/리스크) + 런타임 안정성(Chaos/헬스) + 추세(주간 메트릭)**를
**Prometheus → Grafana 단일 대시보드 1장**으로 10초 안에 읽게 만든다.

## 1) 현재 시스템 분석 (지피지기)

### ✅ 이미 구축된 인프라
- **Prometheus**: AFO Kingdom API /metrics 스크레이핑 중
- **Grafana**: 4개 대시보드 존재 (afo-kingdom-overview, trinity-score-dashboard 등)
- **CI/CD**: Phase 3-4 메트릭 수집 시스템 완성
- **Alert Rules**: monitoring/alert_rules.yml 존재

### 📊 현재 메트릭 소스
- **Phase 3-4 메트릭**: docs/reports/_metrics/weekly_metrics.json
- **API 메트릭**: /metrics 엔드포인트 (FastAPI)
- **시스템 메트릭**: Node Exporter, Redis, cAdvisor

## 2) 아키텍처 청사진 (Pushgateway 옵션 선택)

### 데이터 흐름
```
1. GitHub Actions CI 산출물(JSON/MD)
   ↓
2. Pushgateway에 메트릭 전송
   ↓
3. Prometheus 스크레이핑
   ↓
4. Grafana 대시보드 표시
   ↓
5. Alerting (선택적)
```

### 컴포넌트 상세

#### A) CI 메트릭 수집기 (scripts/emit_ci_metrics.py)
**역할**: CI 결과를 Prometheus text format으로 변환
```python
# CI에서 실행되는 스크립트
def emit_prometheus_metrics():
    # SSOT 위반 카운트
    print(f"afo_report_ssot_gate_fail_total {ssot_failures}")

    # 영어 비율 게이지
    print(f"afo_report_english_ratio {english_ratio}")

    # Chaos 성공률
    print(f"afo_chaos_nightly_success {chaos_success}")

    # Pushgateway로 전송
    push_to_gateway('pushgateway:9091', job='afo-ci-metrics')
```

#### B) Pushgateway (Docker 컨테이너)
**설정**: docker-compose.monitoring.yml에 추가
```yaml
pushgateway:
  image: prom/pushgateway:v1.6.0
  ports:
    - "9091:9091"
  networks:
    - monitoring
```

#### C) Prometheus 설정 확장
**파일**: monitoring/prometheus.yml
```yaml
# 기존 설정 유지 + Pushgateway 추가
- job_name: 'afo-ci-metrics'
  static_configs:
    - targets: ['pushgateway:9091']
  honor_labels: true
```

#### D) Grafana 대시보드 신규 생성
**파일**: monitoring/grafana/dashboards/afo-observability-conscience.json

## 3) 메트릭 모델링 (SSOT 준수)

### 보고 품질 메트릭
| 메트릭 이름 | 타입 | 설명 | 단위 |
|-------------|------|------|------|
| `afo_report_ssot_gate_fail_total` | Counter | SSOT 검증 실패 횟수 | count |
| `afo_report_english_ratio` | Gauge | 영어 비율 (0-1) | ratio |
| `afo_report_completion_claim_block_total` | Counter | 금지어 사용 차단 횟수 | count |

### PR 리스크 메트릭
| 메트릭 이름 | 타입 | 설명 | 단위 |
|-------------|------|------|------|
| `afo_pr_risk_score` | Gauge | PR 위험 점수 (0-100) | score |
| `afo_pr_risk_level` | Gauge | 위험 레벨 (1=Low, 2=Medium, 3=High) | level |

### Chaos 안정성 메트릭
| 메트릭 이름 | 타입 | 설명 | 단위 |
|-------------|------|------|------|
| `afo_chaos_nightly_success` | Gauge | 최근 Chaos 테스트 성공 (0/1) | boolean |
| `afo_chaos_selfheal_seconds` | Histogram | 자가 치유 소요 시간 | seconds |

### Phase 5 적응형 임계값
| 메트릭 이름 | 타입 | 설명 | 단위 |
|-------------|------|------|------|
| `afo_threshold_english_warn` | Gauge | 영어 경고 임계값 | ratio |
| `afo_threshold_risk_crit` | Gauge | 위험 Critical 임계값 | score |

## 4) 대시보드 설계 (10초 읽기 목표)

### 섹션 1: "실시간 상태" (상단, 가장 중요)
```
┌─────────────────────────────────────────────────────────────┐
│  🔴 SSOT Gate Status    🟡 영어 비율   🔵 PR 위험도   🟢 Chaos   │
│  [PASS/FAIL + 카운트]   [XX% + 추세]   [XX점 + 레벨]   [성공/실패] │
└─────────────────────────────────────────────────────────────┘
```

### 섹션 2: "품질 추세" (중간)
```
┌─────────────────────────────────────────────────────────────┐
│  📈 영어 비율 30일 추세    📉 SSOT 준수율 30일 추세         │
│  [선 그래프]               [막대 그래프]                     │
└─────────────────────────────────────────────────────────────┘
```

### 섹션 3: "시스템 건강" (하단)
```
┌─────────────────────────────────────────────────────────────┐
│  🏥 API 응답시간    💾 메모리 사용량    🔄 Chaos 안정성      │
│  [히스토그램]       [게이지]            [업타임 %]           │
└─────────────────────────────────────────────────────────────┘
```

## 5) 알림 전략 (선택적)

### Grafana Alerting 룰
```yaml
# 영어 비율 경고
alert: HighEnglishRatio
expr: afo_report_english_ratio > afo_threshold_english_warn
for: 5m
labels:
  severity: warning

# Chaos 실패 알림
alert: ChaosFailure
expr: afo_chaos_nightly_success == 0
for: 10m
labels:
  severity: critical
```

## 6) 구현 로드맵

### Phase 5-1: 인프라 준비 (1일)
- [ ] Pushgateway Docker 구성 추가
- [ ] Prometheus 설정 확장
- [ ] CI 메트릭 수집기 스크립트 작성

### Phase 5-2: 메트릭 모델링 (1일)
- [ ] 메트릭 이름 SSOT 문서 작성
- [ ] CI 워크플로우에 메트릭 전송 추가
- [ ] 테스트 데이터 수집

### Phase 6-1: 대시보드 디자인 (2일)
- [ ] Grafana 대시보드 JSON 설계
- [ ] PromQL 쿼리 작성 및 테스트
- [ ] 왕국 테마 적용

### Phase 6-2: 알림 및 최적화 (1일)
- [ ] Alerting 룰 설정
- [ ] 대시보드 성능 최적화
- [ ] 문서화 및 검증

## 7) 성공 기준

- [ ] **10초 읽기**: 대시보드에서 주요 지표를 10초 안에 파악 가능
- [ ] **실시간성**: CI 결과가 대시보드에 즉시 반영
- [ ] **직관성**: 위험도별 색상 코딩 (🔴🟡🟢)
- [ ] **확장성**: 새로운 메트릭 추가가 용이

## 8) 위험 요소 및 완화

### 위험 1: 메트릭 폭증
**완화**: 메트릭 이름 SSOT 준수 + 주기적 정리

### 위험 2: Pushgateway 장애
**완화**: Graceful degradation (CI 실패해도 메인 기능 영향 없음)

### 위험 3: 대시보드 복잡도
**완화**: 1장 대시보드 원칙 + 드릴다운 링크

---

*이 청사진은 실제 구현 전 설계 검토를 위한 문서입니다.*