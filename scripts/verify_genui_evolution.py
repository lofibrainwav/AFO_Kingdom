
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Path setup to ensure imports work
sys.path.append(os.path.join(os.getcwd(), "packages/afo-core"))

from AFO.genui.genui_orchestrator import GenUIOrchestrator
from AFO.config.antigravity import antigravity

class TestGenUIEvolution(unittest.TestCase):
    def setUp(self):
        self.orchestrator = GenUIOrchestrator()
        
    @patch.object(antigravity, 'get_feature_flag')
    def test_rollout_zero_percent(self, mock_flag):
        """Test blocking when flag is False (0% rollout or disabled)"""
        print("\n🧪 Testing 0% Rollout / Disabled Flag...")
        mock_flag.return_value = False
        
        result = self.orchestrator.create_project("test_blocked", "dashboard")
        
        self.assertEqual(result.get("status"), "BLOCKED_BY_GOVERNANCE")
        print("✅ Correctly BLOCKED by Governance.")

    @patch.object(antigravity, 'get_feature_flag')
    @patch('AFO.genui.genui_orchestrator.PlaywrightBridgeMCP')
    def test_rollout_hundred_percent(self, mock_playwright, mock_flag):
        """Test allowing when flag is True (100% rollout)"""
        print("\n🧪 Testing 100% Rollout / Enabled Flag...")
        mock_flag.return_value = True
        
        # Mock Playwright to avoid real browser calls
        mock_playwright.navigate.return_value = {"success": True}
        mock_playwright.screenshot.return_value = {"success": True}
        
        result = self.orchestrator.create_project("test_allowed", "dashboard")
        
        self.assertNotEqual(result.get("status"), "BLOCKED_BY_GOVERNANCE")
        self.assertIn("code_path", result)
        print("✅ Correctly ALLOWED by Governance.")

    @patch.object(antigravity, 'get_feature_flag')
    def test_vision_blocked(self, mock_flag):
        """Test allowing creation but blocking vision"""
        print("\n🧪 Testing Vision Blocked...")
        
        # check_governance is called twice:
        # 1. genui_create -> True (Allow creation)
        # 2. genui_vision -> False (Block vision)
        mock_flag.side_effect = [True, False] 
        
        result = self.orchestrator.create_project("test_vision_block", "dashboard")
        
        self.assertNotEqual(result.get("status"), "BLOCKED_BY_GOVERNANCE")
        
        # Verify vision result failure message or state
        vision = result.get("vision_result", {})
        self.assertEqual(vision.get("success"), False)
        print("✅ Correctly BLOCKED Vision while allowing Creation.")

if __name__ == "__main__":
    unittest.main()
