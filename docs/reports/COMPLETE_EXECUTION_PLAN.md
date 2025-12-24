# Grafana 포트 불일치 해결 - 완전 실행 계획

**날짜**: 2025-12-23  
**상태**: 논리적 순차 실행 준비 완료

---

## ✅ 완료된 작업

### Phase 1: 진단 스크립트 준비
- ✅ `scripts/diagnose_monitoring_ports.sh` 생성 완료
- ⚠️ Hetzner 서버에서 실행 필요 (로컬 Mac에서는 불가)

### Phase 2: 자동 수정 스크립트
- ✅ `scripts/fix_grafana_tunnel_port.sh` 생성 완료
- ⚠️ API 호출 실패 (인증 문제 가능성)
- ✅ 수동 변경 가이드 생성: `docs/reports/MANUAL_TUNNEL_PORT_FIX.md`

### Phase 3: Tunnel 재시작
- ✅ `scripts/restart_cloudflare_tunnel.sh` 준비 완료

### Phase 4: 검증
- ✅ `scripts/verify_grafana_external_access.sh` 생성 완료

---

## 🎯 최종 실행 순서

### 1단계: Cloudflare Dashboard에서 수동 변경 (필수)

**브라우저에서 실행**:
1. `https://one.dash.cloudflare.com/networks/tunnels` 접속
2. `afo-kingdom-tunnel` → Edit
3. Public Hostnames → `afo-grafana.brnestrm.com`
4. Service: `http://localhost:3100` → `http://localhost:3000` 변경
5. Save

**또는 자동 스크립트 재시도** (API 키 확인 후):
```bash
bash scripts/fix_grafana_tunnel_port.sh
```

### 2단계: Tunnel 재시작

```bash
bash scripts/restart_cloudflare_tunnel.sh
# 그 다음 Tunnel을 다시 실행
nohup cloudflared tunnel run --token <TOKEN> > /tmp/cloudflared.log 2>&1 &
```

### 3단계: 검증

```bash
# 로컬 확인
curl -I http://localhost:3000  # HTTP 302

# 외부 확인
bash scripts/verify_grafana_external_access.sh
# 또는
curl -I https://afo-grafana.brnestrm.com  # HTTP/2 302 (성공!)
```

---

## 📋 생성된 파일 목록

1. `scripts/diagnose_monitoring_ports.sh` - 진단 스크립트
2. `scripts/fix_grafana_tunnel_port.sh` - 자동 수정 스크립트 (API)
3. `scripts/restart_cloudflare_tunnel.sh` - Tunnel 재시작
4. `scripts/verify_grafana_external_access.sh` - 검증 스크립트
5. `docs/reports/MANUAL_TUNNEL_PORT_FIX.md` - 수동 변경 가이드
6. `docs/reports/GRAFANA_PORT_FIX_SEQUENTIAL_PLAN.md` - 상세 계획
7. `docs/reports/SEQUENTIAL_EXECUTION_SUMMARY.md` - 요약

---

## ⚠️ 주의사항

1. **API 자동 수정 실패**: Cloudflare API 인증 문제 가능성
   - 해결: 수동으로 Dashboard에서 변경 (권장)

2. **Hetzner 서버 접근 필요**: 
   - 진단 스크립트는 Hetzner 서버에서 실행 필요
   - Tunnel 재시작도 Hetzner 서버에서 실행

3. **설정 반영 시간**:
   - Dashboard에서 변경 후 즉시 반영되지만
   - Tunnel 재시작 시 더 확실함

---

**상태**: 모든 스크립트 및 가이드 준비 완료. 수동 변경 후 검증 단계로 진행 가능.

