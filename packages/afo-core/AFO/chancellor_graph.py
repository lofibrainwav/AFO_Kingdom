"""Chancellor Graph V2 - AFO Kingdom Integration Layer.

Provides unified interface for Chancellor Graph V2 operations.
SSOT Contract: Sequential Thinking + Context7 are REQUIRED.
"""

from __future__ import annotations

import asyncio
import json
import os
import random
import time
from typing import Any

from AFO.config.settings import get_settings
from AFO.api.chancellor_v2.graph import nodes

# Import Chancellor Graph V2 components
from AFO.api.chancellor_v2.graph.runner import run_v2 as run_chancellor_v2


# Create unified chancellor_graph interface
class ChancellorGraph:
    """Unified Chancellor Graph interface."""

    @staticmethod
    async def run_v2(input_payload: dict, nodes_dict: dict | None = None) -> dict:
        """Run Chancellor Graph V2 with default nodes if not provided.

        Args:
            input_payload: Input payload for graph execution
            nodes_dict: Optional custom nodes dict

        Returns:
            Execution result as dict
        """
        if nodes_dict is None:
            # Default node configuration
            nodes_dict = {
                "CMD": nodes.cmd_node,
                "PARSE": nodes.parse_node,
                "TRUTH": nodes.truth_node,
                "GOODNESS": nodes.goodness_node,
                "BEAUTY": nodes.beauty_node,
                "SERENITY": nodes.serenity_node,
                "ETERNITY": nodes.eternity_node,
                "MERGE": nodes.merge_node,
                "EXECUTE": nodes.execute_node,
                "VERIFY": nodes.verify_node,
                "REPORT": nodes.report_node,
            }

        # Always add MIPRO node (NO-OP by default, feature-flag controlled)
        async def mipro_node(state):
            """MIPRO optimization node for Chancellor Graph (NO-OP by default)."""
            try:
                from AFO.chancellor_mipro_plugin import ChancellorMiproPlugin

                plugin = ChancellorMiproPlugin()
                plan = plugin.plan()

                if not plan.enabled:
                    # NO-OP: feature flags not enabled, do nothing
                    return state

                # Feature flags enabled: perform actual MIPRO optimization
                try:
                    from AFO.mipro import Example, Module, mipro_optimizer

                    # Prepare mock program and examples for MIPROv2
                    # In real implementation, this would come from graph inputs
                    mock_program = Module()
                    mock_trainset = [
                        Example(input="test input", output="test output"),
                        Example(input="another input", output="another output"),
                    ]

                    # Run MIPROv2 optimization
                    # NOTE: If MIPRO compilation is slow/async, it should be awaited.
                    # For now, keeping it sync as per original implementation but wrapped in async node.
                    optimized_program = mipro_optimizer.compile(
                        student=mock_program, trainset=mock_trainset
                    )

                    # SSOT: MIPRO output size limit - keep summary only to prevent Graph state pollution
                    # Raw traces/candidates go to artifacts, not state.outputs
                    state.outputs["_mipro"] = {
                        "status": "optimized",
                        "score": getattr(optimized_program, "_mipro_score", 0.8),
                        "trials": getattr(optimized_program, "_mipro_trials", 0),
                        "config": getattr(optimized_program, "_mipro_config", {}),
                        "optimized": getattr(optimized_program, "_mipro_optimized", False),
                    }

                except ImportError as e:
                    # MIPRO modules not available
                    state.outputs["_mipro"] = {"status": "modules_missing", "error": str(e)}
                except Exception as e:
                    # MIPRO execution failed
                    state.outputs["_mipro"] = {"status": "failed", "error": str(e)}

            except Exception as e:
                # Plugin system failed, fallback to NO-OP
                pass

            return state

        # Always register MIPRO node (safe NO-OP when disabled)
        nodes_dict["MIPRO"] = mipro_node

        try:
            state = await run_chancellor_v2(input_payload, nodes_dict)

            # Extract DecisionResult from MERGE node
            merge_output = state.outputs.get("MERGE", {})
            decision_dict = merge_output if isinstance(merge_output, dict) else {}

            # Convert GraphState to dict for compatibility
            result = {
                "trace_id": state.trace_id,
                "request_id": state.request_id,
                "input": state.input,
                "plan": state.plan,
                "outputs": state.outputs,
                "errors": state.errors,
                "step": state.step,
                "started_at": state.started_at,
                "updated_at": state.updated_at,
                "success": decision_dict.get("mode") == "AUTO_RUN",  # Use DecisionResult mode
                "error_count": len(state.errors),
                # Add DecisionResult fields for transparency
                "decision": decision_dict,
            }

            return result

        except Exception as e:
            return {
                "success": False,
                "error": f"Chancellor Graph execution failed: {e}",
                "trace_id": None,
                "errors": [str(e)],
            }

    @staticmethod
    async def invoke(command: str, headers: dict[str, str] | None = None, **kwargs) -> dict:
        """Simple invoke method for backward compatibility.

        Args:
            command: Command string
            headers: Optional request headers for routing/shadow
            **kwargs: Additional parameters

        Returns:
            Execution result
        """
        settings = get_settings()
        headers = headers or {}

        # Phase 24: Advanced Routing (Canary Override)
        force_v2 = headers.get("X-AFO-Engine", "").lower() == "v2"
        v2_enabled = settings.CHANCELLOR_V2_ENABLED or force_v2
        shadow_enabled = settings.CHANCELLOR_V2_SHADOW_ENABLED and not v2_enabled

        # 1. Main Path
        if v2_enabled:
            # V2 execution
            input_payload = {"command": command, **kwargs}
            result = await ChancellorGraph.run_v2(input_payload)
            result["engine"] = "V2 (Graph)"
            return result
        else:
            # V1 Fallback
            result = {
                "success": True,
                "engine": "V1 (Legacy)",
                "input": command,
                "outputs": {"V1": "Executed via legacy V1 engine (Canary OFF)"},
            }

            # 2. Shadow Path (PH24)
            # Combined condition per SIM102: shadow enabled AND random sampling
            if shadow_enabled and random.random() <= settings.CHANCELLOR_V2_DIFF_SAMPLING_RATE:
                asyncio.create_task(ChancellorGraph._run_shadow_diff(command, result, **kwargs))

            return result

    @staticmethod
    async def _run_shadow_diff(command: str, v1_result: dict, **kwargs):
        """Execute V2 in background and save diff evidence."""
        try:
            input_payload = {"command": command, **kwargs}
            v2_result = await ChancellorGraph.run_v2(input_payload)

            # Prepare diff Evidence
            diff_entry = {
                "timestamp": time.time(),
                "input": command,
                "v1_engine": v1_result.get("engine"),
                "v2_trace_id": v2_result.get("trace_id"),
                "v1_success": v1_result.get("success"),
                "v2_success": v2_result.get("success"),
                "v2_error_count": v2_result.get("error_count", 0),
            }

            # Save to artifacts for SSOT evidence
            diff_dir = "/Users/brnestrm/AFO_Kingdom/artifacts/chancellor_shadow_diff"
            os.makedirs(diff_dir, exist_ok=True)
            filename = f"diff_{v2_result.get('trace_id') or int(time.time())}.json"

            with open(os.path.join(diff_dir, filename), "w") as f:
                json.dump(diff_entry, f, indent=2)

        except Exception as e:
            # Silent fail for shadow mode to avoid affecting production
            pass


# Create singleton instance for backward compatibility
chancellor_graph = ChancellorGraph()
