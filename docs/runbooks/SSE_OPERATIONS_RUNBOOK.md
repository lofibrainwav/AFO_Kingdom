# SSE Operations Runbook

## 개요

AFO 왕국의 실시간 신경 연결(Server-Sent Events) 운영 가이드입니다.
브라우저와 서버 간 실시간 로그 스트리밍을 유지하고 모니터링하는 방법을 설명합니다.

## 아키텍처

```
브라우저 ← EventSource → Dashboard ← rewrites → Soul Engine SSE
   ↓                        ↓                      ↓
SSEHealthWidget → /api/system/sse/health → Prometheus Metrics
```

## 모니터링 메트릭

### 핵심 메트릭

- `afo_sse_open_connections`: 현재 활성화된 SSE 연결 수
- `afo_sse_reconnect_count_total`: 누적 재연결 시도 횟수
- `afo_sse_last_event_age_seconds`: 마지막 이벤트로부터 경과 시간
- `afo_sse_connection_status{status="healthy|stale|down"}`: 연결 상태

### 대시보드 위젯

Royal Governance 페이지에서 SSE Health 위젯으로 실시간 상태 확인:
- 🟢 **OK**: 정상 연결 (마지막 이벤트 < 30초)
- 🟡 **STALE**: 지연 상태 (30-60초)
- 🔴 **DOWN**: 연결 끊김 (60초 초과)

## 알림 규칙

### 🚨 Critical Alerts (즉시 대응)

#### SSEConnectionDown
```
조건: afo_sse_connection_status{status="down"} == 1 (2분 이상)
대응:
1. Dashboard 브라우저 콘솔 확인: EventSource 에러 메시지
2. Soul Engine 로그 확인: SSE 스트림 중단 여부
3. 네트워크 연결 상태 확인
4. 브라우저 캐시 클리어 및 재접속
```

#### SSEZeroConnections
```
조건: afo_sse_open_connections == 0 (5분 이상)
대응:
1. Dashboard 서비스 상태 확인
2. SSEHealthWidget 렌더링 여부 확인
3. 브라우저 JavaScript 에러 확인
4. Soul Engine /api/logs/stream 엔드포인트 테스트
```

### ⚠️ Warning Alerts (주의)

#### SSEConnectionStale
```
조건: afo_sse_connection_status{status="stale"} == 1 (1분 이상)
대응:
1. 네트워크 지연 확인
2. Soul Engine CPU/메모리 사용량 확인
3. 이벤트 전송 빈도 확인
```

#### SSEHighReconnectRate
```
조건: rate(afo_sse_reconnect_count_total[5m]) > 0.5 (3분 이상)
대응:
1. 네트워크 불안정 여부 확인
2. 브라우저 탭 다중 오픈 여부 확인
3. EventSource 구현 버그 확인
```

## 문제 해결 가이드

### 브라우저에서 SSE 연결 실패

#### 증상
- Dashboard에서 로그가 실시간으로 업데이트되지 않음
- SSE Health 위젯이 🔴 DOWN 상태

#### 진단
```bash
# 1. Dashboard SSE 엔드포인트 직접 테스트
curl -I http://localhost:3000/api/logs/stream

# 2. Soul Engine SSE 스트림 확인
curl -s http://localhost:8010/api/logs/stream | head -3

# 3. 브라우저 콘솔 에러 확인
# Network 탭에서 /api/logs/stream 요청 상태 확인
```

#### 해결
1. **Next.js rewrites 확인**: `next.config.ts`에서 SSE rewrite 설정 확인
2. **CORS 헤더 확인**: Soul Engine 응답에 적절한 헤더 포함 확인
3. **브라우저 캐시 클리어**: 강제 새로고침 (Ctrl+F5)
4. **EventSource 구현 확인**: `createEventSource()` 헬퍼 사용 여부 확인

### 이벤트가 늦게 도착하거나 누락

#### 증상
- SSE Health 위젯이 🟡 STALE 상태
- 로그가 간헐적으로 업데이트됨

#### 진단
```bash
# 1. Soul Engine 이벤트 전송 확인
curl -s http://localhost:8010/api/logs/stream | head -10

# 2. Prometheus 메트릭 확인
curl -s http://localhost:9090/api/v1/query?query=afo_sse_last_event_age_seconds
```

#### 해결
1. **네트워크 지연 확인**: ping/트레이스라우트로 지연 측정
2. **Soul Engine 부하 확인**: CPU/메모리 사용량 확인
3. **이벤트 빈도 조정**: 로그 양에 따른 전송 빈도 조정
4. **프록시 버퍼링 확인**: 중간 프록시의 buffering 설정 확인

### 재연결 빈도가 높음

#### 증상
- SSE High Reconnect Rate 알림 발생
- 브라우저에서 빈번한 재연결 로그

#### 진단
```bash
# 1. 재연결 빈도 확인
curl -s http://localhost:9090/api/v1/query?query=rate\(afo_sse_reconnect_count_total\[5m\]\)

# 2. 브라우저 탭 수 확인
# 브라우저 개발자 도구에서 연결 수 확인
```

#### 해결
1. **StrictMode 방지 확인**: EventSource 생성 시 guard 적용 확인
2. **탭 다중 오픈 제한**: 필요시 연결 공유 로직 구현
3. **네트워크 안정화**: VPN/프록시 설정 최적화
4. **EventSource 타임아웃 조정**: 브라우저별 타임아웃 설정 확인

## 유지보수

### 정기 점검 항목

- [ ] SSE Health 메트릭 정상 수집 확인
- [ ] Alert 규칙 작동 확인
- [ ] 브라우저 호환성 테스트 (Chrome/Firefox/Safari)
- [ ] 모바일 브라우저 지원 확인
- [ ] 프록시 환경에서의 작동 확인

### 업데이트 시 주의사항

1. **EventSource API 변경 시**: `lib/sse.ts` 헬퍼 업데이트
2. **메트릭 추가 시**: Prometheus 게이지 추가 및 Alert 규칙 업데이트
3. **브라우저 호환성 변경 시**: SSEHealthWidget 상태 로직 조정

## 관련 문서

- [AFO Kingdom Architecture](../AFO_CHANCELLOR_GRAPH_SPEC.md)
- [Dashboard Frontend Guide](../AFO_FRONTEND_ARCH.md)
- [Monitoring Setup](../monitoring/STAGE3_MONITORING_SSOT.md)
- [Alerting Rules](../monitoring/STAGE3_MONITORING_SSOT.md#알람-정책-설정)

---

**마지막 업데이트**: 2025-12-29
**담당**: 승상 (Antigravity)
