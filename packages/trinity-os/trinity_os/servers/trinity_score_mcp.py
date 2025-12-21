import json
import sys
from datetime import datetime
from typing import Any

# Lazy import for performance: CuPy/NumPy are only imported when needed
_GPU_AVAILABLE: bool | None = None
_cp = None
_np = None


def _get_gpu_status() -> bool:
    """Lazy check for GPU availability (CuPy)."""
    global _GPU_AVAILABLE, _cp
    if _GPU_AVAILABLE is None:
        try:
            import cupy as cp

            _cp = cp
            _GPU_AVAILABLE = True
        except ImportError:
            _GPU_AVAILABLE = False
    return _GPU_AVAILABLE


def _get_numpy():
    """Lazy import NumPy only when needed."""
    global _np
    if _np is None:
        import numpy as np

        _np = np
    return _np


class TrinityScoreEngineHybrid:
    """
    Trinity Score Engine Hybrid (Truth, Goodness, Beauty, Serenity, Eternity).
    Automatically switches to CuPy (GPU) for large-scale metrics if available.
    """

    # SSOT 가중치 (TRINITY_OS_PERSONAS.yaml)
    # Truth: 0.35, Goodness: 0.35, Beauty: 0.20, Serenity: 0.08, Eternity: 0.02
    WEIGHTS = {
        "Truth": 0.35,
        "Goodness": 0.35,
        "Beauty": 0.20,
        "Serenity": 0.08,
        "Eternity": 0.02,
    }
    TOTAL_WEIGHT = sum(WEIGHTS.values())  # Should be 1.0
    THRESHOLD = 100_000

    @staticmethod
    def _hybrid_weighted_sum(weights: list[float], scores: list[float]) -> float:
        """Lazy-loaded hybrid weighted sum with GPU acceleration if available."""
        n = len(weights)
        gpu_available = _get_gpu_status()

        if gpu_available and n > TrinityScoreEngineHybrid.THRESHOLD:
            # CuPy GPU Acceleration (only for large arrays)
            w_gpu = _cp.array(weights)
            s_gpu = _cp.array(scores)
            result = _cp.sum(w_gpu * s_gpu)
            return float(result.get())
        elif gpu_available and n <= TrinityScoreEngineHybrid.THRESHOLD:
            # Small arrays: use NumPy even if CuPy is available (lower overhead)
            np = _get_numpy()
            return float(np.sum(np.array(weights) * np.array(scores)))
        else:
            # NumPy Fallback (CuPy not available)
            np = _get_numpy()
            return float(np.sum(np.array(weights) * np.array(scores)))

    @classmethod
    def evaluate(cls, **metrics: int) -> dict[str, Any]:
        """Evaluate the Trinity Score based on input metrics."""
        # Simplified calculation for MVP
        scores = {
            "Truth": min(100, metrics.get("truth_base", 100)),
            "Goodness": min(100, metrics.get("goodness_base", 100) - metrics.get("risk_score", 0)),
            "Beauty": min(100, metrics.get("beauty_base", 100)),
            "Serenity": min(100, 100 - metrics.get("friction", 0)),
            "Eternity": min(100, metrics.get("eternity_base", 100)),
        }

        # Calculate Weighted Sum using Hybrid Engine (SSOT 가중치)
        # Convert scores to 0.0~1.0 scale for SSOT weights
        keys = ["Truth", "Goodness", "Beauty", "Serenity", "Eternity"]
        w_list = [float(cls.WEIGHTS[k]) for k in keys]
        s_list = [float(scores[k]) / 100.0 for k in keys]  # Convert to 0.0~1.0 scale
        weighted_sum = cls._hybrid_weighted_sum(w_list, s_list)

        # SSOT weights already sum to 1.0, so no division needed
        final_score = round(weighted_sum * 100, 2)  # Convert back to 0~100 scale

        # [NEW] Audit Gate Logic (Auto-Block)
        # Truth Requirement: < 70 is blocked.
        # Serenity Requirement: Friction > 20 is blocked.
        # Goodness Requirement: Risk > 50 is blocked.

        friction = metrics.get("friction", 0)
        risk = metrics.get("risk_score", 0)

        gate_status = "PASS"
        action = "PROCEED"
        reason = "Harmony Achieved"

        if final_score < 70.0:
            gate_status = "BLOCK"
            action = "HALT_FOR_REVIEW"
            reason = "Trinity Score too low (Disharmony)"
        elif friction > 20:
            gate_status = "BLOCK"
            action = "OPTIMIZE_FIRST"
            reason = "Friction too high (Serenity Breach)"
        elif risk > 50:
            gate_status = "BLOCK"
            action = "MITIGATE_RISK"
            reason = "Risk too high (Goodness Breach)"

        auto_run = gate_status == "PASS" and risk < 10

        return {
            "timestamp": datetime.now().isoformat(),
            "component_scores": scores,
            "trinity_score": final_score,
            "auto_run_eligible": auto_run,
            "gate_status": gate_status,
            "recommended_action": action,
            "reason": reason,
        }


if __name__ == "__main__":
    # If run directly script-wise for testing
    if len(sys.argv) > 1 and sys.argv[1] == "evaluate":
        print(json.dumps(TrinityScoreEngineHybrid.evaluate(risk_score=5)))
    else:
        # Lazy import asyncio only when needed (MCP server mode)
        import asyncio

        async def main():
            # Simple JSON-RPC 2.0 Loop over Stdin/Stdout
            while True:
                try:
                    line = await asyncio.to_thread(sys.stdin.readline)
                    if not line:
                        break
                    json.loads(line)
                    # Minimal implementation for "tools/list" and "tools/call"
                    pass
                except Exception:
                    break

        asyncio.run(main())
