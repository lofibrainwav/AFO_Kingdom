#!/usr/bin/env python3
"""
Sequential Thinking MCP Module
Step-by-step reasoning and inference for MCP tools
"""

import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SequentialThinkingMCP:
    """
    Sequential Thinking MCP - Step-by-step reasoning support
    """

    def __init__(self):
        self.thought_history: List[Dict[str, Any]] = []
        self.current_session: Optional[str] = None

    def process_thought(
        self,
        thought: str,
        thought_number: int,
        total_thoughts: int,
        next_thought_needed: bool
    ) -> Dict[str, Any]:
        """
        Process step-by-step thinking

        Args:
            thought: Current thought content
            thought_number: Current step number
            total_thoughts: Total number of steps
            next_thought_needed: Whether next step is needed

        Returns:
            Processing result
        """

        # Save thought record
        thought_entry = {
            "thought": thought,
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "next_thought_needed": next_thought_needed,
            "timestamp": self._get_timestamp(),
            "truth_impact": self._evaluate_truth_impact(thought),
            "serenity_impact": self._evaluate_serenity_impact(thought)
        }

        self.thought_history.append(thought_entry)

        # Generate result
        result = {
            "thought_processed": thought,
            "step": f"{thought_number}/{total_thoughts}",
            "progress": thought_number / total_thoughts,
            "completed": thought_number >= total_thoughts,
            "next_needed": next_thought_needed,
            "metadata": {
                "truth_impact": thought_entry["truth_impact"],
                "serenity_impact": thought_entry["serenity_impact"],
                "session_id": self.current_session or "default"
            }
        }

        if thought_number >= total_thoughts:
            result["summary"] = self._generate_summary()

        return result

    def _evaluate_truth_impact(self, thought: str) -> float:
        """Evaluate truth impact"""
        truth_indicators = [
            "fact", "evidence", "data", "logic", "reason", "verify", "validate",
            "evidence", "proof", "logic", "verify", "validate"
        ]

        score = 0.1  # Base score
        thought_lower = thought.lower()

        for indicator in truth_indicators:
            if indicator in thought_lower:
                score += 0.1

        return min(score, 1.0)

    def _evaluate_serenity_impact(self, thought: str) -> float:
        """Evaluate serenity impact"""
        serenity_indicators = [
            "calm", "stable", "balanced", "harmony", "clear", "simple",
            "serenity", "balance", "harmony", "calm", "clear", "simple"
        ]

        score = 0.1  # Base score
        thought_lower = thought.lower()

        for indicator in serenity_indicators:
            if indicator in thought_lower:
                score += 0.08

        return min(score, 1.0)

    def _get_timestamp(self) -> str:
        """Return current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _generate_summary(self) -> str:
        """Generate step-by-step thinking summary"""
        if not self.thought_history:
            return "No thought process recorded."

        total_steps = len(self.thought_history)
        avg_truth = sum(t.get("truth_impact", 0) for t in self.thought_history) / total_steps
        avg_serenity = sum(t.get("serenity_impact", 0) for t in self.thought_history) / total_steps

        return f"Total {total_steps} steps completed. Average truth: {avg_truth:.2f}, Average serenity: {avg_serenity:.2f}"

    def get_thought_history(self) -> List[Dict[str, Any]]:
        """Return thought history"""
        return self.thought_history.copy()

    def clear_history(self) -> None:
        """Clear thought history"""
        self.thought_history.clear()

    def start_session(self, session_id: str) -> None:
        """Start new thinking session"""
        self.current_session = session_id
        self.clear_history()

    def end_session(self) -> Dict[str, Any]:
        """End current session and return summary"""
        summary = {
            "session_id": self.current_session,
            "total_thoughts": len(self.thought_history),
            "completed_at": self._get_timestamp(),
            "final_summary": self._generate_summary()
        }

        self.current_session = None
        return summary
