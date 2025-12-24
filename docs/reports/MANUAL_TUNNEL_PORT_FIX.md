# Cloudflare Tunnel 포트 설정 수동 변경 가이드

**날짜**: 2025-12-23  
**목적**: Grafana 포트 불일치 해결 (3100 → 3000)

---

## 문제

- Grafana 실제 포트: 3000 (host network mode)
- Tunnel 설정 포트: 3100
- 결과: 포트 불일치로 연결 실패

---

## 해결 방법 (수동)

### Step 1: Cloudflare Zero Trust Dashboard 접속

1. 브라우저에서 접속: `https://one.dash.cloudflare.com/networks/tunnels`
2. 로그인 (필요시)

### Step 2: Tunnel 편집

1. `afo-kingdom-tunnel` 찾기
2. **Edit** 클릭

### Step 3: Public Hostname 설정 변경

**Public Hostnames** 섹션에서:

1. `afo-grafana.brnestrm.com` 찾기
2. **Service** 필드 확인:
   - 현재: `http://localhost:3100` ❌
   - 변경: `http://localhost:3000` ✅
3. **Save** 또는 **Update** 클릭

### Step 4: 저장 확인

- 저장 성공 메시지 확인
- 페이지 새로고침하여 변경사항 확인

### Step 5: Tunnel 재시작 (선택)

설정 변경 후 자동 반영되지만, 확실히 하기 위해:

```bash
bash scripts/restart_cloudflare_tunnel.sh
```

또는:

```bash
# Tunnel 프로세스 재시작
PID=$(ps aux | grep "cloudflared tunnel" | grep -v grep | awk '{print $2}')
kill $PID
nohup cloudflared tunnel run --token <TOKEN> > /tmp/cloudflared.log 2>&1 &
```

### Step 6: 검증

```bash
# 로컬 확인
curl -I http://localhost:3000  # HTTP 302 확인

# 외부 확인
curl -I https://afo-grafana.brnestrm.com  # HTTP/2 302 (성공!)
```

---

## 완료 확인

✅ `afo-grafana.brnestrm.com` Service가 `http://localhost:3000`으로 변경됨  
✅ 외부 접근 시 HTTP/2 302 응답 (성공)

---

**상태**: 수동 변경 가이드 준비 완료.
