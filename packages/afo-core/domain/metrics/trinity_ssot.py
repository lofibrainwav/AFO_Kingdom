# Trinity Score: 90.0 (Established by Chancellor)
"""[TRUTH WIRING]
Trinity Pillar SSOT (Single Source of Truth)
Defines the immutable weights for the 5 Pillars of the AFO Kingdom.
This file must be treated as a constant law.
"""

from typing import Final

# 🏛️ SSOT Trinity Weights (眞善美孝永) - Friction Calculator v2.0 Standard
WEIGHTS = {
    "truth": 0.35,  # 眞: 제갈량 (Technical Certainty - System Friction)
    "goodness": 0.35,  # 善: 사마의 (Ethical Safety - Security Friction)
    "beauty": 0.30,  # 美: 주유 (UX/Aesthetics - Cognitive Friction)
    "serenity": 0.00,  # 孝: 승상 (Legacy Merged into Radar Area)
    "eternity": 0.00,  # 永: 승상 (Legacy Merged into Radar Area)
}

# 🏛️ 5 Pillar Weights (Total: 1.0) - Legacy compatibility
WEIGHT_TRUTH: Final[float] = 0.35
WEIGHT_GOODNESS: Final[float] = 0.35
WEIGHT_BEAUTY: Final[float] = 0.30
WEIGHT_SERENITY: Final[float] = 0.00
WEIGHT_ETERNITY: Final[float] = 0.00

# 🛡️ Governance Thresholds
THRESHOLD_AUTO_RUN_SCORE: Final[float] = 90.0
THRESHOLD_AUTO_RUN_RISK: Final[float] = 10.0

# 🌉 System Constants
DEFAULT_HEARTBEAT: Final[int] = 68


class TrinityWeights:
    """[Compatibility Layer]
    Namespace for Trinity Weights to match usage in trinity.py
    """

    TRUTH = WEIGHT_TRUTH
    GOODNESS = WEIGHT_GOODNESS
    BEAUTY = WEIGHT_BEAUTY
    SERENITY = WEIGHT_SERENITY
    ETERNITY = WEIGHT_ETERNITY
