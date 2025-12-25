"""
Strangler Fig Compatibility Router
Phase 15: The Grok Singularity

Provides API endpoints for React components to consume HTML dashboard data.
Implements the Strangler Fig pattern for gradual migration from HTML to React.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from AFO.api.compat import (
    get_personas_list,
    get_service_ports,
    get_royal_constitution,
    get_philosophy_pillars,
    get_system_architecture,
    get_project_stats
)

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
    rules: List[RuleResponse]

class PhilosophyResponse(BaseModel):
    pillars: List[Dict[str, Any]]
    trinity_formula: str
    auto_run_condition: str

@router.get("/personas", response_model=List[PersonaResponse])
async def get_personas():
    """
    Get personas data from HTML dashboard.
    Used by RoyalLibrary React component.
    """
    try:
        data = get_personas_list()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load personas: {str(e)}")

@router.get("/ports", response_model=List[PortResponse])
async def get_ports():
    """
    Get service ports data from HTML dashboard.
    Used by RoyalLibrary React component.
    """
    try:
        data = get_service_ports()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load ports: {str(e)}")

@router.get("/royal-rules", response_model=List[BookResponse])
async def get_royal_rules():
    """
    Get Royal Constitution rules from HTML dashboard.
    Used by RoyalLibrary React component.
    """
    try:
        data = get_royal_constitution()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load royal rules: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Failed to load philosophy: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Failed to load architecture: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Failed to load stats: {str(e)}")

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
            "/api/compat/stats"
        ]
    }