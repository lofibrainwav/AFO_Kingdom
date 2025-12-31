# MIPROv2 Chancellor Graph Operational Runbook

## 🎯 목적
MIPROv2 Bayesian 최적화를 Chancellor Graph에 안전하게 통합하고 운영하기 위한 가이드

## 🔒 기본 원칙

### 1. 기본값 OFF 유지 (Safety First)
```bash
# 기본값: 완전 NO-OP, 시스템 영향 없음
export AFO_MIPRO_V2_ENABLED=0
export AFO_MIPRO_ENABLED=0
export AFO_MIPRO_CHANCELLOR_ENABLED=0
```

### 2. ON은 실험/튜닝 세션에서만
```bash
# ON: MIPROv2 최적화 활성화 (실험용)
export AFO_MIPRO_V2_ENABLED=1
export AFO_MIPRO_ENABLED=1
export AFO_MIPRO_CHANCELLOR_ENABLED=1
```

### 3. 즉시 롤백 규칙
장애/비용/지연 발생 시 **즉시 OFF → 재시작**:
```bash
# 즉시 롤백
export AFO_MIPRO_V2_ENABLED=0 AFO_MIPRO_ENABLED=0 AFO_MIPRO_CHANCELLOR_ENABLED=0
# 서비스 재시작 (필요시)
```

## 📊 모니터링 메트릭

### 필수 메트릭 (로그에서 확인)
- `mipro.enabled`: 0(OFF) 또는 1(ON)
- `mipro.trials`: 수행된 최적화 시도 횟수

### 권장 메트릭
- `mipro.best_score`: 최적화된 최고 점수
- `mipro.execution_time`: 최적화 소요 시간

## 🚨 장애 대응

### 증상: API latency 증가
```bash
# 즉시 OFF
export AFO_MIPRO_V2_ENABLED=0 AFO_MIPRO_ENABLED=0 AFO_MIPRO_CHANCELLOR_ENABLED=0
# 재시작
```

### 증상: Graph state 오염
```bash
# MIPRO 노드 출력을 확인
# _mipro 필드에 요약 데이터만 있는지 검증
```

### 증상: 비용 증가
```bash
# 즉시 OFF + 비용 모니터링
# Bayesian 최적화 비용 vs 성능 이득 평가
```

## ✅ 건강 체크

### OFF 상태 확인 (기본값)
```bash
env -i PATH="$PATH" AFO_MIPRO_V2_ENABLED=0 AFO_MIPRO_ENABLED=0 AFO_MIPRO_CHANCELLOR_ENABLED=0 \
  poetry run python -c "from AFO.api.chancellor_v2.graph.runner import run_graph; print('MIPRO OFF OK')"
```

### ON 상태 확인 (실험용)
```bash
env -i PATH="$PATH" AFO_MIPRO_V2_ENABLED=1 AFO_MIPRO_ENABLED=1 AFO_MIPRO_CHANCELLOR_ENABLED=1 \
  poetry run python -c "from AFO.api.chancellor_v2.graph.runner import run_graph; print('MIPRO ON OK')"
```

## 🎯 다음 단계 옵션

### A) 튜닝 품질 향상
- 실제 DSPy compile loop 점진적 통합
- 타임아웃/샘플 수 제한 포함

### B) 운영 안전 강화
- ON일 때 별도 워커/잡으로 실행
- API latency 영향 0 만들기

### C) 리포트 자동화
- `_mipro` 요약을 하루 1회 자동 기록
- Slack/Notion 연동

---

## 📝 변경 이력
- 2025-12-30: MIPROv2 Chancellor Graph 연결 완료
- 운영 런북 작성 및 안전 가이드라인 수립
