"""
AFO Kingdom Visual Agent - Brain + Eye + Hand Integration
Janus Protocol: Internal Code Vision + External GUI Control
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from AFO.domain.janus.contract import VisualAction, VisualPlan
from AFO.llm_router import route_and_execute
from AFO.serenity.action_validator import action_validator, ValidatedAction

logger = logging.getLogger(__name__)


class VisualAgent:
    """
    Step 2: Loop Engine (Brain + Eye + Hand)
    Screenshot → Plan → Gate → Execute → Screenshot
    """

    def __init__(self, max_steps_per_turn: int = 5):
        self.max_steps_per_turn = max_steps_per_turn
        self.current_plan: Optional[VisualPlan] = None
        self.execution_history: List[Dict[str, Any]] = []

    async def analyze_and_plan(
        self,
        screenshot: str,
        goal: str,
        context: Optional[Dict[str, Any]] = None
    ) -> VisualPlan:
        """
        Brain (LLM Router) + Eye (Qwen3-VL): Analyze screenshot and create action plan
        """
        context = context or {}

        # LLM Router를 통해 Qwen3-VL 호출 (Computer Vision)
        prompt = self._build_vision_prompt(screenshot, goal, context)

        llm_response = await route_and_execute({
            "query": prompt,
            "provider": "ollama",  # Qwen3-VL 우선
            "max_tokens": 1024,
            "temperature": 0.1,  # Deterministic for actions
        })

        if not llm_response.get("success"):
            # Fallback: Basic plan for navigation
            return self._create_fallback_plan(goal)

        # Parse LLM response into VisualPlan
        try:
            raw_plan = self._parse_llm_response(llm_response["response"])
            plan = self._validate_and_structure_plan(raw_plan, goal)

            self.current_plan = plan
            logger.info(f"✅ Visual plan created: {len(plan.actions)} actions for goal '{goal}'")
            return plan

        except Exception as e:
            logger.error(f"❌ Plan parsing failed: {e}")
            return self._create_fallback_plan(goal)

    async def execute_plan(
        self,
        plan: VisualPlan,
        screenshot_updater: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Hand (Playwright): Execute validated actions with safety gates
        """
        results = []

        for action in plan.actions:
            try:
                # Convert to validator format
                validator_action = {
                    "type": action.type,
                    "bbox": self._denormalize_bbox(action.bbox) if action.bbox else None,
                    "text": action.text,
                    "confidence": action.confidence,
                    "why": action.why
                }

                # Safety Gate 검증 (5개 게이트)
                context = {
                    "trinity_score": 95,  # 실제로는 Trinity Calculator에서 가져옴
                    "domain": "localhost:3000",  # 실제로는 현재 페이지에서 가져옴
                    "is_production": False
                }

                validated_actions = action_validator.validate_actions([validator_action], context)
                validated = validated_actions[0]

                if not validated.is_allowed:
                    logger.warning(f"🚫 Action blocked: {validated.block_reason}")
                    results.append({
                        "action": action.dict(),
                        "status": "blocked",
                        "reason": validated.block_reason,
                        "risk_score": validated.risk_score
                    })
                    continue

                # Execute action (Playwright integration placeholder)
                execution_result = await self._execute_single_action(validated)

                # Update screenshot if callback provided
                if screenshot_updater:
                    await screenshot_updater()

                results.append({
                    "action": action.dict(),
                    "status": "executed" if execution_result["success"] else "failed",
                    "result": execution_result,
                    "validated": validated.dict()
                })

                # Respect safety: wait between actions
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"❌ Action execution failed: {e}")
                results.append({
                    "action": action.dict(),
                    "status": "error",
                    "error": str(e)
                })

        # Record execution history
        self.execution_history.append({
            "plan": plan.dict(),
            "results": results,
            "timestamp": self._get_timestamp()
        })

        return results

    async def run_loop(
        self,
        initial_screenshot: str,
        goal: str,
        max_iterations: int = 10,
        screenshot_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Complete Loop: Screenshot → Plan → Gate → Execute → Screenshot
        """
        current_screenshot = initial_screenshot
        iteration = 0
        total_results = []

        while iteration < max_iterations:
            logger.info(f"🔄 Iteration {iteration + 1}/{max_iterations}")

            # Step 1: Analyze and Plan
            plan = await self.analyze_and_plan(current_screenshot, goal)

            if plan.stop or len(plan.actions) == 0:
                logger.info("🏁 Goal achieved or no actions needed")
                break

            # Step 2: Execute Plan
            results = await self.execute_plan(plan, screenshot_callback)
            total_results.extend(results)

            # Check if we should continue
            failed_actions = [r for r in results if r["status"] in ["blocked", "error", "failed"]]
            if len(failed_actions) > len(results) * 0.5:  # 50% 이상 실패
                logger.warning("⚠️ Too many failed actions, stopping loop")
                break

            iteration += 1

        return {
            "iterations": iteration,
            "total_actions": len(total_results),
            "successful_actions": len([r for r in total_results if r["status"] == "executed"]),
            "results": total_results,
            "final_plan": self.current_plan.dict() if self.current_plan else None
        }

    def _build_vision_prompt(self, screenshot: str, goal: str, context: Dict[str, Any]) -> str:
        """Build prompt for Qwen3-VL vision analysis"""
        return f"""You are a Visual Agent analyzing a screenshot to accomplish a goal.

GOAL: {goal}

INSTRUCTIONS:
1. Analyze the screenshot and identify UI elements
2. Create a sequence of actions to achieve the goal
3. Each action must be atomic and safe
4. Use normalized coordinates (0.0-1.0) for bbox
5. Limit to maximum 3 actions per response

RESPONSE FORMAT (JSON):
{{
  "goal": "{goal}",
  "actions": [
    {{
      "type": "click|type|scroll|wait|goto",
      "bbox": {{"x": 0.5, "y": 0.5, "w": 0.1, "h": 0.05}},
      "text": "optional text",
      "confidence": 0.95,
      "why": "reason for this action",
      "safety": "safe|confirm|block"
    }}
  ],
  "stop": false,
  "summary": "brief plan summary"
}}

SCREENSHOT DESCRIPTION: [Screenshot of web interface]
Analyze the visible UI elements and create actions to achieve: {goal}"""

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM JSON response"""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"JSON parsing failed: {e}")
            raise

    def _validate_and_structure_plan(self, raw_plan: Dict[str, Any], goal: str) -> VisualPlan:
        """Validate and structure raw plan into VisualPlan"""
        try:
            # Ensure required fields
            actions_data = raw_plan.get("actions", [])

            # Validate each action
            validated_actions = []
            for action_data in actions_data[:self.max_steps_per_turn]:
                # Ensure required fields
                action_data.setdefault("safety", "safe")
                action_data.setdefault("confidence", 0.8)
                action_data.setdefault("why", "AI determined action")

                validated_actions.append(VisualAction(**action_data))

            return VisualPlan(
                goal=goal,
                actions=validated_actions,
                stop=raw_plan.get("stop", False),
                summary=raw_plan.get("summary", "AI generated plan")
            )
        except Exception as e:
            logger.error(f"Plan validation failed: {e}")
            return self._create_fallback_plan(goal)

    def _create_fallback_plan(self, goal: str) -> VisualPlan:
        """Create safe fallback plan when analysis fails"""
        return VisualPlan(
            goal=goal,
            actions=[
                VisualAction(
                    type="wait",
                    bbox=None,
                    text=None,
                    confidence=0.5,
                    why="Fallback: waiting for user guidance",
                    safety="confirm"
                )
            ],
            stop=True,
            summary="Fallback plan: requires user guidance"
        )

    def _denormalize_bbox(self, bbox) -> Dict[str, int]:
        """Convert normalized bbox (0-1) to screen coordinates"""
        if not bbox:
            return None

        screen_width, screen_height = 1920, 1080  # Default screen size

        return {
            "x": int(bbox.x * screen_width),
            "y": int(bbox.y * screen_height),
            "w": int(bbox.w * screen_width),
            "h": int(bbox.h * screen_height)
        }

    async def _execute_single_action(self, validated_action: ValidatedAction) -> Dict[str, Any]:
        """Execute single action via Playwright (placeholder)"""
        try:
            # Placeholder for Playwright integration
            # 실제 구현 시:
            # - Playwright 브라우저 컨텍스트 연결
            # - validated_action에 따라 실제 DOM 조작 수행
            # - 결과 캡처 및 반환

            logger.info(f"🎯 Executing action: {validated_action.type} on {validated_action.bbox}")

            # Simulate execution
            await asyncio.sleep(0.1)  # Simulate action time

            return {
                "success": True,
                "action_type": validated_action.type,
                "bbox": validated_action.bbox,
                "timestamp": self._get_timestamp()
            }

        except Exception as e:
            logger.error(f"Action execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "action_type": validated_action.type
            }

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.execution_history:
            return {"total_executions": 0}

        total_actions = sum(len(exec["results"]) for exec in self.execution_history)
        successful_actions = sum(
            len([r for r in exec["results"] if r["status"] == "executed"])
            for exec in self.execution_history
        )

        return {
            "total_executions": len(self.execution_history),
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "success_rate": successful_actions / total_actions if total_actions > 0 else 0
        }


# Global instance
visual_agent = VisualAgent()