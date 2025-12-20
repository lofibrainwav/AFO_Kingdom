from strategists.base import robust_execute, log_action
from typing import Dict

try:
    from AFO.config.antigravity import antigravity
except ImportError:
    class MockAntiGravity:
        AUTO_DEPLOY = True
        DRY_RUN_DEFAULT = True
    antigravity = MockAntiGravity()

def deploy(config: Dict) -> str:
    """
    Ma Chao (Serenity): Frictionless Deployment
    
    [Serenity Philosophy]:
    - Automation: Checks AUTO_DEPLOY flag.
    - Stability: Returns DEPLOY_FAILED on error rather than crashing pipeline.
    """
    def _logic(cfg):
        if antigravity.AUTO_DEPLOY and not antigravity.DRY_RUN_DEFAULT:
            return "DEPLOY_COMPLETE (Zero Friction)"
        return "DRY_RUN_MODE (Serenity Preserved)"

    # Robust Execute: Fallback to Error Message
    result = robust_execute(_logic, config, fallback_value="DEPLOY_FAILED")
    log_action("Ma Chao 孝", result)
    return str(result)
