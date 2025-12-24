# Ticket 5A 최종 완료 보고서 (Edge Revalidate)

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A 전체 완료 상태  
**Status:** 🟢 **Commit 1 Implementation Complete**

---

## 1) 완료 범위 (팩트)

### Commit 1 — 구현 완료 ✅

- **파일**: `packages/dashboard/src/app/api/revalidate/route.ts`
- **Edge Runtime**: `export const runtime = "edge"`
- **인증**: `x-revalidate-secret` 헤더 필수
- **입력 검증**: fragmentKey 정규식 `/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/` (공백 없음)
- **동작**: `revalidatePath("/fragments/{fragmentKey}.html")`
- **보안**: Query Parameter 금지
- **GET 차단**: 405 Method Not Allowed
- **검증**: TypeScript 타입 체크 통과 (에러 0)

### Commit 2 — 선택 기능 (미구현/준비) 🟡

- **목적**: Fragment + Page 동시 revalidate (pageSlug 선택)
- **상태**: 필요 시 Commit 2로 구현 가능 (현재는 예시만 존재)
- **파일**: `packages/dashboard/src/app/api/revalidate/route.ts` (Commit 1 수정)

### Commit 3 — CI 통합 (설계/예시 단계) 🟡

- **목적**: 변경된 fragment에 대해 CI에서 revalidate API 호출 자동화
- **상태**: 워크플로우 YAML 예시 준비 (적용 전)
- **파일**: `.github/workflows/revalidate.yml` (예시)

---

## 2) SSOT 안전 범위 (팩트)

- Gate 영향 없음
- SSOT 경로 0 변경
- 읽기 경로만 확장
- fragment overwrite 금지 유지

---

## 3) 모노레포 팩트체크 (팩트)

- **루트**: `package-lock.json` 존재 (npm 흔적/사용 가능)
- **packages/dashboard**: `pnpm-lock.yaml` 존재 (pnpm 사용 확인)

---

## 4) 테스트 (팩트)

### curl 3종

#### 1) 성공 (200)

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

#### 2) 헤더 없음 (401)

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

#### 3) fragmentKey 불량 (400)

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

---

## 5) 커밋 메시지 (확정)

```txt
feat(dashboard): add fragment revalidate API route (edge, header-auth)
```

---

## 6) 참고 자료

- **실제 구현**: `packages/dashboard/src/app/api/revalidate/route.ts`
- **설계 문서**: `docs/reports/TICKET_5A_COMMIT3_EDGE_REVALIDATE_DESIGN_SSOT.md`
- **구현 가이드**: `docs/reports/TICKET_5A_COMMIT1_REVALIDATE_API_IMPLEMENTATION.md`

---

**Status:** 🟢 **Commit 1 Implementation Complete**  
**Next Action:** Commit 2 (선택) 또는 Commit 3 (CI 통합)

