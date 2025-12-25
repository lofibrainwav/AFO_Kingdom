.PHONY: lint test type-check check

lint:
	cd packages/afo-core && ruff check .

test:
	cd packages/afo-core && pytest -q -m "not integration and not external" --ignore=tests/test_scholars.py

type-check:
	export MYPYPATH=packages/afo-core && mypy -p AFO --config-file packages/afo-core/pyproject.toml

check: lint test type-check

pre-push: check
