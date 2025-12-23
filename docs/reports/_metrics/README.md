# AFO Kingdom Metrics & History

이 디렉토리는 AFO 왕국의 주요 메트릭과 히스토리를 주간 단위로 누적하여 저장합니다.

## 메트릭 종류

### 1. 영어 비율 메트릭 (English Ratio Metrics)
- **소스**: `scripts/detect_english_ratio.py`
- **실행 시점**: PR에서 CI 실행 시
- **목적**: 영어 과다 사용 경고 및 습관 교정 추적
- **저장**: `english_ratio_weekly_[YYYY-WW].json`

### 2. SSOT 위반 메트릭 (SSOT Violation Metrics)
- **소스**: `scripts/ssot_report_gate.py`
- **실행 시점**: PR에서 CI 실행 시
- **목적**: 보고서 품질 게이트 준수율 추적
- **저장**: `ssot_violations_weekly_[YYYY-WW].json`

### 3. Chaos 테스트 메트릭 (Chaos Test Metrics)
- **소스**: Nightly Chaos Lite 워크플로우
- **실행 시점**: 매일 LA 09:30 (UTC 17:30/16:30)
- **목적**: 시스템 자가 치유 능력 추적
- **저장**: `chaos_lite_weekly_[YYYY-WW].json`

## 저장 형식

### JSON 형식 (구조화 데이터)
```json
{
  "week": "2025-W01",
  "period": {
    "start": "2025-01-06",
    "end": "2025-01-12"
  },
  "metrics": {
    "english_ratio": {
      "total_reports": 15,
      "high_ratio_reports": 2,
      "avg_ratio": 0.23,
      "max_ratio": 0.67
    },
    "ssot_violations": {
      "total_prs": 12,
      "violations": 1,
      "compliance_rate": 0.917
    },
    "chaos_tests": {
      "total_runs": 7,
      "success_rate": 1.0,
      "avg_recovery_time": 45.2
    }
  },
  "trends": {
    "english_ratio_trend": "decreasing",
    "compliance_trend": "stable",
    "chaos_stability": "excellent"
  }
}
```

### Markdown 형식 (가독성 보고서)
자동 생성되는 주간 요약 보고서

## 자동화

- **수집**: CI 워크플로우에서 자동 실행
- **저장**: Git에 커밋되어 영구 보존
- **보고**: 주간 단위로 MD 보고서 생성

## 사용 목적

1. **품질 추세 분석**: 시간에 따른 개선 추이
2. **문제 조기 발견**: 이상 패턴 식별
3. **문화 형성**: 팀의 SSOT 준수 문화 정착 증거