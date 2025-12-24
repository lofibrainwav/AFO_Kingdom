# Monitoring Stack 호스트 네트워크 모드 재시작 가이드

**날짜**: 2025-12-23  
**목적**: Grafana 및 Pushgateway를 호스트 네트워크 모드로 재시작하여 Cloudflare Tunnel 접근 가능하게 함

---

## 현재 상태

### ✅ Grafana 설정 확인
- **파일**: `packages/afo-core/docker-compose.yml`
- **라인 81**: `network_mode: host` ✅ 이미 설정됨
- **포트**: 호스트 네트워크 모드이므로 `localhost:3100`에 직접 바인딩

### ⚠️ Pushgateway 확인 필요
- Pushgateway는 docker-compose.yml에 없음
- 별도로 실행 중일 수 있음
- 포트 9091에서 리스닝 중 확인됨

---

## 실행 방법

### Hetzner 서버에서 실행

```bash
# AFO Kingdom 프로젝트 디렉토리로 이동
cd /path/to/AFO_Kingdom

# 스크립트 실행
bash scripts/restart_monitoring_host_network.sh
```

### 수동 실행

```bash
cd packages/afo-core

# 현재 컨테이너 중지
docker-compose --profile monitoring down

# 호스트 네트워크 모드로 재시작
docker-compose --profile monitoring up -d

# 상태 확인
docker ps | grep -E "(grafana|prometheus|pushgateway)"
```

---

## 재시작 후 확인

### 로컬 확인 (Hetzner 서버에서)

```bash
# Grafana 확인
curl -I http://localhost:3100  # HTTP 302 확인

# Pushgateway 확인 (별도 실행 중인 경우)
curl -I http://localhost:9091  # HTTP 200 확인
```

### 외부 확인 (Tunnel 재시작 후)

```bash
# Grafana 외부 접근
curl -I https://afo-grafana.brnestrm.com  # HTTP/2 302 (성공!)

# Pushgateway 외부 접근
curl -s https://afo-metrics.brnestrm.com/-/ready  # OK (성공!)
```

---

## 중요 포인트

1. **호스트 네트워크 모드**
   - Grafana가 `localhost:3100`에 직접 바인딩됨
   - Cloudflare Tunnel이 `localhost:3100`에 접근 가능해짐

2. **프로파일 기반 활성화**
   - `--profile monitoring`으로 monitoring 스택만 재시작
   - 다른 서비스는 영향 없음

3. **Tunnel 재시작 필요**
   - 컨테이너 재시작 후 Tunnel도 재시작해야 새 연결이 반영됨

---

## 다음 단계

1. ✅ 컨테이너 재시작 스크립트 생성 완료
2. ⏳ Hetzner 서버에서 스크립트 실행
3. ⏳ 로컬 서비스 확인
4. ⏳ Tunnel 재시작
5. ⏳ 외부 접근 테스트

---

**상태**: 스크립트 생성 완료. Hetzner 서버에서 실행 대기 중.

