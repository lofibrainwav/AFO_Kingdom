# Grafana 포트 불일치 문제 진단 및 해결

**날짜**: 2025-12-23  
**문제**: 호스트 네트워크 모드에서 Grafana 포트 매핑 불일치

---

## 문제 원인

### 호스트 네트워크 모드의 포트 매핑 동작

**Bridge 네트워크 모드 (이전)**:
- `ports: "3100:3000"` → 호스트 3100 → 컨테이너 3000
- Cloudflare Tunnel: `http://localhost:3100` ✅

**Host 네트워크 모드 (현재)**:
- `network_mode: host` → 포트 매핑 무효
- Grafana는 컨테이너 내부 기본 포트 **3000**에서 직접 리스닝
- Cloudflare Tunnel: `http://localhost:3100` ❌ (실제는 3000에서 듣고 있음)

---

## 진단 방법

### 30초 진단 스크립트

```bash
bash scripts/diagnose_monitoring_ports.sh
```

**예상 결과 (문제 있는 경우)**:
```
== LISTEN PORTS (3000/3100/9091) ==
LISTEN  0  4096  0.0.0.0:3000  *:*  users:(("grafana-server",pid=1234,fd=3))

== LOCAL CURL ==
HTTP/1.1 302 Found  # 3000 OK
3100 NO              # 3100 NO
```

---

## 해결 방법

### 옵션 A: Cloudflare Tunnel 설정 변경 (권장)

**장점**: 빠르고 안전, compose 파일 수정 불필요

**단계**:
1. Cloudflare Zero Trust Dashboard 접속
2. Networks → Tunnels → `afo-kingdom-tunnel` → Edit
3. Public Hostnames 섹션에서:
   - `afo-grafana.brnestrm.com` → Service: `http://localhost:3000` (3100 → 3000 변경)
4. Save tunnel
5. Tunnel 재시작 (필요시)

**테스트**:
```bash
curl -I https://afo-grafana.brnestrm.com  # HTTP/2 302 (성공!)
```

### 옵션 B: Grafana를 3100에서 듣게 설정

**장점**: 기존 Tunnel 설정 유지

**단계**:
1. `docker-compose.yml` 수정:
   ```yaml
   grafana:
     image: grafana/grafana:latest
     container_name: afo-grafana
     network_mode: host
     environment:
       GF_SECURITY_ADMIN_PASSWORD: admin
       GF_SERVER_HTTP_PORT: 3100  # 추가
   ```
2. 컨테이너 재시작:
   ```bash
   docker-compose --profile monitoring down
   docker-compose --profile monitoring up -d
   ```

---

## 권장 사항

**옵션 A (Tunnel 설정 변경)를 권장합니다:**
- ✅ 빠른 해결 (1분 이내)
- ✅ compose 파일 수정 불필요
- ✅ Grafana 기본 포트(3000) 유지 (표준 준수)
- ✅ 다른 설정에 영향 없음

---

## 다음 단계

1. ⏳ 진단 스크립트 실행 (`scripts/diagnose_monitoring_ports.sh`)
2. ⏳ 결과 확인 (3000 OK / 3100 NO 확인)
3. ⏳ 옵션 A 또는 B 선택
4. ⏳ 적용 후 외부 접근 테스트

---

**상태**: 진단 스크립트 준비 완료. Hetzner 서버에서 실행 대기 중.

