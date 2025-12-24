# INSPIRATION_NOTES (SSOT) — Tidying + Strangler Fig + Builder Josh + 배휘동 리드

**As-of**: 2025-12-24
**Status**: 초안(FACTS/NOTES 분리 완료)
**SSOT 원칙**: "팩트는 근거로 고정", "영감/해석은 NOTES로 격리", 과장/단정 금지

---

## 0) 범위
- 이 문서는 **전략/철학을 "실행 가능한 운영 규칙"으로 바꾸기 위한 노트**다.
- **FACTS** = 정의/원칙/실측 로그/커밋처럼 **근거로 고정 가능한 것만**.
- **NOTES** = 강연/대화에서 얻은 영감, 해석, 비유, 추천(검증 전).

---

## 1) FACTS (근거로 고정 가능한 것)

### 1.1 개념 FACTS (정의/원칙)
- **Tidying(타이딩)**: 기능 변경이 아닌 "작고 안전한 정리"를 먼저 해서 다음 변경의 비용/리스크를 낮추는 접근.
- **Strangler Fig(교살자 무화과) 패턴**: 레거시를 한 번에 갈아엎지 않고, 경계(라우터/프록시/파사드)를 두고 **일부 기능부터 새 구현으로 점진 라우팅**해 결국 레거시를 제거하는 패턴.
- **Facade(파사드)**: 레거시 내부 복잡도를 바깥으로 새지 않게 **단일 인터페이스로 감싸는 경계 레이어**.
- **SSE(Server-Sent Events)**: 서버 → 클라이언트로 이벤트 스트림을 단방향 전송하는 방식(실시간 로그/상태 투영에 사용 가능).

**외부 근거 링크(실제 URL만, 참고용)**
- Tidying / Tidy First: https://tidyfirst.com/
- Strangler Fig (Martin Fowler): https://martinfowler.com/bliki/StranglerFigApplication.html
- Strangler Fig (Microsoft): https://learn.microsoft.com/azure/architecture/patterns/strangler-fig
- SSE (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events

### 1.2 AFO 현재 상태 FACTS (형님이 제공한 실측 로그 기반)
- Next.js dashboard가 **localhost:3000**에서 실행 중.
- fragments HTML이 생성되었고, `/fragments/<name>.html`이 **200 OK**로 서빙됨.
- `/api/revalidate`가 로컬에서 **200 OK**로 동작했고, revalidated 경로 배열을 반환함.
- 프로덕션에서는 `x-revalidate-secret` 같은 헤더 인증이 필요(로컬에서 생략 가능).

> NOTE: 아래 "Cline 로그"에 나온 `compat.py 존재/내용`, `AFO_EVOLUTION_LOG.md 내용`, "mypy 4→0" 같은 수치는
> **현재 이 문서에서는 '형님이 붙여준 도구 출력'일 뿐, SSOT 팩트로 승격 전**이라서 NOTES로 둔다.

---

## 2) NOTES (영감/해석/제안 — 검증 전)

### 2.1 Builder Josh / 커서마피아에서 얻은 운영 아이디어 (NOTES)
- **서브 에이전트 vs 스킬 분리**:
  - "판단 필요한 복잡 작업"은 역할/책임이 있는 서브 에이전트에 위임
  - "반복/정형 작업"은 스킬(스크립트/툴)로 분리해 컨텍스트 오염 최소화
- **컨텍스트 정화**: 반복 작업은 TS/쉘 스크립트로 내려서 "결과만 LLM에 남기는" 파이프라인화
- **Self-expanding**: 에이전트가 스스로 보조 에이전트를 만들 수 있는 구조(확장 방향 제안)

### 2.2 배휘동 리드 분석(AX 관점) (NOTES, 인물 정보 단정 금지)
- AX의 핵심 = 도구 제공이 아니라 **행동 변화**를 만드는 것(개인/팀/조직)
- "Tidying"을 **대규모 변경의 기반이 되는 안전한 축적**으로 본다
- "Pair Prompting(짝 프롬프팅)"을 통해 서로의 논리를 비교/압축 학습한다

> 인물 경력/소속/연혁 등은 **공개 링크(프로필/강연 페이지/회사 소개)**가 붙기 전까지는 전부 NOTES로 유지한다.

### 2.3 Cline 출력에서 주장된 AFO 내부 상태 (NOTES → 검증 후 FACTS 승격 가능)
- `packages/afo-core/AFO/api/compat.py`가 "Facade/compat layer"로 이미 구현되어 있다는 주장
- `AFO_EVOLUTION_LOG.md`에 "Phase 0~26 자율 확장 로그"가 있다는 주장
- "legacy 검색어로는 못 찾았다"는 주장
- "mypy/ruff/test 통과 수치" 주장

---

## 3) PROPOSAL (AFO 적용 제안 — 실행 단위로 쪼갬)

### 3.1 Tidying 루틴 (제안)
- 규칙: "동작 변경 없음"만 허용 + PR/커밋 단위는 작게
- 타이딩 대상 예시:
  - import/정렬/이름/파일 분리(동작 불변)
  - 타입 힌트/스키마 보강(동작 불변)
  - dead code 제거(테스트/검증이 가능한 경우만)

### 3.2 Strangler Fig 이관 루프 (제안)
1) 경계(compat/router/proxy) 마련
2) 새 구현(동일 계약) 준비
3) 일부 트래픽/기능만 라우팅
4) 관측(에러율/지연/성공률) 확인
5) 범위 확장
6) 레거시 사용량 0 확인 후 제거

### 3.3 관측(선택) — SSE로 "정화/이관 상태" 투영 (제안)
- tidying 진행률, revalidate 호출 결과, 라우팅 토글 상태 등을 대시보드에서 스트리밍 표시

---

## 4) NOTES → FACTS 승격 체크리스트 (복붙용)

### 4.1 "파일 존재/내용" 검증 (AFO 레포 루트에서)
```bash
ls -la packages/afo-core/AFO/api/compat.py AFO_EVOLUTION_LOG.md 2>/dev/null || true
sed -n '1,160p' packages/afo-core/AFO/api/compat.py 2>/dev/null || true
sed -n '1,200p' AFO_EVOLUTION_LOG.md 2>/dev/null || true
```

### 4.2 "레거시 흔적" 빠른 검색(있으면 후보 추출)

```bash
rg -n --hidden --no-ignore -S "legacy|deprecated|deprecate|old code|unused|TODO\(remove\)|remove later" .
```

### 4.3 "정화/이관 작업 로그"를 SSOT로 남기는 최소 템플릿

* 커밋 해시 / 변경 파일 / 검증 결과(빌드/테스트/런타임)만 기록
* "좋다/완벽" 같은 감정 단정은 NOTES로만

---

## 5) 결론

* 이 문서는 **전략을 운영 규칙으로 변환하기 위한 SSOT 노트**다.
* 지금은 "강한 주장"을 NOTES로 격리해둔 상태이며,
* 위 체크리스트로 근거가 붙는 항목만 FACTS로 승격한다.