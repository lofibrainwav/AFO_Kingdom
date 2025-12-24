# Ticket 5-A Commit 1: Edge Revalidate API 구현 가이드

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 1 (Edge Revalidate API)  
**Status:** 🟡 **Ready for Implementation**

---

## 📋 커밋 메시지 (Conventional Commits)

**확정 버전 (형님 승인):**

```txt
feat(dashboard): add fragment revalidate API route (edge, header-auth)
```

**대안 옵션:**

- Option B: `feat(dashboard): add fragment revalidate API (TICKET-5A commit1)`
- Option C: `feat(dashboard): implement /api/revalidate (edge, header-only secret, fragment path)`

---

## 🔧 구현 파일

**파일 경로**: `packages/dashboard/src/app/api/revalidate/route.ts`

**구현 내용:**
- Edge Runtime
- `x-revalidate-secret` 헤더 인증
- `fragmentKey` 파라미터 받기
- `revalidatePath("/fragments/{fragmentKey}.html")` 호출
- 성공/실패 응답

---

## ✅ 테스트 curl (4개)

### 1) ✅ 성공 케이스 (정상 revalidate)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"home-hero"}'
```

**예상 응답:**
```json
{
  "ok": true,
  "revalidated": ["/fragments/home-hero.html"]
}
```

**HTTP 상태 코드**: `200 OK`

---

### 2) ❌ 인증 실패 (헤더 없음)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"home-hero"}'
```

**예상 응답:**
```json
{
  "ok": false,
  "error": "unauthorized"
}
```

**HTTP 상태 코드**: `401 Unauthorized`

---

### 3) ❌ 입력값 실패 (fragmentKey 불량)

```bash
curl -i -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"../evil"}'
```

**예상 응답:**
```json
{
  "ok": false,
  "error": "invalid_fragmentKey"
}
```

**HTTP 상태 코드**: `400 Bad Request`

---

## 🔍 검증 curl (Revalidate 후 Fragment 확인)

### 검증 1-2타: Revalidate 후 Fragment 확인

```bash
# 1. Revalidate 호출
curl -sS -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"philosophy-widget"}'

# 2. Fragment 확인 (최신 캐시 반환 확인)
curl -sS -I "http://localhost:3000/fragments/philosophy-widget.html" | head -10
```

**예상 결과:**
- Revalidate 호출: `200 OK` + `{"revalidated": true, ...}`
- Fragment 확인: 최신 내용 반환 (캐시 헤더 확인)

---

## 🔒 SSOT 일관성 보장

### ✅ 유지할 것 (절대 건드리지 않음)

1. **SSOT 규칙**
   - slug 검증 (Contract Gate와 동일)
   - fragment_key 필수 (빌드 타임 검증)
   - 렌더링 우선순위 (React → Fragment → 404)

2. **Gate 검증**
   - 빌드 타임 검증 유지
   - Contract Gate 유지
   - fragment_key 검증 유지

3. **기존 Fragment**
   - `public/fragments/{fragment_key}.html` 유지
   - fragment overwrite 없음

### ✅ 확장 가능한 것 (읽기 경로만)

1. **Edge Revalidate**
   - On-demand revalidation API
   - Fragment revalidate (필수)
   - Page revalidate (선택적, Commit 2)

---

## ✅ 검증 체크리스트 (재현 가능)

### 1. Gate 영향 없음 보증

```bash
# Contract Gate 검증 (변경 없음)
python3 scripts/validate_widgets_json.py
# 예상: ✅ 통과

# TypeScript 타입 체크
pnpm -C packages/dashboard type-check
# 예상: ✅ 통과

# Next.js 빌드 (정적 생성 유지)
pnpm -C packages/dashboard build
# 예상: ✅ 통과
```

### 2. Revalidate API 테스트

```bash
# 환경변수 설정
export REVALIDATE_SECRET="dev-secret-key"

# 성공 케이스
curl -sS -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"philosophy-widget"}'

# 인증 실패 테스트
curl -sS -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -d '{"fragmentKey":"philosophy-widget"}'

# 입력값 실패 테스트
curl -sS -X POST "http://localhost:3000/api/revalidate" \
  -H "content-type: application/json" \
  -H "x-revalidate-secret: $REVALIDATE_SECRET" \
  -d '{"fragmentKey":"../evil"}'
```

---

## 🏁 결론

Commit 1 (Edge Revalidate API)는 **Fragment만 revalidate**하는 최소 구현입니다.

**안전 범위:**
- SSOT 규칙 유지
- Gate 영향 없음
- 기존 fragment 유지
- 읽기 경로만 확장

**구현 계획:**
- Edge Runtime
- `x-revalidate-secret` 헤더 인증
- Fragment revalidate만 (Page는 Commit 2)

---

**Status:** 🟡 **Ready for Implementation**  
**Next Action:** 구현 시작 (커밋 메시지 및 테스트 curl 준비 완료)

