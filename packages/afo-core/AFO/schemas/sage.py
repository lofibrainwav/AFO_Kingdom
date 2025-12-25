# Trinity Score: 90.0 (Established by Chancellor)
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import Field

from .base import BaseSchema


class SageType(str, Enum):
    """Type of Sage (MoE Expert)"""

    SAMAHWI = "samahwi"
    JWAJA = "jwaja"
    HWATA = "hwata"


class SageRequest(BaseSchema):
    """
    Request to a Yeongdeok Sage
    Validation ensures Truth (Correct Expert) & Goodness (Safe Prompt)
    """

    sage: SageType = Field(..., description="Target Sage (Expert)")
    prompt: str = Field(..., min_length=1, description="User query / prompt")
    system_context: str | None = Field(
        None, description="Optional override system prompt"
    )
    temperature: float = Field(
        default=0.2, ge=0.0, le=1.0, description="Creativity control"
    )


class SageResponse(BaseSchema):
    """
    Response from a Yeongdeok Sage
    Validation ensures strict output format
    """

    sage: SageType = Field(..., description="Sage who responded")
    content: str = Field(..., description="Generated content")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Time of generation"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Execution metadata (latency, tokens)"
    )
    is_fallback: bool = Field(
        default=False, description="Whether fallback mechanism was used"
    )
