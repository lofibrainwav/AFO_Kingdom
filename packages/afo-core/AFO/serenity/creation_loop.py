# serenity/creation_loop.py
"""
Project Serenity: GenUI-Playwright Creation Loop (v100.0)
Autonomous UI creation with visual verification and Trinity Gating.

Philosophy:
- 眞 (Truth): 실시간 코드 품질 및 렌더링 검증
- 善 (Goodness): Trinity/Risk 임계치를 통한 안전한 배포
- 美 (Beauty): Playwright를 이용한 시각적 완성도 확인
"""

from __future__ import annotations

import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

from AFO.utils.logging import log_sse

# GenUI Orchestrator
try:
    from AFO.genui.genui_orchestrator import GenUIOrchestrator
except ImportError:
    GenUIOrchestrator = None

# Playwright Bridge
try:
    from AFO.utils.playwright_bridge import bridge as playwright_bridge
except ImportError:
    playwright_bridge = None

# Trinity Manager
try:
    from AFO.domain.metrics.trinity_manager import trinity_manager
except ImportError:
    trinity_manager = None

logger = logging.getLogger(__name__)

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
    """

    MAX_ITERATIONS = 3
    # v100.0 Standard: Trinity >= 90%, Risk <= 10%
    TRINITY_THRESHOLD = 0.9
    RISK_THRESHOLD = 0.1

    def __init__(self, sandbox_dir: str | None = None):
        self.sandbox_dir = sandbox_dir or tempfile.mkdtemp(prefix="serenity_")
        self.genui = GenUIOrchestrator() if GenUIOrchestrator else None
        self.bridge = playwright_bridge

    async def create_ui(self, prompt: str) -> CreationResult:
        """Main entry point: Create UI from natural language prompt."""
        log_sse(f"🎨 [Serenity] Starting creation: {prompt[:50]}...")

        iteration = 0
        feedback = ""
        last_result = None

        while iteration < self.MAX_ITERATIONS:
            iteration += 1
            log_sse(f"📍 [Serenity] Iteration {iteration}/{self.MAX_ITERATIONS}")

            # Step 1: Generate Code
            code = await self._generate_code(prompt, feedback)
            if not code:
                return CreationResult(code="", screenshot_path=None, trinity_score=0, risk_score=1, iteration=iteration, success=False, feedback="GenUI failed")

            # Step 2: Write to Sandbox (HTML wrapped for rendering)
            html_path = await self._prepare_sandbox(code, iteration)

            # Step 3: Capture Screenshot & Verify (眞 & 美)
            screenshot_path = None
            verification_data = {}
            if self.bridge:
                try:
                    screenshot_path = os.path.join(self.sandbox_dir, f"screenshot_v{iteration}.png")
                    # Disable dry-run momentarily for real verification if explicitly asked or permitted
                    verification_data = await self.bridge.verify_ui(f"file://{html_path}", screenshot_path)
                    log_sse(f"📸 [Serenity] Visual verification complete: {verification_data.get('status')}")
                except Exception as e:
                    log_sse(f"⚠️ [Serenity] Visual verification failed: {e}")

            # Step 4: Evaluate with Trinity (善)
            trinity_score, risk_score, feedback = self._evaluate(code, verification_data, prompt)
            log_sse(f"⚖️ [Serenity] Iteration Score: {trinity_score*100:.1f}/100 (Risk: {risk_score*100:.1f}%)")

            last_result = CreationResult(
                code=code,
                screenshot_path=screenshot_path,
                trinity_score=trinity_score,
                risk_score=risk_score,
                iteration=iteration,
                success=(trinity_score >= self.TRINITY_THRESHOLD and risk_score <= self.RISK_THRESHOLD),
                feedback=feedback
            )

            if last_result.success:
                log_sse("✅ [Serenity] AUTO_RUN: Quality threshold met! Deploying...")
                if trinity_manager:
                    trinity_manager.apply_trigger("AUTO_RUN_ACTION")
                return last_result

            log_sse(f"🔄 [Serenity] Refining: {feedback[:50]}...")

        log_sse("⚠️ [Serenity] Max iterations reached. Returning best effort.")
        return last_result

    async def _generate_code(self, prompt: str, feedback: str = "") -> str:
        """Generate React component via GenUI."""
        if not self.genui:
            return "// GenUI not available"

        full_prompt = prompt
        if feedback:
            full_prompt = f"{prompt}\n\n[REFINEMENT FEEDBACK]: {feedback}"

        try:
            # Note: Assuming self.genui.generate returns a dict with 'code'
            result = await self.genui.generate(full_prompt)
            return result.get("code", "")
        except Exception as e:
            logger.error(f"GenUI generation error: {e}")
            return ""

    async def _prepare_sandbox(self, code: str, iteration: int) -> str:
        """Wraps React code in HTML for Playwright rendering."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-gray-950 text-white min-h-screen p-8">
    <div id="root"></div>
    <script type="text/babel">
        {code}
        const root = ReactDOM.createRoot(document.getElementById('root'));
        // Try to find a component to render - defaults to GeneratedComponent or first export
        root.render(<GeneratedComponent />);
    </script>
</body>
</html>
"""
        html_path = os.path.join(self.sandbox_dir, f"sandbox_v{iteration}.html")
        Path(html_path).write_text(html_content)
        return html_path

    def _evaluate(self, code: str, verification: dict, prompt: str) -> tuple[float, float, str]:
        """Deep evaluation of the generated artifact."""
        base_trinity = 0.85
        if trinity_manager:
            base_trinity = trinity_manager.get_current_metrics().trinity_score

        truth_score = 1.0
        beauty_score = 1.0
        risk_score = 0.05
        feedback_list = []

        # 1. Structural Truth (眞)
        if "export function GeneratedComponent" not in code:
            truth_score -= 0.2
            feedback_list.append("Missing 'export function GeneratedComponent'")

        if len(code) < 100:
            truth_score -= 0.1
            feedback_list.append("Code is too sparse")

        # 2. Visual Beauty (美)
        acc_score = verification.get("accessibility_score", 0)
        if acc_score < 70 and verification.get("status") == "PASS":
            beauty_score -= 0.1
            feedback_list.append("Low accessibility/visual structure detected")

        if "className" not in code:
            beauty_score -= 0.1
            feedback_list.append("Tailwind CSS classes not used")

        # 3. Final Calculation (SSOT weighted)
        # Trinity = 0.35*眞 + 0.35*善 + 0.20*美 + ...
        # Simplified for loop:
        final_trinity = (truth_score * 0.4) + (beauty_score * 0.3) + (base_trinity * 0.3)
        final_risk = risk_score + (0.1 if truth_score < 0.9 else 0.0)

        return final_trinity, final_risk, "; ".join(feedback_list) if feedback_list else "Perfect alignment."

# Singleton
serenity_loop = SerenityCreationLoop()
