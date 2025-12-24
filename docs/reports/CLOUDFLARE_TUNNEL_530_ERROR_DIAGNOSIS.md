# Cloudflare Tunnel 530 오류 진단 보고서

**날짜**: 2025-12-23  
**문제**: HTTP/2 530 오류 (error code: 1033)  
**원인**: Tunnel 설정 변경 후 재시작 필요

---

## 현재 상태 확인

### ✅ 로컬 서비스 정상 작동
- **Grafana (3100)**: HTTP 302 (정상)
- **Pushgateway (9091)**: HTTP 200 (정상)

### ✅ Tunnel 프로세스 실행 중
- **PID**: 확인됨
- **명령**: `cloudflared tunnel run --token ...`

### ✅ 포트 리스닝 확인
- **3100**: 리스닝 중
- **9091**: 리스닝 중

### ❌ 외부 접근 실패
- **Grafana**: HTTP/2 530 (error code: 1033)
- **Pushgateway**: HTTP/2 530 (error code: 1033)

---

## 문제 원인

**Cloudflare error code 1033**: Argo Tunnel error
- Tunnel이 로컬 서비스에 연결할 수 없음
- **가장 가능성 높은 원인**: Tunnel 설정 변경 후 재시작하지 않음

**Cloudflare Tunnel 동작 방식**:
1. Dashboard에서 Public Hostname 설정 변경
2. 설정이 Cloudflare 서버에 저장됨
3. **하지만 실행 중인 Tunnel 프로세스는 새 설정을 자동으로 읽지 않음**
4. **Tunnel을 재시작해야 새 설정이 적용됨**

---

## 해결 방법

### 방법 1: Tunnel 프로세스 재시작 (권장)

**Step 1: 현재 Tunnel 프로세스 확인**
```bash
ps aux | grep "cloudflared tunnel" | grep -v grep
```

**Step 2: Tunnel 프로세스 종료**
```bash
PID=$(ps aux | grep "cloudflared tunnel" | grep -v grep | awk '{print $2}')
kill $PID
```

**Step 3: Tunnel 재시작**
- Tunnel을 실행하는 방법에 따라 재시작
- 예: `cloudflared tunnel run --token ...`

### 방법 2: 자동 반영 대기 (비권장)

- Cloudflare가 자동으로 설정을 반영하기까지 몇 분 소요될 수 있음
- 하지만 일반적으로 **재시작이 필요함**

---

## 확인 사항

### Public Hostname 설정 확인
1. Cloudflare Zero Trust Dashboard 접속
2. Networks → Tunnels → afo-kingdom-tunnel → Edit
3. Public Hostnames 섹션 확인:
   - ✅ `afo-grafana.brnestrm.com` → `http://localhost:3100`
   - ✅ `afo-metrics.brnestrm.com` → `http://localhost:9091`

### DNS 레코드 확인
- ✅ `afo-grafana.brnestrm.com` → `tunnel-id.cfargotunnel.com` (Proxied)
- ✅ `afo-metrics.brnestrm.com` → `tunnel-id.cfargotunnel.com` (Proxied)

---

## 다음 단계

1. ✅ Public Hostname 설정 완료 (형님 확인)
2. ⏳ Tunnel 재시작 필요
3. ⏳ 외부 접근 테스트 재실행

---

**상태**: 설정은 완료되었으나 Tunnel 재시작 필요.

