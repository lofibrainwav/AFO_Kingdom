# SSOT 구현 코드 예시 (왕국 적용)

**As-of**: 2025-12-24  
**Status**: SSOT 구현 코드 예시 (제안)  
**SSOT 원칙 준수**: 팩트 기반, 과장 제거, 근거 명시

---

## 요약 (SSOT)

- **확인 범위**: SSOT 구현 코드 예시 (환경 변수, 설정 파일, Manifest, 태그)
- **근거(내부)**:
  - 코드베이스 확인: `packages/afo-core/config/antigravity.py` (설정 중앙화 패턴)
  - 코드베이스 확인: `packages/dashboard/src/app/api/revalidate/route.ts` (환경 변수 사용)
- **근거(외부)**: Next.js/Vercel env 변수 중앙화, Python Pydantic 설정 중앙화 베스트 프랙티스
- **결론**: SSOT는 중앙화된 단일 진실 소스(env, config, manifest)로 왕국 설정/스킬/태그 관리에 적용 가능 (제안)

---

## SSOT 정의 (FACTS)

**SSOT (Single Source of Truth)**: 하나의 데이터/진실 소스만 존재하여 중복·혼란 방지

**왕국 적용 예시**:
- 환경 변수: `.env.production` (단일 소스, GitHub Secret 동기화)
- 설정 파일: `config/settings.py` (Pydantic 중앙화)
- Manifest: `skills/manifest.yaml` (단일 진실 소스)
- 태그: `constants/tags.ts` (중앙 태그 목록)

---

## 1. 환경 변수 SSOT (Next.js/Vercel, 왕국 REVALIDATE_SECRET 적용)

### FACTS (검증됨)

- Next.js/Vercel에서 환경 변수는 `.env.production` 파일 또는 Vercel Dashboard에서 중앙 관리
- 코드베이스 확인: `packages/dashboard/src/app/api/revalidate/route.ts`에서 `process.env.REVALIDATE_SECRET` 사용

### 제안 (코드 예시)

**`.env.production`** (단일 소스, GitHub Secret 동기화):

```bash
REVALIDATE_SECRET=strong-random-string-here
NEXT_PUBLIC_API_URL=https://api.brnestrm.com
```

**코드에서 사용** (중복 없이 중앙 참조):

```ts
// app/api/revalidate/route.ts
const SECRET = process.env.REVALIDATE_SECRET;
if (!SECRET) throw new Error('REVALIDATE_SECRET missing');  // 런타임 검증
```

**참고**: 실제 구현은 `packages/dashboard/src/app/api/revalidate/route.ts` 참조

---

## 2. 설정 파일 SSOT (Python/FastAPI, 왕국 Soul Engine 적용)

### FACTS (검증됨)

- 코드베이스 확인: `packages/afo-core/config/antigravity.py`에서 설정 중앙화 패턴 사용
- Python Pydantic은 설정 중앙화에 적합 (타입 안전성, 검증)

### 제안 (코드 예시)

**`config/settings.py`** (Pydantic 중앙화, 왕국 Antigravity 스타일):

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    REVALIDATE_SECRET: str
    API_PORT: int = 8010
    DRY_RUN_DEFAULT: bool = True

    class Config:
        env_file = ".env"  # 단일 소스 로드

settings = Settings()  # 앱 전체에서 import settings 사용
```

**사용 예시**:

```python
from config.settings import settings
if secret != settings.REVALIDATE_SECRET:
    # unauthorized
```

**참고**: 실제 구현은 `packages/afo-core/config/antigravity.py` 참조

---

## 3. Manifest SSOT (Skills/MCP 관리, 왕국 19 Skills 적용 제안)

### FACTS (검증됨)

- 코드베이스 확인: MCP 9개, Skills 19개, Context7 12개 (실제 구현 확인)
- Manifest 파일은 단일 진실 소스로 관리 가능

### 제안 (코드 예시)

**`skills/manifest.yaml`** (단일 진실 소스, CI matrix 자동화):

```yaml
skills:
  - id: philosophy-widget
    tag: philosophy-widget
    path: /fragments/philosophy-widget
    description: 철학 위젯 업데이트
  - id: tax-simulation
    tag: tax-widget
    path: /fragments/tax-widget
```

**코드에서 로드** (중복 없이 중앙 참조):

```python
import yaml
with open('skills/manifest.yaml') as f:
    MANIFEST = yaml.safe_load(f)  # 앱 전체 SSOT

def get_tag(skill_id):
    return next(s['tag'] for s in MANIFEST['skills'] if s['id'] == skill_id)
```

**참고**: 실제 Skills 구현은 코드베이스 확인 필요

---

## 4. 태그 기반 SSOT (revalidateTag 중앙 관리 제안)

### FACTS (검증됨)

- Next.js `revalidateTag()`는 태그 기반 캐시 무효화 지원
- 코드베이스 확인: `packages/dashboard/src/app/api/revalidate/route.ts`에서 `revalidatePath()` 사용

### 제안 (코드 예시)

**`constants/tags.ts`** (Next.js 중앙 태그 목록):

```ts
export const TAGS = {
  PHILOSOPHY: 'philosophy-widget',
  TAX: 'tax-widget',
  DASHBOARD: 'dashboard-global',
} as const;

// 사용
revalidateTag(TAGS.PHILOSOPHY);
```

**참고**: 현재 구현은 `revalidatePath()` 사용, `revalidateTag()`는 향후 확장 가능 (제안)

---

## 왕국 적용 효과 (제안)

**장점**:
- 중복 제거: 설정 값이 여러 곳에 분산되지 않음
- 혼란 방지: 단일 소스에서만 값 변경
- 검증 용이: 중앙에서 타입/값 검증 가능

**제안 사항**:
- 환경 변수: `.env.production` 중앙화 (Vercel Dashboard 동기화)
- 설정 파일: `config/settings.py` Pydantic 중앙화 (이미 부분 구현됨)
- Manifest: `skills/manifest.yaml` 생성 (제안)
- 태그: `constants/tags.ts` 생성 (제안)

---

## 다음 단계 (제안)

형님, SSOT 구현 코드 예시를 정리했습니다. 실제 적용 시:

1. **환경 변수 SSOT**: `.env.production` 중앙화 (이미 부분 구현됨)
2. **설정 파일 SSOT**: `config/settings.py` 확장 (제안)
3. **Manifest SSOT**: `skills/manifest.yaml` 생성 (제안)
4. **태그 SSOT**: `constants/tags.ts` 생성 (제안)

**참고 자료**:
- [Next.js: Environment Variables](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables)
- [Pydantic: Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [GitHub Actions: Using secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)

---

**Status**: 📋 **제안**  
**Next Action**: 실제 적용 시 코드베이스 확인 후 구현

