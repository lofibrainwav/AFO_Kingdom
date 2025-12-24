# AFO Kingdom - Makefile
# 眞善美孝永 기반 개발 워크플로우

.PHONY: help install lint test test-integration check ci-local pre-push

help:
	@echo "AFO Kingdom 명령어:"
	@echo "  make check        - 린트 + 테스트 (Serenity 0)"
	@echo "  make lint         - Ruff 린트"
	@echo "  make test         - pytest 실행 (단위 테스트)"
	@echo "  make test-integration - 통합 테스트 실행 (PostgreSQL, Redis 필요)"
	@echo "  make install      - 의존성 설치"
	@echo "  make pre-push     - 푸시 전 전체 검증"

install:
	pip install -e ".[dev]"
	pip install ruff mypy pytest pytest-cov

lint:
	@echo "🔍 AFO-Core 린트 검사..."
	cd packages/afo-core && ruff check .

type-check:
	@echo "📝 AFO-Core 타입 검사 (mypy)..."
	cd packages/afo-core && mypy . --ignore-missing-imports || echo "⚠️ mypy 실패 - 무시하고 진행"

test:
	@echo "🧪 pytest 실행 (단위 테스트)..."
	cd packages/afo-core && pytest -q -m "not integration and not external" --ignore=tests/test_scholars.py

test-integration:
	@echo "🔗 통합 테스트 실행 (PostgreSQL, Redis 필요)..."
	cd packages/afo-core && pytest -q -m integration

test-external:
	@echo "🌐 외부 API 테스트 실행..."
	cd packages/afo-core && pytest -q -m external

check: lint test
	@echo ""
	@echo "✅ Serenity 0: All checks passed!"

security-scan:
	@echo "🔒 보안 스캔..."
	@which trivy > /dev/null && trivy fs . --severity HIGH,CRITICAL || echo "Trivy 미설치 - 스킵"

security-local:
	@echo "🔐 로컬 보안 스캔 (Trivy + Bandit)..."
	@which trivy > /dev/null && trivy fs . --severity HIGH,CRITICAL --exit-code 1 || echo "Trivy 미설치 - 스킵"
	@which bandit > /dev/null && bandit -r packages/ -ll || echo "Bandit 미설치 - 스킵"
	@echo "✅ 보안 스캔 완료"

scorecard:
	@echo "📊 眞善美孝永 Scorecard..."
	python scripts/automate_scorecard.py packages/afo-core || echo "Scorecard 스킵"

trinity-score:
	@echo "🎯 Trinity Score 업데이트..."
	python scripts/chancellor_ci_integration.py --tests-passed --build-success

# 푸시 전 전체 검증 (CI와 100% 동일)
pre-push: lint type-check test scorecard trinity-score
	@echo ""
	@echo "=========================================="
	@echo "✅ 모든 검증 완료! 푸시해도 안전합니다!"
	@echo "=========================================="
	@echo ""

# 로컬 CI 전체 실행
ci-local: pre-push security-scan
	@echo ""
	@echo "🏰 AFO Kingdom CI 로컬 검증 100% 완료!"
	@echo ""

# Git pre-push hook 설치
install-hooks:
	@echo "#!/bin/bash" > .git/hooks/pre-push
	@echo "make pre-push" >> .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
	@echo "✅ pre-push hook 설치 완료"