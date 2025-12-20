from .base import robust_execute, log_action
from typing import Dict, Any
from pydantic import BaseModel, ValidationError, Field

# Defines the data contract for Truth verification (Modular Interface)
class QueryModel(BaseModel):
    query: str = Field(..., description="Query body - Required")
    context: Dict[str, Any] = Field(default_factory=dict, description="Context data")
    validation_level: int = Field(1, ge=1, le=10, description="Validation Intensity")

def evaluate(query_data: Dict[str, Any]) -> float:
    """
    Zhuge Liang (Truth): Architectural Validation
    
    [Modular Design Benefit]: 
    - Isolated Logic: Validation rules are encapsulated here.
    - Testability: Can be unit tested independently with mock data.
    """
    def _logic(data):
        # Truth Verification Logic
        model = QueryModel(**data)
        arch_fit = 1.0 if "valid_structure" in model.context else 0.8
        type_coverage = min(1.0, model.validation_level / 10)
        return (arch_fit + type_coverage) / 2

    # Robust Execution with Fallback (Graceful Degradation)
    # If logic fails, returns 0.5 (Partial Truth) instead of crashing.
    result = robust_execute(_logic, query_data, fallback_value=0.5)
    log_action("Zhuge Liang 眞", result)
    return result
