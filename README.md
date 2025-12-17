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

- [CI/CD Pipeline](docs/CI_CD_PIPELINE.md)
- [OSS Strategy (세종대왕 정신)](docs/OSS_STRATEGY.md)
- [Security Policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT
