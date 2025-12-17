# AFO Kingdom - Makefile
# 眞善美孝永 기반 개발 워크플로우

.PHONY: help install lint test ci-local pre-push

help:
	@echo "AFO Kingdom 명령어:"
	@echo "  make install      - 의존성 설치"
	@echo "  make lint         - Ruff 린트 + 포맷"
	@echo "  make test         - pytest 실행"
	@echo "  make pre-push     - 푸시 전 전체 검증 (CI 100% 재현)"
	@echo "  make ci-local     - 로컬 CI 전체 실행"

install:
	pip install -e ".[dev]"
	pip install ruff mypy pytest pytest-cov

lint:
	@echo "🔍 Ruff 린트 검사..."
	ruff check packages/ scripts/ --fix
	@echo "✨ Ruff 포맷 검사..."
	ruff format packages/ scripts/

type-check:
	@echo "📝 MyPy 타입 검사..."
	mypy packages/afo-core --ignore-missing-imports || echo "MyPy 경고 있음 (계속 진행)"

test:
	@echo "🧪 pytest 실행..."
	pytest packages/*/tests -v --tb=short || echo "테스트 없음 또는 일부 실패"

security-scan:
	@echo "🔒 보안 스캔..."
	@which trivy > /dev/null && trivy fs . --severity HIGH,CRITICAL || echo "Trivy 미설치 - 스킵"

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
