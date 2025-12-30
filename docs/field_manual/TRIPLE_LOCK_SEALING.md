# Triple-Lock Sealing (永) Strategy

To ensure the "Ghost Code" never returns and the system remains truthful (眞), we implement a three-layer defense.

## 1. CI Contract Test (眞)
Prevent code regressions that remove the `build_version` artifact from the `/health` endpoint.

#### [NEW] [test_fingerprint_contract.py](file://<LOCAL_WORKSPACE>/AFO_Kingdom/packages/afo-core/tests/health/test_fingerprint_contract.py)
```python
import pytest
from AFO.services.health_service import get_comprehensive_health

@pytest.mark.asyncio
async def test_health_response_contains_fingerprint():
    health = await get_comprehensive_health()
    assert "build_version" in health
    assert health["build_version"] != "unknown"
```

## 2. Automated Exorcism Runbook (善)
Standardize the "Ghost Removal" process into a single, safe script.

#### [NEW] [exorcise_8010.sh](file://<LOCAL_WORKSPACE>/AFO_Kingdom/scripts/exorcise_8010.sh)
```bash
#!/bin/bash
# Surgical removal of any process/container hijacking port 8010
echo "⚔️  Exorcising Port 8010 hijackers..."
docker stop $(docker container ls --all --filter "publish=8010" -q) || true
docker rm $(docker container ls --all --filter "publish=8010" -q) || true
BUILD_VERSION=$(date +%Y%m%d_%H%M%S) docker compose up --build -d soul-engine
```

## 3. Dashboard E2E Verification (美)
Confirm the `BUILD_FINGERPRINT` is visible to the Commander at all times.

---
> "Three locks, one truth. The Kingdom stands eternal." - Chancellor
