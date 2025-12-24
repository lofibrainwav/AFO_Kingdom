# Grafana 포트 불일치 최종 해결 방안

**날짜**: 2025-12-23  
**상황**: Tunnel이 API에서 찾을 수 없음 (로컬에서만 실행 중)

---

## 🔍 발견된 문제

1. **Tunnel API 오류**: "Tunnel not found" 또는 "Configuration for tunnel not found"
2. **Tunnel 상태**: "down" (deleted_at 존재)
3. **로컬 실행**: Tunnel 프로세스는 실행 중 (PID: 60959)

---

## 💡 해결 방안

### 옵션 1: Cloudflare Dashboard에서 수동 변경 (가장 확실)

**단계**:
1. `https://one.dash.cloudflare.com/networks/tunnels` 접속
2. 로그인 및 보안 검증 완료
3. Tunnel 목록에서 실제 Tunnel 찾기 (이름 확인)
4. Tunnel → Edit
5. Public Hostnames → `afo-grafana.brnestrm.com`
6. Service: `http://localhost:3100` → `http://localhost:3000` 변경
7. Save

### 옵션 2: 로컬 설정 파일 수정 (Tunnel이 로컬 설정 사용 시)

Tunnel이 로컬 설정 파일을 사용하는 경우:
```bash
# 설정 파일 위치 확인
cloudflared tunnel info

# 설정 파일 수정
# ingress 섹션에서 localhost:3100 → localhost:3000 변경
```

### 옵션 3: Grafana 포트 변경 (docker-compose.yml)

`docker-compose.yml` 수정:
```yaml
grafana:
  network_mode: host
  environment:
    GF_SECURITY_ADMIN_PASSWORD: admin
    GF_SERVER_HTTP_PORT: 3100  # 추가
```

---

## 🎯 권장 순서

1. **Cloudflare Dashboard에서 수동 변경** (가장 확실)
2. Tunnel 재시작
3. 검증

---

**상태**: API 자동 수정 불가. 수동 변경 필요.
