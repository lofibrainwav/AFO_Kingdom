"""
Strangler Fig Compatibility Router
Phase 15: The Grok Singularity

Provides API endpoints for React components to consume HTML dashboard data.
Implements the Strangler Fig pattern for gradual migration from HTML to React.
"""

from typing import Any, Dict, List

from AFO.api.compat import (get_personas_list, get_philosophy_pillars,
                            get_project_stats, get_royal_constitution,
                            get_service_ports, get_system_architecture)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/compat", tags=["compat"])


# Pydantic models for API responses
class PersonaResponse(BaseModel):
    name: str
    code: str
    role: str


class PortResponse(BaseModel):
    service: str
    port: str
    description: str


class RuleResponse(BaseModel):
    id: int
    name: str
    principle: str
    code: str = ""


class BookResponse(BaseModel):
    title: str
    weight: str
    rules: list[RuleResponse]


class PhilosophyResponse(BaseModel):
    pillars: list[dict[str, Any]]
    trinity_formula: str
    auto_run_condition: str


@router.get("/personas", response_model=list[PersonaResponse])
async def get_personas():
    """
    Get personas data from HTML dashboard.
    Used by RoyalLibrary React component.
    """
    try:
        data = get_personas_list()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load personas: {e!s}")


@router.get("/ports", response_model=list[PortResponse])
async def get_ports():
    """
    Get service ports data from HTML dashboard.
    Used by RoyalLibrary React component.
    """
    try:
        data = get_service_ports()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load ports: {e!s}")


@router.get("/royal-rules", response_model=list[BookResponse])
async def get_royal_rules():
    """
    Get Royal Constitution rules from HTML dashboard.
    Used by RoyalLibrary React component.
    """
    try:
        data = get_royal_constitution()
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load royal rules: {e!s}"
        )


@router.get("/philosophy", response_model=PhilosophyResponse)
async def get_philosophy():
    """
    Get 5 Pillars philosophy data from HTML dashboard.
    Used by Trinity components.
    """
    try:
        data = get_philosophy_pillars()
        return PhilosophyResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load philosophy: {e!s}")


@router.get("/architecture")
async def get_architecture():
    """
    Get system architecture data from HTML dashboard.
    Used by architecture visualization components.
    """
    try:
        data = get_system_architecture()
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load architecture: {e!s}"
        )


@router.get("/stats")
async def get_stats():
    """
    Get project statistics from HTML dashboard.
    Used by dashboard widgets.
    """
    try:
        data = get_project_stats()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load stats: {e!s}")


@router.get("/health")
async def compat_health():
    """
    Health check for compat router.
    """
    return {
        "status": "healthy",
        "service": "strangler-fig-compat",
        "pattern": "HTML → React Migration",
        "endpoints": [
            "/api/compat/personas",
            "/api/compat/ports",
            "/api/compat/royal-rules",
            "/api/compat/philosophy",
            "/api/compat/architecture",
            "/api/compat/stats",
        ],
    }
