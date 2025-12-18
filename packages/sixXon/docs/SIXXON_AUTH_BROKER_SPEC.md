# SixXon Auth Broker 최소 명세 (OAuth 2.1 + Subscription 모드)

**목표**: "한 번만 인증 → 갱신 가능한 토큰 → 물처럼 흐르는 자동화"

**원칙**: MCP는 인증을 직접 들지 않고, Wallet에서 토큰을 요청만 함.

---

## 현재 우선순위(현실 정렬)

SixXon은 “API 키 강제”가 아니라 **월구독(웹 로그인) 기반** 사용을 먼저 지원합니다.

- **정본(현재 SSOT)**: `docs/SIXXON_AUTH_SUBSCRIPTION_FLOW.md`
- **이 문서의 범위**: OAuth 기반 Auth Broker를 **Stage 2+ (가능한 provider 한정)**으로 정리한 최소 명세

즉, “지금 당장”의 기본 루트는 다음입니다:

1. `sixxon auth capture --provider <name> --browser system-chrome --refresh`
2. `sixxon auth status` (decryptable 확인)
3. `sixxon auth open` (수동 사용; 가장 안정적)

## 핵심 구조 (3-Layer)

```
Layer A: SixXon CLI (Auth Broker)
  ↓
Layer B: Wallet (Secure Storage)
  ↓
Layer C: MCP (Token Request Only)
```

---

## Layer A: SixXon CLI 명령어

### `sixxon auth login <provider>`

**동작:**
1. 브라우저 열어서 OAuth 2.1 흐름 시작
2. 사용자가 한 번만 로그인 (최초 1회)
3. **Access Token + Refresh Token** 받아서 Wallet에 저장
4. 결과: `✅ Authenticated. Token saved to wallet.`

**지원 Provider:**
- `claude` (Anthropic OAuth)
- `codex` (OpenAI OAuth)
- `gemini` (Google OAuth)
- `gmail` (Google OAuth)

**저장 위치:** macOS Keychain (로컬) 또는 서버 Vault

---

### `sixxon auth status`

**출력 (3줄):**
```
Status: OK | Providers: claude, gemini
Next: Run `sixxon auth refresh` if tokens expire
Receipt: logs/receipts/auth_status_20251213_143022
```

**JSON 출력 (`--json`):**
```json
{
  "status": "OK",
  "providers": {
    "claude": {
      "authenticated": true,
      "token_expires_at": "2025-12-20T10:00:00Z",
      "refresh_available": true
    },
    "gemini": {
      "authenticated": true,
      "token_expires_at": "2025-12-15T14:30:00Z",
      "refresh_available": true
    }
  }
}
```

---

### `sixxon auth refresh [--provider=<name>]`

**동작:**
1. Wallet에서 Refresh Token 꺼내기
2. OAuth Provider에 Refresh 요청
3. 새 Access Token 받아서 Wallet 갱신
4. 결과: `✅ Token refreshed. Expires: 2025-12-20T10:00:00Z`

**자동 갱신:**
- Token 만료 1시간 전에 자동 갱신 (선택)
- `--auto` 플래그로 활성화

---

### `sixxon auth logout [--provider=<name>]`

**동작:**
1. Wallet에서 토큰 삭제
2. (선택) OAuth Provider에 Revoke 요청
3. 결과: `✅ Logged out. Token removed from wallet.`

---

## Layer B: Wallet Storage (Secure)

### 저장 위치 우선순위

1. **macOS Keychain** (로컬 최고)
   - `security add-generic-password -a "sixxon" -s "claude_token" -w "<token>"`
   - 암호화 자동, OS 레벨 보안

2. **서버 Vault** (서버 환경)
   - HashiCorp Vault / AWS Secrets Manager
   - 환경 변수: `SIXXON_VAULT_URL`

3. **로컬 파일** (fallback, 암호화 필수)
   - `~/.sixxon/wallet/` (gitignored)
   - AES-256-GCM 암호화
   - Master key는 Keychain에만 저장

### 저장 형식

