# Ticket 3 진입 전 Gate 보강 최종 완료 (SSOT)

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7

---

## ✅ 완료 요약 (SSOT)

### 1. Rust/PyO3 연구 격리 완료
- `docs/research/MATURIN_PYO3_NOTES.md`
- `NOT_IN_SCOPE: do not implement until Ticket5+`

### 2. Ticket 3 진입 전 Gate 보강 완료

#### Gate 1: slug 규칙 + 중복 체크
- **slug = `id`에서 파생** (`widget-` 제거)
- **SSOT 규칙**:
  - 허용 문자: `a-z`, `0-9`, `-`, `가-힣`
  - 공백/언더스코어/대문자 불가
  - 연속 하이픈(`--`), 양끝 하이픈(`-foo` / `foo-`) 불가
- 중복 체크 포함

#### Gate 2: fragment 포인터 필드 점검 (경고)
- **표준 키**: `fragment_key` (Ticket 3에서 표준화 예정)
- **Fallback (읽을 때만)**: `fragment_key ?? html_section_id ?? sourceId`
- **생성(Node)은 무조건 `fragment_key`만 사용**
- 현재: `fragment_key`(권장) / `html_section_id` / `sourceId` 탐지
- Ticket 3에서 **`fragment_key`로 표준화 예정**

### 3. 검증 통과
- Widget count: 35 / validated: 35
- Slug 규칙: OK (허용 문자: a-z, 0-9, -, 가-힣)
- Fragment 포인터 점검: OK (경고 레벨)

---

## 🔧 수정된 파일

1. `scripts/validate_widgets_json.py` - Gate 보강 수정
   - slug 규칙 명확화 (허용 문자셋 명시, 연속/양끝 하이픈 체크)
   - fragment_key 표준화 (fallback은 읽을 때만)

2. `packages/afo-core/models/widget_spec.py` - Pydantic 모델 업데이트
   - `fragment_key` 필드 추가 (표준)
   - `html_section_id`, `sourceId`는 legacy (fallback)

3. `docs/reports/TICKET_3_GATE_BOOSTER_COMPLETE.md` - 문서 업데이트

---

## 🎯 Ticket 3 첫 커밋 체크리스트 (실수 방지)

### 1. fragment_key 표준화 결정
- Node generator가 `fragment_key`만 생성하도록 수정
- 기존 `sourceId` / `html_section_id`는 읽을 때만 fallback

### 2. HTML에서 섹션 찾는 기준 결정
- `id` 속성 사용?
- `data-widget-id` 속성 사용?
- 둘 다 지원?

### 3. fragment 저장 경로 고정
- 예: `packages/dashboard/public/fragments/{slug}.html`
- 또는: `packages/dashboard/src/generated/fragments/{slug}.html`

### 4. `/docs/[slug]` 라우트에서 sanitize + 404 처리
- slug sanitize (허용 문자셋 검증)
- 파일 없으면 404 반환

---

## 📋 다음 단계

### Ticket 3 준비 완료
- ✅ Gate 보강 완료 (slug 규칙 명확화, fragment_key 표준화)
- ✅ Rust/PyO3 문서 격리 완료
- ✅ 검증 통과

### Ticket 3 작업
- HTML fragment 추출 (각 위젯의 innerHTML)
- 빌드 타임에 섹션별 HTML fragment 파일 생성
- `/docs/[slug]`에서 fragment 렌더
- React 위젯이 있으면 override(교체)

---

**상태**: Ticket 3 진입 전 Gate 보강 최종 완료. Ticket 3 진행 가능.

