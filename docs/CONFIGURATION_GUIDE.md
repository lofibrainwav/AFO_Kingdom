# 설정 가이드

## 📋 개요

AFO Kingdom 시스템의 설정 및 환경 변수 가이드를 제공합니다.

---

## ⚙️ 설정 파일 구조

```
AFO_Kingdom/
├── packages/afo-core/
│   ├── config/
│   │   ├── settings.py          # 기본 설정
│   │   ├── antigravity.py       # AntiGravity 설정
│   │   └── .env                 # 환경 변수 (로컬)
│   └── .env.example             # 환경 변수 예시
├── packages/trinity-os/
│   └── TRINITY_OS_PERSONAS.yaml # SSOT 페르소나 설정
└── .cursor/
    └── mcp.json                 # Cursor MCP 설정
```

---

## 🔧 환경 변수 설정

### 1. 데이터베이스 설정

#### PostgreSQL

```bash
# 필수
POSTGRES_HOST=localhost
POSTGRES_PORT=15432
POSTGRES_DB=afo_memory
POSTGRES_USER=afo
POSTGRES_PASSWORD=your-secure-password

# 선택적 (전체 URL 사용 시)
DATABASE_URL=postgresql://afo:password@localhost:15432/afo_memory
```

#### Redis

```bash
# 필수
REDIS_URL=redis://localhost:6379

# 선택적 (개별 설정)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

#### Qdrant

```bash
# 선택적
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
```

---

### 2. API 키 설정

#### LLM API Keys

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
GEMINI_API_KEY=...

# Ollama (로컬)
OLLAMA_BASE_URL=http://localhost:11434
```

#### 기타 API Keys

```bash
# Brave Search
BRAVE_API_KEY=...

# Tavily
TAVILY_API_KEY=...

# Suno AI
SUNO_API_KEY=...
```

---

### 3. AntiGravity 설정

```bash
# 환경
ENVIRONMENT=dev  # dev, prod, test

# 자동 배포
AUTO_DEPLOY=true

# DRY_RUN 기본값
DRY_RUN_DEFAULT=true

# 중앙 설정 동기화
CENTRAL_CONFIG_SYNC=true

# 자동 동기화
AUTO_SYNC=true

# 자율 확장 모드
SELF_EXPANDING_MODE=true
```

---

### 4. MCP 설정

```bash
# MCP 서버 URL
MCP_SERVER_URL=http://localhost:8010

# 작업 공간 루트
WORKSPACE_ROOT=<LOCAL_WORKSPACE>/AFO_Kingdom
```

---

### 5. Soul Engine 설정

```bash
# Soul Engine URL
SOUL_ENGINE_URL=http://localhost:8010

# API 서버 포트
API_PORT=8010

# 프론트엔드 포트
FRONTEND_PORT=3000
```

---

## 📝 설정 파일 예시

### `.env` 파일

```bash
# ============================================================================
# AFO Kingdom Environment Variables
# ============================================================================

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

# AntiGravity
ENVIRONMENT=dev
AUTO_DEPLOY=true
DRY_RUN_DEFAULT=true

# MCP
MCP_SERVER_URL=http://localhost:8010
WORKSPACE_ROOT=<LOCAL_WORKSPACE>/AFO_Kingdom

# Soul Engine
SOUL_ENGINE_URL=http://localhost:8010
```

---

## 🔐 보안 설정

### 1. 환경 변수 보안

- `.env` 파일을 `.gitignore`에 추가
- 프로덕션에서는 Secrets Manager 사용

### 2. API 키 관리

- API Wallet을 통한 중앙 관리
- 암호화된 저장소 사용

### 3. 비밀번호 설정

```bash
# 강력한 비밀번호 생성
openssl rand -base64 32
```

---

## 🎯 설정 우선순위

1. **환경 변수** (`.env` 파일)
2. **환경별 설정 파일** (`settings_dev.py`, `settings_prod.py`)
3. **기본값** (`settings.py`)

---

## 📊 중앙 설정 시스템

### `config/settings.py`

```python
from pydantic_settings import BaseSettings

class AFOSettings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 15432
    POSTGRES_DB: str = "afo_memory"
    POSTGRES_USER: str = "afo"
    POSTGRES_PASSWORD: str = "afo_secret_change_me"
    
    REDIS_URL: str = "redis://localhost:6379"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
```

---

## 🔄 설정 동기화

### 자동 동기화

AntiGravity의 `AUTO_SYNC` 기능을 통해 설정이 자동으로 동기화됩니다:

```python
from config.antigravity import antigravity

# 자동 동기화 실행
antigravity.auto_sync()
```

### 수동 동기화

```bash
# 설정 내보내기
python scripts/export_keys.py

# 설정 가져오기
python scripts/import_keys.py
```

---

## 🧪 환경별 설정

### 개발 환경

```bash
ENVIRONMENT=dev
AUTO_DEPLOY=true
DRY_RUN_DEFAULT=true
```

### 프로덕션 환경

```bash
ENVIRONMENT=prod
AUTO_DEPLOY=false
DRY_RUN_DEFAULT=true
```

### 테스트 환경

```bash
ENVIRONMENT=test
AUTO_DEPLOY=false
DRY_RUN_DEFAULT=true
```

---

## 📚 관련 문서

- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [API Endpoints Reference](API_ENDPOINTS_REFERENCE.md)

---

**최종 업데이트**: 2025-01-27  
**담당**: 승상 (丞相) - AFO Kingdom