```json
{
  "provider": "claude",
  "access_token": "encrypted...",
  "refresh_token": "encrypted...",
  "expires_at": "2025-12-20T10:00:00Z",
  "token_type": "Bearer",
  "scope": "read write"
}
```

**절대 금지:**
- 레포/깃에 토큰 저장 (암호화해도 리스크)
- 평문 토큰 저장

---

## Layer C: MCP Token Request

### MCP Tool 호출 시

**에러 처리:**
```python
# MCP tool이 401 Unauthorized 받으면
if response.status == 401:
    # Wallet에서 토큰 요청
    token = wallet.get_token(provider="claude")
    
    # 만료면 자동 refresh
    if token.is_expired():
        token = wallet.refresh_token(provider="claude")
    
    # 재시도
    response = retry_with_token(token)
```

**MCP는 토큰을 소유하지 않음:**
- MCP 서버는 토큰을 직접 저장하지 않음
- 필요할 때만 Wallet에서 요청
- 토큰 만료 시 자동 refresh (또는 에러 반환)

---

## 브라우저 세션 캡처 (Fallback Only)

**Subscription(월구독) 플로우:**
- OAuth가 제공되지 않거나(또는 API 키가 목적이 아닐 때) 월구독 웹 로그인 흐름을 사용합니다.
- `sixxon auth capture <provider>`로 세션을 Wallet에 저장하고,
- `sixxon auth open`으로 수동 사용을 기본값으로 둡니다.

**OAuth 플로우(가능한 경우):**
- OAuth를 지원하는 provider에 한해 `sixxon auth login/refresh`를 사용합니다.
  - 지원 여부가 불명확하면 “가능”을 단정하지 않고, Receipt로 검증 후 문서화합니다.

---

## 구현 우선순위

### Phase 1: OAuth 기반 Wallet (정석)

1. **Google OAuth** (Gmail, Gemini)
   - `google-auth` 라이브러리 사용
   - Refresh token 자동 관리

2. **Anthropic OAuth** (Claude)
   - OAuth 2.1 흐름 구현
   - Refresh token 지원 확인

3. **OpenAI OAuth** (Codex)
   - OAuth 2.1 흐름 구현
   - API key → OAuth 전환 가이드

### Phase 2: MCP 통합

- MCP tool에서 Wallet 토큰 요청
- 자동 refresh 로직
- 에러 핸들링 (`www_authenticate` 스타일)

### Phase 3: 브라우저 세션 Deprecation

- 브라우저 세션 캡처는 "legacy"로 표시
- OAuth로 마이그레이션 가이드 제공

---

## 보안 원칙 (眞善美孝永)

- **眞 (Truth)**: 모든 토큰은 Wallet에만 저장, MCP는 소유하지 않음
- **善 (Goodness)**: Keychain/Vault 사용, 평문 저장 금지
- **美 (Beauty)**: 간단한 CLI 인터페이스, 3줄 출력
- **孝 (Serenity)**: 자동 refresh, 만료 걱정 없음
- **永 (Eternity)**: OAuth 표준 준수, 장기 안정성

---

## 예시 사용법

```bash
# 1. 최초 로그인 (한 번만)
$ sixxon auth login claude
Opening browser for OAuth login...
✅ Authenticated. Token saved to wallet.

# 2. 상태 확인
$ sixxon auth status
Status: OK | Providers: claude, gemini
Next: Tokens valid until 2025-12-20
Receipt: logs/receipts/auth_status_20251213_143022

# 3. MCP tool 사용 (자동으로 Wallet에서 토큰 가져옴)
$ sixxon toolflow "ask claude about philosophy"
# MCP가 자동으로 Wallet에서 토큰 요청 → 사용

# 4. 토큰 만료 시 (자동 refresh)
$ sixxon toolflow "ask claude..."
# Token expired, refreshing...
✅ Token refreshed. Continuing...
```

---

**"한 번만 인증하고, 물처럼 흐르는 자동화."**

**MCP는 요청만 하고, Wallet이 인증을 관리한다.**
