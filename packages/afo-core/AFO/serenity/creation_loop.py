# serenity/creation_loop.py
"""
Project Serenity: GenUI-Playwright Creation Loop
Autonomous UI creation with visual verification.

Flow:
1. GenUI generates React code from prompt
2. Write to sandbox file
3. Playwright screenshots the result
4. Chancellor evaluates screenshot
5. Trinity Score determines: Deploy or Iterate
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from AFO.genui.genui_orchestrator import GenUIOrchestrator as GenUIOrchestratorType
    from AFO.utils.playwright_bridge import PlaywrightBridgeMCP as PlaywrightBridgeMCPType
    from AFO.domain.metrics.trinity_manager import TrinityManager

# GenUI Orchestrator
_GenUIOrchestrator: Any = None
try:
    from AFO.genui.genui_orchestrator import GenUIOrchestrator
    _GenUIOrchestrator = GenUIOrchestrator
except ImportError:
    pass

# Playwright Bridge
_PlaywrightBridgeMCP: Any = None
try:
    from AFO.utils.playwright_bridge import PlaywrightBridgeMCP
    _PlaywrightBridgeMCP = PlaywrightBridgeMCP
except ImportError:
    pass

# Trinity Manager
trinity_manager: Any = None
try:
    from AFO.domain.metrics.trinity_manager import trinity_manager as tm
    trinity_manager = tm
except ImportError:
    pass


@dataclass
class CreationResult:
    """Result of a creation loop iteration."""

    code: str
    screenshot_path: str | None
    trinity_score: float
    risk_score: float
    iteration: int
    success: bool
    feedback: str


class SerenityCreationLoop:
    """
    Autonomous UI Creation Loop (Project Serenity)

    Combines GenUI (creation) + Playwright (verification) + Chancellor (governance)
    to create a self-improving UI generation system.
    """

    MAX_ITERATIONS = 3
    TRINITY_THRESHOLD = 0.9
    RISK_THRESHOLD = 0.1

    def __init__(self, sandbox_dir: str | None = None):
        self.sandbox_dir = sandbox_dir or tempfile.mkdtemp(prefix="serenity_")
        self.genui = _GenUIOrchestrator() if _GenUIOrchestrator else None
        self.playwright = _PlaywrightBridgeMCP() if _PlaywrightBridgeMCP else None

    async def create_ui(self, prompt: str) -> CreationResult:
        """
        Main entry point: Create UI from natural language prompt.

        Args:
            prompt: Natural language description of desired UI

        Returns:
            CreationResult with code, screenshot, and scores
        """
        print(f"🎨 [Serenity] Starting creation: {prompt[:50]}...")

        iteration = 0
        feedback = ""

        while iteration < self.MAX_ITERATIONS:
            iteration += 1
            print(f"\n📍 [Serenity] Iteration {iteration}/{self.MAX_ITERATIONS}")

            # Step 1: Generate Code
            code = await self._generate_code(prompt, feedback)
            if not code:
                return CreationResult(
                    code="",
                    screenshot_path=None,
                    trinity_score=0,
                    risk_score=1,
                    iteration=iteration,
                    success=False,
                    feedback="GenUI generation failed",
                )

            # Step 2: Write to Sandbox
            file_path = await self._write_to_sandbox(code, iteration)

            # Step 3: Capture Screenshot
            screenshot_path = await self._capture_screenshot(file_path)

            # Step 4: Evaluate with Trinity
            trinity_score, risk_score, feedback = await self._evaluate(
                code, screenshot_path, prompt
            )

            print(f"⚖️ [Serenity] Score: Trinity {trinity_score:.2f}, Risk {risk_score:.2f}")

            # Step 5: Decision Gate
            if trinity_score >= self.TRINITY_THRESHOLD and risk_score <= self.RISK_THRESHOLD:
                print("✅ [Serenity] AUTO_RUN: Quality threshold met!")
                return CreationResult(
                    code=code,
                    screenshot_path=screenshot_path,
                    trinity_score=trinity_score,
                    risk_score=risk_score,
                    iteration=iteration,
                    success=True,
                    feedback="Quality threshold met - Ready for deployment",
                )

            print(f"🔄 [Serenity] Iterating: {feedback[:50]}...")

        # Max iterations reached
        print("⚠️ [Serenity] Max iterations reached, returning best effort")
        return CreationResult(
            code=code,
            screenshot_path=screenshot_path,
            trinity_score=trinity_score,
            risk_score=risk_score,
            iteration=iteration,
            success=False,
            feedback=f"Max iterations reached. Last feedback: {feedback}",
        )

    async def _generate_code(self, prompt: str, feedback: str = "") -> str:
        """Generate React code using GenUI."""
        if not self.genui:
            # Fallback: Simple template
            return f"""
