# AGENTS.md (TRINITY-OS) — AFO Kingdom Trinity OS Operating Rules

목적: Trinity OS 도메인에서 AI 모델과 지능 확장을 위한 특화된 운영 규칙입니다.
원칙: **RAG 최적화 / 메모리 효율성 / LLM 안전성 우선**.

---

## 0) 10초 프로토콜 (Trinity OS 특화)
- decision: Trinity Score ≥ 90 AND Risk ≤ 10이면 AUTO_RUN
- evidence: RAG 성능 메트릭 + 메모리 사용량 + LLM 응답 품질
- plan: 스트리밍 최적화 → 메모리 관리 → 안전성 검증
- checks_to_run: rag_test | memory_test | llm_safety | streaming_perf
- rollback_plan: 모델 롤백 + 캐시 클리어 + 메모리 재할당

---

## 1) SSOT 읽는 순서 (Trinity OS 우선)
Trinity OS 도메인에서는 다음 SSOT를 우선적으로 참고:

1) docs/TRINITY_PHILOSOPHY_MASTER.md (트리니티 철학)
2) docs/KINGDOM_UNIFIED_AUTORUN_GUIDE.md (통합 가이드)
3) packages/trinity-os/docs/ (도메인별 문서)
4) Root AGENTS.md (글로벌 헌법)

---

## 2) Evidence 규칙 (RAG/LLM 특화)
모든 주장의 근거는 다음 중 하나 이상:
- RAG 검색 결과 정확도 메트릭
- 메모리 사용량 및 누수 테스트 결과
- LLM 응답 품질 및 안전성 평가
- 스트리밍 성능 벤치마크

---

## 3) Trinity Score (Trinity OS 가중치 조정)
가중치(Trinity OS 특화):
- Truth(眞) 0.40 (RAG 정확성, 검색 품질)
- Goodness(善) 0.30 (메모리 효율성, 시스템 안정성)
- Beauty(美) 0.20 (사용자 경험, 응답 품질)
- Serenity(孝) 0.05 (연속성, 오류 복구)
- Eternity(永) 0.05 (지식 영속성, 모델 버전 관리)

행동 게이트 (Trinity OS 특화):
- RAG 성능 저하 시 즉시 BLOCK
- 메모리 누출 감지 시 자동 ALERT
- LLM 안전성 위반 시 즉시 SHUTDOWN

---

## 4) Risk Score (Trinity OS 위험 평가)
- RAG 검색 실패: +50 (정보 정확성 저하)
- 메모리 누출: +40 (시스템 안정성 위협)
- LLM 할루시네이션: +60 (사용자 안전 위협)
- 스트리밍 지연: +20 (사용자 경험 저하)
- 모델 버전 불일치: +30 (예측 불가능성)

---

## 5) 작업 표준 플로우 (Trinity OS 특화)
1) **RAG 검증**: 검색 정확도 및 관련성 테스트
2) **메모리 프로파일링**: 사용량 및 누수 검사
3) **LLM 안전성 테스트**: 프롬프트 인젝션 및 출력 필터링
4) **스트리밍 최적화**: 응답 시간 및 사용자 경험 평가
5) **지식 영속성 확인**: 벡터 DB 일관성 및 백업 검증

---

## 6) Package Manager (Trinity OS 특화)
Trinity OS는 Python 중심이므로 poetry 우선:
- poetry.lock 우선 (프로젝트 락파일)
- pip-tools/poetry 환경 유지
- 의존성 업데이트 시 RAG 성능 회귀 테스트 필수

---

## 7) 금지 구역 (Trinity OS 특화)
- 프로덕션 LLM API 키 노출
- 민감한 학습 데이터 유출
- RAG 검색 결과 조작
- 메모리 덤프나 모델 가중치 유출
- 스트리밍 응답 중간 가로채기

---

## 8) 기록(永) (Trinity OS 특화)
완료 시 다음 메트릭을 artifacts/에 기록:
- RAG 정확도 점수 (0-100)
- 메모리 사용량 추이 그래프
- LLM 응답 품질 메트릭
- 스트리밍 성능 벤치마크
- 모델 버전 및 설정 SSOT

---

## 9) Definition of Done (Trinity OS 특화)
- 眞: RAG 정확도 ≥ 95%
- 善: 메모리 누수 0% + 시스템 안정성 99.9%
- 美: 응답 품질 점수 ≥ 90%
- 孝: 스트리밍 연속성 100%
- 永: 모든 메트릭 artifacts/에 기록 및 백업

---

## 10) 도메인별 규칙 (Trinity OS 확장)
Trinity OS는 다음 하위 모듈로 확장:
- RAG 파이프라인 (검색/색인/랭킹)
- 메모리 관리 (컨텍스트7/벡터 DB)
- LLM 오케스트레이션 (멀티모달/스트리밍)
- 안전성 레이어 (프롬프트 필터링/출력 검열)

---
# End
