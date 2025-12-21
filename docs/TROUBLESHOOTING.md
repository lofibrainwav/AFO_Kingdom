# 문제 해결 가이드

## 📋 개요

AFO Kingdom 시스템의 일반적인 문제 및 해결 방법을 제공합니다.

---

## 🔍 일반적인 문제

### 1. 포트 충돌

#### 증상
```
Error: Address already in use
```

#### 해결 방법

```bash
# 포트 사용 확인
lsof -i :8010

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트 사용
export API_SERVER_PORT=8010
```

---

### 2. 데이터베이스 연결 실패

#### 증상
```
Error: could not connect to server
```

#### 해결 방법

```bash
# PostgreSQL 연결 확인
psql -h localhost -p 15432 -U afo -d afo_memory

# Docker 컨테이너 확인
docker-compose ps postgres

# 로그 확인
docker-compose logs postgres
```

#### 환경 변수 확인

```bash
# .env 파일 확인
cat packages/afo-core/.env | grep POSTGRES
```

---

### 3. Redis 연결 실패

#### 증상
```
Error: Connection refused
```

#### 해결 방법

```bash
# Redis 연결 확인
redis-cli -h localhost -p 6379 ping

# Docker 컨테이너 확인
docker-compose ps redis

# 로그 확인
docker-compose logs redis
```

---

### 4. 의존성 설치 실패

#### 증상
```
Error: No module named 'xxx'
```

#### 해결 방법

```bash
# 의존성 재설치
pip install -r packages/afo-core/requirements.txt

# 가상환경 사용
python3 -m venv venv
source venv/bin/activate
pip install -r packages/afo-core/requirements.txt
```

---

### 5. MCP 서버 연결 실패

#### 증상
```
Error: MCP server not responding
```

#### 해결 방법

```bash
# MCP 서버 상태 확인
curl http://localhost:8010/health

# Cursor MCP 설정 확인
cat .cursor/mcp.json

# PYTHONPATH 확인
echo $PYTHONPATH
```

---

### 6. Trinity Score 계산 오류

#### 증상
```
Error: Trinity Score calculation failed
```

#### 해결 방법

```bash
# SSOT 파일 확인
cat packages/trinity-os/TRINITY_OS_PERSONAS.yaml

# Trinity Score 엔진 확인
python3 -c "from trinity_os.servers.trinity_score_mcp import TrinityScoreEngineHybrid; print('OK')"
```

---

## 🐛 디버깅 방법

### 1. 로그 확인

#### Docker 로그

```bash
# 전체 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs api-server

# 실시간 로그
docker-compose logs -f
```

#### Python 로그

```bash
# 로그 레벨 설정
export LOG_LEVEL=DEBUG

# 로그 파일 확인
tail -f api_server.log
```

---

### 2. 헬스 체크

#### API 헬스 체크

```bash
curl http://localhost:8010/health
```

#### 서비스별 헬스 체크

```bash
# Chancellor
curl http://localhost:8010/chancellor/health

# Skills
curl http://localhost:8010/api/skills/health

# System
curl http://localhost:8010/api/system/metrics
```

---

### 3. 환경 변수 확인

```bash
# 모든 환경 변수 확인
env | grep AFO

# .env 파일 확인
cat packages/afo-core/.env
```

---

## 🔧 성능 문제

### 1. 느린 응답 시간

#### 원인
- 데이터베이스 쿼리 최적화 필요
- Redis 캐시 미사용
- 네트워크 지연

#### 해결 방법

```bash
# 데이터베이스 인덱스 확인
psql -h localhost -p 15432 -U afo -d afo_memory -c "\d"

# Redis 캐시 확인
redis-cli -h localhost -p 6379 INFO stats
```

---

### 2. 메모리 부족

#### 증상
```
Error: Out of memory
```

#### 해결 방법

```bash
# 메모리 사용량 확인
docker stats

# 컨테이너 리소스 제한 설정
# docker-compose.yml
services:
  api-server:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 🔐 보안 문제

### 1. API 키 누출

#### 증상
```
Error: Invalid API key
```

#### 해결 방법

```bash
# API 키 확인
python3 scripts/export_keys.py

# API Wallet 확인
curl http://localhost:8010/api/wallet/keys
```

---

### 2. 인증 실패

#### 증상
```
Error: Unauthorized
```

#### 해결 방법

```bash
# 토큰 확인
curl -H "Authorization: Bearer <token>" http://localhost:8010/api/auth/verify
```

---

## 📊 모니터링

### 1. 시스템 메트릭

```bash
# Prometheus 메트릭
curl http://localhost:8010/metrics

# 시스템 헬스
curl http://localhost:8010/api/system/metrics
```

### 2. 로그 스트리밍

```bash
# SSE 로그 스트리밍
curl http://localhost:8010/api/system/logs/stream
```

---

## 🆘 지원

### 문제 보고

1. **로그 수집**
   ```bash
   docker-compose logs > logs.txt
   ```

2. **환경 정보 수집**
   ```bash
   python3 scripts/collect_debug_info.py
   ```

3. **GitHub Issue 생성**
   - 로그 파일 첨부
   - 환경 정보 첨부
   - 재현 단계 설명

---

## 📚 관련 문서

- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [API Endpoints Reference](API_ENDPOINTS_REFERENCE.md)

---

**최종 업데이트**: 2025-01-27
**담당**: 승상 (丞相) - AFO Kingdom
