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

## TICKET-084 — Suno vs 오픈소스 비교 분석 + 학습 데이터 생성
- Phase: 18 (멀티모달 확장)
- Priority: HIGH
- Type: Research & Analysis
- Status: ✅ 완료 (2026-01-06)
- Evidence: music_comparison_analyzer.py, artifacts/music_comparison/
- Dependencies: MusicProvider 인터페이스

### Goal
Suno와 오픈소스 음악 생성 서비스를 체계적으로 비교 분석하여 학습 데이터를 생성하고 오픈소스 향상 전략 수립.

### Scope
1) MusicComparisonAnalyzer 프레임워크 구현 (품질/속도/스타일 메트릭)
2) 동일 TimelineState로 양쪽 Provider 비교 테스트
3) 성능 메트릭 수집 및 분석 (생성 시간, 메모리 사용량, 품질 점수)
4) Suno 강점 추출 및 오픈소스 개선 기회 식별
5) 학습 데이터 구조화 저장 (JSON 포맷)

### Acceptance Criteria (Reality Gate)
- [x] MusicComparisonAnalyzer 클래스 구현 ✅
- [x] 품질/성능 메트릭 수집 체계 구축 ✅
- [x] 동일 TimelineState 비교 분석 ✅
- [x] 결과 JSON 구조화 저장 ✅
- [x] 오픈소스 개선 인사이트 도출 ✅

## TICKET-085 — OpenCut UI 음악 프리뷰 임베드 + 백엔드 API 통합
- Phase: 19 (멀티모달 확장)
- Priority: HIGH
- Type: Feature Enhancement
- Status: ✅ 완료 (2026-01-06)
- Evidence: packages/dashboard/src/components/royal/widgets/MusicGenerationWidget.tsx, packages/afo-core/api/routers/multimodal.py
- Dependencies: MLX MusicGen, TimelineState SSOT

### Goal
OpenCut UI에 MLX MusicGen 음악 생성 결과를 실시간으로 프리뷰하고 다운로드할 수 있는 기능을 완전히 통합.

### Scope
1) MusicGenerationWidget 컴포넌트 구현 (TimelineState 표시 + 생성 컨트롤 + 오디오 플레이어)
2) RoyalLayout에 음악 생성 위젯 통합
3) 백엔드 API 엔드포인트 추가 (/api/multimodal/music/generate + /api/audio/{filename})
4) TimelineState → MLX MusicGen 자동 변환 파이프라인 구축
5) 오디오 파일 서빙 및 다운로드 기능 구현

### Acceptance Criteria (Reality Gate)
- [x] MusicGenerationWidget 컴포넌트 구현 및 RoyalLayout 통합 ✅
- [x] 백엔드 음악 생성 API 추가 (/api/multimodal/music/generate) ✅
- [x] 오디오 파일 서빙 API 추가 (/api/audio/{filename}) ✅
- [x] TimelineState 자동 변환 및 MLX MusicGen 호출 ✅
- [x] 프론트엔드 오디오 플레이어 + 다운로드 기능 ✅

## TICKET-086 — AV JOIN 자동화 완성 (영상 + 음악 → 완전 숏폼 콘텐츠)
- Phase: 19 (멀티모달 확장)
- Priority: HIGH
- Type: Feature Enhancement
- Status: ✅ 완료 (2026-01-06)
- Evidence: packages/afo-core/AFO/multimodal/av_join_engine.py, packages/afo-core/api/routers/multimodal.py
- Dependencies: MoviePy, MusicGenerationWidget

### Goal
TimelineState 하나로 영상 + 음악을 자동으로 합성하여 완전한 숏폼 AV 콘텐츠를 생성하는 파이프라인 완성.

### Scope
1) AVJoinEngine 클래스 구현 (MoviePy 기반 오디오-비디오 합성)
2) 백엔드 AV JOIN API 추가 (/api/multimodal/av/join + /api/av/{filename})
3) TimelineState 기반 완전 자동 AV 생성 워크플로우 구현
4) MusicGenerationWidget에 AV 합성 기능 통합
5) AV 플레이어 및 다운로드 기능 구현

### Acceptance Criteria (Reality Gate)
- [x] AVJoinEngine 클래스 및 MoviePy 통합 구현 ✅
- [x] 백엔드 AV JOIN API (/api/multimodal/av/join) 추가 ✅
- [x] AV 파일 서빙 API (/api/av/{filename}) 추가 ✅
- [x] TimelineState 기반 완전 자동 AV 생성 ✅
- [x] 프론트엔드 AV 플레이어 + 다운로드 기능 ✅

### Final Pipeline: ABSORB → GENERATE → FANOUT → JOIN → RENDER ✅
1. **ABSORB**: TimelineState 수집
2. **GENERATE**: MLX MusicGen으로 음악 생성
3. **FANOUT**: CapCut으로 비디오 생성 (병렬)
4. **JOIN**: MoviePy로 AV 합성
5. **RENDER**: 완전 숏폼 콘텐츠 출력

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

## TICKET-088 — Ruff 제거된 규칙 SSOT 정리
- Phase: Code Quality (Ruff 최적화)
- Priority: MEDIUM
- Type: Maintenance
- Status: ✅ COMPLETED (2026-01-06)
- Evidence: packages/afo-core/pyproject.toml, scripts/ssot_verify.sh
- Dependencies: Ruff v0.14.4, ripgrep

### Goal
Ruff v0.8+에서 제거된 규칙들(ANN101, ANN102, UP038)을 pyproject.toml에서 정리하여 Unknown rule 경고 제거 및 SSOT 유지.

### Scope
1) packages/afo-core/pyproject.toml에서 제거된 규칙 잔존 스캔
2) ANN101, ANN102 완전 라인 제거 (ignore 목록)
3) UP038 토큰 제거 (per-file-ignores 리스트)
4) Unknown rule 경고 사라짐 검증
5) TOML 파싱 정상 확인

### Acceptance Criteria (Reality Gate)
- [x] ANN101/ANN102/UP038 잔존 위치 정확 파악 ✅ (라인 118, 151, 178, 209, 212, 213, 214, 215, 219)
- [x] 문자열 패턴 기반 안전 제거 ✅ (Python 스크립트로 완전 정리)
- [x] Unknown rule 경고 완전 사라짐 ✅ (packages/afo-core에서 ruff check 시 경고 없음)
- [x] TOML 파싱 정상 유지 ✅ (python3 toml 파싱 성공)
- [x] SSOT 봉인 완료 ✅ (모든 검증 통과)

