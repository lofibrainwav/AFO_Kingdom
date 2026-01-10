# AFO Kingdom 코드베이스 감사 보고서

**감사일**: 2026-01-07
**브랜치**: `chore/phase11-hardening`
**감사자**: Zilong (Claude Code - 眞 Sword)

---

## Executive Summary

AFO Kingdom 코드베이스에 대한 종합 감사를 수행했습니다.
총 **180개 이슈**가 발견되었으며, CRITICAL 16개, HIGH 42개, MEDIUM 76개, LOW 46개로 분류됩니다.

| 카테고리 | CRITICAL | HIGH | MEDIUM | LOW | 합계 |
|----------|----------|------|--------|-----|------|
| 보안 | 12 | 4 | 6 | - | 22 |
| 코드 품질 | 3 | 31 | 66 | 44 | 144 |
| 아키텍처 | 1 | 7 | 4 | 2 | 14 |
| **합계** | **16** | **42** | **76** | **46** | **180** |

---

## 1. CRITICAL 이슈 (즉시 조치 필요)

### 1.1 XSS 취약점 (Cross-Site Scripting)

| # | 파일 | 라인 | 문제 | Risk |
|---|------|------|------|------|
| 1 | `packages/dashboard/src/components/docs/MarkdownViewer.tsx` | 63 | `dangerouslySetInnerHTML` 새니타이징 없음 | +25 |
| 2 | `packages/dashboard/src/components/live/LiveEditPoller.tsx` | 99 | 외부 HTML 직접 렌더링 | +25 |
| 3 | `packages/dashboard/src/app/docs/[slug]/page.tsx` | 127 | 파일 콘텐츠 무검증 주입 | +25 |
| 4 | `packages/dashboard/src/components/docs/MermaidDiagram.tsx` | 87 | `securityLevel: "loose"` | +15 |

**권장 조치**:
- DOMPurify 라이브러리로 HTML 새니타이징
- Mermaid `securityLevel: "strict"` 변경
- Content Security Policy (CSP) 헤더 추가

### 1.2 하드코딩된 시크릿

| # | 파일 | 라인 | 내용 | Risk |
|---|------|------|------|------|
| 1 | `packages/afo-core/config/settings.py` | 60 | `"afo_secret_change_me"` | +60 |
| 2 | `packages/afo-core/config/settings.py` | 113 | `"default_yungdeok_key"` | +60 |
| 3 | `packages/afo-core/api/utils/auth.py` | 32 | JWT 시크릿 하드코딩 | +60 |

**권장 조치**:
- 모든 시크릿을 환경변수로 이동
- 프로덕션 시작 시 필수 환경변수 검증
- `.env.example` 템플릿 제공

### 1.3 자격증명 추출 스크립트 (분석 결과)

아래 스크립트들은 **브라우저 쿠키 복호화 및 세션 토큰 추출** 기능을 포함합니다:

| # | 파일 | 기능 | 위험 수준 |
|---|------|------|----------|
| 1 | `scripts/admin/decrypt_chrome_cookies.py` | Chrome/Chromium 쿠키 복호화, macOS Keychain 접근 | CRITICAL |
| 2 | `scripts/admin/extract_openai_auth_token.py` | OpenAI 세션 토큰 추출 | CRITICAL |
| 3 | `scripts/admin/extract_openai_force.py` | 강제 토큰 추출 | CRITICAL |
| 4 | `scripts/admin/extract_claude_force.py` | Claude/Anthropic 토큰 추출 | CRITICAL |

**기능 분석**:
- `decrypt_chrome_cookies.py`: Chromium 쿠키 DB에서 `session`, `auth`, `key`, `token` 패턴 검색
- PostgreSQL에 평문으로 자격증명 저장
- 사용자 동의 메커니즘 없음
- 감사 로깅 없음

**권장 조치**:
- 접근 제어 (RBAC) 구현
- 저장 시 암호화 (Vault 또는 KMS)
- 명시적 사용자 동의 UI
- 모든 자격증명 접근에 대한 감사 로깅

---

## 2. HIGH 이슈

### 2.1 500줄 규칙 위반 (31개 파일)

CLAUDE.md §Boundaries에 명시된 "500-line rule" 위반:

| # | 파일 | 라인 수 | 권장 조치 |
|---|------|---------|----------|
| 1 | `afo_skills_registry.py` | 1,366 | 스킬 카테고리별 모듈 분리 |
| 2 | `llm_router.py` | 944 | 라우팅 결정 로직 분리 |
| 3 | `api_wallet.py` | 910 | 엔드포인트별 라우터 분리 |
| 4 | `AFO/multimodal/music_provider.py` | 899 | 프로바이더별 분리 |
| 5 | `AFO/skills/skill_041_royal_library.py` | 872 | 기능별 헬퍼 분리 |
| 6 | `api/routers/chancellor_router.py` | 844 | 노드별 핸들러 분리 |
| 7 | `services/hybrid_rag.py` | 795 | RAG 컴포넌트 분리 |
| 8 | `AFO/julie/ai_agents.py` | 732 | 에이전트별 클래스 분리 |
| 9 | `api/compat.py` | 729 | 호환성 레이어 정리 |
| 10 | `api/services/skills_service.py` | 725 | 서비스 레이어 분리 |
| ... | (21개 더) | 500-729 | - |

### 2.2 Bare Exception 처리 (3개)

예외를 구체화하지 않고 삼키는 안티패턴:

```python
# matching_engine.py:331
except:
    print("새 인덱스 생성 중...")  # 모든 예외 무시

# mlx_unified_memory.py:60
except:
    return "Unknown"  # 디버깅 불가

# ticket_generator.py:484
except:
    skeleton_index = indexer.scan_folders()  # 오류 로깅 없음
```

