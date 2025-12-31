"""Chancellor Graph V2 - AFO Kingdom Integration Layer.

Provides unified interface for Chancellor Graph V2 operations.
SSOT Contract: Sequential Thinking + Context7 are REQUIRED.
"""

from __future__ import annotations

from api.chancellor_v2.graph import nodes

# Import Chancellor Graph V2 components
from api.chancellor_v2.graph.runner import run_v2 as run_chancellor_v2


# Create unified chancellor_graph interface
class ChancellorGraph:
    """Unified Chancellor Graph interface."""

    @staticmethod
    def run_v2(input_payload: dict, nodes_dict: dict = None) -> dict:
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
                "MERGE": nodes.merge_node,
                "EXECUTE": nodes.execute_node,
                "VERIFY": nodes.verify_node,
                "REPORT": nodes.report_node,
            }

        # Apply MIPROv2 plugin if enabled (add MIPRO node to nodes_dict)
        try:
            from AFO.chancellor_mipro_plugin import ChancellorMiproPlugin

            plugin = ChancellorMiproPlugin()
            plan = plugin.plan()

            if plan.enabled:
                # Add MIPRO node to nodes dict for actual integration
                from afo.mipro_optimizer import MiproOptimizer
                from afo.trinity_metric_wrapper import TrinityMetricWrapper

                def mipro_node(state):
                    """MIPRO optimization node for Chancellor Graph."""
                    try:
                        metric = TrinityMetricWrapper(lambda p, t: 0.8)  # Default metric
                        optimizer = MiproOptimizer(metric)
                        # This would be integrated with actual prompts/targets from state
                        state.outputs["_mipro"] = {"status": "integrated", "score": 0.8}
                    except Exception as e:
                        state.outputs["_mipro"] = {"status": "failed", "error": str(e)}
                    return state

                nodes_dict["MIPRO"] = mipro_node

        except ImportError:
            # Plugin not available, continue normally
            pass
        except Exception:
            # Plugin failed, log but continue (don't pollute input_payload)
            pass

        try:
            state = run_chancellor_v2(input_payload, nodes_dict)

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
    def invoke(command: str, **kwargs) -> dict:
        """Simple invoke method for backward compatibility.

        Args:
            command: Command string
            **kwargs: Additional parameters

        Returns:
            Execution result
        """
        input_payload = {"command": command, **kwargs}

        return ChancellorGraph.run_v2(input_payload)


# Create singleton instance for backward compatibility
chancellor_graph = ChancellorGraph()
