"""
Trinity Score Calculator (SSOT)
동적 Trinity Score 계산기 - SSOT 가중치 기반 정밀 산출
PDF 페이지 1: Trinity Score 계산기, 페이지 3: 5대 가치 동적 평가
"""

import logging
import numpy as np
from typing import List, Dict, Any
from config.friction_calibrator import friction_calibrator

logger = logging.getLogger(__name__)

# SSOT 가중치 (agents.md Ⅱ. SSOT)
# Truth(35%), Goodness(35%), Beauty(20%), Serenity(8%), Eternity(2%)
SSOT_WEIGHTS = np.array([0.35, 0.35, 0.20, 0.08, 0.02])

class TrinityCalculator:
    """
    Trinity Score Calculator (SSOT Implementation)
    """

    def calculate_raw_scores(self, query_data: Dict[str, Any]) -> List[float]:
        """
        Calculates Raw Scores [0.0, 1.0] for each Pillar.
        Ideally this delegates to specific evaluators (TruthVerifier, RiskGate, etc.)
        For this service method, we implement the logic aggregation.
        """
        # 1. 眞 (Truth): Validation & Architecture
        # Simplified logic based on input quality
        truth = 1.0
        if "invalid" in query_data or query_data.get("valid_structure") is False:
            truth = 0.0
            
        # 2. 善 (Goodness): Risk & Ethics
        goodness = 1.0
        risk = query_data.get("risk_level", 0.0)
        if risk > 0.1:
            goodness = 0.0 # Block logic
            
        # 3. 美 (Beauty): Narrative & UX
        beauty = 1.0
        if query_data.get("narrative") == "partial":
            beauty = 0.85
            
        # 4. 孝 (Serenity): Automation Friction
        # Integrated with FrictionCalibrator (Phase 13)
        serenity_metrics = friction_calibrator.calculate_serenity()
        serenity = serenity_metrics.score / 100.0 # Normalize 0-100 to 0.0-1.0
        
        # 5. 永 (Eternity): Logging
        eternity = 1.0
        # Placeholder
        
        return [truth, goodness, beauty, serenity, eternity]

    def calculate_trinity_score(self, raw_scores: List[float]) -> float:
        """
        Calculates final Trinity Score using SSOT Weights.
        Range: 0.0 to 100.0
        """
        if len(raw_scores) != 5:
            raise ValueError(f"Must have 5 raw scores, got {len(raw_scores)}")
            
        if not all(0.0 <= s <= 1.0 for s in raw_scores):
            raise AssertionError("Raw scores must be between 0.0 and 1.0")
            
        # SSOT Weighted Sum
        weighted_sum = np.dot(raw_scores, SSOT_WEIGHTS)
        
        # Scale to 100 and Round
        final_score = round(weighted_sum * 100, 1)
        
        logger.info(f"[TrinityCalculator] Raw: {raw_scores} -> Score: {final_score}")
        return final_score

# Singleton Instance
trinity_calculator = TrinityCalculator()
