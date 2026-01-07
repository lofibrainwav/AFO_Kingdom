# AFO Kingdom 최적화 Claude Code 가이드 (SSOT)

> **최종 업데이트**: 2025-01-07 | **봉인**: Zilong (Claude Code)

## 0) 목적

- Claude Code에서 AFO 작업 흐름을 **10초 프리플라이트 → 모의전(리스크/전략) → 4-Gate 검증 → Evidence 봉인**으로 고정합니다.
- 원칙: **眞·善·美·孝·永 + 지피지기 + 회귀 방지**

---

## 1) 커스텀 슬래시 명령어 (7개)

| 명령어 | 설명 | AFO 철학 |
|---|---|---|
| `/preflight` | 10초 프로토콜 실행 | 지피지기 (손자병법 #1) |
| `/check` | 4-Gate CI 프로토콜 | 眞善美永 Gate |
| `/ssot` | SSOT 문서 읽기 | 지피지기 (Context7) |
| `/trinity` | Trinity Score 계산 | 5기둥 평가 |
| `/evidence` | Evidence 번들 생성 | 永 (기록) |
| `/dryrun` | 모의전 분석 | 병자궤도야 (손자병법 #3) |
| `/strategist` | 3 Strategists 분석 | 제갈량/사마의/주유 |

**파일 위치**: `.claude/commands/*.md`

---

## 2) AFO 워크플로우 최적화 팁

### (1) 작업 시작 전 — 지피지기

```bash
/preflight [작업 내용]     # 10초 프로토콜
/ssot [관련 주제]          # SSOT 문서 확인
```

### (2) 리스크 평가 — 병자궤도야

```bash
/dryrun [작업 내용]        # DRY_RUN 모의전
/trinity [작업 내용]       # Trinity Score 계산
/strategist [작업 내용]    # 3 전략가 분석
```

### (3) 실행 후 검증 — 4-Gate

```bash
/check                     # make check 실행
/evidence [작업 내용]      # Evidence 기록/봉인
```

---

## 3) 키보드 단축키 매핑 (권장: 사용자 정의 컨벤션)

> **주**: 아래는 **AFO 운영 컨벤션(권장)** 입니다.
> 실제 기본 단축키는 환경/에디터/Claude Code 설정에 따라 다를 수 있으니, Claude Code의 도움말/설정에서 최종 확인하세요.

| 단축키 | 용도 | AFO 매핑 |
|---|---|---|
| `Ctrl+O` | Verbose 모드 | 眞 (Truth) 상세 확인 |
| `Shift+Tab` | 권한 모드 전환 | AUTO_RUN ↔ ASK |
| `Esc` → `Esc` | 되돌리기 | 롤백 (永) |
| `?` | 단축키 보기 | 지피지기 |
| `!` + 명령어 | Bash 직접 실행 | 兵貴神速 (속도) |

---

## 4) Trinity Score 빠른 참조

| 기둥 | 가중치 | 의미 |
|---|---|---|
| 眞 (Truth) | 35% | 타입 안전, 정확성 |
| 善 (Goodness) | 35% | 테스트, 안정성 |
| 美 (Beauty) | 20% | 코드 품질, 린트 |
| 孝 (Serenity) | 8% | UX, 에러 메시지 |
| 永 (Eternity) | 2% | 문서, Evidence |

### 실행 모드 판정

| 조건 | 행동 |
|---|---|
| Trinity ≥ 90 **AND** Risk ≤ 10 | **AUTO_RUN** |
| 그 외 | **ASK_COMMANDER** |
| Secrets/Auth/Prod 영향 | **BLOCK** |

---

## 5) Risk Score 기준

| 요인 | 가산 |
|---|---|
| Auth/Payment/Secrets/Prod | +60 |
| DB/데이터/비가역 | +40 |
| 의존성 업데이트/대규모 리팩터 | +30 |
| 테스트 부재 상태 핵심 로직 변경 | +25 |
| 문서/소규모 버그/UI | +5~10 |

---

## 6) 추천 워크플로우 (전체 사이클)

```
1. /preflight "버그 수정"     # 10초 프로토콜
2. /dryrun "버그 수정"        # 모의전 분석
3. (코드 수정)                 # 실행
4. /check                      # 4-Gate 검증
5. /evidence "버그 수정"      # Evidence 봉인
6. git commit                  # 커밋
```

---

## 7) 관련 SSOT 문서

| 문서 | 역할 |
|---|---|
| [AGENTS.md](../AGENTS.md) | 거버넌스 규칙 (10초 프로토콜) |
| [AFO_ROYAL_LIBRARY.md](AFO_ROYAL_LIBRARY.md) | 41가지 원칙 (헌법) |
| [CLAUDE.md](../CLAUDE.md) | Claude Code 작업 지침 |

---

## 8) 3 Strategists (Chancellor Graph)

| 전략가 | 역할 | 기둥 |
|---|---|---|
| 諸葛亮 (Zhuge Liang) | Sword ⚔️ - 아키텍처, 전략, 기술적 확신 | 眞 |
| 司馬懿 (Sima Yi) | Shield 🛡️ - 윤리, 안정성, 리스크 평가 | 善 |
| 周瑜 (Zhou Yu) | Bridge 🌉 - 내러티브, UX, 커뮤니케이션 | 美 |

---

**End of SSOT**
