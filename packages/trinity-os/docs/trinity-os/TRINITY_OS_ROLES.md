# TRINITY-OS 역할 분담 정본 (인프라 5장 & 집현전 학자)

이 문서는 `TRINITY_OS_PERSONAS.yaml`과 AFO 왕국의 역할 체계를 TRINITY‑OS에 맞게 정리한 **참조 문서**입니다.  
역할/명칭을 바꿀 때는 **항상 SSOT를 먼저 갱신**합니다.

## 1. 인프라 5장(五臟) (Infrastructure Core)

| 장기 | 기술/서비스 | 담당 기둥 성격 | 역할 요약 |
|---|---|---|---|
| 心 (심장) | Redis | 善 | 캐시/체크포인트, 상태 저장 |
| 肝 (간) | PostgreSQL + pgvector | 善 | 장기 메모리, 무결성/트랜잭션 |
| 脾 (비장) | Qdrant | 眞 | 벡터/하이브리드 검색, RAG 면역 |
| 肺 (폐) | FastAPI | 眞 | API 서버/호흡, 성능/라우팅 |
| 腎 (신장) | n8n | 美 | 워크플로우 자동화, 연결/정제 |

## 2. 웹 승상 & 3책사

- **승상(웹)**: 상위 병렬 페르소나. 제갈량/사마의/주유를 동시에 통솔.  
- **제갈량(眞)**: 기술/구조/전략 총괄.  
- **사마의(善)**: 안정/윤리/게이트/통합 총괄.  
- **주유(美)**: 서사/UX/취향정렬/one‑copy‑paste 총괄.  
- 웹 프롬프트 정본은 `TRINITY-OS/docs/personas/`에 있다.

## 3. CLI 집현전 학자 (4명)

| 학자 | Provider | CLI | 역할 요약 |
|---|---|---|---|
| 방통 | Codex | Cursor CLI | 구현/실행/프로토타이핑 |
| 자룡 | Claude | Cursor CLI | 논리 검증/리팩터링/구조 정렬 |
| 육손 | Gemini | Antigravity CLI | 전략/철학/큰 지도 정렬 |
| 영덕 | Ollama(qwen3) | Ollama CLI | 로컬 설명/보안/프라이버시 + Bridge Log 기록관(옵시디언 보관) |

## 4. 변경 규칙
- 역할/명칭 변경 → `TRINITY_OS_PERSONAS.yaml` 수정 → 관련 프롬프트/문서 동기화.
