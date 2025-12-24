# Grafana 포트 불일치 해결 - 논리적 순차 실행 계획

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7 분석 기반

---

## 📊 Sequential Thinking 분석 결과

### Thought 1-2: 문제 정의 및 원인 분석
- **문제**: HTTP/2 530 오류 (외부 접근 실패)
- **원인**: Host network mode에서 포트 매핑 무효화
  - Bridge mode: `3100:3000` → 호스트 3100 접근 가능
  - Host mode: 포트 매핑 없음 → Grafana가 기본 3000에서 직접 리스닝
  - Tunnel 설정: `localhost:3100` → 실제 서비스는 3000 → 불일치

### Thought 3-4: 해결 방안 도출
- **옵션 A**: Tunnel 설정을 3000으로 변경 (권장)
  - 빠름 (1분 이내)
  - 안전 (compose 파일 수정 불필요)
  - 표준 준수 (Grafana 기본 포트 유지)
- **옵션 B**: Grafana를 3100에서 듣게 설정
  - compose 파일 수정 필요
  - 컨테이너 재시작 필요

### Thought 5-8: 실행 계획 수립
1. 검증 (필수)
2. 해결 (옵션 A 우선)
3. 검증 (해결 후)

---

## 🔍 Context7 분석 결과

### Docker Host Network Mode
- Host network mode에서는 `ports` 매핑이 무효화됨
- 컨테이너는 호스트의 네트워크 스택을 직접 사용
- 포트는 컨테이너 내부 설정 그대로 호스트에 바인딩

### Grafana Docker Configuration
- 기본 HTTP 포트: 3000
- 환경변수 `GF_SERVER_HTTP_PORT`로 포트 변경 가능
- Host network mode에서는 이 환경변수 필수

---

## ✅ 논리적 순차 실행 계획

### Phase 1: 검증 (현재 상태 확인)

**Hetzner 서버에서 실행**:
```bash
bash scripts/diagnose_monitoring_ports.sh
```

**예상 결과**:
```
== LISTEN PORTS (3000/3100/9091) ==
LISTEN  0  4096  0.0.0.0:3000  *:*  users:(("grafana-server",...))

== LOCAL CURL ==
HTTP/1.1 302 Found  # 3000 OK
3100 NO              # 3100 NO
```

**확인 사항**:
- ✅ 3000에서 리스닝 확인
- ❌ 3100에서 리스닝 없음
- → 가설 확정: 포트 불일치

---

### Phase 2: 해결 (옵션 A - 권장)

**Cloudflare Zero Trust Dashboard에서 설정 변경**:

1. **접속**: `https://one.dash.cloudflare.com/networks/tunnels`
2. **Tunnel 선택**: `afo-kingdom-tunnel` → Edit
3. **Public Hostnames 섹션**:
   - `afo-grafana.brnestrm.com` 찾기
   - Service: `http://localhost:3100` → `http://localhost:3000` 변경
4. **저장**: Save tunnel

**자동화 스크립트** (API 사용):
```bash
bash scripts/update_tunnel_config.sh
# Service를 3000으로 변경하도록 수정 필요
```

---

### Phase 3: 검증 (해결 후 확인)

**로컬 확인** (Hetzner 서버):
```bash
curl -I http://localhost:3000  # HTTP 302 확인
```

**외부 확인** (Tunnel 재시작 후):
```bash
# Tunnel 재시작 (필요시)
bash scripts/restart_cloudflare_tunnel.sh
# 또는
sudo systemctl restart cloudflared

# 외부 접근 테스트
curl -I https://afo-grafana.brnestrm.com  # HTTP/2 302 (성공!)
```

---

## 🔄 대안: 옵션 B (옵션 A 실패 시)

**docker-compose.yml 수정**:
```yaml
grafana:
  environment:
    GF_SECURITY_ADMIN_PASSWORD: admin
    GF_SERVER_HTTP_PORT: 3100  # 추가
```

**재시작**:
```bash
cd packages/afo-core
docker-compose --profile monitoring down
docker-compose --profile monitoring up -d
```

---

## 📋 실행 체크리스트

- [ ] Phase 1: 진단 스크립트 실행
- [ ] Phase 1: 결과 확인 (3000 OK / 3100 NO)
- [ ] Phase 2: Cloudflare Dashboard에서 Tunnel 설정 변경
- [ ] Phase 2: Service를 3000으로 변경
- [ ] Phase 2: 저장 확인
- [ ] Phase 3: Tunnel 재시작 (필요시)
- [ ] Phase 3: 로컬 접근 테스트
- [ ] Phase 3: 외부 접근 테스트
- [ ] Phase 3: 성공 확인

---

**상태**: Sequential Thinking + Context7 분석 완료. 실행 계획 수립 완료.