**권장 조치**:
```python
# 수정 예시
except (FileNotFoundError, IndexError) as e:
    logger.warning(f"Index load failed: {e}, creating new...")
```

### 2.3 인증 취약점

| # | 파일 | 라인 | 문제 |
|---|------|------|------|
| 1 | `api/routers/auth.py` | 167-180 | 폴백 인증이 비암호화 `hash()` 사용 |
| 2 | `api/routers/auth.py` | 111 | 타이밍 공격 취약한 비밀번호 비교 |
| 3 | `api/routers/auth.py` | 38-118 | `/keys` 엔드포인트 인증 없음 |

---

## 3. MEDIUM 이슈

### 3.1 순환 임포트 (아키텍처 위반)

```python
# AFO/chancellor_graph.py:9-12
from api.chancellor_v2.graph import nodes  # Domain → API (금지)
from api.chancellor_v2.graph.runner import run_v2
```

4-Layer Architecture 위반: Domain 레이어가 API 레이어에 의존

### 3.2 코드 중복 (~95% 유사)

| 원본 | 중복 | 유사도 |
|------|------|--------|
| `afo_agent_fabric.py` | `afo_agent_fabric_v2.py` | ~95% |
| `mipro_optimizer.py` | `mipro/optimizer.py` | ~80% |

### 3.3 미완성 구현 (TODO 14개)

| # | 파일 | 내용 |
|---|------|------|
| 1 | `AFO/audit.py` | "TICKET-XXX" 미추적 |
| 2 | `AFO/rag_flag.py` | "실제 RAG 파이프라인 호출" 2건 |
| 3 | `api/routers/users.py:267,295` | 유저 CRUD 미구현 |
| 4 | `api/routes/wallet/setup.py` | API 키 저장 미구현 |
| 5 | `AFO/cache/query_cache.py` | 패턴 기반 캐시 무효화 미구현 |

### 3.4 타입 안전성 문제

- **66개 파일**에 `type: ignore` 사용 (전체 12%)
- `llm_router.py:115`: 중복 `type: ignore[assignment]` (복붙 오류)
- `legacy/chancellor_graph.py:19-78`: 14개 연속 type: ignore

### 3.5 Docker 보안 비활성화

```yaml
# docker-compose.hardened.yml
# Line 28: PostgreSQL non-root user DISABLED
# Line 67: Qdrant non-root user DISABLED
# Line 77, 91: Common security DISABLED
```

---

## 4. LOW 이슈

| 문제 | 개수 | 파일 예시 |
|------|------|----------|
| Wildcard imports (`from X import *`) | 5 | `browser_auth/*.py` |
| `print()` 대신 logging | 15 | `dspy_metrics.py`, `matching_engine.py` |
| Silent `pass` statements | 24 | 다수 |
| 글로벌 상태 사용 | 10 | `afo_agent_fabric.py`, `zerotrust/rate_limiting.py` |
| 백업 파일 (.bak) | 4 | `api_server.py.bak.*` |

---

## 5. 현재 CI 상태

| Gate | 상태 | 결과 |
|------|------|------|
| pytest (善) | PASS | 320/324 통과, 4 skipped |
| Import | WARN | 18개 모듈 safe import 실패 |
| Git | INFO | 14개 파일 수정됨 (미커밋) |

### Safe Import 실패 목록

```
AFO.api.routers.aicpa: No module named 'AFO.service'
AFO.api.routers.thoughts: No module named 'sse_starlette'
AFO.api.routers.learning_log_router: No module named 'sqlmodel'
AFO.api.routes.serenity_router: No module named 'playwright'
AFO.api.routers.ssot: cannot import name 'TrinityInputs'
api.routes.wallet: cannot import name 'API_PROVIDERS'
... (총 18개)
```

---

## 6. 권장 조치 우선순위

### 즉시 (오늘)
1. XSS 취약점 수정 - DOMPurify 적용
2. Mermaid `securityLevel: "strict"` 변경
3. 시크릿 환경변수 이동

### 단기 (이번 주)
4. 인증 폴백 메커니즘 제거
5. bare except → specific exception 변경
6. API 키 엔드포인트 인증 추가

### 중기 (이번 스프린트)
7. 500줄 초과 파일 분할 (상위 10개)
8. 순환 임포트 해결
9. v1/v2 코드 통합

### 장기 (분기)
10. type:ignore 감소 (66 → 20 목표)
11. Docker 보안 재활성화
12. 테스트 커버리지 85% 달성

---

## 7. SSOT 정합성 확인

| SSOT 문서 | 정합성 |
|-----------|--------|
| AGENTS.md §7 금지 구역 | 준수 (수정 안함) |
| CLAUDE.md §Boundaries | 위반 발견 (500줄 규칙) |
| AFO_ROYAL_LIBRARY.md #3 병자궤도야 | 준수 (DRY_RUN 모드) |
| AFO_ROYAL_LIBRARY.md #25 사랑보다 두려움 | 위반 (66개 type:ignore) |

---

## 8. Evidence (永)

```
분석 일시: 2026-01-07T16:40:00+09:00
브랜치: chore/phase11-hardening
커밋: dc5da173
분석 범위: packages/afo-core, packages/dashboard, packages/trinity-os
총 파일: 506 Python + 123 TypeScript
총 라인: 92,821 (backend) + 28,410 (frontend)
```

---

**이 문서는 AFO Kingdom의 眞 (Truth) 기둥에 따라 객관적 사실만을 기록합니다.**
