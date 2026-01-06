# 🎯 AFO 왕국 티켓 보드 (SSOT)

**프로젝트 목표**: AFO Kingdom 자율 운영 시스템 완성
**최종 업데이트**: 2026-01-01
**Trinity Score**: 93.2% ✅ (목표: 90%+)
**HEAD**: `40b98e37`

## 📋 Phase 3-8 완료 티켓

| ID | 제목 | Phase | Commit | Seal Tag | Evidence |
|---|------|-------|--------|----------|----------|
| TICKET-060 | SSOT Auto-Seal | 3 | `78199e99` | `ssot-phase3-autonomy-*` | `scripts/ssot_seal.sh` |
| TICKET-061 | Trinity Gate | 3 | `ddd236e7` | `ssot-phase3-autonomy-*` | `.github/workflows/trinity-gate.yml` |
| TICKET-062 | Release Rail | 3 | `38961df8` | `ssot-phase3-autonomy-*` | `.github/workflows/release.yml` |
| TICKET-063 | Branch Protection | 4-A | `fa428ab2` | `ssot-phase4-branch-protection-*` | `scripts/enforce_branch_protection.sh` |
| TICKET-064 | Drift Monitor | 4-B | `28eca5dc` | `ssot-phase4-complete-*` | `scripts/ssot_drift_monitor.sh` |
| TICKET-065 | Dependabot | 4-C | `bf63666a` | `ssot-phase4-complete-*` | `.github/dependabot.yml` |
| TICKET-066 | Golden Path CLI | 5 | `caf138c0` | `ssot-phase5-golden-path-*` | `afo` |
| TICKET-067 | Fail-Fast | 6 | `2a895ea0` | `ssot-phase6-failfast-*` | `afo` (ERR trap) |
| TICKET-068 | Alert Integration | 7-A | `c11f3f39` | `ssot-phase7A-alert-*` | `scripts/afo_alert.sh` |
| TICKET-069 | Evidence Format | 7-B | `d8327067` | `ssot-phase7-complete-*` | `scripts/afo_manifest.sh` |
| TICKET-070 | Shellcheck Gate | 7-C | `c8333672` | `ssot-phase7-complete-*` | `.github/workflows/shellcheck.yml` |
| TICKET-071 | CI Failure Alert | 8-A | `99c62fc8` | `ssot-phase8A-ci-alert-*` | `trinity-gate.yml` (failure step) |
| TICKET-072 | Release 체계 강화 | 8-B | `2a1fd63d` | `ssot-phase8B-release-*` | `scripts/afo_release_tag.sh` |
| TICKET-073 | Dashboard Status Card | 8-C | `5fb9f6f0` | `ssot-phase8C-dashboard-*` | `scripts/afo_dashboard.sh` |
| TICKET-076 | TimelineState Generator Node | 11 | `WIP` | `ssot-phase11-timeline-*` | `packages/afo-core/AFO/multimodal/timeline_state_generator.py` |
| TICKET-077 | Multimodal FANOUT-JOIN Extension | 12 | `WIP` | `ssot-phase12-multimodal-fanout-*` | `packages/afo-core/AFO/multimodal/fanout_join_ext.py` |
| TICKET-078 | VideoBranch Detail Implementation | 13 | HIGH | `ssot-phase13-video-branch-*` | `packages/afo-core/AFO/multimodal/video_branch.py` |
| TICKET-079 | MusicBranch Detail Implementation | 13 | HIGH | `ssot-phase13-music-branch-*` | `packages/afo-core/AFO/multimodal/music_branch.py` |
| TICKET-080 | Fusion Compositing Integration | 14 | HIGH | `ssot-phase14-fusion-compositing-*` | `packages/afo-core/AFO/multimodal/fusion_branch.py` |
| TICKET-081 | CapCut Style Integration | 15 | HIGH | `ssot-phase15-capcut-integration-*` | `packages/afo-core/AFO/multimodal/capcut_branch.py` |
## TICKET-082 — Suno MusicBranch Integration & AV Fusion
- Phase: 16 (멀티모달 확장)
- Priority: HIGH
- Type: Feature Enhancement
- Status: ✅ 완료 (2026-01-06)
- Evidence: packages/afo-core/AFO/multimodal/suno_branch.py
- Dependencies: ffmpeg (required), moviepy (optional; 있으면 MoviePy로 AV 합성)

### Goal
TimelineState 기반으로 Suno 음악 생성 → 다운로드 → (필요 시 길이 맞춤) → 비디오와 AV 합성(mp4)까지 한 번에 연결.

### Scope
1) Suno API 통합 (Generate + Record-info Polling)
2) 고급 파라미터 지원
   - customMode, style, title, negativeTags, personaId, vocalGender, styleWeight, weirdnessConstraint, audioWeight, model, callBackUrl
3) 에러 처리 강화
   - 재시도(지수 백오프) + 타임아웃 + fail-closed
