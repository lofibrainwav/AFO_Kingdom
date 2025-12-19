"""
Trinity 5-Pillar SSOT (Single Source of Truth)
眞善美孝永 (Truth·Goodness·Beauty·Serenity·Eternity)

This module defines the canonical weights for the Trinity Score.
All evaluators MUST import from here to ensure consistency.

[Weights Reference]
- Truth (眞): 35% - Technical Certainty, Type Safety
- Goodness (善): 35% - Ethical Priority, Stability, Security
- Beauty (美): 20% - UX, Aesthetics, Code Quality
- Serenity (孝): 8% - Low Friction, Peace of Mind (Commander)
- Eternity (永): 2% - Sustainability, Self-Healing, Long-term Vision
"""

from typing import Final


class TrinityWeights:
    """Canonical Weights for Trinity Score"""

    TRUTH: Final[float] = 0.35
    GOODNESS: Final[float] = 0.35
    BEAUTY: Final[float] = 0.20
    SERENITY: Final[float] = 0.08
    ETERNITY: Final[float] = 0.02

    @classmethod
    def validate(cls) -> bool:
        """Verify that weights sum to roughly 1.0"""
        total = cls.TRUTH + cls.GOODNESS + cls.BEAUTY + cls.SERENITY + cls.ETERNITY
        return 0.99 <= total <= 1.01
