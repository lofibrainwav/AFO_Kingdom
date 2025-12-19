"""
Vision Verifier Service (The Eyes)
Phase 9: Self-Expanding Kingdom

Autonomous visual inspection of generated UI components.
"""
import logging
from pathlib import Path
from typing import Any

from AFO.utils.playwright_bridge import bridge

logger = logging.getLogger("afo.services.vision_verifier")

class VisionVerifier:
    """
    Autonomous visual verification service.
    Uses Playwright to "see" the generated component.
    """

    def __init__(self) -> None:
        self.screenshot_dir = Path("packages/dashboard/public/artifacts/verification")
        # Ensure directory exists relative to CWD or absolute
        # Assuming CWD is project root
        if not self.screenshot_dir.exists():
            try:
                self.screenshot_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.warning(f"⚠️ [Vision] Could not create screenshot dir: {e}")

    async def verify_component(self, component_name: str) -> dict[str, Any]:
        """
        Visits the Sandbox Preview URL and takes a screenshot.
        """
        # Determine Dashboard URL (default localhost:3000)
        # The preview page is likely /gen-ui/preview/{component_name}
        # But wait, we didn't build a specific route for individual component preview in Next.js yet.
        # Ideally, we should view it on the SandboxCanvas or a dedicated page.
        # For Phase 9-2 MVP, let's assume we visit the sandbox page and maybe component is loaded?
        # Actually, let's implement a 'dedicated preview' URL logic on frontend side later.
        # For now, we verify the generic sandbox.

        target_url = f"http://localhost:3000/sandbox/{component_name}" # Hypothetical route

        logger.info(f"👁️ [Vision] Verifying {component_name} at {target_url}...")

        try:
            filename = f"{component_name}_verified.png"
            path = str(self.screenshot_dir / filename)

            # Using the bridge to capture
            result = await bridge.verify_ui(
                url=target_url,
                screenshot_path=path
            )

            if result.get("status") == "PASS":
                logger.info(f"✅ [Vision] Captured screenshot: {path}")
                return {
                    "success": True,
                    "screenshot_path": path,
                    "details": result
                }
            else:
                 logger.warning(f"⚠️ [Vision] Verification simulation or failure: {result}")
                 return {
                     "success": False,
                     "error": "Verification failed or simulated",
                     "details": result
                 }

        except Exception as e:
            logger.error(f"❌ [Vision] Verification error: {e}")
            return {"success": False, "error": str(e)}

vision_verifier = VisionVerifier()
