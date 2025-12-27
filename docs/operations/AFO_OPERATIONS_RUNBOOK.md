# AFO Kingdom 운영 런북 (Operations Runbook)

**As-of: 2025-12-27**  
**Version: 1.0**  
**Based on: EXP_007 Rollback Drill (45s TTR)**

## 📋 목적

장애 발생 시 **60초 내 판정 + 5분 내 복구**를 보장하는 표준 운영 절차.  
**"기술 문제"가 아니라 "사람의 기억 문제"를 방지**하는 것이 핵심.

---

## 🎯 핵심 원칙

1. **관측 먼저, 추측 금지**: 증거 없이는 "될 것 같다" 금지
2. **보안 가드 우선**: 권한/시크릿 문제는 즉시 BLOCK
3. **롤백 준비**: 모든 변경은 "5분 내 되돌릴 수 있는" 상태에서만 실행
4. **시간 제한 준수**: 60초 관측 → 5분 판정 → 10분 복구

---

## 🔍 1. 관측 단계 (60초 - Evidence Collection)

### 1.1 헬스 체크 (10초)

```bash
# 동시 실행
curl -sS http://localhost:8010/api/health &
curl -sS http://localhost:8001/health &
curl -sS http://localhost:3000/ &
wait
```

**정상 기준:**
- 8010: HTTP 200
- 8001: HTTP 200
- 3000: HTTP 200

### 1.2 보안 가드 체크 (20초)

```bash
# 동시 실행 - 시크릿 설정 확인
curl -sS http://localhost:8010/api/revalidate/status &
curl -sS -H "X-Internal-Secret: WRONG" http://localhost:8010/api/revalidate/status &
curl -sS -H "X-Internal-Secret: ${AFO_INTERNAL_SECRET}" http://localhost:8010/api/revalidate/status &
wait
```

**정상 기준:**
- unauth: 401 (또는 503)
- wrong: 401 (또는 503)
- auth: 200

### 1.3 SSE 스트림 체크 (20초)

```bash
curl -sS -N --max-time 10 "http://localhost:8010/api/thoughts/sse" > /tmp/sse_check.txt || true
wc -c < /tmp/sse_check.txt
```

**정상 기준:**
- 바이트 수 > 0 (heartbeat 포함)

### 1.4 컨테이너 상태 (10초)

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

**정상 기준:**
- 모든 컨테이너 Up 상태
- 포트 매핑 정상

---

## 🏥 2. 판정 단계 (5분 - Decision Making)

### 2.1 문제 분류

| 증상 | 원인 가능성 | 우선순위 | 대응 |
|------|------------|---------|------|
| 헬스 200 → 보안 401 유지 | 정상 | - | 모니터링 지속 |
| 헬스 200 → 보안 200 | 시크릿 누락 | 🚨 즉시 | 롤백 실행 |
| 헬스 5xx | 서비스 다운 | 🚨 즉시 | 재시작 시도 |
| SSE 0 bytes | heartbeat 실패 | 🔶 5분 | 재시작 검토 |
| 컨테이너 Exit | 크래시 | 🚨 즉시 | 로그 확인 후 재시작 |

### 2.2 증거 기록

**모든 판정은 로그로 기록:**

```bash
echo "$(date): INCIDENT - $(증상 요약)" >> /var/log/afo-incidents.log
echo "Evidence: $(관측 결과 요약)" >> /var/log/afo-incidents.log
echo "Decision: $(판정 결과)" >> /var/log/afo-incidents.log
```

---

## 🔄 3. 복구 단계 (10분 - Recovery Actions)

### 3.1 롤백 우선 (보안 문제 시)

```bash
# EXP_007 기반 - 45초 롤백
T0=$(date +%s)

# 1. 현재 서버 중지 (5초)
if docker ps | grep -q afo-core; then
  docker restart $(docker ps -q --filter name=afo-core)
else
  kill $(ps aux | grep AFO.api_server | grep -v grep | awk '{print $2}')
fi

# 2. 환경변수 재설정 (5초)
export AFO_INTERNAL_SECRET="AFO_SECURE_SECRET_2025"

# 3. 클린 재시작 (30초)
cd packages/afo-core
python -m AFO.api_server &
sleep 30

# 4. 복구 검증 (5초)
curl -sS http://localhost:8010/api/health
curl -sS -H "X-Internal-Secret: ${AFO_INTERNAL_SECRET}" http://localhost:8010/api/revalidate/status

T1=$(date +%s)
echo "Rollback completed in $((T1-T0)) seconds"
```

### 3.2 서비스 재시작 (일반 문제 시)

```bash
# Docker Compose 사용 시
docker compose restart afo-core

# 또는 직접 재시작
cd packages/afo-core
python -m AFO.api_server
```

### 3.3 모니터링 복구 확인

**롤백 후 60초 관측 재실행** (1번 단계 반복)

---

## 📊 4. 사후 처리 (Post-Incident)

### 4.1 로그 분석

```bash
# 최근 1시간 로그
docker logs --since 1h afo-core 2>&1 | grep -i error

# SSE heartbeat 확인
grep "heartbeat" /var/log/afo-*.log
```

### 4.2 근본 원인 기록

**반드시 GitHub Issue 생성:**

```markdown
## Incident Report

**Time:** $(date)
**Duration:** X분
**Impact:** 서비스 다운타임 Y분
**Root Cause:** [시크릿 누락|컨테이너 크래시|SSE heartbeat 실패]
**Evidence:** [로그 링크|스크린샷]
**Resolution:** [롤백|재시작|패치 적용]
**Prevention:** [환경변수 표준화|모니터링 강화|테스트 추가]
```

### 4.3 재발 방지

- **시크릿 문제**: `.env.afo` + `docker-compose.yml` env_file 적용 확인
- **컨테이너 문제**: healthcheck 추가 검토
- **SSE 문제**: heartbeat 로그 모니터링 추가

---

## 🎯 5. 긴급 연락처

| 역할 | 연락처 | 역할 |
|------|-------|------|
| 사령관 | 형님 | 최종 결정권자 |
| 승상 | AI Assistant | 자동 판정/롤백 |
| 집현전 | 개발팀 | 수동 개입 필요 시 |

---

## 📈 6. 성능 지표

**목표 (월별):**
- MTTR (Mean Time To Recovery): < 5분
- 가용성: > 99.9%
- 보안 인시던트: 0건
- 자동 복구율: > 95%

**모니터링:**
```bash
# 주간 리포트 생성
grep "INCIDENT\|RECOVERY" /var/log/afo-*.log | tail -20
```

---

**이 런북은 EXP_007의 45초 롤백 실험 결과를 기반으로 작성되었습니다.**  
**모든 장애 대응은 이 절차를 따릅니다.**