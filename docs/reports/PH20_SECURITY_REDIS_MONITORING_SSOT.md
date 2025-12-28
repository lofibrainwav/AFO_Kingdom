# PH20 — Security + Redis Monitoring SSOT
As-of: 2025-12-27 (America/Los_Angeles)

## 0) 목표
- 眞: 런타임 사실 검증(Trinity Gate)
- 善: 취약점 차단 + 기록(Trivy 2-step + SARIF)
- 孝: 자동화로 마찰 제거(Dependabot)
- 美: Redis 운영 가시화(RedisInsight + Streams)
- 永: CI 최적화/기록/재현성

---

## 1) Trinity Gate (眞)
- /health vs /metrics 일관성 자동 검증
- warmup으로 메트릭 등록 트리거

검증:
- CI 로그에서 /health, /metrics 비교 구간 확인

---

## 2) Trivy 2-step (善)
구성:
- Gate: HIGH/CRITICAL 발견 시 실패(exit-code=1)
- SARIF: 결과 업로드로 Code Scanning에 영구 기록

검증:
- CI 로그에서 Trivy step 결과, upload-sarif step 성공 확인

권장:
- 액션 버전 pinning(태그/sha) 적용

---

## 3) Dependabot 자동화 (孝)
- patch/minor 자동 처리
- 충돌 PR은 수동 해결 후 다시 자동 루프 복귀

검증:
- 열려있는 dependabot PR 목록/체크 확인

---

## 4) RedisInsight (美)
### 4.1 Docker로 올리는 표준(운영 마찰 최소)
- 포트: 5540
- 데이터: /data 볼륨 영속

예시:
docker run -d --name redisinsight -p 5540:5540 -v redisinsight:/data redis/redisinsight:latest

접속:
- http://localhost:5540

### 4.2 운영 체크리스트
- key browser/CLI(workbench)로 데이터 확인
- slowlog/profiler/memory 관점에서 병목 탐지

---

## 5) Redis Streams (美 + 永)
### 5.1 기본 템플릿
- XADD: 이벤트 추가
- XGROUP + XREADGROUP: consumer group 처리
- XACK: 처리 완료 ack
- XTRIM: 무한 성장 방지

### 5.2 장애 복구/재처리(고급)
- XAUTOCLAIM: 죽은 consumer의 pending을 자동 회수
- XACKDEL / XDELEX: ack+정리(정확한 정리 정책에 맞춰 선택)

운영 원칙:
- 재처리 자동화(XAUTOCLAIM) + 트리밍(XTRIM) + 정리(XACKDEL/XDELEX)로 "영속 운영" 달성

---

## 6) 최종 Runbook (A→B→C→D)
A) CI 결과 확정
B) Dependabot PR #6 충돌 해결
C) Medium 취약점 우선순위 정리
D) main 승격 PR 생성 및 머지
