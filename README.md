# AFO Kingdom 🏰

> 眞善美孝永 (Truth · Goodness · Beauty · Serenity · Eternity)

## Packages

| Package | Description |
|---------|-------------|
| [afo-core](packages/afo-core/) | FastAPI 백엔드, API Wallet, LLM Router |
| [trinity-os](packages/trinity-os/) | 眞善美孝永 철학 엔진 |
| [sixXon](packages/sixXon/) | SixXon 모듈 |
| [dashboard](packages/dashboard/) | Next.js 대시보드 |

## 🚀 Quick Start (딱 이것만 기억하세요)

이미 떠 있으면 스킵하고, 없으면 알아서 켜줍니다.

```bash
./start_kingdom_v2.sh
```

**실행되는 것들 (Local Kingdom):**
*   ✅ **Redis** (brew): 심장 (자동 실행)
*   ✅ **Qdrant** (local): 폐 (자동 실행)
*   ✅ **API** (:8010): 영혼
*   ✅ **UI** (:3000): 얼굴
*   ⏸ **Postgres** (docker): 간 (옵션 - 데이터 영속성 필요시 `brew install postgresql` 권장)


## CI/CD

- **Trivy**: 취약점 + 시크릿 스캔
- **Snyk**: 의존성 보안 + 자동 Fix PR
- **Ruff**: 린팅/포맷
- **MyPy**: 타입 검사
- **Codecov**: 커버리지 추적

## Documentation

- **[Final Handover Report (MUST READ)](docs/AFO_FINAL_HANDOVER.md)**
- **[대시보드 가이드](DASHBOARD_README.md)** - 메인 대시보드 사용법
- **[Claude Code AFO 가이드](docs/CLAUDE_CODE_AFO_GUIDE.md)** - 10초 프로토콜 + 커스텀 명령어
- [CI/CD Pipeline](docs/CI_CD_PIPELINE.md)
- [OSS Strategy (세종대왕 정신)](docs/OSS_STRATEGY.md)
- [Security Policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## Key Features (New)
- **Digital Royal Palace**: The Living Dashboard (Organs, Skills, Chancellor Stream).
- **Family Hub**: Dashboard for Happiness Tracking (`/family`).
- **Playwright Bridge**: Browser Automation Node.
- **Context7**: Self-Awareness Knowledge Base.

## License

MIT
