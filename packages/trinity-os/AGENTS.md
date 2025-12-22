# 📚 AFO Trinity OS — agents.md (trinity-os)

이 문서는 루트 `AGENTS.md`의 하위 규칙이다. 충돌 시 **루트 규칙이 우선**한다.

---

## 0) Scope (이 폴더의 책임)

- RAG 파이프라인, Context7 관리, 메모리/페르소나 정책, LLM 라우팅, 인덱싱/검색/평가
- "할루시네이션 방지"와 "비용/안전"이 최우선

---

## 1) SSOT (이 폴더에서 최우선으로 보는 근거)

에이전트는 작업 전 아래 파일의 **존재 여부를 확인하고** 존재하는 것만 읽는다.

- `./packages/trinity-os/README.md`
- `./packages/trinity-os/pyproject.toml` 또는 `package.json`(존재하는 쪽)
- Context 관련 문서/정책 파일(존재 시)
- 루트: `./AGENTS.md`, `./docs/AFO_ROYAL_LIBRARY.md`, `./docs/AFO_CHANCELLOR_GRAPH_SPEC.md`

---

## 2) Truth Rules (RAG/LLM에서 眞는 "근거")

- 출력/결정은 항상 SSOT/코드/테스트 로그로 뒷받침해야 한다.
- "추측 기반 답변 생성" 금지.
- RAG 변경 시:
  - 검색 품질(precision/recall)을 최소 1개 테스트/샘플로 검증 가능해야 한다.
  - 인덱싱/청킹/스코어링 변경은 "왜"를 근거로 설명해야 한다.

---

## 3) Goodness Rules (비용/보안/데이터 안전)

- 민감정보 보호:
  - 프롬프트/컨텍스트/로그에 키/토큰/개인정보가 섞이지 않도록 redaction 규칙 유지
- 비용:
  - 비싼 호출(원격 LLM/대량 임베딩/대량 재인덱싱)은 기본적으로 DRY_RUN + ASK
  - "측정 없는 n배 향상" 주장 금지
- 안전:
  - 라우팅/프로바이더 폴백은 "예측 가능"해야 한다(조용히 실패 금지)

---

## 4) DRY_RUN Policy (이 폴더에서 DRY_RUN이 필수인 작업)

아래 작업은 반드시 DRY_RUN 선행 + 결과 요약(샘플/로그) 제출:

- 대량 인덱싱/리인덱싱/임베딩 재생성
- 라우팅 정책 변경(프로바이더 우선순위/폴백/캐시 전략)
- 메모리 정책 변경(저장/삭제/요약/리텐션)
- 비용이 큰 배치 작업

---

## 5) Command Resolution (커맨드 추측 금지)

이 패키지는 Python 또는 Node일 수 있다. **존재하는 파일로만** 결정한다.

### A) 패키지 타입 판별(Discovery)

- `./packages/trinity-os/package.json`이 있으면 Node 스크립트 우선
- `./packages/trinity-os/pyproject.toml`이 있으면 Python 툴체인 우선
- 둘 다 있으면 CI(.github/workflows)에서 사용하는 기준을 우선

### B) Quality Gates 실행(존재하는 것만)

- Node인 경우: `scripts`에 있는 `lint/typecheck/test/build` 중 존재하는 것만 실행
- Python인 경우: Makefile/scripts/pyproject 기반으로 lint/type/tests 중 존재하는 것만 실행

---

## 6) Beauty Rules (구조의 미학)

- 파이프라인은 단계별로 분리한다:
  - ingest → chunk → embed → index → retrieve → generate → evaluate
- 각 단계는 입력/출력을 명확히 하고, 로깅은 최소/구조화로 유지한다.
- "복잡해 보이는 최적화"보다 "명확한 디버깅 가능성"을 우선한다.

---

## 7) Eternity Rules (기록/재현)

- 변경 시 반드시 남길 것:
  - 어떤 정책이 바뀌었는지
  - 왜 바뀌었는지(근거)
  - 어떻게 검증했는지(커맨드/샘플)
  - 롤백 방법

---

## 8) Output Contract (보고 포맷)

작업 결과는 반드시 아래 JSON 요약을 포함한다.

```json
{
  "decision": "AUTO_RUN | ASK_COMMANDER | BLOCK",
  "risk_score": 0,
  "trinity_score": 0,
  "evidence": ["..."],
  "files_changed": ["..."],
  "checks_ran": ["..."],
  "rollback_plan": ["..."],
  "dry_run_summary": ["..."]
}
```

---

# End of ./packages/trinity-os/agents.md

