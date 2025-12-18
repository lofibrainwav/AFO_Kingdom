import sys
from pathlib import Path
from typing import Any

try:
    import cupy as cp

    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    import numpy as np
import json


class AfoSkillsMCP:
    """Specialized Toolkit MCP: CuPy Acceleration & Core Skills."""

    @staticmethod
    def cupy_weighted_sum(data: list[float], weights: list[float]) -> float:
        """High-performance weighted sum using CuPy if available."""
        if GPU_AVAILABLE:
            return float(cp.sum(cp.array(data) * cp.array(weights)))
        else:
            return float(np.sum(np.array(data) * np.array(weights)))

    @staticmethod
    def read_file(path: str) -> str:
        """Reads a file from the filesystem (Standard Skill)."""
        return Path(path).read_text(encoding="utf-8")

    @staticmethod
    def verify_fact(claim: str, context: str = "") -> dict[str, Any]:
        """
        Hallucination Defense: Verifies a claim against known context or logic.
        'Universe Teacher' Logic: Checks for grounding and consistency.
        """
        # In a full implementation, this connects to Vector DB or Search
        risk_score = 0
        verdict = "PLAUSIBLE"

        if not claim:
            return {"verdict": "EMPTY", "risk": 100, "reason": "Claim is empty"}

        claim_lower = claim.lower()
        if "always" in claim_lower or "never" in claim_lower:
            # Absolute claims are suspicious (Truth Pillar)
            risk_score += 20
            verdict = "CHECK_ABSOLUTES"

        if not context and "fact" in claim_lower:
            # Fact without context is unverified
            risk_score += 40
            verdict = "UNVERIFIED"

        return {
            "claim": claim,
            "verdict": verdict,
            "risk_score": risk_score,
            "defense_mechanism": "Universe Teacher v1 (Heuristic)",
        }

    @classmethod
    def run_loop(cls):
        """Simple JSON-RPC loop handling tool calls."""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                method = request.get("method")
                params = request.get("params", {})

                result = None
                if method == "cupy_weighted_sum":
                    result = cls.cupy_weighted_sum(params.get("data", []), params.get("weights", []))
                elif method == "read_file":
                    result = cls.read_file(params.get("path"))
                elif method == "verify_fact":
                    result = cls.verify_fact(params.get("claim"), params.get("context", ""))
                elif method == "tools/list":
                    result = {
                        "tools": [
                            {
                                "name": "cupy_weighted_sum",
                                "description": "Calculate weighted sum using GPU (CuPy) acceleration if available.",
                            },
                            {"name": "read_file", "description": "Read file content from filesystem."},
                            {
                                "name": "verify_fact",
                                "description": "Verify a fact claim against context (Hallucination Defense).",
                            },
                        ]
                    }
                else:
                    result = {"error": "Unknown method"}

                print(json.dumps({"jsonrpc": "2.0", "result": result, "id": request.get("id")}))
                sys.stdout.flush()
            except Exception as e:
                print(json.dumps({"jsonrpc": "2.0", "error": str(e), "id": None}))
                sys.stdout.flush()


if __name__ == "__main__":
    # Mock execution for verification if args provided
    if len(sys.argv) > 1 and sys.argv[1] == "cupy_test":
        print(AfoSkillsMCP.cupy_weighted_sum([1.0, 2.0], [0.5, 0.5]))
    else:
        AfoSkillsMCP.run_loop()
