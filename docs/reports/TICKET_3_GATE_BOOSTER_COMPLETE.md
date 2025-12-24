# Ticket 3 진입 전 Gate 보강 완료

**날짜**: 2025-12-23  
**방법**: Sequential Thinking + Context7

---

## ✅ 완료된 작업

### 1. Rust/PyO3 문서 격리
- ✅ `docs/research/MATURIN_PYO3_NOTES.md` 생성
- ✅ 기존 Rust/PyO3 관련 문서를 research 폴더로 이동
- ✅ `NOT_IN_SCOPE (Do not implement until Ticket5+)` 명시

### 2. Ticket 3 진입 전 Gate 보강
- ✅ **Gate 1: slug 규칙 고정 + 중복 체크**
  - slug는 id에서 파생 (id 자체가 slug)
  - **SSOT 규칙**:
    - 허용 문자: 소문자 `a-z`, 숫자 `0-9`, 하이픈 `-`, 한글 `가-힣`
    - 공백/언더스코어/대문자 불가
    - 연속 하이픈(`--`), 양끝 하이픈(`-foo` / `foo-`) 불가
  - 중복 체크 포함

- ✅ **Gate 2: fragment 경로 필드 유무 체크**
  - **표준 키**: `fragment_key` (Ticket 3에서 표준화 예정)
  - **Fallback (읽을 때만)**: `fragment_key ?? html_section_id ?? sourceId`
  - **생성(Node)은 무조건 `fragment_key`만 사용**
  - 경고만 (에러 아님, Ticket 3에서 추가 가능)

---

## 📊 검증 결과

### 현재 widgets.generated.json
- **위젯 개수**: 35개
- **Slug 규칙**: 통과 (허용 문자: a-z, 0-9, -, 가-힣)
- **Fragment 경로 필드**: 
  - 표준 키(`fragment_key`) 사용: 0개 (Ticket 3에서 추가 예정)
  - Fallback 필드 사용: 일부 (경고, Ticket 3에서 `fragment_key`로 표준화 예정)

---

## 🔧 수정된 파일

1. `scripts/validate_widgets_json.py` - Gate 보강 추가
   - slug 규칙 검증
   - fragment 경로 필드 검증

2. `docs/research/MATURIN_PYO3_NOTES.md` - 연구 노트 (격리)

---

## 🎯 다음 단계

### Ticket 3 준비 완료
- ✅ Gate 보강 완료 (slug 규칙 명확화, fragment_key 표준화)
- ✅ Rust/PyO3 문서 격리 완료
- ✅ 검증 통과

### Ticket 3 첫 커밋 체크리스트 (실수 방지)
1. **fragment_key 표준화 결정** (Node generator가 써야 함)
2. **HTML에서 섹션 찾는 기준 결정** (id? data-attribute?)
3. **fragment 저장 경로 고정**: 예) `packages/dashboard/public/fragments/{slug}.html`
4. **`/docs/[slug]` 라우트에서 sanitize + 파일 없으면 404**

### Ticket 3 작업
- HTML fragment 추출 (각 위젯의 innerHTML)
- 빌드 타임에 섹션별 HTML fragment 파일 생성
- `/docs/[slug]`에서 fragment 렌더
- React 위젯이 있으면 override(교체)

---

**상태**: Ticket 3 진입 전 Gate 보강 완료. Ticket 3 진행 가능.

