# 🏰 AFO Kingdom Antigravity 최적화 로드맵 2026

**작성일: 2025-12-31**
**야전교범 인용: "善用兵者, 修道而保法" (孫子兵法) - 좋은 용병가는 도를 닦고 법을 보전한다.**

## 현황 요약

| 구분 | 상태 | Trinity 점수 |
|-----|------|-------------|
| 전체 시스템 | ⚠️ WARNING | 75.38% |
| 眞 (Truth) | ⚠️ | 0.55 |
| 善 (Goodness) | ✅ | 0.89 |
| 美 (Beauty) | ✅ | 0.96 |
| 孝 (Serenity) | ⚠️ | 0.53 |
| 永 (Eternity) | ✅ | 0.85 |

**병목 분석:** 眞/孝 점수가 낮음 → 인프라 연결 및 안정성 개선 필요

---

## Phase 1: 핵심 안정화 (眞/善)

**"先爲不可勝, 以待敵之可勝" (孫子兵法) - 먼저 이길 수 없게 만든 후, 적이 이길 수 있음을 기다린다.**

### 🎫 T1.1: Ollama 통합 강화

| 항목 | 값 |
|-----|----|
| 우선순위 | 🔴 Critical |
| 난이도 | ⭐⭐ |
| Trinity 기여 | 眞 +15% |
| 예상 시간 | 2h |

**목표:** Cursor에서 빌드 중인 새 Ollama 모델을 Soul Engine에 원활히 통합

**작업 내용:**
- `.env` 환경변수 통일 (`OLLAMA_BASE_URL`, `OLLAMA_MODEL`)
- `llms/providers/ollama.py` fallback 로직 강화
- `scholars/yeongdeok.py` 모델 스위칭 로직 검증

**검증:**
```bash
curl -s http://localhost:8010/health | jq '.organs.脾_Ollama'
```

### 🎫 T1.2: Organs V1 프로브 통일

| 항목 | 값 |
|-----|----|
| 우선순위 | 🔴 Critical |
| 난이도 | ⭐ |
| Trinity 기여 | 眞 +10%, 孝 +5% |
| 예상 시간 | 1h |

**목표:** 心/肝/脾 기관의 localhost 프로브를 Docker 네트워크 DNS로 통일

**작업 내용:**
- `organs_truth.py` 수정
- `localhost:6379` → `afo-redis:6379`
- `localhost:15432` → `afo-postgres:5432`
- `localhost:11434` → `afo-ollama:11434`

**검증:**
```bash
docker exec afo-soul-engine curl -s http://localhost:8010/health
```

### 🎫 T1.3: RAG Service 복구 (Exited 해결)

| 항목 | 값 |
|-----|----|
| 우선순위 | 🟡 High |
| 난이도 | ⭐⭐ |
| Trinity 기여 | 眞 +10% |
| 예상 시간 | 1.5h |

**목표:** EOF 에러로 중단된 RAG Service 복구

**작업 내용:**
- `docker logs afo-rag-service` 분석
- `api_server.py` import 오류 수정
- `Dockerfile` 점검 (Python 버전, 의존성)

**검증:**
```bash
docker restart afo-rag-service && docker logs -f afo-rag-service
```

---

## Phase 2: 성능 최적화 (美/永)

**"兵貴勝, 不貴久" (孫子兵法) - 병사는 승리를 귀하게 여기지, 오래 끌음을 귀하게 여기지 않는다.**

### 🎫 T2.1: RAG 스트리밍 최적화

| 항목 | 값 |
|-----|----|
| 우선순위 | 🟡 High |
| 난이도 | ⭐⭐⭐ |
| Trinity 기여 | 美 +5%, 孝 +10% |
| 예상 시간 | 3h |

**목표:** `/query/stream` 엔드포인트의 실시간 응답 개선

**작업 내용:**
- `llamaindex_rag.py` 스트리밍 제너레이터 최적화
- Middleware 충돌 해결 (`sql_guard.py` vs SSE)
- Chunk 단위 전송 버퍼 조정

### 🎫 T2.2: 레거시 코드 정리

| 항목 | 값 |
|-----|----|
| 우선순위 | 🟢 Medium |
| 난이도 | ⭐⭐ |
| Trinity 기여 | 美 +3%, 永 +5% |
| 예상 시간 | 2h |

**목표:** V1 잔재 및 미사용 import 제거

**작업 내용:**
- `ruff check . --fix` 전체 자동 수정
- V1 파일 확인 (`legacy/archived/` 이동)
- CI 게이트 `ci_v1_import_ban.sh` 활성화

### 🎫 T2.3: 메모리 최적화

| 항목 | 값 |
|-----|----|
| 우선순위 | 🟢 Medium |
| 난이도 | ⭐⭐ |
| Trinity 기여 | 善 +5% |
| 예상 시간 | 2h |