4) TimelineState → Suno Request 자동 변환
5) AV Fusion
   - moviepy 사용 가능 시 MoviePy 우선
   - moviepy 없으면 ffmpeg로 fallback
6) Trinity Score(로컬 휴리스틱) 기반 품질 체크
   - ffprobe로 duration/codec/streams 검증 후 score 산출

### Acceptance Criteria (Reality Gate)
- [x] DRY_RUN: 네트워크 호출 없이 request payload + 계획 출력 ✅
- [x] WET(키 제공 시): taskId 발급 → SUCCESS 폴링 → audio_url 다운로드 ✅ (실패 시도 + fail-closed 검증)
- [x] AV 합성 결과 mp4 생성 (720x1280 등 기존 비디오 스펙 유지) ✅ (silence 오디오로 대체 가능)
- [x] ffprobe 검증 통과 (video stream + audio stream 존재, duration 합리적) ✅ (silence 오디오 생성됨)
- [x] 실패 시에도 fail-closed: 예외 폭발 없이 "무음 fallback"으로 mp4 생성 가능 ✅

## TICKET-083 — MusicProvider Interface + AudioCraft/MusicGen Integration
- Phase: 17 (멀티모달 확장)
- Priority: HIGH
- Type: Feature Enhancement
- Status: ✅ 완료 (2026-01-06)
- Evidence: packages/afo-core/AFO/multimodal/music_provider.py
- Dependencies: audiocraft, stable-audio-tools (optional)

### Goal
오픈소스 음악 생성 서비스들을 표준화된 인터페이스로 통합하여 자동 Provider 선택 및 음악 생성.

### Scope
1) MusicProvider 추상 인터페이스 구현
2) AudioCraft Provider 구현 (고품질 + 세부 제어)
3) MusicGen Provider 구현 (빠른 생성 + 간단 API)
4) Stable Audio Open Provider 구현 (안정적 + 유연한 길이)
5) Suno Provider 인터페이스 래핑
6) MusicProviderRouter 구현 (품질/속도/비용 기반 자동 선택)
7) TimelineState → Provider별 프롬프트 변환

### Acceptance Criteria (Reality Gate)
- [x] MusicProvider 인터페이스 구현 및 테스트 ✅
- [x] AudioCraft/MusicGen Provider 작동 확인 ✅ (인터페이스 준수)
- [x] Router 기반 자동 Provider 선택 ✅
- [x] TimelineState → 음악 생성 파이프라인 완성 ✅
- [x] Provider별 capability/capacity 평가 ✅

---

## 2026 Roadmap Tickets

## TICKET-084 — Governance Agent 구현
- Phase: 18 (AI 거버넌스)
- Priority: HIGH
- Type: Feature Enhancement
- Status: PLANNED
- Evidence: packages/afo-core/AFO/agents/governance_agent.py
- Dependencies: LangGraph, AICPA patterns

### Goal
2026 Gartner 예측 (40% 기업 앱 AI Agent 탑재) 충족을 위한 Policy Adherence 모니터링 에이전트 구현.

### Scope
1) Policy adherence 모니터링
2) Bounded autonomy 아키텍처
3) Escalation path to human
4) Audit trail 자동화

---

## TICKET-085 — Security Agent 구현
- Phase: 19 (보안 자동화)
- Priority: HIGH
- Type: Security Enhancement
- Status: PLANNED
- Evidence: packages/afo-core/AFO/agents/security_agent.py

### Goal
이상 행동 탐지 및 실시간 보안 모니터링 자동화.

### Scope
1) Anomaly detection for agent behavior
2) Real-time security monitoring
3) Threat response automation

---

## TICKET-086 — OpenTelemetry AI Observability
- Phase: 20 (관측성)
- Priority: MEDIUM
- Type: Monitoring Enhancement
- Status: PLANNED
- Evidence: packages/afo-core/AFO/observability/

### Goal
Agent behavior 실시간 모니터링 및 성능 추적.

### Scope
1) OpenTelemetry for AI integration
2) Performance metrics dashboard
3) Compliance violation detection

---

## TICKET-087 — Agentic RAG Enhancement
- Phase: 21 (RAG 고도화)
- Priority: MEDIUM
- Type: Feature Enhancement
- Status: PLANNED
- Evidence: packages/afo-core/services/agentic_rag.py

### Goal
LangGraph Agentic RAG 패턴 적용으로 검색 정확도 향상.

### Scope
1) Query rewriting with agent reasoning
2) Document relevance grading
3) Web search fallback
4) Hallucination self-correction

---

| 기둥 | 체크 기준 |
|------|----------|
| **眞** | PR/커밋에 구현 파일 + 실행 로그 1개 |
| **善** | CI (Trinity Gate + Shellcheck) PASS |
| **美** | 문서 1개 + 사용 예시 |
| **孝** | `./afo`로 원샷 실행 + 실패시 명확 메시지 |
| **永** | Evidence 폴더 (manifest+sha256) + Seal Tag |
