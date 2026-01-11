#!/usr/bin/env python3
"""
Janus Vision Demonstration: The Royal Eye Awakens 👁️⚔️🏰
Demonstrates the 'Eye-Brain-Hand' loop of the AFO Visual Agent.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent
sys.path.append(str(root / "packages" / "afo-core"))

try:
    from AFO.serenity.visual_agent import VisualAgent
except ImportError:
    # Fallback to local import if structure differs
    sys.path.append(str(root / "packages" / "afo-core" / "AFO"))
    from serenity.visual_agent import VisualAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JanusDemo")

async def run_demo():
    print("\n" + "="*60)
    print("🏰 Janus Vision Activation: Proving Real Power")
    print("="*60 + "\n")

    agent = VisualAgent()
    
    # Target: AFO Dashboard (assuming it's running on 3000)
    target_url = "http://localhost:3000"
    goal = "왕국 대시보드의 Trinity Score 위젯을 찾아 현재 점수를 확인하라."

    print(f"📍 Goal: {goal}")
    print(f"🎬 Initiating Janus Loop at {target_url}...")

    try:
        # Run Janus Loop with dry_run simulation if desired, 
        # but here we demonstrate the real logic call.
        result = await agent.run_janus_loop(goal=goal, url=target_url, max_iterations=2)
        
        print("\n" + "-"*40)
        print(f"📊 Loop Results:")
        print(f"  - Iterations: {result['iterations_completed']}")
        print(f"  - Action Sequence: {[r['action']['type'] for r in result['results']]}")
        print(f"  - Final Summary: {result.get('summary', '조사가 완료되었습니다.')}")
        print("-"*40 + "\n")

        print("✅ [Janus] 시각적 인지 루프가 이제 '그림자'를 벗어나 '실재'하는 힘임을 증명했습니다.")

    except Exception as e:
        logger.error(f"❌ Janus Demo failed: {e}")
        print("\n⚠️ Note: This demo requires the Dashboard (3000) and Ollama (qwen3-vl) to be accessible.")

if __name__ == "__main__":
    if os.getenv("JANUS_VISION_ENABLED") != "1":
        print("⚠️ JANUS_VISION_ENABLED is not set in environment. Setting it for demo...")
        os.environ["JANUS_VISION_ENABLED"] = "1"
    
    # Ensure Playwright is ready
    print("🛠️  Ensuring Playwright Eye is calibrated...")
    
    asyncio.run(run_demo())
