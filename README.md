# AFO Kingdom 🏰

> 眞善美孝永 (Truth · Goodness · Beauty · Serenity · Eternity)

## Packages

| Package | Description |
|---------|-------------|
| [afo-core](packages/afo-core/) | FastAPI 백엔드, API Wallet, LLM Router |
| [trinity-os](packages/trinity-os/) | 眞善美孝永 철학 엔진 |
| [sixXon](packages/sixXon/) | SixXon 모듈 |
| [dashboard](packages/dashboard/) | Next.js 대시보드 |

## Quick Start

```bash
# Python 의존성
pip install -e .

# 개발 의존성
pip install -e ".[dev]"

# 테스트
# 단위 테스트 (기본)
make test

# 통합 테스트 (PostgreSQL, Redis 필요)
make test-integration

# 외부 API 테스트
make test-external

# 또는 직접 실행
pytest --cov=packages

# 린팅
ruff check packages/
mypy packages/afo-core --strict
```

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
