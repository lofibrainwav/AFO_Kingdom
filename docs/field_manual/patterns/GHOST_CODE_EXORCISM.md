# Pattern: Ghost Code Exorcism & Fingerprinting

## Context
When "Ghost Code" (outdated code running in containers/cache despite source updates) disrupts the "Truth" (眞) pillar.

## Solution
1. **Fingerprinting**: Inject a `build_version` (timestamp) during build time.
2. **Contract Testing**: Ensure `/health` always returns this fingerprint.
3. **E2E UI Verification**: Display the fingerprint in the Dashboard Footer and verify it matches the backend via Playwright.
4. **Surgical Exorcism**: Use `docker compose build --no-cache` for a specific service to force truth.

## Tools
- `scripts/exorcise_8010.sh`: No-cache target rebuild.
- `scripts/verify_fingerprint.sh`: CLI verification.
- `packages/dashboard/tests/fingerprint.spec.ts`: E2E verification.
