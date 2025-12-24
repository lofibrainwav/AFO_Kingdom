# Cloudflare Tunnel 최종 상태 보고서

**날짜**: 2025-12-23  
**작업**: Tunnel 설정 및 외부 접근 구성

---

## 완료된 작업

### 1. Public Hostname 설정
- ✅ Dashboard에서 설정 추가
  - `afo-grafana.brnestrm.com` → `http://localhost:3100`
  - `afo-metrics.brnestrm.com` → `http://localhost:9091`

### 2. Tunnel 재시작
- ✅ Tunnel 프로세스 종료 및 재시작 완료
- ✅ Tunnel 연결 정상 (4개 연결 등록)

### 3. 로컬 서비스 확인
- ✅ Grafana (3100): HTTP 302 (정상)
- ✅ Pushgateway (9091): HTTP 200 (정상)

### 4. 스크립트 생성
- ✅ `scripts/restart_cloudflare_tunnel.sh`: Tunnel 재시작 스크립트
- ✅ `scripts/update_tunnel_config.sh`: API를 통한 설정 업데이트 스크립트

---

## 지속되는 문제

### HTTP/2 530 오류 (error code: 1033)
- **Grafana**: `https://afo-grafana.brnestrm.com` → 530
- **Pushgateway**: `https://afo-metrics.brnestrm.com` → 530

### 가능한 원인
1. **설정 전파 지연**: Cloudflare 서버에 설정이 전파되는 데 시간이 필요 (10-15분 소요 가능)
2. **설정 저장 실패**: Dashboard에서 설정을 저장했지만 실제로 반영되지 않았을 수 있음
3. **DNS/라우팅 문제**: DNS는 정상이지만 Tunnel 라우팅 테이블에 반영되지 않음

---

## 해결 방법

### 방법 1: Dashboard에서 설정 재확인 (권장)

1. **Cloudflare Zero Trust Dashboard 접속**
   - `https://one.dash.cloudflare.com/networks/tunnels`

2. **Tunnel 편집**
   - `afo-kingdom-tunnel` → Edit

3. **Public Hostnames 섹션 확인**
   - 두 개의 Hostname이 정확히 설정되어 있는지 확인
   - 각 Hostname의 Service URL이 정확한지 확인

4. **설정 저장**
   - "Save tunnel" 클릭
   - 저장 성공 메시지 확인

5. **Tunnel 재시작**
   ```bash
   bash scripts/restart_cloudflare_tunnel.sh
   # 그 다음 Tunnel을 다시 실행
   nohup cloudflared tunnel run --token <TOKEN> > /tmp/cloudflared.log 2>&1 &
   ```

### 방법 2: 대기 후 재시도

- Cloudflare 설정 전파는 최대 10-15분 소요될 수 있음
- 15분 후 다시 테스트:
  ```bash
  curl -I https://afo-grafana.brnestrm.com
  curl -I https://afo-metrics.brnestrm.com
  ```

### 방법 3: API를 통한 설정 확인

```bash
bash scripts/update_tunnel_config.sh
```

---

## 다음 단계

1. ⏳ Dashboard에서 Public Hostname 설정 재확인
2. ⏳ 설정 저장 후 Tunnel 재시작
3. ⏳ 10-15분 대기 후 외부 접근 재테스트
4. ⏳ 성공 시 SSL 인증서 자동 발급 확인

---

## 참고 자료

- **Tunnel 재시작 스크립트**: `scripts/restart_cloudflare_tunnel.sh`
- **설정 업데이트 스크립트**: `scripts/update_tunnel_config.sh`
- **Tunnel 로그**: `/tmp/cloudflared.log`

---

**상태**: 설정 완료. 설정 전파 대기 또는 재확인 필요.