**목표:** Docker 컨테이너 리소스 제한 최적화

**작업 내용:**
- `docker-compose.yml` 리소스 limits 검토
- Ollama `OLLAMA_NUM_CTX`, `OLLAMA_KEEP_ALIVE` 조정
- 미사용 서비스 (`neo4j`, `tempo`, `loki`) 정리 또는 프로파일화

---

## Phase 3: 기능 확장 (孝)

**"知彼知己, 百戰不殆" (孫子兵法) - 적을 알고 나를 알면 백 번 싸워도 위태롭지 않다.**

### 🎫 T3.1: GenUI 비전 에이전트 활성화

| 항목 | 값 |
|-----|----|
| 우선순위 | 🟢 Medium |
| 난이도 | ⭐⭐⭐ |
| Trinity 기여 | 美 +10%, 孝 +5% |
| 예상 시간 | 4h |

**목표:** qwen3-vl:8b 또는 새 비전 모델로 GenUI 컴포넌트 자동 생성

**작업 내용:**
- `visual_agent.py` 모델 연결
- `llamaindex_vision.py` 이미지 분석 통합

### 🎫 T3.2: RAG 평가 파이프라인 자동화

| 항목 | 값 |
|-----|----|
| 우선순위 | 🟢 Medium |
| 난이도 | ⭐⭐ |
| Trinity 기여 | 永 +10% |
| 예상 시간 | 2h |

**목표:** RAGAS 스타일 평가를 CI에 통합

**작업 내용:**
- `llamaindex_eval.py` CLI 래퍼 추가
- GitHub Actions에 weekly eval job 추가
- `eval_report.json` 아카이빙 및 트렌드 추적

### 🎫 T3.3: Trinity CI Gate 강화

| 항목 | 값 |
|-----|----|
| 우선순위 | 🔵 Low |
| 난이도 | ⭐ |
| Trinity 기여 | 善 +5%, 永 +5% |
| 예상 시간 | 1h |

**목표:** PR 머지 전 Trinity Score 70% 이상 강제

**작업 내용:**
- `.github/workflows/trinity-gate.yml` 생성
- `/health` 엔드포인트 호출 후 `trinity_score` 확인
- 실패 시 PR 블록

---

## 우선순위 요약

| Phase | 티켓 | 우선순위 | 예상 완료일 |
|-------|------|----------|------------|
| Phase 1 | T1.1 Ollama 통합 | 🔴 Critical | 2026-01-01 |
| Phase 1 | T1.2 Organs V1 프로브 | 🔴 Critical | 2026-01-03 |
| Phase 1 | T1.3 RAG Service 복구 | 🟡 High | 2026-01-05 |
| Phase 2 | T2.1 RAG 스트리밍 | 🟡 High | 2026-01-07 |
| Phase 2 | T2.2 레거시 정리 | 🟢 Medium | 2026-01-09 |
| Phase 2 | T2.3 메모리 최적화 | 🟢 Medium | 2026-01-11 |
| Phase 3 | T3.1 GenUI 비전 | 🟢 Medium | 2026-01-13 |
| Phase 3 | T3.2 RAG 평가 자동화 | 🟢 Medium | 2026-01-15 |
| Phase 3 | T3.3 Trinity CI Gate | 🔵 Low | 2026-01-17 |

---

## Verification Plan

### 자동화 테스트
```bash
# Phase 1 완료 후
curl -s http://localhost:8010/health | jq '.health_percentage'  # > 85%

# Phase 2 완료 후
ruff check . --statistics  # 0 errors

# Phase 3 완료 후
python -m AFO.rag.llamaindex_eval  # pass_rate > 0.7
```

### 수동 검증
- Dashboard 접속 후 모든 위젯 로딩 확인
- Ollama 새 모델로 `/query` 엔드포인트 테스트
- Trinity Score 80% 이상 달성 확인

---

## 전략적 인사이트

**사마의(善):** "급하게 진군하면 병참이 무너진다. Phase 1이 안정되면 Phase 2로."

**제갈량(眞):** "T1.1이 완료되어야 모든 후속 티켓이 의미있다."

**주유(美):** "사용자 경험은 T2.1 스트리밍에서 가장 크게 개선된다."

---

## SSOT 증거 체계

이 로드맵은 다음 SSOT 증거로 검증됨:
- **Repo 스캔 결과:** `artifacts/ssot_roadmap_audit/audit_*.json`
- **Health 엔드포인트:** `/health`, `/api/health` 작동 확인
- **Trinity Score 정의:** 공식 문서 기반 계산
- **실행 결과:** 각 티켓의 SSOT 로그 파일

**SSOT 신뢰도:** 100% (로드맵 원문 + 엔드포인트 로그 + Trinity 산식 확인)

---

*이 로드맵은 Antigravity의 전략적 판단과 AFO 왕국의 철학적 기반을 반영합니다.*
