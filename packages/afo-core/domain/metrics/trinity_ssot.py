"""
[TRUTH WIRING]
Trinity Pillar SSOT (Single Source of Truth)
Defines the immutable weights for the 5 Pillars of the AFO Kingdom.
This file must be treated as a constant law.
"""

from typing import Final

# 🏛️ 5 Pillar Weights (Total: 1.0)
WEIGHT_TRUTH: Final[float] = 0.35  # 眞: 제갈량 (Technical Certainty)
WEIGHT_GOODNESS: Final[float] = 0.35  # 善: 사마의 (Ethical Safety)
WEIGHT_BEAUTY: Final[float] = 0.20  # 美: 주유 (UX/Aesthetics)
WEIGHT_SERENITY: Final[float] = 0.08  # 孝: 승상 (Friction Reduction)
WEIGHT_ETERNITY: Final[float] = 0.02  # 永: 승상 (Persistence/Legacy)

# 🛡️ Governance Thresholds
THRESHOLD_AUTO_RUN_SCORE: Final[float] = 90.0
THRESHOLD_AUTO_RUN_RISK: Final[float] = 10.0

# 🌉 System Constants
DEFAULT_HEARTBEAT: Final[int] = 68


class TrinityWeights:
    """
    [Compatibility Layer]
    Namespace for Trinity Weights to match usage in trinity.py
    """

    TRUTH = WEIGHT_TRUTH
    GOODNESS = WEIGHT_GOODNESS
    BEAUTY = WEIGHT_BEAUTY
    SERENITY = WEIGHT_SERENITY
    ETERNITY = WEIGHT_ETERNITY
