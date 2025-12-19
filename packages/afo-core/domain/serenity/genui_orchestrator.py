
import os
import asyncio
import logging
from typing import Any, Dict
from pydantic import BaseModel, Field

# AFO Components
from AFO.scholars.yeongdeok import yeongdeok
from AFO.config.settings import get_settings

logger = logging.getLogger("afo.genui")

class GenUISpec(BaseModel):
    """Specification for a Generated UI (GenUI) App"""
    app_id: str = Field(..., description="Unique ID for the sub-app (e.g. 'health-dashboard')")
    description: str = Field(..., description="High-level description of what to build")
    requirements: list[str] = Field(default_factory=list, description="Specific features compliant with Royal Standards")

class GenUIOrchestrator:
    """
    [Serenity] GenUI Orchestrator
    Autonomous UI Generation & Verification Loop
    
    1. Create (Jwaja): Generate Next.js code
    2. Deploy: Write to filesystem (Hot Reload)
    3. Verify (Hwata): Visual Inspection via Browser
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.genui_base_path = "packages/dashboard/src/app/genui"

    async def create_sub_app(self, spec: GenUISpec) -> Dict[str, Any]:
        """
        [Step 1] Create Sub-App Code using Jwaja (Frontend Expert)
        """
        logger.info(f"🎨 [GenUI] Creating sub-app: {spec.app_id}")
        
        # 1. Consult Jwaja for Code
        prompt = (
            f"Create a Next.js Page component for: {spec.description}\n"
            f"Requirements: {', '.join(spec.requirements)}\n"
            "Tech Stack: Next.js 14, TailwindCSS, Lucide React.\n"
            "Output ONLY the TypeScript code for page.tsx."
        )
        
        code = await yeongdeok.consult_jwaja(prompt)
        
        # Clean code (strip markdown blocks if any)
        clean_code = self._clean_code(code)
        
        # 2. Deploy (Write File)
        target_dir = os.path.join(self.genui_base_path, spec.app_id)
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, "page.tsx")
        
        with open(file_path, "w") as f:
            f.write(clean_code)
            
        logger.info(f"💾 [GenUI] Deployed to {file_path}")
        
        return {
            "status": "deployed",
            "path": file_path,
            "url": f"/genui/{spec.app_id}"
        }

    async def verify_ui(self, app_id: str) -> Dict[str, Any]:
        """
        [Step 2] Verify UI Visuals using Hwata (Vision)
        Note: Requires Antigravity Browser Tool integration.
        For now, returns a verification prompt that the Chancellor can execute.
        """
        # In a fully autonomous loop, we would call the browser tool here.
        # Currently, we design this to provide instructions to the Chancellor.
        
        url = f"http://localhost:3000/genui/{app_id}"
        
        prompt = (
            f"Please verify the UI at {url}.\n"
            "Active Agent: Use 'browser_screenshot' tool on this URL.\n"
            "Then consult Hwata with the image to check for:\n"
            "1. Broken Layouts\n"
            "2. Aesthetic Harmony (Beauty)\n"
            "3. Text Readability"
        )
        
        return {
            "status": "pending_verification",
            "action_required": "browser_screenshot",
            "target_url": url,
            "instruction": prompt
        }

    def _clean_code(self, raw: str) -> str:
        """Strip markdown code blocks"""
        if "```tsx" in raw:
            return raw.split("```tsx")[1].split("```")[0].strip()
        if "```typescript" in raw:
            return raw.split("```typescript")[1].split("```")[0].strip()
        if "```" in raw:
            return raw.split("```")[1].split("```")[0].strip()
        return raw

# Singleton
genui_orchestrator = GenUIOrchestrator()
