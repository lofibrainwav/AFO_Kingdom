# AFO Kingdom Metrics SSOT (Single Source of Truth)

## 0) 메트릭 네이밍 원칙

### 네이밍 컨벤션
```
afo_{domain}_{subdomain}_{metric_name}_{suffix}
```

- **afo**: AFO Kingdom 접두어 (필수)
- **domain**: 주요 도메인 (report, pr, chaos, threshold, system)
- **subdomain**: 세부 영역 (없으면 생략)
- **metric_name**: 메트릭 의미
- **suffix**: 메트릭 타입 (_total, _ratio, _score 등)

### 예시
```bash
# 올바른 네이밍
afo_report_ssot_gate_fail_total     # SSOT 실패 카운트
afo_report_english_ratio           # 영어 비율 게이지
afo_pr_risk_score                  # PR 위험 점수
afo_chaos_nightly_success          # Chaos 성공 여부

# 잘못된 네이밍
ssot_failures                      # afo_ 접두어 없음
afo_english_ratio_reports          # 순서 틀림
report_afo_ssot_fail               # 컨벤션 위반
```

## 1) 보고 품질 메트릭

### SSOT 준수 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_report_ssot_gate_fail_total` | Counter | SSOT 검증 실패 누적 횟수 | 0~∞ | count | `repo`, `branch` |
| `afo_report_ssot_compliance_rate` | Gauge | SSOT 준수율 (최근 30일) | 0.0~1.0 | ratio | `repo` |
| `afo_report_completion_claim_block_total` | Counter | 금지어("완료"/"구현됨") 차단 누적 횟수 | 0~∞ | count | `repo`, `word` |

### 영어 비율 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_report_english_ratio` | Gauge | 보고서 영어 비율 | 0.0~1.0 | ratio | `repo`, `file` |
| `afo_report_english_ratio_high_total` | Counter | 영어 비율 50% 초과 보고서 수 | 0~∞ | count | `repo` |
| `afo_report_english_ratio_avg` | Gauge | 평균 영어 비율 (주간) | 0.0~1.0 | ratio | `repo` |

### 보고서 템플릿 준수
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_report_template_compliance` | Gauge | 템플릿 준수율 | 0.0~1.0 | ratio | `repo` |
| `afo_report_template_violations_total` | Counter | 템플릿 위반 누적 횟수 | 0~∞ | count | `repo`, `violation_type` |

## 2) PR 리스크 메트릭

### 리스크 점수 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_pr_risk_score` | Gauge | PR 위험 점수 (종합) | 0~100 | score | `repo`, `pr_number` |
| `afo_pr_risk_level` | Gauge | 위험 레벨 (1=Low, 2=Medium, 3=High, 4=Critical) | 1~4 | level | `repo`, `pr_number` |
| `afo_pr_risk_trend` | Gauge | 리스크 추세 (-1=감소, 0=유지, 1=증가) | -1~1 | trend | `repo` |

### 리스크 요인별 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_pr_changes_lines_total` | Counter | 변경 라인 수 | 0~∞ | lines | `repo`, `pr_number` |
| `afo_pr_files_modified` | Gauge | 수정 파일 수 | 0~∞ | files | `repo`, `pr_number` |
| `afo_pr_reviewers_count` | Gauge | 리뷰어 수 | 0~∞ | count | `repo`, `pr_number` |

## 3) Chaos 안정성 메트릭

### 테스트 결과 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_chaos_nightly_success` | Gauge | 최근 Chaos 테스트 성공 여부 | 0/1 | boolean | `test_type` |
| `afo_chaos_nightly_fail_total` | Counter | Chaos 테스트 실패 누적 횟수 | 0~∞ | count | `test_type` |
| `afo_chaos_success_rate` | Gauge | Chaos 성공률 (최근 7일) | 0.0~1.0 | ratio | `test_type` |

### 자가 치유 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_chaos_selfheal_seconds` | Histogram | 자가 치유 소요 시간 | 0~∞ | seconds | `pod_name`, `failure_type` |
| `afo_chaos_recovery_success_total` | Counter | 성공적 자가 치유 누적 횟수 | 0~∞ | count | `component` |
| `afo_chaos_recovery_fail_total` | Counter | 자가 치유 실패 누적 횟수 | 0~∞ | count | `component` |

## 4) Phase 5 적응형 임계값 메트릭

