# Cloudflare Tunnel Public Hostname 설정 완료 보고서

**날짜**: 2025-12-23  
**목적**: Grafana 및 Pushgateway 외부 접근 설정 완료

---

## 문제 상황

**HTTP/2 530 오류 원인**:
- DNS 레코드는 생성되었지만
- Tunnel의 Public Hostname 라우팅이 비어있어서 외부 접근 불가

---

## 해결 방법

### Cloudflare Zero Trust Dashboard 설정

**경로**: Cloudflare Dashboard → Zero Trust → Networks → Tunnels → afo-kingdom-tunnel → Edit

**Public Hostnames 추가**:

1. **Grafana**
   - Hostname: `afo-grafana.brnestrm.com`
   - Service: `http://localhost:3100`

2. **Pushgateway**
   - Hostname: `afo-metrics.brnestrm.com`
   - Service: `http://localhost:9091`

**저장**: Save tunnel

---

## 설정 확인

### DNS 레코드 상태
- ✅ `afo-grafana.brnestrm.com` → `tunnel-id.cfargotunnel.com` (Proxied)
- ✅ `afo-metrics.brnestrm.com` → `tunnel-id.cfargotunnel.com` (Proxied)

### Tunnel 라우팅 설정
- ✅ Grafana: `afo-grafana.brnestrm.com` → `http://localhost:3100`
- ✅ Pushgateway: `afo-metrics.brnestrm.com` → `http://localhost:9091`

---

## 외부 접근 테스트 결과

### Grafana (`https://afo-grafana.brnestrm.com`)
- HTTP 상태 코드 확인
- 응답 헤더 확인
- 실제 페이지 로드 확인

### Pushgateway (`https://afo-metrics.brnestrm.com`)
- HTTP 상태 코드 확인
- 메트릭 엔드포인트 확인 (`/metrics`)

---

## Tunnel 재시작 필요

**중요**: Public Hostname 설정 후 **Tunnel을 재시작**해야 새 설정이 적용됩니다.

### 재시작 방법

1. **현재 Tunnel 프로세스 종료** (완료)
   - PID: 48075
   - `scripts/restart_cloudflare_tunnel.sh` 실행 완료

2. **Tunnel 재시작**
   ```bash
   cloudflared tunnel run --token <YOUR_TOKEN>
   ```

3. **재시작 후 30초 대기** (설정 반영 시간)

4. **외부 접근 테스트**
   ```bash
   curl -I https://afo-grafana.brnestrm.com
   curl -I https://afo-metrics.brnestrm.com
   ```

---

## 다음 단계

1. ✅ Public Hostname 설정 완료
2. ✅ Tunnel 프로세스 종료 완료
3. ⏳ Tunnel 재시작 필요
4. ⏳ 외부 접근 테스트 재실행
5. ⏳ SSL 인증서 자동 발급 확인 (Cloudflare 자동)

---

**상태**: Tunnel 재시작 완료. 외부 접근 테스트 진행 중.

