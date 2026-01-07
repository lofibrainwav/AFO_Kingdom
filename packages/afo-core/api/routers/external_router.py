import logging

from fastapi import APIRouter, Depends, HTTPException

from AFO.config.antigravity import antigravity
from AFO.evolution.dgm_engine import EvolutionMetadata, dgm_engine
from AFO.governance.kill_switch import sentry
from AFO.governance.narrative_sanitizer import sanitizer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/public", tags=["External Interface"])


def check_exposure_gate():
    """Ensure external exposure is permitted by the Sovereign."""
    if not antigravity.EXTERNAL_EXPOSURE_ENABLED:
        raise HTTPException(status_code=403, detail="External Exposure Locked by Sovereign Decree.")


@router.get("/chronicle", response_model=list[dict], dependencies=[Depends(check_exposure_gate)])
async def get_public_chronicle():
    """Returns a sanitized, read-only summary of the kingdom's optimization history."""
    history = dgm_engine.chronicle.get_history()

    # Sanitize for public consumption
    public_data = []
    for h in history:
        if h.decree_status == "APPROVED":
            public_data.append(
                {
                    "iteration": h.generation,
                    "summary": [sanitizer.sanitize(m) for m in h.modifications],
                    "reliability_index": h.trinity_score,
                    "timestamp": h.timestamp,
                }
            )
    return public_data


@router.get("/status", dependencies=[Depends(check_exposure_gate)])
async def get_public_status():
    """Returns the high-level health of the civilization."""
    return {
        "status": "OPERATIONAL" if not sentry.is_locked() else "MAINTENANCE",
        "mode": "ADAPTIVE",
        "governance": "ACTIVE",
    }
