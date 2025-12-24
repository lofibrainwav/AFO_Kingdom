# Cloudflare Tunnel 530 오류 지속 문제 진단

**날짜**: 2025-12-23  
**문제**: Tunnel 재시작 후에도 여전히 HTTP/2 530 오류 발생

---

## 현재 상태

### ✅ 정상 작동 중
1. **Tunnel 프로세스**: 실행 중 (PID: 60071)
2. **Tunnel 연결**: 정상 등록 (로그 확인)
   - 연결 4개 등록됨 (las01, mci01, mci03)
   - QUIC 프로토콜 사용
3. **로컬 서비스**: 정상 작동
   - Grafana (3100): HTTP 302
   - Pushgateway (9091): HTTP 200

### ❌ 문제 지속
- **외부 접근**: HTTP/2 530 오류 (error code: 1033)
- **Grafana**: `https://afo-grafana.brnestrm.com` → 530
- **Pushgateway**: `https://afo-metrics.brnestrm.com` → 530

---

## 가능한 원인

### 1. Public Hostname 설정 미반영
- Dashboard에서 설정을 저장했지만 Cloudflare 서버에 전파되지 않았을 수 있음
- 설정 전파에 시간이 더 필요할 수 있음 (몇 분~수십 분 소요 가능)

### 2. 설정 저장 실패
- Dashboard에서 "Save" 버튼을 눌렀지만 실제로 저장되지 않았을 수 있음
- 브라우저 캐시 문제로 설정이 반영되지 않았을 수 있음

### 3. DNS/라우팅 문제
- DNS 레코드는 정상이지만 Tunnel 라우팅 테이블에 반영되지 않았을 수 있음

---

## 해결 방법

### 방법 1: Dashboard에서 설정 재확인 (권장)

1. **Cloudflare Zero Trust Dashboard 접속**
   - `https://one.dash.cloudflare.com/networks/tunnels`

2. **Tunnel 편집**
   - `afo-kingdom-tunnel` → Edit

3. **Public Hostnames 섹션 확인**
   - `afo-grafana.brnestrm.com` → `http://localhost:3100` 존재 확인
   - `afo-metrics.brnestrm.com` → `http://localhost:9091` 존재 확인

4. **설정 저장**
   - "Save tunnel" 클릭
   - 저장 성공 메시지 확인

5. **Tunnel 재시작**
   - `scripts/restart_cloudflare_tunnel.sh` 실행

### 방법 2: API를 통한 설정 확인

```bash
# Tunnel 설정 확인
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/tunnels/$TUNNEL_ID/configurations" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $KEY" \
  -H "Content-Type: application/json"
```

### 방법 3: 대기 후 재시도

- Cloudflare 설정 전파는 최대 수십 분 소요될 수 있음
- 10-15분 후 다시 테스트

---

## 다음 단계

1. ⏳ Dashboard에서 Public Hostname 설정 재확인
2. ⏳ 설정 저장 후 Tunnel 재시작
3. ⏳ 10-15분 대기 후 외부 접근 재테스트

---

**상태**: Tunnel 재시작 완료. Public Hostname 설정 재확인 필요.

