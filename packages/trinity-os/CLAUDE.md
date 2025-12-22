# CLAUDE.md — Trinity OS & MCP (Claude Override)

> MCP/Context7 전용 Claude 지침 (루트 `CLAUDE.md` 상속).  
> 충돌 시 **루트 규칙이 우선**한다.

이 문서는 `packages/trinity-os/` 폴더에서 작업하는 Claude 에이전트를 위한 세부 지침입니다.

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
- 루트: `./CLAUDE.md`, `./AGENTS.md`, `./docs/AFO_ROYAL_LIBRARY.md`, `./docs/AFO_CHANCELLOR_GRAPH_SPEC.md`

---

## 2) 핵심 자원 (Core Resources)

- **MCP 서버**: 9개 (통합 서버: `afo_ultimate_mcp_server.py`)
- **Skills**: 19개 (레지스트리: `afo_skills_registry.py`)
- **Context7**: 12항목 (통합 지식 베이스)
- **Sequential Thinking**: MCP 도구로 사용 가능
- **Memory System**: Redis 기반 영구 저장

---

## 3) Setup Commands (이 폴더 전용)

### 패키지 타입 판별
- `./packages/trinity-os/package.json`이 있으면 Node 스크립트 우선
- `./packages/trinity-os/pyproject.toml`이 있으면 Python 툴체인 우선
- 둘 다 있으면 CI(.github/workflows)에서 사용하는 기준을 우선

### 실행
- Node인 경우: `npm run <script>` 또는 `pnpm <script>`
- Python인 경우: `poetry run <command>` 또는 `python -m <module>`

---

## 4) Quality Gates (이 폴더의 완료 기준)

### Node인 경우
- `scripts`에 있는 `lint/typecheck/test/build` 중 존재하는 것만 실행

### Python인 경우
- Makefile/scripts/pyproject 기반으로 lint/type/tests 중 존재하는 것만 실행

---

## 5) Truth Rules (RAG/LLM에서 眞는 "근거")

- 출력/결정은 항상 SSOT/코드/테스트 로그로 뒷받침해야 한다.
- "추측 기반 답변 생성" 금지.
- RAG 변경 시:
  - 검색 품질(precision/recall)을 최소 1개 테스트/샘플로 검증 가능해야 한다.
  - 인덱싱/청킹/스코어링 변경은 "왜"를 근거로 설명해야 한다.

---

## 6) Goodness Rules (비용/보안/데이터 안전)

- 민감정보 보호:
  - 프롬프트/컨텍스트/로그에 키/토큰/개인정보가 섞이지 않도록 redaction 규칙 유지
- 비용:
  - 비싼 호출(원격 LLM/대량 임베딩/대량 재인덱싱)은 기본적으로 DRY_RUN + ASK
  - "측정 없는 n배 향상" 주장 금지
- 안전:
  - 라우팅/프로바이더 폴백은 "예측 가능"해야 한다(조용히 실패 금지)

---

## 7) DRY_RUN Policy (이 폴더에서 DRY_RUN이 필수인 작업)

아래 작업은 반드시 DRY_RUN 선행 + 결과 요약(샘플/로그) 제출:

- 대량 인덱싱/리인덱싱/임베딩 재생성
- 라우팅 정책 변경(프로바이더 우선순위/폴백/캐시 전략)
- 메모리 정책 변경(저장/삭제/요약/리텐션)
- 비용이 큰 배치 작업

---

## 8) Beauty Rules (구조의 미학)

- 파이프라인은 단계별로 분리한다:
  - ingest → chunk → embed → index → retrieve → generate → evaluate
- 각 단계는 입력/출력을 명확히 하고, 로깅은 최소/구조화로 유지한다.
- "복잡해 보이는 최적화"보다 "명확한 디버깅 가능성"을 우선한다.

---

## 9) Eternity Rules (기록/재현)

- 변경 시 반드시 남길 것:
  - 어떤 정책이 바뀌었는지
  - 왜 바뀌었는지(근거)
  - 어떻게 검증했는지(커맨드/샘플)
  - 롤백 방법

---

## 10) 금지구역 (추가)

루트 `CLAUDE.md`의 금지구역에 추가:

- Trinity Score 가중치 변경 금지 (명시 지시 없이)
- MCP 도구 중복 금지 (기존 도구와 기능 겹치면 ASK)
- Context7 통합 지식 베이스 핵심 변경 금지

---

## 11) Claude-Specific Tips (이 폴더 작업 시)

- **Tree-of-Thoughts**: 복잡한 RAG 파이프라인 변경 시 여러 접근 방식을 병렬로 고려
- **단계별 검증**: ingest → chunk → embed → index 각 단계를 개별적으로 검증
- **비용 최적화 우선**: 로컬(Ollama) 우선, 원격 API는 폴백으로

---

## 12) Output Contract (보고 포맷)

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

**작성일**: 2025-12-21  
**Claude 팁**: 복잡 작업 시 Tree-of-Thoughts 활용. RAG 파이프라인은 단계별로 검증하세요.

---

# End of ./packages/trinity-os/CLAUDE.md

