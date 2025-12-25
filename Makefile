.PHONY: lint test type-check check

lint:
	cd packages/afo-core && ruff check .

test:
	cd packages/afo-core && pytest -q -m "not integration and not external" --ignore=tests/test_scholars.py

type-check:
	cd packages/afo-core && mypy AFO --ignore-missing-imports

check: lint test type-check

pre-push: check