from strategists.base import robust_execute, log_action
from typing import Dict, Any
from pydantic import BaseModel, ValidationError, Field

class TruthModel(BaseModel):
    data: Dict[str, Any] = Field(..., description="Data Structure - Required")
    validation_level: int = Field(1, ge=1, le=10, description="Validation Intensity")

def guard(data: Dict[str, Any]) -> float:
    """
    Guan Yu (Truth): Type Integrity Guard
    
    [Modular Design Benefit]:
    - Type Safety: Enforces contract via Pydantic.
    - Robustness: Graceful degradation to 0.5 on validation error.
    """
    def _logic(d):
        model = TruthModel(**d)
        return min(1.0, model.validation_level / 10)

    # Fallback to 0.5 (Partial Trust) if validation crashes unexpectly
    result = robust_execute(_logic, data, fallback_value=0.5)
    log_action("Guan Yu 眞", result)
    return result
