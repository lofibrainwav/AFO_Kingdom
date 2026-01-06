"""
Alliance API Router
Exposes alliance observation data for the Dashboard.
Trinity Pillar: 善 (Goodness) - Transparency & Stability
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/alliances", tags=["Alliances"])

# Path to the observation report
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REPORT_PATH = REPO_ROOT / "artifacts" / "alliance_observation.json"
CONFIG_PATH = REPO_ROOT / "config" / "alliances.json"


class AllianceStatus(BaseModel):
    id: str
    name: str
    status: str
    dns_reachable: bool | None = None
    observed_at: str | None = None


@router.get("/status")
async def get_alliance_status() -> dict[str, Any]:
    """Get the latest alliance observation report."""
    if not REPORT_PATH.exists():
        # If report doesn't exist, try to read the raw config as fallback
        if not CONFIG_PATH.exists():
            raise HTTPException(status_code=404, detail="Alliance data not found")

        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                config = json.load(f)
                return {
                    "timestamp": None,
                    "alliances": config.get("alliances", []),
                    "source": "config",
                }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read alliance config: {e}")

    try:
        with open(REPORT_PATH, encoding="utf-8") as f:
            report = json.load(f)
            report["source"] = "observer"
            return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read observation report: {e}")


@router.get("/config")
async def get_alliance_config() -> dict[str, Any]:
    """Get the alliance configuration."""
    if not CONFIG_PATH.exists():
        raise HTTPException(status_code=404, detail="Alliance configuration not found")

    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read alliance config: {e}")
