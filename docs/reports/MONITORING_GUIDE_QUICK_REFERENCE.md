# 모니터링 통합 가이드 초간결 요약 (Quick Reference)

**As-of**: 2025-12-24  
**Status**: 완료됨 (핵심 섹션만)  
**SSOT 원칙 준수**: 팩트 기반, 제안 명시

---

## 최종 구조 (제안 명시)

### 1. structlog 통합 (제안)
- 구조화 로깅 (JSON 출력, 컨텍스트 바인딩)
- 설치: `poetry add structlog`
- 기본 설정: `logging_config.py` 수정

### 2. structlog + Sentry 통합 (제안)
- 에러 트래킹 + 구조화 로깅
- 설치: `poetry add structlog structlog-sentry sentry-sdk`
- SentryProcessor 통합

### 3. FastAPI Middleware 예시 (제안)
- LoggingMiddleware (structlog 컨텍스트 + Sentry tracing)
- CORS Middleware

### 4. Error Handling 예시 (제안)
- 글로벌 에러 핸들러 (Pydantic ValidationError, 일반 Exception)
- 엔드포인트 에러 처리

### 5. Unit Test Cases (제안)
- 테스트 파일: `tests/test_revalidate.py`
- 실행: `pytest -v tests/test_revalidate.py --cov=api`

### 6. 고급 설정 (제안)
- Processors 체인 (add_log_level, TimeStamper, JSONRenderer)
- Context Binding (structlog.contextvars)
- Custom Processor

### 7. 성능 최적화 (제안)
- AsyncRenderer (비동기 로깅)
- Cache Logger (`cache_logger_on_first_use=True`)
- Processors 최소화

### 8. 성능 벤치마크 (제안)
- AsyncRenderer 벤치마크 (공식 문서 참조)
- Sentry 벤치마크 (공식 문서 참조)

### 9. 시각화 참고 자료
- Sentry Performance 대시보드
- 인터랙티브 그래프 라이브러리 (Recharts, Plotly, ECharts, Chart.js, D3.js)

### 10. Datadog Tracing 통합 (제안)
- **Custom Metrics (제안)**: Count, Gauge, Distribution, Histogram, Set
- **9.1 Datadog Tracing Code Examples (제안)**: 초기화, 자동 Tracing, 커스텀 Span, 태그/컨텍스트, 에러 처리
- **9.2 Datadog APM Integration Details (제안)**: 설치, 기본 초기화, Next.js 통합, 커스텀 Span, 환경 변수
- **9.3 Datadog Metrics Alerting Setup (제안)**: Monitor 생성, 쿼리/조건 설정, 알림 채널, Multi-Alert, Thresholds
- **9.4 Datadog Anomaly Detection (제안)**: Algorithm, Deviation Bands, Window, Alert Conditions, Recovery
- **9.5 Outlier Detection Comparison (제안)**: Datadog, Sentry, Prometheus+Grafana, Elastic ML, Splunk ML 비교
- **9.6 Cost-Benefit Analysis (제안)**: Sentry, Datadog, Prometheus+Grafana, Thanos, Grafana Cloud 비용/이점
- **9.7 Detailed ROI Calculations (제안)**: ROI 계산 가정, 테이블, 계산 세부, 왕국 적용 추천

### 11. Prometheus 메트릭스 통합 (제안)
- **Grafana Dashboard 가이드 (제안)**:
  - **11.1 Dashboard Panel List**: Timeseries, Gauge, Stat, Heatmap, Table, Bar Gauge, Pie Chart, Logs
  - **11.2 Timeseries Panel**: Graph Style, Legend, Tooltip, Axis, Thresholds, Fill/Gradient, Stacking
  - **11.3 Heatmap Panel**: Data Format, Color Mode, Y-Axis Buckets, X-Axis, Cell Values, Tooltip, Legend
  - **11.4 Stat Panel**: Value Mode, Color Mode, Thresholds, Sparkline, Unit/Decimals, Text Size, Orientation
  - **11.5 Grafana Alerting Features**: Alert Rules, Notification Policies, Contact Points
  - **11.6 Prometheus Alertmanager**: Alert Rules, Routing, Inhibition, Silencing
  - **11.7 Prometheus Federation Setup**: Hierarchical metrics collection, `prometheus.yml` configuration
  - **11.8 Advanced match[] Filters**: Federation 필터링
  - **11.9 Grafana Federation Dashboard**: Multi-cluster visualization
  - **11.10 Thanos for Long-term Storage**: Sidecar, Store Gateway, Query, Compactor, docker-compose.yml, s3.yaml
  - **11.11 Thanos Downsampling Techniques**: Raw, 5m, 1h downsampling
  - **11.12 Grafana Dashboard Examples 확장**: 통합 예시

---

## 참고 자료 (공식 문서)

- structlog: https://www.structlog.org
- Sentry Python SDK: https://docs.sentry.io/platforms/python/
- Datadog Tracing: https://docs.datadoghq.com/tracing/
- Datadog Monitors: https://docs.datadoghq.com/monitors/
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/grafana/latest/

---

## 다음 단계 (왕국 확장)

- **즉시**: 초간결 요약 문서 적용 (커밋)
- **단기**: Ticket 82 – 초간결 구조 기반 문서 리뷰
- **중기**: 전체 가이드 Grafana 대시보드 연계

---

**참고**: 전체 상세 가이드는 `docs/reports/STRUCTLOG_SENTRY_INTEGRATION_GUIDE_SSOT.md` 참조

