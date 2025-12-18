# 배포 가이드

## 📋 개요

AFO Kingdom 시스템의 프로덕션 배포 가이드를 제공합니다.

---

## 🏗️ 아키텍처 개요

### 시스템 구성

```
AFO Kingdom
├── Backend (Soul Engine)
│   ├── FastAPI (Port 8010)
│   ├── PostgreSQL (Port 15432)
│   ├── Redis (Port 6379)
│   └── Qdrant (Port 6333)
├── Frontend (Dashboard)
│   └── Next.js (Port 3000)
└── MCP Servers
    ├── AFO Ultimate MCP
    ├── AFO Skills MCP
    └── Trinity Score MCP
```

---

## 🐳 Docker 배포

### 1. Docker Compose 사용

#### 기본 배포

```bash
cd packages/afo-core
docker-compose up -d
```

#### 서비스 확인

```bash
docker-compose ps
```

#### 로그 확인

```bash
docker-compose logs -f
```

### 2. Docker Compose 파일 구조

```yaml
services:
  postgres:
    image: postgres:15-alpine
    ports:
      - "15432:5432"
    environment:
      POSTGRES_DB: afo_memory
      POSTGRES_USER: afo
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  
  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
  
  qdrant:
    image: qdrant/qdrant:v1.7.4
    ports:
      - "6333:6333"
      - "6334:6334"
```

---

## ☸️ Kubernetes 배포

### 1. Helm Chart 사용

```bash
cd helm/afo-chart
helm install afo-kingdom . -f values.yaml
```

### 2. Kubernetes 매니페스트

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: afo-soul-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: afo-soul-engine
  template:
    metadata:
      labels:
        app: afo-soul-engine
    spec:
      containers:
      - name: api-server
        image: afo-kingdom/api-server:latest
        ports:
        - containerPort: 8010
        env:
        - name: POSTGRES_HOST
          value: postgres-service
        - name: REDIS_URL
          value: redis://redis-service:6379
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: afo-soul-engine-service
spec:
  selector:
    app: afo-soul-engine
  ports:
  - protocol: TCP
    port: 8010
    targetPort: 8010
  type: LoadBalancer
```

---

## 🔧 환경 변수 설정

### 필수 환경 변수

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=15432
POSTGRES_DB=afo_memory
POSTGRES_USER=afo
POSTGRES_PASSWORD=your-secure-password

# Redis
REDIS_URL=redis://localhost:6379

# Qdrant
QDRANT_URL=http://localhost:6333

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

### 선택적 환경 변수

```bash
# AntiGravity
ANTIGRAVITY_MODE=true
DRY_RUN_DEFAULT=true

# MCP
MCP_SERVER_URL=http://localhost:8010

# Soul Engine
SOUL_ENGINE_URL=http://localhost:8010
```

---

## 📦 의존성 설치

### Python 의존성

```bash
# 개발 환경
pip install -r packages/afo-core/requirements.txt

# 프로덕션 환경
pip install -r packages/afo-core/requirements_minimal.txt
```

### Node.js 의존성

```bash
cd packages/dashboard
npm install
```

---

## 🚀 시작 스크립트

### 전체 시스템 시작

```bash
./start_kingdom.sh
```

### 개별 서비스 시작

```bash
# Backend
cd packages/afo-core
uvicorn api_server:app --host 0.0.0.0 --port 8010

# Frontend
cd packages/dashboard
npm run dev
```

---

## 🔍 헬스 체크

### API 헬스 체크

```bash
curl http://localhost:8010/health
```

### Docker 서비스 헬스 체크

```bash
docker-compose ps
```

### Kubernetes 헬스 체크

```bash
kubectl get pods
kubectl logs -f deployment/afo-soul-engine
```

---

## 📊 모니터링

### Prometheus 메트릭

```bash
curl http://localhost:8010/metrics
```

### 로그 확인

```bash
# Docker
docker-compose logs -f api-server

# Kubernetes
kubectl logs -f deployment/afo-soul-engine
```

---

## 🔐 보안 설정

### 1. 환경 변수 보안

- `.env` 파일을 `.gitignore`에 추가
- 프로덕션에서는 Secrets Manager 사용 (AWS Secrets Manager, HashiCorp Vault)

### 2. API 키 관리

- API Wallet을 통한 중앙 관리
- 암호화된 저장소 사용

### 3. 네트워크 보안

- 방화벽 규칙 설정
- HTTPS 사용 (프로덕션)
- CORS 설정

---

## 🔄 업데이트 및 롤백

### 업데이트

```bash
# Docker
docker-compose pull
docker-compose up -d

# Kubernetes
kubectl rollout restart deployment/afo-soul-engine
```

### 롤백

```bash
# Kubernetes
kubectl rollout undo deployment/afo-soul-engine
```

---

## 📈 스케일링

### 수평 스케일링

```bash
# Docker Compose
docker-compose up -d --scale api-server=3

# Kubernetes
kubectl scale deployment/afo-soul-engine --replicas=3
```

### 수직 스케일링

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

---

## 🐛 문제 해결

### 일반적인 문제

1. **포트 충돌**
   ```bash
   # 포트 사용 확인
   lsof -i :8010
   ```

2. **데이터베이스 연결 실패**
   ```bash
   # PostgreSQL 연결 확인
   psql -h localhost -p 15432 -U afo -d afo_memory
   ```

3. **Redis 연결 실패**
   ```bash
   # Redis 연결 확인
   redis-cli -h localhost -p 6379 ping
   ```

---

## 📚 관련 문서

- [Configuration Guide](CONFIGURATION_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [API Endpoints Reference](API_ENDPOINTS_REFERENCE.md)

---

**최종 업데이트**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom

