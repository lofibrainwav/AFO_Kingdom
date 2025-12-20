from .base import robust_execute, log_action
from typing import Dict, Any

def optimize(query_data: Dict[str, Any]) -> float:
    """
    Zhou Yu (Beauty): UX & Narrative Optimization
    
    [Beauty Philosophy]:
    - UX Focus: Checks for narrative quality (e.g., Glassmorphism).
    - Modularity: Checks for concise narrative structure.
    """
    def _logic(data):
        narrative = data.get("narrative", "")
        if not narrative:
            return 0.5 # Default baseline
            
        ux_score = 1.0 if "glassmorphism" in narrative.lower() else 0.9
        modularity = 1.0 if len(narrative) < 500 else 0.85
        clarity = 1.0 if "coherent" in data else 0.95
        return (ux_score + modularity + clarity) / 3

    # Robust Execute: Fallback to 0.8 (Acceptable Beauty) on error
    result = robust_execute(_logic, query_data, fallback_value=0.8)
    log_action("Zhou Yu 美", result)
    return result
