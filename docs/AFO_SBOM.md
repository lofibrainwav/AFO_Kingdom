# AFO Kingdom SBOM (Software Bill of Materials)
**Date**: 2025-12-20 | **Protocol**: LOCK Re-Sealing (孝永)

## [afo-core] Python Dependencies
Captured via `pip list`

| Package | Version |
|---------|---------|
| fastapi | 0.115.0 |
| pydantic | 2.12.0 |
| ruff | 0.14.10 |
| mypy | 1.15.0 |
| pytest | 9.0.2 |
| sqlmodel | 0.0.22 |
| anthropic | 0.42.0 |
| google-generativeai| 0.8.3 |
| openai | 1.58.1 |
| redis | 5.2.1 |
| psycopg2-binary | 2.9.10 |

## [dashboard] Node.js Dependencies
Captured via `npm list`

| Package | Version |
|---------|---------|
| next | 14.2.5 |
| react | 18.3.1 |
| typescript | 5.5.4 |
| swr | 2.3.0 |
| lucide-react | 0.428.0 |
| tailwind-merge | 2.5.2 |

## Supply Chain Security
- All keys managed via **Vault KMS**.
- Code audited via **MyPy (眞)** and **Ruff (善)**.
- Internal logic verified via **Pytest (美)**.
