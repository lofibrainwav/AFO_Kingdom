#!/usr/bin/env python3
"""
TICKET-043 SSOT 증거 생성 스크립트
Big 4 AI 에이전트 군단 실행 테스트
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "packages", "afo-core"))

try:
    from afo.julie.ai_agents import JulieAgentOrchestrator

    print("✅ Import successful")

    orchestrator = JulieAgentOrchestrator()
    result = orchestrator.process_tax_request(
        {
            "entity_type": "C_CORP",
            "tax_year": 2025,
            "purpose": "tax_optimization",
        }
    )
    print("✅ Execution successful")
    print(f"Evidence ID: {result['orchestrator_id'][:8]}")
    print(f"Final Trinity Score: {result['trinity_score']['total']:.3f}")
    print(f"Humility Report - DOING: {result['humility_report']['DOING']}")
    print(f"Humility Report - DONE: {result['humility_report']['DONE']}")
    print(f"Humility Report - NEXT: {result['humility_report']['NEXT']}")

    # Evidence Bundle 저장
    import json
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"artifacts/ticket043_execution_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"✅ Evidence Bundle saved: {filename}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
