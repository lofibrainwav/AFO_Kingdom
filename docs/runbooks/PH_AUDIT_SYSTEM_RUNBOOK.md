# 📊 PH-AUDIT: 시스템 감사 및 최적화 런북

## 🎯 목적
왕국 운영 상태를 체계적으로 감사하고, 리스크를 숫자로 고정하여 프로덕션 안정성 확보

## 📋 감사 체크리스트

### 1. 코드 품질 게이트 (眞)
- [ ] `make lint` - Ruff linting (S104 제외 - Docker용 의도적)
- [ ] `make type-check` - MyPy 타입 체크  
- [ ] `make test` - 단위 테스트 (284/284 통과 목표)
- [ ] `pnpm build` - Dashboard 빌드 성공

### 2. 인프라 건강 (善) 
- [ ] Core Services: Soul Engine (8010), Dashboard (3000)
- [ ] Data Services: PostgreSQL (15432), Redis (6379) 
- [ ] AI Services: Ollama (11435)
- [ ] Wallet Services: API Wallet (8011)

### 3. 보안 감사 (善)
- [ ] Vault KMS: fail-closed 정책 준수
- [ ] API Keys: 환경별 적절한 격리
- [ ] SSE Auth: Bearer token + Rate limit
- [ ] Secrets: REDACT 적용 확인

### 4. 성능/관측 (孝)
- [ ] Metrics: Prometheus /health + /metrics 노출
- [ ] Alerts: SSE 관련 4개 규칙 활성화
- [ ] Logs: SSE 이벤트 스트리밍 정상
- [ ] Trinity Score: 1.0 유지

### 5. 비용/효율 (善)
- [ ] Docker: 불필요한 컨테이너 정리
- [ ] Dependencies: 보안 취약점 0개
- [ ] CI/CD: 빌드 시간 최적화
- [ ] Storage: artifacts/ 정리

## 🚀 실행 가이드

### Quick Audit (5분)
```bash
# 1. 코드 품질
make lint type-check test

# 2. 서비스 상태  
docker compose ps

# 3. API 건강
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/metrics | head -20
```

### Full Audit (15분)
```bash
# 1. 종합 게이트
make pre-push

# 2. 보안 스캔
./packages/afo-core/scripts/ph19_security_sweep.sh

# 3. SSE 종단간 테스트
curl -H "Authorization: Bearer $AFO_INTERNAL_API_KEY" \
     http://127.0.0.1:8010/api/system/sse/health
```

## 📊 감사 결과 템플릿

### 상태 분류
- 🟢 GREEN: 모든 게이트 통과
- 🟡 YELLOW: 경미한 경고 (운영 영향 없음)  
- 🔴 RED: 즉시 조치 필요

### Trinity Score 기반 평가
```
眞 (코드 품질): __/100
善 (보안/안정): __/100  
美 (성능/UX): __/100
孝 (운영 편의): __/100
永 (재현성): __/100
총점: __/500 (목표: 450+)
```

## 🔧 최적화 우선순위

1. **긴급**: 보안 취약점 패치
2. **중요**: 성능 병목 해소  
3. **개선**: 비용 최적화
4. **예방**: 모니터링 강화

## 📞 비상 대응

- **빌드 실패**: `make clean && make build`
- **서비스 다운**: `docker compose restart`  
- **메트릭 이상**: Alertmanager 확인
- **보안 경고**: 즉시 패치 적용

---

**감사자**: 승상 (AFO Kingdom)
**날짜**: 2025-12-28
**버전**: PH-AUDIT-001
