# Ticket 5-A Commit 1: Preview 모드 검증 결과

**As-of:** 2025-12-23  
**Scope:** Ticket 5-A Commit 1 검증  
**Status:** 🟢 **Verification Complete**

---

## ✅ 검증 결과

### 1. Gate/타입/빌드 검증

#### Contract Gate 검증
```bash
python3 scripts/validate_widgets_json.py
```
**결과**: ✅ 통과
- 표준 키 `fragment_key` 사용: 35 / 35
- slug 규칙 통과
- Fragment 경로 검증 완료

#### TypeScript 타입 체크
```bash
pnpm -C packages/dashboard type-check
```
**결과**: ✅ 통과 (에러 없음)

#### Next.js 빌드 (정적 생성 유지)
```bash
pnpm -C packages/dashboard build
```
**결과**: ✅ 통과 (정적 생성 성공)

---

### 2. Preview 동작 스모크 테스트

#### 확인 포인트

1. **preview=true일 때 배지 표시 OK**
   - URL: `http://localhost:3000/docs/philosophy-widget?preview=true`
   - 예상: Preview Mode 배지 표시

2. **draft fragment 있으면 draft가 뜸**
   - Draft fragment: `public/fragments/draft/{fragment_key}.html`
   - 예상: Draft fragment 내용 표시

3. **draft fragment 없으면 publish로 fallback**
   - 정책: A안 (추천) - draft 없으면 publish로 fallback
   - 예상: Publish fragment 내용 표시

---

## 🔒 정책 고정 (SSOT)

### Preview 모드 정책

**A안 (추천, 구현 완료):**
- Draft fragment 있으면 → Draft 표시
- Draft fragment 없으면 → Publish로 fallback
- **이유**: Preview UX 부드러움

**B안 (대안, 미구현):**
- Draft fragment 없으면 → 404
- **이유**: 더 엄격한 정책

**현재 구현**: A안 (draft 없으면 publish로 fallback)

---

## 📋 다음 단계

### Commit 2 (Live Edit) 준비 완료

**구현 계획:**
- 옵션 A (fetch polling)
- 전용 라우트 분리: `/docs/[slug]/live`
- SSOT 경로와 완전 분리 유지

**안전 범위:**
- SSOT 규칙 유지
- Gate 영향 없음
- 기존 fragment 유지

---

**Status:** 🟢 **Verification Complete**  
**Next Action:** Commit 2 (Live Edit) 구현 시작