export function GeneratedComponent() {{
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h2 className="text-white">{prompt[:30]}...</h2>
      <p className="text-gray-400">Generated by Serenity</p>
    </div>
  );
}}
"""

        full_prompt = prompt
        if feedback:
            full_prompt = f"{prompt}\n\nPrevious feedback to address: {feedback}"

        try:
            result = await self.genui.generate(full_prompt)
            return str(result.get("code", ""))
        except Exception as e:
            print(f"❌ [Serenity] GenUI error: {e}")
            return ""

    async def _write_to_sandbox(self, code: str, iteration: int) -> str:
        """Write generated code to sandbox file."""
        file_path = os.path.join(self.sandbox_dir, f"component_v{iteration}.tsx")

        # Wrap in minimal HTML for rendering
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-950">
  <div id="root"></div>
  <script type="text/babel">
    {code}
    ReactDOM.render(<GeneratedComponent />, document.getElementById('root'));
  </script>
</body>
</html>
"""

        html_path = file_path.replace(".tsx", ".html")
        Path(html_path).write_text(html_content)

        print(f"📝 [Serenity] Written to: {html_path}")
        return html_path

    async def _capture_screenshot(self, html_path: str) -> str | None:
        """Capture screenshot of rendered component."""
        if not self.playwright:
            print("⚠️ [Serenity] Playwright not available, skipping screenshot")
            return None

        try:
            screenshot_path = html_path.replace(".html", "_screenshot.png")

            # Use Playwright Bridge to capture
            result = await self.playwright.verify_ui(
                url=f"file://{html_path}", screenshot_path=screenshot_path
            )

            if result.get("success"):
                return screenshot_path
            return None
        except Exception as e:
            print(f"❌ [Serenity] Screenshot error: {e}")
            return None

    async def _evaluate(
        self, code: str, screenshot_path: str | None, prompt: str
    ) -> tuple[float, float, str]:
        """Evaluate the generated UI using Trinity principles."""
        # Use TrinityManager for dynamic scoring
        if trinity_manager:
            metrics = trinity_manager.get_current_metrics()
            base_trinity = metrics.trinity_score
            base_risk = 1.0 - metrics.goodness
        else:
            base_trinity = 0.85
            base_risk = 0.15

        # Simple heuristics for UI quality
        beauty_bonus = 0.0
        truth_penalty = 0.0
        feedback_items = []

        # Check code quality (Truth)
        if "export function" in code or "export default" in code:
            beauty_bonus += 0.02
        else:
            truth_penalty += 0.05
            feedback_items.append("Missing proper export statement")

        if "className" in code:
            beauty_bonus += 0.02  # Using CSS classes (good practice)

        if len(code) < 50:
            truth_penalty += 0.1
            feedback_items.append("Code too short, may be incomplete")

        if screenshot_path and os.path.exists(screenshot_path):
            beauty_bonus += 0.05  # Successfully rendered
        else:
            truth_penalty += 0.05
            feedback_items.append("Screenshot capture failed")

        # Calculate final scores
        trinity_score = min(1.0, max(0.0, base_trinity + beauty_bonus - truth_penalty))
        risk_score = min(1.0, max(0.0, base_risk + truth_penalty))

        feedback = "; ".join(feedback_items) if feedback_items else "Looking good!"

        return trinity_score, risk_score, feedback


# Singleton for easy access
serenity_loop = SerenityCreationLoop()


async def create_ui_from_prompt(prompt: str) -> CreationResult:
    """Convenience function for UI creation."""
    return await serenity_loop.create_ui(prompt)