### 영어 비율 임계값
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_threshold_english_warn` | Gauge | 영어 경고 임계값 (적응형) | 0.0~1.0 | ratio | `repo` |
| `afo_threshold_english_crit` | Gauge | 영어 위험 임계값 (적응형) | 0.0~1.0 | ratio | `repo` |

### PR 리스크 임계값
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_threshold_risk_warn` | Gauge | 리스크 경고 임계값 (적응형) | 0~100 | score | `repo` |
| `afo_threshold_risk_crit` | Gauge | 리스크 위험 임계값 (적응형) | 0~100 | score | `repo` |

### SSOT 준수 임계값
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_threshold_ssot_min_compliance` | Gauge | 최소 SSOT 준수율 (적응형) | 0.0~1.0 | ratio | `repo` |

## 5) 시스템 메트릭 (기존 인프라 통합)

### API 성능 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_api_http_requests_total` | Counter | HTTP 요청 총수 | 0~∞ | count | `method`, `endpoint`, `status` |
| `afo_api_http_request_duration_seconds` | Histogram | HTTP 요청 응답 시간 | 0~∞ | seconds | `method`, `endpoint` |
| `afo_api_http_requests_in_flight` | Gauge | 진행 중 요청 수 | 0~∞ | count | `endpoint` |

### 데이터베이스 메트릭
| 메트릭 이름 | 타입 | 설명 | 값 범위 | 단위 | 레이블 |
|-------------|------|------|---------|------|--------|
| `afo_db_connections_active` | Gauge | 활성 DB 연결 수 | 0~∞ | count | `db_name` |
| `afo_db_query_duration_seconds` | Histogram | 쿼리 실행 시간 | 0~∞ | seconds | `query_type` |
| `afo_db_connection_pool_size` | Gauge | 연결 풀 크기 | 0~∞ | count | `db_name` |

## 6) 메트릭 수집 및 전송 규칙

### CI 메트릭 전송 규칙
```bash
# Pushgateway URL
PUSHGATEWAY_URL="http://pushgateway:9091"

# 메트릭 전송 예시
curl -X POST "${PUSHGATEWAY_URL}/metrics/job/afo-ci-metrics" \
  --data-binary @- << EOF
# HELP afo_report_ssot_gate_fail_total SSOT 검증 실패 횟수
# TYPE afo_report_ssot_gate_fail_total counter
afo_report_ssot_gate_fail_total{repo="lofibrainwav/AFO_Kingdom"} 5

# HELP afo_report_english_ratio 보고서 영어 비율
# TYPE afo_report_english_ratio gauge
afo_report_english_ratio{repo="lofibrainwav/AFO_Kingdom"} 0.23
EOF
```

### 메트릭 만료 정책
- **Counter**: 영구 유지 (누적 값)
- **Gauge**: 24시간 유지 (현재 상태)
- **Histogram**: 7일 유지 (통계 데이터)

### 메트릭 정리 규칙
- 매주 일요일 02:00 UTC에 오래된 메트릭 정리
- Prometheus의 `--storage.tsdb.retention.time=30d` 적용

## 7) PromQL 쿼리 표준

### 주요 대시보드 쿼리
```promql
# SSOT 준수율 (최근 30일)
rate(afo_report_ssot_gate_fail_total[30d]) / rate(afo_report_ssot_gate_total[30d]) * 100

# 영어 비율 추세 (7일 이동평균)
avg_over_time(afo_report_english_ratio[7d])

# PR 리스크 분포
histogram_quantile(0.95, rate(afo_pr_risk_score_bucket[1h]))

# Chaos 성공률
afo_chaos_nightly_success == 1
```

### 알림 쿼리
```promql
# 영어 비율 경고
afo_report_english_ratio > afo_threshold_english_warn

# SSOT 준수율 저하
afo_report_ssot_compliance_rate < afo_threshold_ssot_min_compliance

# Chaos 연속 실패
up == 0 and afo_chaos_nightly_success == 0
```

## 8) 메트릭 모니터링 및 유지보수

### 메트릭 건강 체크
- 매일 06:00 UTC: 메트릭 수집 상태 확인
- 메트릭이 1시간 이상 업데이트되지 않으면 경고
- Pushgateway 재시작 시 메트릭 복원 확인

### 메트릭 추가 승인 프로세스
1. `docs/architecture/METRICS_SSOT.md`에 추가 요청
2. 메트릭 이름 컨벤션 검토
3. 중복 메트릭 존재 확인
4. 대시보드 영향 평가
5. 승인 후 구현

### 메트릭 폐기 프로세스
1. 사용하지 않는 메트릭 식별
2. 대시보드/알림 영향 평가
3. 30일 유예 기간 설정
4. 메트릭 폐기 및 문서 업데이트

---

*이 문서는 AFO Kingdom 메트릭의 Single Source of Truth입니다. 모든 메트릭 추가/변경은 이 문서를 통해 관리됩니다.*