from __future__ import annotations

from typing import Any, Dict, Literal

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/genui", tags=["genui"])

TEMPLATE_IDS = ("hero", "stats", "cta", "list", "card")
TemplateId = Literal["hero", "stats", "cta", "list", "card"]


class GenUIRequest(BaseModel):
    template_id: TemplateId
    props: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "forbid"


class GenUIResponse(BaseModel):
    ok: bool
    template_id: str
    props: Dict[str, Any]


@router.post("/generate", response_model=GenUIResponse)
def generate(req: GenUIRequest) -> GenUIResponse:
    if req.template_id not in TEMPLATE_IDS:
        raise HTTPException(status_code=400, detail="template_id not allowed")

    return GenUIResponse(ok=True, template_id=req.template_id, props=req.props)
