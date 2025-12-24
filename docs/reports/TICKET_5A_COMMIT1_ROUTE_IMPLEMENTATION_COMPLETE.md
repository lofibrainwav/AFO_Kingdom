# Ticket 5-A Commit 1: Edge Revalidate API Route 구현 완료

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 1 (Edge Revalidate API Route)  
**Status:** 🟢 **Implementation Complete**

---

## ✅ 구현 완료

### 파일 생성

**파일 경로**: `packages/dashboard/src/app/api/revalidate/route.ts`

**구현 내용:**
- Edge Runtime (`export const runtime = "edge"`)
- `x-revalidate-secret` 헤더 인증
- `fragmentKey` 검증 (정규식: `/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/`)
- `revalidatePath("/fragments/{fragmentKey}.html")` 호출
- Query Parameter 금지 (보안)
- GET 메서드 차단 (405 Method Not Allowed)

---

## 📋 커밋 메시지 (확정)

```txt
feat(dashboard): add fragment revalidate API route (edge, header-auth)
```

---

## ✅ 테스트 curl (3개)

### 1) 성공 케이스

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

### 2) 헤더 없음 (401)

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

### 3) fragmentKey 불량 (400)

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

## ✅ 검증 체크리스트

### 1. TypeScript 타입 체크

```bash
pnpm -C packages/dashboard type-check
```

**결과**: ✅ 통과 (에러 없음)

---

## 🏁 결론

Commit 1 (Edge Revalidate API Route)는 **Fragment만 revalidate**하는 최소 구현입니다.

**안전 범위:**
- SSOT 규칙 유지 ✅
- Gate 영향 없음 ✅
- 기존 fragment 유지 ✅
- 읽기 경로만 확장 ✅

**구현 완료:**
- Edge Runtime ✅
- `x-revalidate-secret` 헤더 인증 ✅
- Fragment revalidate만 (Page는 Commit 2) ✅

---

**Status:** 🟢 **Implementation Complete**  
**Next Action:** Commit 2 (Page Revalidate 확장) 또는 Commit 3 (CI 통합)

