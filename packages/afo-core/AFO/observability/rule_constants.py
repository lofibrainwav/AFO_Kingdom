"""
Chancellor Graph Rule Constants (SSOT)

All decision rules used by the Chancellor Graph for AUTO_RUN/ASK routing.
These constants ensure consistency across all nodes and provide audit trails.
"""

from typing import Literal

# Rule IDs for Chancellor Graph decision making
RULE_DRY_RUN_OVERRIDE = "R1_DRY_RUN_OVERRIDE"
RULE_RESIDUAL_DOUBT = "R2_RESIDUAL_DOUBT"
RULE_VETO_LOW_PILLARS = "R3_VETO_LOW_PILLARS"
RULE_AUTORUN_THRESHOLD = "R4_AUTORUN_THRESHOLD"
RULE_FALLBACK_ASK = "R5_FALLBACK_ASK"

# Type alias for valid rule IDs
RuleId = Literal[
    "R1_DRY_RUN_OVERRIDE",
    "R2_RESIDUAL_DOUBT",
    "R3_VETO_LOW_PILLARS",
    "R4_AUTORUN_THRESHOLD",
    "R5_FALLBACK_ASK",
]

# Rule descriptions for documentation and debugging
RULE_DESCRIPTIONS: dict[RuleId, str] = {
    RULE_DRY_RUN_OVERRIDE: "Global DRY_RUN_DEFAULT flag overrides all decisions",
    RULE_RESIDUAL_DOUBT: "High uncertainty or incomplete pillar assessment",
    RULE_VETO_LOW_PILLARS: "Any pillar score below minimum threshold vetoes AUTO_RUN",
    RULE_AUTORUN_THRESHOLD: "Trinity Score >= 90 AND Risk Score <= 10 enables AUTO_RUN",
    RULE_FALLBACK_ASK: "Default fallback to ASK_COMMANDER for all other cases",
}

# Export all rule constants
__all__ = [
    "RULE_AUTORUN_THRESHOLD",
    "RULE_DESCRIPTIONS",
    "RULE_DRY_RUN_OVERRIDE",
    "RULE_FALLBACK_ASK",
    "RULE_RESIDUAL_DOUBT",
    "RULE_VETO_LOW_PILLARS",
    "RuleId",
]
