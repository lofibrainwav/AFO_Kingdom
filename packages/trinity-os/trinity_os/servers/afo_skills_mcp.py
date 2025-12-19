import sys
import time
from typing import Any

try:
    import cupy as cp

    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    import numpy as np
import json
import os

# Trinity Score Evaluator (동적 점수 계산)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../afo-core"))
    from AFO.services.mcp_tool_trinity_evaluator import mcp_tool_trinity_evaluator
except ImportError:
    mcp_tool_trinity_evaluator = None


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
        """Simple JSON-RPC loop handling tool calls with Trinity Score evaluation."""
        for line in sys.stdin:
            try:
                request = json.loads(line)
                method = request.get("method")
                params = request.get("params", {})
                msg_id = request.get("id")

                result = None
                trinity_score = None

                # Tool execution with Trinity Score evaluation
                if method == "tools/call":
                    tool_name = params.get("name")
                    args = params.get("arguments", {})

                    start_time = time.time()
                    is_error = False
                    execution_result = None

                    try:
                        if tool_name == "cupy_weighted_sum":
                            execution_result = cls.cupy_weighted_sum(args.get("data", []), args.get("weights", []))
                        elif tool_name == "verify_fact":
                            execution_result = cls.verify_fact(args.get("claim"), args.get("context", ""))
                        else:
                            execution_result = f"Unknown tool: {tool_name}"
                            is_error = True

                        # Error detection
                        if isinstance(execution_result, str) and (
                            "Error" in execution_result or "error" in execution_result.lower()
                        ):
                            is_error = True

                    except Exception as e:
                        execution_result = f"Execution Error: {e!s}"
                        is_error = True

                    execution_time_ms = (time.time() - start_time) * 1000

                    # Trinity Score calculation
                    if mcp_tool_trinity_evaluator:
                        try:
                            result_str = (
                                json.dumps(execution_result)
                                if isinstance(execution_result, dict)
                                else str(execution_result)
                            )
                            trinity_eval = mcp_tool_trinity_evaluator.evaluate_execution_result(
                                tool_name=tool_name,
                                execution_result=result_str,
                                execution_time_ms=execution_time_ms,
                                is_error=is_error,
                            )
                            trinity_score = trinity_eval["trinity_metrics"]
                        except Exception:
                            trinity_score = None

                    # Build result with Trinity Score
                    result_content = [{"type": "text", "text": str(execution_result)}]
                    if trinity_score:
                        result_content.append(
                            {
                                "type": "text",
                                "text": f"\n\n[眞善美孝永 Trinity Score]\n"
                                f"眞 (Truth): {trinity_score.get('truth', 0):.2%}\n"
                                f"善 (Goodness): {trinity_score.get('goodness', 0):.2%}\n"
                                f"美 (Beauty): {trinity_score.get('beauty', 0):.2%}\n"
                                f"孝 (Serenity): {trinity_score.get('filial_serenity', 0):.2%}\n"
                                f"永 (Eternity): {trinity_score.get('eternity', 0):.2%}\n"
                                f"Trinity Score: {trinity_score.get('trinity_score', 0):.2%}\n"
                                f"Balance: {trinity_score.get('balance_status', 'unknown')}",
                            }
                        )

                    result = {
                        "content": result_content,
                        "isError": is_error,
                        "trinity_score": trinity_score,
                    }

                elif method == "tools/list":
                    result = {
                        "tools": [
                            {
                                "name": "cupy_weighted_sum",
                                "description": "Calculate weighted sum using GPU (CuPy) acceleration if available.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"type": "array", "items": {"type": "number"}},
                                        "weights": {"type": "array", "items": {"type": "number"}},
                                    },
                                    "required": ["data", "weights"],
                                },
                            },
                            {
                                "name": "verify_fact",
                                "description": "Verify a fact claim against context (Hallucination Defense).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "claim": {"type": "string"},
                                        "context": {"type": "string"},
                                    },
                                    "required": ["claim"],
                                },
                            },
                        ]
                    }
                elif method == "initialize":
                    result = {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {"name": "AfoSkills", "version": "1.0.0"},
                    }
                elif method == "notifications/initialized":
                    continue
                else:
                    result = {"error": "Unknown method"}

                response = {"jsonrpc": "2.0", "result": result, "id": msg_id}
                print(json.dumps(response))
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
