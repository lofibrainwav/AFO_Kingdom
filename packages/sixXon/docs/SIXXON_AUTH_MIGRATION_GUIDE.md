# SixXon Auth Migration Guide: Browser Session → OAuth 2.1

**목적**: 브라우저 세션 캡처에서 OAuth 2.1 + Refresh Token 기반으로 전환

**원칙**: 프릭션 최소화, 영속성(永) 우선

---

## 현재 상태 vs 목표 상태

### 현재 (Browser Session)

```
sixxon auth login claude
  → 브라우저 열어서 로그인
  → 쿠키/로컬스토리지 캡처
  → Wallet에 암호화 저장
  → 재사용 시 세션 로드

문제점:
- 세션 만료/2FA/Cloudflare 재인증 반복
- 계정 잠금/탐지 리스크
- 자동화가 사이트 UI에 종속
```

### 목표 (OAuth 2.1)

```
sixxon auth login claude
  → OAuth 2.1 흐름 시작
  → Access Token + Refresh Token 받음
  → Wallet에 토큰 저장
  → 만료 시 자동 refresh

장점:
- 표준 프로토콜, 안정적
- 자동 갱신, 프릭션 최소
- 보안 베스트 프랙티스 준수
```

---

## 마이그레이션 전략

### Phase 1: 병행 운영 (현재)

- 기존 브라우저 세션 방식 유지
- OAuth 방식 추가 (새 provider부터)
- 사용자가 선택 가능

### Phase 2: OAuth 우선 (6개월 후)

- 새 인증은 OAuth만 지원
- 브라우저 세션은 "legacy" 표시
- 마이그레이션 가이드 제공

### Phase 3: 브라우저 세션 Deprecation (1년 후)

- 브라우저 세션 방식 제거
- OAuth만 지원

---

## Provider별 OAuth 지원 현황

| Provider | OAuth 지원 | 구현 상태 | 우선순위 |
|----------|-----------|----------|---------|
| Google (Gmail, Gemini) | ✅ OAuth 2.0 | 구현 가능 | P0 (정석) |
| Anthropic (Claude) | ⚠️ 확인 필요 | 조사 중 | P1 |
| OpenAI (Codex) | ✅ OAuth 2.1 | 구현 가능 | P1 |
| 기타 | ❌ OAuth 없음 | 브라우저 세션 유지 | P2 |

---

## 구현 가이드

### Google OAuth (Gmail, Gemini)

**라이브러리:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

**코드 예시:**
```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# OAuth flow 시작
flow = Flow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly'],
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)
auth_url, _ = flow.authorization_url()
# 브라우저 열어서 인증
# authorization_code 받아서
flow.fetch_token(code=authorization_code)
credentials = flow.credentials

# Wallet에 저장
wallet.save_token(
    provider="gmail",
    access_token=credentials.token,
    refresh_token=credentials.refresh_token,
    expires_at=credentials.expiry
)
```

### Anthropic OAuth (Claude)

**현재 상태:** 확인 필요

**가능한 옵션:**
1. Anthropic API Key 기반 (OAuth 없음)
2. 브라우저 세션 유지 (fallback)
3. Anthropic OAuth 출시 대기

### OpenAI OAuth (Codex)

**라이브러리:**
```bash
pip install openai
```

**코드 예시:**
```python
from openai import OpenAI

# OAuth flow (OpenAI Apps SDK 스타일)
# https://developers.openai.com/apps-sdk/build/auth/
```

---

## Wallet Storage 구현

### macOS Keychain (로컬)

```python
import subprocess
import json

def save_to_keychain(provider: str, token_data: dict):
    """Save token to macOS Keychain."""
    key = f"sixxon_{provider}_token"
    value = json.dumps(token_data)
    
    subprocess.run([
        "security", "add-generic-password",
        "-a", "sixxon",
        "-s", key,
        "-w", value,
        "-U"  # Update if exists
    ], check=True)

def load_from_keychain(provider: str) -> dict | None:
    """Load token from macOS Keychain."""
    key = f"sixxon_{provider}_token"
    
    result = subprocess.run([
        "security", "find-generic-password",
        "-a", "sixxon",
        "-s", key,
        "-w"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        return None
    
    return json.loads(result.stdout.strip())
```

### 서버 Vault (HashiCorp Vault)

```python
import hvac

def save_to_vault(provider: str, token_data: dict):
    """Save token to HashiCorp Vault."""
    client = hvac.Client(url=os.getenv("VAULT_URL"))
    client.token = os.getenv("VAULT_TOKEN")
    
    client.secrets.kv.v2.create_or_update_secret(
        path=f"sixxon/{provider}",
        secret=token_data
    )
```

---

## MCP 통합 예시

### MCP Tool에서 Wallet 토큰 사용

```python
# MCP tool 구현
@mcp.tool()
async def ask_claude(prompt: str) -> str:
    """Ask Claude via OAuth token from Wallet."""
    
    # Wallet에서 토큰 요청
    token = wallet.get_token(provider="claude")
    
    if not token:
        raise MCPError(
            code="UNAUTHENTICATED",
            message="Run `sixxon auth login claude` first"
        )
    
    # 만료면 자동 refresh
    if token.is_expired():
        token = wallet.refresh_token(provider="claude")
    
    # API 호출
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Authorization": f"Bearer {token.access_token}"},
            json={"model": "claude-3-opus", "messages": [{"role": "user", "content": prompt}]}
        )
        
        if response.status_code == 401:
            # Token 만료, refresh 후 재시도
            token = wallet.refresh_token(provider="claude")
            response = await client.post(...)  # 재시도
        
        return response.json()["content"][0]["text"]
```

---

## 에러 처리 (`www_authenticate` 스타일)

### MCP Error Format

```python
class MCPError(Exception):
    def __init__(self, code: str, message: str, auth_hint: str | None = None):
        self.code = code
        self.message = message
        self.auth_hint = auth_hint  # "Run `sixxon auth login claude`"
```

### MCP Tool 응답

```json
{
  "error": {
    "code": "UNAUTHENTICATED",
    "message": "Authentication required",
    "data": {
      "auth_hint": "Run `sixxon auth login claude`",
      "provider": "claude",
      "wallet_status": "no_token"
    }
  }
}
```

---

## 마이그레이션 체크리스트

### 사용자 (형님)

- [ ] `sixxon auth login claude` (OAuth 방식으로 재로그인)
- [ ] `sixxon auth status` 확인 (OAuth 토큰 저장 확인)
- [ ] 기존 브라우저 세션 삭제: `sixxon auth logout --provider=claude --legacy`

### 개발자 (구현)

- [ ] Google OAuth 구현 (Gmail, Gemini)
- [ ] Anthropic OAuth 확인/구현 (Claude)
- [ ] OpenAI OAuth 구현 (Codex)
- [ ] Wallet Storage 구현 (Keychain/Vault)
- [ ] MCP 통합 (토큰 요청 로직)
- [ ] 자동 refresh 로직
- [ ] 에러 핸들링 (`www_authenticate` 스타일)

---

## 참고 문서

- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [OpenAI Apps SDK Auth](https://developers.openai.com/apps-sdk/build/auth/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)

---

**"한 번만 인증하고, 물처럼 흐르는 자동화."**

**OAuth 2.1 + Refresh Token = 영속성(永)의 길**
