check:
	bash scripts/ci_lock_protocol.sh

type-check:
	pyright --project packages/afo-core/pyproject.toml

lint:
	cd packages/afo-core && ruff check .

test:
	cd packages/afo-core && pytest -q -m "not integration and not external" --ignore=tests/test_scholars.py

sbom:
	cd scripts && poetry run python generate_sbom.py || python3 generate_sbom.py
	mkdir -p artifacts
	mv sbom artifacts/ 2>/dev/null || true

pre-push: check
